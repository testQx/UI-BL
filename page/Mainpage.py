from Base.Baseapi import Baseapi
from selenium.webdriver.common.by import By

class Mainpage(Baseapi):

    jidselect = (By.XPATH, "//*[@id='tbody']/tr[1]/td[1]/input")
    surekey = (By.XPATH, "/html/body/div[2]/button")
    jidselectiframe = (By.XPATH, "/html/body/div[4]/div[2]/iframe")
    title = (By.XPATH, "//div[@class='layui-layer-content']")

    def loginjid(self):
        iframe = self.find_element(self.jidselectiframe)
        self.iframe(iframe)
        self.click(self.jidselect)
        self.click(self.surekey)
        self.iframe_defalut()
        return self.get_text(self.title)