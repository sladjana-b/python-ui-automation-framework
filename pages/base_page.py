from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class BasePage:
    def __init__(self, driver):
        self.driver = driver 
        self.wait = WebDriverWait(driver, 10)

    def find(self, locator):
        return self.driver.find_element(*locator)
    
    def click(self, locator):
        self.find(locator).click()

    def type(self, locator, text):
        self.find(locator).send_keys(text)
    
    def get_text(self, locator):
        return self.find(locator).text