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

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    

    outcome = yield
    rep = outcome.get_result()

    setattr(item, "rep_" + rep.when, rep)

    if rep.when != "call":
        return

    screenshots_dir = "screenshots"
    test_name = item.name

    screenshot_file = None
    for file in os.listdir(screenshots_dir):
        if file.startswith(test_name) and file.endswith(".png"):
            screenshot_file = os.path.join(screenshots_dir, file)
            break

    if not screenshot_file:
        return

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
