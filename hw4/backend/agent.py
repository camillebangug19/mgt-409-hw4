from pathlib import Path
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

try:
    from .models import ChatReply, ShopperDeps
    from .tools import get_product_details, search_products
except ImportError:
    from models import ChatReply, ShopperDeps
    from tools import get_product_details, search_products


BACKEND_PATH = Path(__file__).resolve().parent
PROMPT_PATH = BACKEND_PATH / "prompts" / "prompt.md"

# The course .env lives at the AI Foundations for Managers root; the first path
# also supports placing a project-specific .env beside this backend.
load_dotenv(BACKEND_PATH.parent / ".env")
load_dotenv(BACKEND_PATH.parent.parent / ".env")


def build_agent() -> Agent[ShopperDeps, ChatReply]:
    portkey_api_key = os.environ["PORTKEY_API_KEY"]
    openai_client = AsyncOpenAI(
        api_key=portkey_api_key,
        base_url="https://api.portkey.ai/v1",
        default_headers={
            "x-portkey-api-key": portkey_api_key,
            "x-portkey-provider": "openai",
        },
    )
    provider = OpenAIProvider(openai_client=openai_client)
    model = OpenAIModel("gpt-5.6-luna", provider=provider)
    return Agent(
        model=model,
        output_type=ChatReply,
        system_prompt=PROMPT_PATH.read_text(encoding="utf-8"),
        tools=[search_products, get_product_details],
        deps_type=ShopperDeps,
        retries=2,
        name="campus_customs_shop_agent",
    )


shop_agent = build_agent()


@shop_agent.instructions
def add_shopper_context(ctx: RunContext[ShopperDeps]) -> str:
    deps = ctx.deps
    identity = "This is a guest shopper with no account identity." if not deps.email else f"The logged-in shopper is {deps.name or 'the customer'} ({deps.email})."
    page = f"Current page context: {deps.page_context}" if deps.page_context else "The shopper is not currently on a product detail page."
    if deps.conversation:
        turns = []
        for turn in deps.conversation[-8:]:
            product_context = ""
            if turn.products:
                product_context = " Product cards shown: " + ", ".join(
                    f"{product.name} (product_id: {product.product_id})" for product in turn.products
                ) + "."
            turns.append(f"{turn.role}: {turn.content}{product_context}")
        conversation = "Recent conversation context:\n" + "\n".join(turns)
    else:
        conversation = "There is no earlier conversation context."
    return (
        f"{identity} {page} {conversation} "
        "Use this context when it is relevant, but never reveal private account details unnecessarily. "
        "Resolve references only when the page or recent conversation identifies one product clearly; "
        "otherwise ask a clarifying question before using a product tool."
    )
