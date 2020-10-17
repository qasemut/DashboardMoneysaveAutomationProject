import unittest
from selenium import webdriver

from test_data import TestData
from locators import Locators
from pages import LoginPage, DashboardPage, AdminManagementPage, AturPengeluaranPage

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=TestData.CHROME)
        self.driver.set_window_size(1366, 768)
        # self.driver.maximize_window()
    def tearDown(self):
        self.driver.quit()


class LoginDashboardTest(BaseTest):
    def test_login_superadmin_success(self):
        """
        Test case untuk berhasil login sebagai superadmin

        """
        # membuat objek loginpage
        self.loginpage = LoginPage(self.driver)

        # Step 1 - input username dan password sebagai superadmin kemudian klik login
        self.loginpage.login_superadmin_success()

        # membuat objek dashboard page
        self.dashboardpage = DashboardPage(self.driver)

        # Step 2 - Assertion
        self.dashboardpage.is_visible(Locators.LOGO_DASHBOARD_HEADER)
        self.dashboardpage.is_visible(Locators.ADMIN_MANAGEMENT_MENU_SIDER)

    def test_login_admin_success(self):
        """
        Test case untuk berhasil login sebagai admin

        """
        # membuat objek loginpage
        self.loginpage = LoginPage(self.driver)

        # Step 1 - input username dan password sebagai admiin kemudian klik login
        self.loginpage.login_admin_success()

        # membuat objek dashboard page
        self.dashboardpage = DashboardPage(self.driver)

        # Step 2 - Assertion
        self.dashboardpage.is_visible(Locators.LOGO_DASHBOARD_HEADER)

    def test_login_failed_wrong_username(self):
        """
        Test case untuk memastikan bahwa login akan gagal kemudian muncul toast alert jika username salah

        """
        # membuat objek loginpage
        self.loginpage = LoginPage(self.driver)

        # Step 1 - input wrong username, input password kemudian klik tombol login
        self.loginpage.login_failed_if_wrong_username()

        # Step 2 - Assertion
        self.loginpage.is_visible(Locators.LOGIN_ALERT_TOAST)

    def test_login_failed_wrong_password(self):
        """
        Test case untuk memastikan bahwa login akan gagal kemudian muncul toast alert jika password salah

        """
        # membuat objek loginpage
        self.loginpage = LoginPage(self.driver)

        # Step 1 - input  username, input wrong password kemudian klik tombol login
        self.loginpage.login_failed_if_wrong_password()

        # Step 2 - Assertion
        self.loginpage.is_visible(Locators.LOGIN_ALERT_TOAST)

    def test_login_failed_no_fill_username_password(self):
        """
        Test case untuk memastikan bahwa login akan gagal kemudian mucul warning alert jika tidak menginput username dan password
        """
        # membuat objek loginpage
        self.loginpage = LoginPage(self.driver)

        # Step 1 - no fill username and password, click login button
        self.loginpage.login_login_failed_if_no_fill_username_password()

        # Step 2 - Assertion
        element_text = self.loginpage.get_text(Locators.LOGIN_ERROR_ALERT_USERNAME)
        element_text1 = self.loginpage.get_text(Locators.LOGIN_ERROR_ALERT_PASSWORD)
        self.assertEqual("Mohon masukkan username", element_text)
        self.assertEqual("Mohon masukkan password", element_text1)

