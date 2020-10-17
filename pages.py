from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains as chains
# Import
from test_data import TestData
from locators import Locators

class BasePage():
    """
        Kelas ini akan jadi parent untuk kelas lainnya
        Kelas ini akan memuat element dan fungsi yang dapat digunakan di kelas lain
    """
    def __init__(self, driver):
        self.driver = driver

    # Fungsi untuk click locator yang diberikan
    def click(self, locator):
        WDW(self.driver, 10).until(EC.element_to_be_clickable(locator)).click()

    # Fungsi enter teks
    def enter_text(self, locator, text):
        WDW(self.driver, 10).until(EC.element_to_be_clickable(locator)).send_keys(text)

    # Fungsi untuk memperoleh teks dari suatu locator
    def get_text(self, locator):
        return WDW(self.driver, 10).until(EC.visibility_of_element_located(locator)).text

    # Fungsi untuk mengecek visibility suuatu element
    def is_visible(self, locator):
        try:
            element = WDW(self.driver, 30).until(EC.visibility_of_element_located(locator))
            return bool(element)
        except TimeoutException:
            return False

    # fungsi untuk mouse hover and click elemet yang di hover
    def hover_to_click(self, locator):
        element = WDW(self.driver, 10).until(EC.presence_of_element_located(locator))
        chains(self.driver).move_to_element(element).click().perform()

    # fungsi untuk mouse hover and click element yang muncul setelah di hover
    def hover_to_click_element(self, locator1, locator2):
        element = WDW(self.driver,10).until(EC.presence_of_element_located(locator1))
        chains(self.driver).move_to_element(element).perform()
        WDW(self.driver, 10).until(EC.visibility_of_element_located(locator2)).click()

