import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.inventory_page import InventoryPage


def test_successful_login(driver):
    login = LoginPage(driver)
    login.open()
    login.login("standard_user", "secret_sauce")

    home = HomePage(driver)
    assert home.get_title() == "Products"

    #input("STOP, Enter za nastavak")

def test_invalid_login(driver):
    login = LoginPage(driver)
    login.open()
    login.login("standard_user", "pogresan_password")

    assert "do not match" in login.get_error()

def test_inventory_items(login_as_standard_user, driver):
    inventory = InventoryPage(driver)
    items = inventory.get_items()
    assert len(items) > 0, "Inv.list shouldn't be empty"
 
def test_cart_icon_is_visible(login_as_standard_user, driver):
    page = InventoryPage(driver)
    assert page.is_cart_icon_visible(), "Cart icon should be seen after successfull login"