"""Append-only audit logging for Campus Customs agent runs."""

from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import threading
import uuid
from typing import Any, Callable, Iterator, TypeVar


PROJECT_ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = PROJECT_ROOT / "output" / "audit_trail.json"
_CURRENT_RUN_ID: ContextVar[str | None] = ContextVar("current_audit_run_id", default=None)
_WRITE_LOCK = threading.Lock()
_MAX_TEXT_LENGTH = 240
_T = TypeVar("_T")


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _redact_text(value: str) -> str:
    redacted = re.sub(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", "[redacted email]", value)
    return re.sub(
        r"(?i)(password|passcode|secret)\s*[:=]?\s*\S+",
        r"\1=[redacted]",
        redacted,
    )


def _short_value(value: Any, depth: int = 0) -> Any:
    """Keep the audit trail useful without storing large responses or secrets."""
    if depth > 3:
        return "[truncated]"
    if hasattr(value, "model_dump"):
        value = value.model_dump()
    if isinstance(value, str):
        value = _redact_text(value)
        return value if len(value) <= _MAX_TEXT_LENGTH else value[:_MAX_TEXT_LENGTH] + "…"
    if isinstance(value, dict):
        items = list(value.items())[:20]
        result = {str(key): _short_value(item, depth + 1) for key, item in items}
        if len(value) > len(items):
            result["…"] = f"{len(value) - len(items)} more fields"
        return result
    if isinstance(value, (list, tuple)):
        values = [_short_value(item, depth + 1) for item in value[:6]]
        if len(value) > len(values):
            values.append(f"… {len(value) - len(values)} more items")
        return values
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    return _short_value(str(value), depth + 1)


def _read_entries() -> list[dict[str, Any]]:
    if not AUDIT_PATH.exists():
        return []
    contents = AUDIT_PATH.read_text(encoding="utf-8").strip()
    if not contents:
        return []
    entries = json.loads(contents)
    if not isinstance(entries, list):
        raise ValueError(f"{AUDIT_PATH} must contain a JSON array")
    return entries


def append_audit_event(
    *,
    run_id: str,
    event: str,
    tool_name: str,
    args: Any = None,
    result: Any = None,
    stop_reason: str | None = None,
) -> None:
    """Append one event while preserving every previous event in the JSON array."""
    event_record = {
        "time": _timestamp(),
        "run_id": run_id,
        "event": event,
        "tool_name": tool_name,
        "args": _short_value(args),
        "result": _short_value(result),
        "stop_reason": stop_reason,
    }
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _WRITE_LOCK:
        entries = _read_entries()
        entries.append(event_record)
        AUDIT_PATH.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")


def start_agent_run(message: str) -> str:
    run_id = uuid.uuid4().hex
    append_audit_event(
        run_id=run_id,
        event="run_start",
        tool_name="agent_loop",
        args={"message": message},
        stop_reason="started",
    )
    return run_id


def finish_agent_run(run_id: str, *, stop_reason: str, result: Any = None) -> None:
    append_audit_event(
        run_id=run_id,
        event="run_stop",
        tool_name="agent_loop",
        result=result,
        stop_reason=stop_reason,
    )


@contextmanager
def audit_run(run_id: str) -> Iterator[None]:
    token = _CURRENT_RUN_ID.set(run_id)
    try:
        yield
    finally:
        _CURRENT_RUN_ID.reset(token)


def audited_tool_call(tool_name: str, args: Any, function: Callable[[], _T]) -> _T:
    """Run a catalogue tool and record its short result when inside an agent run."""
    run_id = _CURRENT_RUN_ID.get()
    if run_id is None:
        return function()

    try:
        result = function()
    except Exception as error:
        append_audit_event(
            run_id=run_id,
            event="tool_call",
            tool_name=tool_name,
            args=args,
            result={"error": str(error)},
            stop_reason="tool_error",
        )
        raise

    append_audit_event(
        run_id=run_id,
        event="tool_call",
        tool_name=tool_name,
        args=args,
        result=result,
        stop_reason="tool_completed",
    )
    return result
