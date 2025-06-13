import pytest
import uiautomator2 as u2
from utils.helpers import take_screenshot

from pytest_bdd import scenarios
from pathlib import Path

def pytest_sessionstart(session):
    features_dir = Path(__file__).parent / "tests" / "features"
    scenarios(features_dir)

@pytest.fixture(scope="session")
def driver():
    # Connect to device
    d = u2.connect()
    d.implicitly_wait(10)
    yield d
    d.app_stop("hko.MyObservatory_v1_0")

@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver):
    yield
    if request.node.session.testsfailed > 0:
        take_screenshot(driver, request.node.name)
