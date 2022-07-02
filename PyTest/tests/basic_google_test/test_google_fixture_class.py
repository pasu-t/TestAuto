from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import pytest

@pytest.fixture(scope="class")
def init_chrome_driver(request):
    ch_driver = webdriver.Chrome(ChromeDriverManager().install())
    request.cls.driver = ch_driver
    yield
    ch_driver.quit()

@pytest.fixture(scope="class")
def init_ff_driver(request):
    ff_driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    request.cls.driver = ff_driver
    yield
    ff_driver.quit()

@pytest.mark.usefixtures("init_chrome_driver")
class Base_Chrome_Test:
    pass

class Test_Goole_Chrome(Base_Chrome_Test):
    def test_google_title_chrome(self):
        self.driver.get("https://www.google.com")
        assert self.driver.title == "Google"


@pytest.mark.usefixtures("init_ff_driver")
class Base_FireFox_Test:
    pass

class Test_Goole_Firefox(Base_FireFox_Test):
    def test_google_title_firefox(self):
        self.driver.get("https://www.google.com")
        assert self.driver.title == "Google"


#pytest test_google_fixture_class.py -v -s --html=test_fix_class.html