from __future__ import annotations

from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field

SortBy = TypeVar("SortBy")


class PaginationOptions(BaseModel, Generic[SortBy]):
    """Pagination options for list endpoints.

    Attributes:
        size (int | None, default=100, le=100): The number of items to return.
        sort_by (str | None): The field to sort by.
        sort_order ("asc" | "desc", default="asc"): The order to sort by.
        next_token (str | None): The next token to use for pagination.

    """

    model_config = ConfigDict(populate_by_name=True)

    size: int | None = Field(default=None, gt=0, le=100)
    sort_by: SortBy | None = Field(default=None, alias="sortBy")
    sort_order: Literal["asc", "desc"] | None = Field(default=None, alias="sortOrder")
    next_token: str | None = Field(default=None, alias="nextToken")


class NextRef(BaseModel):
    token: str


Resp = TypeVar("Resp")


class PaginatedResponse(BaseModel, Generic[Resp]):
    """Paginated response from list endpoints.

    Attributes:
        size (int): The number of items returned.
        data (list[obj]): The list of items.
        next.token (str | None): The next token to use for pagination. If None, there are no more pages.

    """

    size: int
    data: list[Resp]
    next: NextRef | None = None
    pagination_options: PaginationOptions | None = None

    def next_pagination_options(self) -> PaginationOptions | None:
        if not self.next:
            return None
        if self.pagination_options:
            return self.pagination_options.model_copy(update={"next_token": self.next.token})
        return PaginationOptions(nextToken=self.next.token)
