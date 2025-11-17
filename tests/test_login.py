import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.login_page import LoginPage
from pages.home_page import HomePage


def test_successful_login(driver):
    login = LoginPage(driver)
    login.open()
    login.login("standard_user", "secret_sauce")

    home = HomePage(driver)
    assert home.get_title() == "Products"

    input("STOP: Pogledaj broswer i pritisni ENTER..")

    def test_invalid_login(driver):
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "pogresan_password")

        assert "do not match" in login.get_error()