class AdminManagementTest(BaseTest):
    def test_add_admin_success(self):
        """
        Test case untuk  super admin berhasil menambah admin
        """
        # membuat objek loginpage
        self.loginpage = LoginPage(self.driver)

        # Step 1 - login sebagai superadmin
        self.loginpage.login_superadmin_success()

        # membuat objek dashboard page
        self.dashboardpage = DashboardPage(self.driver)

        # Step 2 - Click menu admin management
        self.dashboardpage.redirect_to_admin_management_page()

        #membuat objek admin management page
        self.adminmanagementpage = AdminManagementPage(self.driver)

        # Step 3 - Click add admin button dan lengkapi form tambah data admin
        self.adminmanagementpage.superadmin_success_add_admin()

        # Step 4 - Assertion
        self.adminmanagementpage.is_visible(Locators.ADD_ADMIN_BUTTON)

    def test_add_admin_failed_email_registered(self):
        """
        Test case untuk memastikan bahwa superadmin tidak dapat menambahkan admin jika email telah terdaftar
        """
        # membuat objek loginpage
        self.loginpage = LoginPage(self.driver)

        # Step 1 - login sebagai superadmin
        self.loginpage.login_superadmin_success()

        # membuat objek dashboard page
        self.dashboardpage = DashboardPage(self.driver)

        # Step 2 - Click menu admin management
        self.dashboardpage.redirect_to_admin_management_page()

        # membuat objek admin management page
        self.adminmanagementpage = AdminManagementPage(self.driver)

        # Step 3 - Click add admin button dan lengkapi form tambah data admin
        self.adminmanagementpage.superadmin_failed_add_admin_if_email_registered()

        # Step 4 - Assertion
        element_text = self.adminmanagementpage.get_text(Locators.ALERT_FAILED_ADD_ADMIN)
        self.assertEqual("Email is already in use!", element_text)

    def test_add_admin_failed_username_registered(self):
        """
        Test case untuk memastikan bahwa superadmin tidak dapat menambahkan admin jika username telah terdaftar
        """
        # membuat objek loginpage
        self.loginpage = LoginPage(self.driver)

        # Step 1 - login sebagai superadmin
        self.loginpage.login_superadmin_success()

        # membuat objek dashboard page
        self.dashboardpage = DashboardPage(self.driver)

        # Step 2 - Click menu admin management
        self.dashboardpage.redirect_to_admin_management_page()

        # membuat objek admin management page
        self.adminmanagementpage = AdminManagementPage(self.driver)

        # Step 3 - Click add admin button dan lengkapi form tambah data admin
        self.adminmanagementpage.superadmin_failed_add_admin_if_username_registered()

        # Step 4 - Assertion
        element_text = self.adminmanagementpage.get_text(Locators.ALERT_FAILED_ADD_ADMIN)
        self.assertEqual("Username is already in use!", element_text)

class AturPengeluaranTest(BaseTest):
    def test_search_data_found(self):
        """
        Test case untuk mencari data atur pengeluaran dengan account number yang ada
        """
        # membuat objek loginpage
        self.loginpage = LoginPage(self.driver)

        # Step 1 - login
        self.loginpage.login_admin_success()

        # membuat objek dashboard page
        self.dashboardpage = DashboardPage(self.driver)

        # Step 2 - Click menu cashflow and choose atur pengengeluaran
        self.dashboardpage.redirect_to_atur_pengeluaran_page()

        # membuat objek atur pengeluaran page
        self.aturpengeluaranpage = AturPengeluaranPage(self.driver)

        # Step 3 - input no rekening di search bar
        self.aturpengeluaranpage.search_data_atur_pengeluaran_found()

        # Step 4 - Assertion
        element_text = self.aturpengeluaranpage.get_text(Locators.ATUR_PENGELUARAN_INFORMATION_COUNT_DATA)
        self.assertNotEqual('Menampilkan semua "0 atur pengeluaran"', element_text)

    def test_serach_data_not_found(self):
        """
        Test case untuk mencari data atur pengeluaran dengan account number yang tidak ada
        """
        # membuat objek loginpage
        self.loginpage = LoginPage(self.driver)

        # Step 1 - login
        self.loginpage.login_admin_success()

        # membuat objek dashboard page
        self.dashboardpage = DashboardPage(self.driver)

        # Step 2 - Click menu cashflow and choose atur pengengeluaran
        self.dashboardpage.redirect_to_atur_pengeluaran_page()

        # membuat objek atur pengeluaran page
        self.aturpengeluaranpage = AturPengeluaranPage(self.driver)

        # Step 3 - input no rekening di search bar
        self.aturpengeluaranpage.search_data_atur_pengeluaran_not_found()

        # Step 4 - Assertion
        element_text = self.aturpengeluaranpage.get_text(Locators.ATUR_PENGELUARAN_INFORMATION_COUNT_DATA)
        self.assertEqual('Menampilkan semua "0 atur pengeluaran"', element_text)