from __future__ import annotations

from typing import Generic, Literal, TypeVar
from urllib.parse import urljoin

from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class NortechAPISettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NORTECH_API_", env_file=(".env", ".env.prod"))

    URL: str = Field(default="https://api.apps.nor.tech")
    KEY: str = Field(default=...)
    USER_AGENT: str = Field(default="nortech-python/0.0.9")
    IGNORE_PAGINATION: bool = True


class NortechAPI(Session):
    def __init__(self, settings: NortechAPISettings | None = None) -> None:
        super().__init__()
        self.settings = settings or NortechAPISettings()
        self.mount(
            self.settings.URL,
            HTTPAdapter(
                max_retries=Retry(
                    total=5,
                    backoff_factor=1,
                    status_forcelist=[502, 503, 504],
                    allowed_methods=["GET", "POST"],
                    raise_on_status=False,
                )
            ),
        )
        self.headers = {"Authorization": f"Bearer {self.settings.KEY}", "User-Agent": self.settings.USER_AGENT}
        self.ignore_pagination = self.settings.IGNORE_PAGINATION

    def request(
        self,
        method: str | bytes,
        url: str | bytes,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ) -> Response:
        url_str = url.decode() if isinstance(url, bytes) else str(url)
        joined_url = urljoin(self.settings.URL, url_str)
        return super().request(
            method,
            joined_url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
        )


def validate_response(
    response: Response,
    valid_status_codes: list[int] | None = None,
    error_message: str = "Fetch failed.",
) -> None:
    try:
        assert response.status_code in (valid_status_codes or [200])
    except AssertionError as e:
        raise AssertionError(f"{error_message} Status code: {response.status_code}. Response: {response.text}") from e


SortBy = TypeVar("SortBy")


class PaginationOptions(BaseModel, Generic[SortBy]):
    model_config = ConfigDict(populate_by_name=True)

    size: int | None = Field(default=None, gt=0, le=100)
    sort_by: SortBy | None = Field(default=None, alias="sortBy")
    sort_order: Literal["asc", "desc"] | None = Field(default=None, alias="sortOrder")
    next_token: str | None = Field(default=None, alias="nextToken")


class NextRef(BaseModel):
    token: str


Resp = TypeVar("Resp")


class PaginatedResponse(BaseModel, Generic[Resp]):
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
