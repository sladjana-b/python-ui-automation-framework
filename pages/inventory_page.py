from selenium.webdriver.common.by import By

class InventoryPage:
    ITEM_LOCATOR = (By.CLASS_NAME, "inventory_item")
    CART_ICON = (By.ID, "shopping_cart_container")

    def __init__(self, driver):
        self.driver = driver 

    def get_items(self):
        return self.driver.find_elements(*self.ITEM_LOCATOR)
    
    def is_cart_icon_visible(self):
        return len(self.driver.find_elements(*self.CART_ICON))>0
    