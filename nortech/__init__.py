from __future__ import annotations

from nortech.core import Metadata
from nortech.core.gateways.nortech_api import NortechAPI, NortechAPISettings
from nortech.datatools import Datatools
from nortech.derivers import Derivers


class Nortech:
    def __init__(
        self,
        url: str = "https://api.apps.nor.tech",
        api_key: str | None = None,
        ignore_pagination: bool | None = None,
        user_agent: str | None = None,
    ):
        api_settings = {}
        if api_key is not None:
            api_settings["KEY"] = api_key
        if ignore_pagination is not None:
            api_settings["IGNORE_PAGINATION"] = ignore_pagination
        if user_agent is not None:
            api_settings["USER_AGENT"] = user_agent

        api_settings["URL"] = url

        self.settings = NortechAPISettings(**api_settings)

        self.api = NortechAPI(self.settings)
        self.metadata = Metadata(self.api)
        self.datatools = Datatools(self.api)
        self.derivers = Derivers(self.api)
