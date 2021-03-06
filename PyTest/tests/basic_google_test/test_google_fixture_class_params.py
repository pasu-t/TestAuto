from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import pytest

@pytest.fixture(params= ["chrome", "firefox"], scope="class")
def init_driver(request):
	if request.param == "chrome":
		web_driver = webdriver.Chrome(ChromeDriverManager().install())
	elif request.param == "firefox":
		web_driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
	request.cls.driver = web_driver
	yield
	web_driver.quit()

@pytest.mark.usefixtures("init_driver")
class BaseTest():
	pass

class Test_Google(BaseTest):
	def test_google_title(self):
		self.driver.get("https://www.google.com")
		assert self.driver.title == "Google"

	def test_google_url(self):
		self.driver.get("https://www.google.com")
		assert self.driver.current_url == "google.com"


