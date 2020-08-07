from loguru import logger
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from Common.Log import log
from Testcase import conftest


class Baseapi:
    # 该写法不适合用于fixture，使用Setup,terardown时使用
    # def __init__(self,driver:WebDriver=None,browser='chrome'):
    # if driver == None:
    #     if browser=='chrome':
    #         option=webdriver.ChromeOptions()
    #     option.add_argument('disable-infobars')
    #     self.driver= webdriver.Chrome(options=option)
    # else:
    #     self.driver=driver
    # self.driver.maximize_window()
    # self.driver.get(readconfig.url)

    def __init__(self):
        self.driver: WebDriver = conftest.driver
        self.mylog = log()
        self.action = ActionChains(self.driver)

    def find_element(self, element):
        if not isinstance(element, tuple):
            self.mylog.error('find_element：locator参数类型错误，必须传元祖类型：locator=(By.XX,"value")，错误参数为：{}'.format(element))
        else:
            self.mylog.info("find_element：正在定位元素信息：定位方式->%s,value值->%s" % (element[0], element[1]))
        try:
            '''
            若传值进来是调用find_element((By.XPATH, "//*[@id='username']"))
            find_element(slef,*element)，此时element变为(('tes1', "//*[@id='username']"),)
            相当于反向增加了一层元组
            ==================
            此方法等同于find_element(*(By.XPATH, "//*[@id='username']"))
            WebDriverWait(self.driver,10).until(EC.visibility_of_element_located(*element))
            return self.driver.find_element(element)         
            '''
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(element))
            return self.driver.find_element(*element)
        except Exception as e:
            self.mylog.error(f"找不到元素{element}")

    #   重写find_elements方法，增加定位元素的健壮性
    def find_elements(self, element):
        if not isinstance(element, tuple):
            self.mylog.error('find_element：locator参数类型错误，必须传元祖类型：locator=(By.XX,"value")，错误参数为：{}'.format(element))
        else:
            self.mylog.info("find_element：正在定位元素信息：定位方式->%s,value值->%s" % (element[0], element[1]))
        try:
            # 确保元素是可见的。
            # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(element))
            return self.driver.find_elements(*element)
        except Exception as e:
            self.mylog.error(f"找不到元素{element}")

    # 完全关闭所有关联tab窗口的浏览器，在fixture中不使用该方法
    def quit_browse(self):
        self.driver.quit()
        self.mylog.info(u"关闭所有浏览器")

    # 关闭当前窗口浏览器，在fixture中不使用该方法
    def close(self):
        try:
            self.driver.close()
            self.mylog.info(u"关闭当前窗口")
        except Exception as e:
            pass
            self.mylog.error(u"关闭当前窗口失败原因： %s" % e)
            raise e

    # 浏览器前进操作
    def forward(self):
        self.driver.forward()
        self.mylog.info(u"点击浏览器进入下一页")

    # 浏览器后退操作
    def back(self):
        self.driver.back()
        self.mylog.info(u"点击浏览器返回上一页")

    # 配置隐式等待
    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)
        self.mylog.info(u"隐式等待时间为 %d 秒" % seconds)

    # 切换到最新窗口
    def Current_handel(self):
        # 获取所有句柄
        all_handles = self.driver.window_handles
        # 切换到最新窗口
        print(all_handles)
        self.driver.switch_to.window(all_handles[-1])
        self.mylog.info(u"最新窗口为 %s " % self.driver.title)

    def get_text(self, element):
        el = self.element_light(element).text
        return el

    # 输入，重新send_keys,先清除后输入
    def send_keys_clear(self, element, text):
        try:
            el = self.element_light(element)
            el.clear()
            el.send_keys(text)
            self.mylog.info(u"元素对象属于值成功，值为%s" % text)
        except Exception as e:
            self.mylog.error("元素对象输入值失败，错误信息为：{}".format(e))
            raise e

    # 输入，重新send_keys,继续输入，不清空
    def send_keys(self, element, text):
        try:
            el = self.element_light(element)
            el.send_keys(text)
            self.mylog.info(u"元素对象属于值成功，值为%s" % text)
        except Exception as e:
            self.mylog.error("元素对象输入值失败，错误信息为：{}".format(e))
            raise e

    # 单击元素
    def click(self, element):
        try:
            el = self.element_light(element)
            el.click()
            self.mylog.info("元素对象点击成功")
        except Exception as e:
            self.mylog.error(u"点击元素失败： %s" % e)
            raise e

    # 通过文本获取下拉菜单元素并点击
    def select_element_text(self, element, text):
        try:
            el = self.element_light(element)
            Select(el).select_by_visible_text(text)
        except Exception as e:
            self.mylog.error(u'找不到元素:' + str(element))
            raise e

    # 通过value获取下拉菜单元素并点击
    def select_element_value(self, element, value):
        try:
            el = self.element_light(element)
            Select(el).select_by_value(value)
        except Exception as e:
            self.mylog.error(u'找不到元素:' + str(element))
            raise e

    # 通过index获取下拉菜单元素并点击
    def select_element_index(self, element, index):
        try:
            el = self.element_light(element)
            Select(el).select_by_index(index)
        except Exception as e:
            self.mylog.error(u'找不到元素:' + str(element))
            raise e

    # 获取元素的属性值
    # 例子<a class="left" target="_blank" href="http://www.csdn.net" onclick="LogClickCount(this,285);">首页</a>
    # 此例子不可获取"首页"两字，非text
    def get_Attribute(self, element, value):
        el = self.driver.find_element(element).get_attribute(value)
        return el

    # 切换iframe
    def iframe(self, element):
        try:
            self.driver.switch_to.frame(element)
        except Exception as e:
            self.mylog.error(u'切换iframe失败:' + str(element))
            raise e

    # 返回默认iframe
    def iframe_defalut(self):
        return self.driver.switch_to.default_content()

    # 校验按钮是否为选中状态
    def is_selected(self, element):
        el = self.element_light(element)
        try:
            EC.elementSelectionStateToBe(element, True)
            print(u"元素 %s 已被选中" % el)
        except Exception as e:
            # if el.is_selected():
            #     print(el + "被选中")
            # else:
            print(u"元素未被选中 %s" % el)
            raise e

    # 获取网页标题
    def get_page_title(self):
        logger.info("网页标题为： %s" % self.driver.title)
        return self.driver.title

    # 清空内容
    def clear(self, element):
        el = self.element_light(element)
        el.clear()

    # 获取元素的value属性
    def get_value(self, element):
        return self.driver.find_element(element).get_attribute("value")

    # 双击元素
    def double_click(self, element):
        try:
            el = self.element_light(element)
            self.action.double_click(el)
            self.action.perform()
        except Exception as e:
            self.mylog.error(u"双击元素失败： %s" % el)
            raise e

    # 拖拽元素A至元素B
    def drag_and_drop(self, elementA, elementB):
        try:
            el1 = self.element_light(elementA)
            el2 = self.element_light(elementB)
            self.action.drag_and_drop(el1, el2)
            self.action.perform()
        except Exception as e:
            self.mylog.error(u"拖拽元素 %s 失败： %s" % el1, el2)
            raise e

    # 拖拽元素至指定位置
    def drag_and_drop_by_offset(self, element, xoffset, yoffset):
        try:
            el = self.element_light(element)
            self.action.drag_and_drop_by_offset(el, xoffset, yoffset)
            self.action.perform()
        except Exception as e:
            self.mylog.error(u"拖拽元素 %s 失败" % el)
            raise e

    # 将元素高亮
    def element_light(self, element):
        el = self.find_element(element)
        js = 'arguments[0].style.border="3px solid red"'
        try:
            self.driver.execute_script(js, el)
            return el
        except Exception as e:
            logger.error("该元素找不到，无法高亮")
            raise e

    # 鼠标单击并且不放开
    def click_and_hold(self, element):
        try:
            el = self.element_light(element)
            self.action.click_and_hold(el)
            self.action.perform()
        except Exception as e:
            self.mylog.error(u"单击元素不放失败： %s" % el)
            raise e

    # 释放按下的鼠标
    def click_and_hold_relax(self, element):
        try:
            el = self.element_light(element)
            self.action.send_keys(el)
            self.action.perform()
        except Exception as e:
            self.mylog.error(u'释放鼠标失败 ：%s' % el)
            raise e

    # 移动鼠标至某个元素
    def move_to_element(self, element):
        try:
            el = self.element_light(element)
            self.action.move_to_element(el)
            self.action.perform()
        except Exception as e:
            self.mylog.error(u'移动鼠标失败 ：%s' % el)
            raise e

    # 执行js脚本
    def execute_js(self, element, js_file):
        try:
            el = self.element_light(element)
            js = 'arguments[0].' + js_file
            self.driver.execute_script(js, el)

        except Exception as e:
            self.mylog.error(u'执行js脚本失败 ：%s' % el)
            raise e

    # 通过js控制滚动条
    def js_scroll(self, element):
        el = self.find_element(element)
        js = '"arguments[0].scrollIntoView();", org'
        self.driver.execute_script(js, el)

    # 通过js滚动到顶部
    def js_scroll_top(self, element):
        el = self.find_element(element)
        js = 'arguments[0].scrollTop=0'
        self.driver.execute_script(js, el)

    # 通过js滚动到底部
    def js_scroll_down(self, element):
        el = self.find_element(element)
        js = 'arguments[0].scrollTop=10000'
        self.driver.execute_script(js, el)

    # 通过js进行自定义横向/纵向滚动
    def js_scroll_down(self, x, y):
        js = f'window.scrollTo({x},{y});'
        self.driver.execute_script(js)

    # 通过js处理富文本，不需要切换iframe
    def js_richbox(self, element, body):
        el = self.find_element(element)
        js = f'arguments[0].contentWindow.document.body.innerHTML="%s" %{body}'
        self.driver.execute_script(js, el)

    # 处理伪元素
    def js_faker_elem(self, element):
        el = self.find_element(element)
        js = "return window.getComputedStyle(arguments[0], '::before').content"
        self.driver.execute_script(js, el)

# Todo
# 增加TouchActions操作
