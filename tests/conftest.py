import pytest

from nortech.common.gateways.nortech_api import (
    NortechAPI,
    NortechAPISettings,
)


@pytest.fixture(scope="session", name="nortech_api_settings")
def nortech_api_settings_fixture() -> NortechAPISettings:
    return NortechAPISettings(URL="http://mock-customer-api.com", TOKEN="test_token")  # noqa: S106


@pytest.fixture(scope="session", name="nortech_api")
def nortech_api_fixture(nortech_api_settings: NortechAPISettings) -> NortechAPI:
    return NortechAPI(nortech_api_settings)