class LoginPage(BasePage):
    """
        Kelas ini untuk halaman login dashboard
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(TestData.BASE_URL_PRODUCTION)

    def login_admin_success(self):
        self.enter_text(Locators.LOGIN_INPUT_USERNAME, TestData.USERNAME_ADMIN)
        self.enter_text(Locators.LOGIN_INPUT_PASSWORD, TestData.PASSWORD_ADMIN)
        self.click(Locators.LOGIN_BUTTON)
        self.is_visible(Locators.LOGO_DASHBOARD_HEADER)

    def login_superadmin_success(self):
        self.enter_text(Locators.LOGIN_INPUT_USERNAME, TestData.USERNAME_SUPERADMIN)
        self.enter_text(Locators.LOGIN_INPUT_PASSWORD, TestData.PASSWORD_SUPERADMIN)
        self.click(Locators.LOGIN_BUTTON)
        self.is_visible(Locators.LOGO_DASHBOARD_HEADER)
        self.is_visible(Locators.ADMIN_MANAGEMENT_MENU_SIDER)

    def login_failed_if_wrong_username(self):
        self.enter_text(Locators.LOGIN_INPUT_USERNAME, TestData.WRONG_USERNAME)
        self.enter_text(Locators.LOGIN_INPUT_PASSWORD, TestData.PASSWORD_ADMIN)
        self.click(Locators.LOGIN_BUTTON)
        self.is_visible(Locators.LOGIN_ALERT_TOAST)

    def login_failed_if_wrong_password(self):
        self.enter_text(Locators.LOGIN_INPUT_USERNAME, TestData.USERNAME_ADMIN)
        self.enter_text(Locators.LOGIN_INPUT_PASSWORD, TestData.WRONG_PASSWORD)
        self.click(Locators.LOGIN_BUTTON)
        self.is_visible(Locators.LOGIN_ALERT_TOAST)

    def login_login_failed_if_no_fill_username_password(self):
        self.click(Locators.LOGIN_BUTTON)
        self.is_visible(Locators.LOGIN_ERROR_ALERT_USERNAME)
        self.is_visible(Locators.LOGIN_ERROR_ALERT_PASSWORD)



class DashboardPage(BasePage):
    """
        Kelas ini untuk halaman Dashboard
    """

    def __init__(self, driver):
        super().__init__(driver)

    def redirect_to_admin_management_page(self):
        self.click(Locators.ADMIN_MANAGEMENT_MENU_SIDER)
        self.is_visible(Locators.ADD_ADMIN_BUTTON)

    def redirect_to_atur_pengeluaran_page(self):
        self.click(Locators.CASHFLOW_MENU_SIDER)
        self.click(Locators.ATUR_PENGELUARAN_MENU)
        self.is_visible(Locators.ATUR_PENGELUARAN_PAGE_HEADER)

class AdminManagementPage(BasePage):
    """
        Kelas ini untuk halaman admin management
    """

    def __init__(self, driver):
        super().__init__(driver)

    def superadmin_success_add_admin(self):
        self.click(Locators.ADD_ADMIN_BUTTON)
        self.enter_text(Locators.ADD_ADMIN_NAME_INPUT, TestData.NAME_NEW_ADMIN)
        self.enter_text(Locators.ADD_ADMIN_EMAIL_INPUT, TestData.EMAIL_NEW_ADMIN)
        self.enter_text(Locators.ADD_ADMIN_USERNAME_INPUT, TestData.USERNAME_NEW_ADMIN)
        self.enter_text(Locators.ADD_ADMIN_PASSWORD_INPUT, TestData.PASSWORD_NEW_ADMIN)
        self.click(Locators.ADD_ADMIN_SIMPAN_BUTTON)
        self.is_visible(Locators.ADD_ADMIN_BUTTON)

    def superadmin_failed_add_admin_if_email_registered(self):
        self.click(Locators.ADD_ADMIN_BUTTON)
        self.enter_text(Locators.ADD_ADMIN_NAME_INPUT, TestData.RANDOM_NAME)
        self.enter_text(Locators.ADD_ADMIN_EMAIL_INPUT, TestData.EMAIL_REGISTERED)
        self.enter_text(Locators.ADD_ADMIN_USERNAME_INPUT, TestData.RANDOM_USERNAME)
        self.enter_text(Locators.ADD_ADMIN_PASSWORD_INPUT, TestData.PASSWORD_NEW_ADMIN)
        self.click(Locators.ADD_ADMIN_SIMPAN_BUTTON)
        self.is_visible(Locators.ALERT_FAILED_ADD_ADMIN)

    def superadmin_failed_add_admin_if_username_registered(self):
        self.click(Locators.ADD_ADMIN_BUTTON)
        self.enter_text(Locators.ADD_ADMIN_NAME_INPUT, TestData.RANDOM_NAME)
        self.enter_text(Locators.ADD_ADMIN_EMAIL_INPUT, TestData.RANDOM_EMAIL)
        self.enter_text(Locators.ADD_ADMIN_USERNAME_INPUT, TestData.USERNAME_ADMIN)
        self.enter_text(Locators.ADD_ADMIN_PASSWORD_INPUT, TestData.PASSWORD_NEW_ADMIN)
        self.click(Locators.ADD_ADMIN_SIMPAN_BUTTON)
        self.is_visible(Locators.ALERT_FAILED_ADD_ADMIN)

class AturPengeluaranPage(BasePage):
    """
        Kelas ini untuk halaman atur pengeluaran
    """

    def __init__(self, driver):
        super().__init__(driver)

    def search_data_atur_pengeluaran_found(self):
        self.enter_text(Locators.ATUR_PENGELUARAN_SEARCH_BAR, TestData.ACCOUNT_NUMBER_FOUND)
        self.is_visible(Locators.ATUR_PENGELUARAN_INFORMATION_COUNT_DATA)

    def search_data_atur_pengeluaran_not_found(self):
        self.enter_text(Locators.ATUR_PENGELUARAN_SEARCH_BAR, TestData.ACCOUNT_NUMBER_NOT_FOUND)
        self.is_visible(Locators.ATUR_PENGELUARAN_INFORMATION_COUNT_DATA)

