import pytest

from nortech import Nortech
from nortech.gateways.nortech_api import (
    NortechAPISettings,
)


@pytest.fixture(scope="session", name="nortech_api_settings")
def nortech_api_settings_fixture() -> NortechAPISettings:
    return NortechAPISettings(URL="http://mock-customer-api.com", KEY="test_token")  # noqa: S106


@pytest.fixture(scope="session", name="nortech")
def nortech_fixture(nortech_api_settings: NortechAPISettings) -> Nortech:
    return Nortech(url=nortech_api_settings.URL, api_key=nortech_api_settings.KEY)
