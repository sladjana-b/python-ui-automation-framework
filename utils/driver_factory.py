from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os


def create_driver():
    options = webdriver.ChromeOptions()

    # Detect CI environment
    is_ci = os.environ.get("CI") == "true"

    if is_ci:
        # -----------------------------
        # SETTINGS FOR GITHUB ACTIONS
        # -----------------------------
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
    else:
        # -----------------------------
        # LOCAL SETTINGS
        # -----------------------------
        clean_profile_path = os.path.join(os.getcwd(), "selenium_clean_profile")
        options.add_argument(f"--user-data-dir={clean_profile_path}")
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--incognito")
        options.add_argument("--start-maximized")

        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "autofill.profile_enabled": False,
            "autofill.credit_card_enabled": False,
            "autofill.autocomplete_enabled": False,
            "profile.default_content_setting_values.notifications": 2
        }
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--disable-features=PasswordManager,CredentialManager,Autofill")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver
