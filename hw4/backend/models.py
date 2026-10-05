from typing import Literal

from pydantic import BaseModel, Field


class StockOption(BaseModel):
    size: str
    quantity: int


class ProductCard(BaseModel):
    product_id: str
    name: str
    price: float
    description: str
    image_url: str
    sizes: list[StockOption] = Field(default_factory=list)


class ProductDetails(ProductCard):
    garment_type: str
    colors: str
    search_tags: str


class ChatReply(BaseModel):
    reply: str
    products: list[ProductCard] = Field(default_factory=list)


class ConversationTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=2000)
    products: list[ProductCard] = Field(default_factory=list)


class PageContext(BaseModel):
    path: str
    product_id: str | None = None


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    user_id: int | None = None
    user_email: str | None = None
    page_context: PageContext | None = None
    conversation: list[ConversationTurn] = Field(default_factory=list, max_length=12)


class ChatHistoryMessage(BaseModel):
    id: int
    role: str
    content: str
    products: list[ProductCard] = Field(default_factory=list)
    created_at: str


class ShopperDeps(BaseModel):
    user_id: int | None = None
    name: str | None = None
    email: str | None = None
    page_context: str | None = None
    conversation: list[ConversationTurn] = Field(default_factory=list, max_length=12)


class WoofRequest(BaseModel):
    user_id: int = Field(gt=0)
    user_email: str = Field(min_length=3, max_length=254)
    product_id: str = Field(min_length=1, max_length=200)


class WoofResponse(BaseModel):
    saved: bool
    product: ProductDetails
