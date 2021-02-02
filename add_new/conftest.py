from selenium import webdriver
import pytest
from pages.user_login_page import UserLoginPage
from selenium.webdriver.chrome.options import Options
import platform


@pytest.fixture(scope="session", name="driver")
def browser():
    '''定义全局driver'''
    if platform.system() == 'Windows':
        # windows系统
        _driver = webdriver.Chrome()
        _driver.maximize_window()

    else:
        # linux启动
        chrome_options = Options()
        chrome_options.add_argument('--window-size=1920,1080')  # 设置当前窗口的宽度和高度
        chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在报错问题
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')   # 禁用GPU硬件加速。如果软件渲染器没有就位，则GPU进程将不会启动。
        chrome_options.add_argument('--headless')  # 无界面

        # _driver = webdriver.Chrome()
        _driver = webdriver.Chrome(chrome_options=chrome_options)

    yield _driver
    # quit是退出浏览器
    _driver.quit()


# @pytest.fixture(scope="session", name="driver")
# def browser():
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')  # 无界面
#     chrome_options.add_argument('--window-size=1920,1080')  # 设置当前窗口的宽度和高度
#     driver =  webdriver.Chrome(options=chrome_options)
#     # driver = webdriver.Chrome()
#     # driver.maximize_window()  # 最大化窗口
#     yield driver
#     driver.quit()


@pytest.fixture(scope="session")
def base_url():
    return "http://49.235.92.12:8200"


@pytest.fixture(scope="session")
def login_instance(driver, base_url):
    login_ins = UserLoginPage(driver, base_url)
    return login_ins
