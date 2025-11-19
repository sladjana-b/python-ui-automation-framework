import pytest
import os
from datetime import datetime
from utils.driver_factory import create_driver
from selenium.webdriver.remote.webdriver import WebDriver
from pages.login_page import LoginPage
import base64
import pytest_html


@pytest.fixture
def driver(request):
    driver = create_driver()
    yield driver

    # ========== SCREENSHOT ON FAIL/PASS ==========
    status = "FAIL" if request.node.rep_call.failed else "PASS"
    test_name = request.node.name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    screenshot_name = f"{test_name}_{status}_{timestamp}.png"
    screenshot_path = os.path.join(screenshots_dir, screenshot_name)

    driver.save_screenshot(screenshot_path)
    print(f"\n[Screenshot saved]: {screenshot_path}")

    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Attach rep to item so fixture can use it
    setattr(item, "rep_" + rep.when, rep)

    # Only run this for the "call" phase (not setup/teardown)
    if rep.when != "call":
        return

    screenshots_dir = "screenshots"

    # If folder does not exist OR is empty — skip gracefully
    if not os.path.exists(screenshots_dir) or not os.listdir(screenshots_dir):
        return

    # Look for screenshot matching test name
    screenshot_file = None
    for file in os.listdir(screenshots_dir):
        if file.startswith(item.name) and file.endswith(".png"):
            screenshot_file = os.path.join(screenshots_dir, file)
            break

    if not screenshot_file:
        return

    # Attach screenshot to HTML report
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


@pytest.fixture
def login_as_standard_user(driver):
    login = LoginPage(driver)
    login.open()
    login.login("standard_user", "secret_sauce")
    return driver
