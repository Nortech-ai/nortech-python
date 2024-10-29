from __future__ import annotations

from nortech.core import Metadata
from nortech.core.gateways.nortech_api import NortechAPI, NortechAPISettings
from nortech.datatools import Datatools
from nortech.derivers import Derivers


class Nortech:
    def __init__(
        self, api_key: str | None = None, ignore_pagination: bool | None = None, user_agent: str | None = None
    ):
        api_settings = {}
        if api_key is not None:
            api_settings["KEY"] = api_key
        if ignore_pagination is not None:
            api_settings["IGNORE_PAGINATION"] = ignore_pagination
        if user_agent is not None:
            api_settings["USER_AGENT"] = user_agent

        nortech_api = NortechAPI(NortechAPISettings(**api_settings))
        self.metadata = Metadata(nortech_api)
        self.datatools = Datatools(nortech_api)
        self.derivers = Derivers(nortech_api)
