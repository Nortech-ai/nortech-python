from urllib.parse import urljoin

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class CustomerAPISettings(BaseSettings):
    URL: str = Field(default="https://api.apps.nor.tech")
    TOKEN: str = Field(default=...)

    model_config = SettingsConfigDict(env_prefix="CUSTOMER_API_")


class CustomerAPI(Session):
    def __init__(self, settings: CustomerAPISettings):
        super().__init__()
        self.settings = settings
        self.mount(
            settings.URL,
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
        self.headers = {"Authorization": f"Bearer {settings.TOKEN}"}

    def request(self, method, url, *args, **kwargs):
        joined_url = urljoin(self.settings.URL, url)
        return super().request(method, joined_url, *args, **kwargs)
