from __future__ import annotations

from urllib3 import Retry, Timeout

from nortech.datatools import Datatools
from nortech.derivers import Derivers
from nortech.gateways.nortech_api import NortechAPI, NortechAPISettings
from nortech.metadata import Metadata


class Nortech:
    """Main class for interacting with the Nortech SDK.

    Attributes:
        metadata (Metadata): Client for interacting with the Nortech Metadata API.
        datatools (Datatools): Client for interacting with the Nortech Datatools API.
        derivers (Derivers): Client for interacting with the Nortech Derivers API.

    """

    def __init__(
        self,
        url: str = "https://api.apps.nor.tech",
        api_key: str | None = None,
        ignore_pagination: bool | None = None,
        user_agent: str | None = None,
        experimental_features: bool | None = None,
        timeout: float | Timeout | None = None,
        retry: int | Retry | None = None,
    ):
        """Initialize the Nortech class.

        Args:
        url (str): The URL of the Nortech API. Defaults to "https://api.apps.nor.tech".
        api_key (str | None): The API key for the Nortech API.
        ignore_pagination (bool | None): Whether to ignore pagination.
        user_agent (str | None): The user agent for the Nortech API.
        experimental_features (bool | None): Whether to enable experimental features.
        timeout (float | Timeout | None): The timeout setting for the API request. From [urllib3](https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html#urllib3.util.Timeout) package.
        retry (int | Retry | None): The retry setting for the API request. From [urllib3](https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html#urllib3.util.Retry) package.

        Example:
        ```python
        from urllib3 import Retry, Timeout

        from nortech import Nortech

        nortech = Nortech()  # Uses environment variables for configs

        nortech = Nortech(api_key="my_api_key")  # Sets the API key

        nortech = Nortech(ignore_pagination=False)  # Use pagination

        nortech = Nortech(user_agent="my_user_agent")  # Sets the user agent

        nortech = Nortech(timeout=Timeout(connect=10, read=60))  # Sets the timeout

        nortech = Nortech(
            retry=Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504],
                allowed_methods=["GET", "POST"],
                raise_on_status=False,
            )
        )  # Sets the retry configuration

        ```

        """
        api_settings = {}
        if api_key is not None:
            api_settings["KEY"] = api_key
        if ignore_pagination is not None:
            api_settings["IGNORE_PAGINATION"] = ignore_pagination
        if user_agent is not None:
            api_settings["USER_AGENT"] = user_agent
        if experimental_features is not None:
            api_settings["EXPERIMENTAL_FEATURES"] = experimental_features
        if timeout is not None:
            api_settings["TIMEOUT"] = timeout
        if retry is not None:
            api_settings["RETRY"] = retry

        api_settings["URL"] = url

        self.settings = NortechAPISettings(**api_settings)
        self.api = NortechAPI(self.settings)
        self.metadata = Metadata(self.api)
        self.datatools = Datatools(self.api)
        self.derivers = Derivers(self.api)
