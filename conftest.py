import pytest
import os
from datetime import datetime
from utils.driver_factory import create_driver
from selenium.webdriver.remote.webdriver import WebDriver
import base64
import pytest_html


# ==============================
# DRIVER FIXTURE
# ==============================
@pytest.fixture
def driver(request) -> WebDriver:
    driver = create_driver()
    yield driver

    # ========== SCREENSHOT ON FAIL/PASS ==========
    if request.node.rep_call.failed:
        status = "FAIL"
    else:
        status = "PASS"

    test_name = request.node.name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    os.makedirs("screenshots", exist_ok=True)
    screenshot_name = f"{test_name}_{status}_{timestamp}.png"
    screenshot_path = os.path.join("screenshots", screenshot_name)

    driver.save_screenshot(screenshot_path)
    print(f"\n[Screenshot saved]: {screenshot_path}")

    driver.quit()


# ==============================
# PYTEST HOOK – allows knowing PASS/FAIL
# ==============================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook koji:
    - omogućava pristup rep_call.failed u fixture-u
    - embeduje screenshot u HTML report
    """
    outcome = yield
    rep = outcome.get_result()

    # daje nam rep_setup, rep_call, rep_teardown
    setattr(item, "rep_" + rep.when, rep)

    # ---- samo embedujemo screenshot u CALL fazi ----
    if rep.when != "call":
        return

    screenshots_dir = "screenshots"
    test_name = item.name

    # pronađi screenshot fajl
    screenshot_file = None
    for file in os.listdir(screenshots_dir):
        if file.startswith(test_name) and file.endswith(".png"):
            screenshot_file = os.path.join(screenshots_dir, file)
            break

    if not screenshot_file:
        return

    # Učitaj sliku i encode-uj za HTML
    with open(screenshot_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    html = (
        f'<div>'
        f'<img src="data:image/png;base64,{encoded}" '
        f'style="width:300px; border:2px solid #555; margin:5px;" />'
        f'</div>'
    )

    extra = getattr(rep, "extra", [])
    extra.append(pytest_html.extras.html(html))
    rep.extra = extra
