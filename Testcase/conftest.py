import pytest
import time
import os
import sys
from selenium import webdriver
from loguru import logger
from Config import readconfig
import allure
import run

driver =None
dirname = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
osname = os.popen('uname').read().split()[0]
# 添加根目录路径至环境变量中
sys.path.append(dirname)
# 当前时间值
now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
# 截图存放文件夹
screenshot = dirname + f'/screenshot/{run.thread_num}/{now}'

def pytest_addoption(parser):

    """
    定义钩子函数hook进行命令行定义浏览器传参，默认chrome,定义浏览器启动方式传参，默认启动
    @param parser:
    @return:
    """
    # 浏览器选项
    parser.addoption("--browser", action="store", default="chrome", help="browser option: firefox or chrome or ie")
    # 是否开启浏览器界面选项
    parser.addoption("--browser_opt", action="store", default="open", help="browser GUI open or close")
    # driver选项，本地还是远程模式
    parser.addoption("--type_driver", action="store", default="local", help="type of driver: local or remote")


def pytest_collection_modifyitems(items):
    """
    定义钩子函数hook进行测试用例name和_nodeid输出
    @param items:
    @return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        logger.info(item.name)
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode_escape")
        logger.info(item._nodeid)




#截图
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            # let's also access a fixture for the fun of it
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + "\n")
        # pic_info = adb_screen_shot()
        with allure.step('添加失败截图...'):
            now1 = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
            allure.attach(driver.get_screenshot_as_png(),now1+"失败截图", allure.attachment_type.PNG)
            driver.get_screenshot_as_file(screenshot+'/'+now1+".png")

#初始化环境
@pytest.fixture(scope="session",autouse=True)
def bulid_env():
    #新建log日志存放文件夹s
    log_level=readconfig.log_level
    logger.add(f"{dirname}"+"/log/"+f"{run.thread_num}/"+"file_{time}.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",level=f"{log_level}")
    isExists = os.path.exists(screenshot)
    if not isExists:
        os.makedirs(screenshot)


#启动浏览器
@pytest.fixture(scope="session",autouse=True)
def start_browser():
    global driver
    # 浏览器驱动存放位置
    #Todo
    # 增加Drivertool目录下具体drive
    if osname == 'Darwin':
        chrome_driver_path = dirname + r'/Drivertool/chromedriver'
        ie_driver_path = dirname + r'/Drivertool/iedriver'
        fire_driver_path = dirname + r'/Drivertool/firedriver'
        phantomJs_driver_path = dirname + r'/Drivertool/phantomJs'
    else:
        chrome_driver_path = dirname + r'\Drivertool\chromedriver.exe'
        ie_driver_path = dirname + r'\Drivertool\iedriver.exe'
        fire_driver_path = dirname + r'\Drivertool\firedriver.exe'
        phantomJs_driver_path = dirname + r'\Drivertool\phantomJs.exe'
    if readconfig.driver == "Chrome":
        #Todo
        # 需要增加添加配置文件参数
        # option = webdriver.ChromeOptions()
        # option.add_argument('disable-infobars')
        driver = webdriver.Chrome(chrome_driver_path)
    elif readconfig.driver == "Firefox":
        driver = webdriver.Firefox(fire_driver_path)
    elif readconfig.driver == "IE":
        driver = webdriver.Ie(ie_driver_path)
    else:
        #Todo
        # 下载PhantomJS浏览器并配置相应path
        driver = webdriver.PhantomJS(phantomJs_driver_path)
    #窗口最大化
    driver.maximize_window()
    driver.get(readconfig.url)
    yield
    if not os.listdir(screenshot) :
        os.rmdir(screenshot)
    #关闭浏览器
    driver.quit()
