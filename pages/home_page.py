from selenium.webdriver.common.by import By 
from pages.base_page import BasePage

class HomePage(BasePage):
    PRODUCTS_TITLE = (By.CSS_SELECTOR, ".title")

    def get_title(self):
        return self.get_text(self.PRODUCTS_TITLE)
