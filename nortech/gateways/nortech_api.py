from __future__ import annotations

from typing import Sequence
from urllib.parse import urljoin

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3.util import Timeout
from urllib3.util.retry import Retry


class NortechAPISettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NORTECH_API_", env_file=(".env", ".env.prod"))

    URL: str = Field(default="https://api.apps.nor.tech")
    KEY: str = Field(default=...)
    USER_AGENT: str = Field(default="nortech-python/0.9.2")
    IGNORE_PAGINATION: bool = True
    EXPERIMENTAL_FEATURES: bool = False
    TIMEOUT: float | Timeout = Field(default=Timeout(connect=10, read=60))
    RETRY: int | Retry = Field(
        default=Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[502, 503, 504],
            allowed_methods=["GET", "POST"],
            raise_on_status=False,
        )
    )


class NortechAPI(Session):
    def __init__(self, settings: NortechAPISettings | None = None) -> None:
        super().__init__()
        self.settings = settings or NortechAPISettings()
        self.mount(self.settings.URL, HTTPAdapter(max_retries=self.settings.RETRY))
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
            timeout=timeout or self.settings.TIMEOUT,  # type: ignore
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
    valid_status_codes: Sequence[int] | None = None,
    error_message: str = "Fetch failed.",
) -> None:
    try:
        assert response.status_code in (valid_status_codes or [200])
    except AssertionError as e:
        raise AssertionError(f"{error_message} Status code: {response.status_code}. Response: {response.text}") from e
