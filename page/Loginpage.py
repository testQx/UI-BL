from Base.Baseapi import Baseapi
from selenium.webdriver.common.by import By

from page.Mainpage import Mainpage


class Loginpage(Baseapi):
    username=(By.XPATH,"//*[@id='username']")
    password=(By.XPATH,"//*[@id='password']")
    loginclick=(By.XPATH,"//*[@id='submit']")
    test=(By.XPATH, "//*[@id='submit']")

    def inputusername(self,agentusername):
        self.send_keys_clear(self.username,agentusername)
        return self

    def inputpassword(self,agentpassword):
        self.send_keys_clear(self.password,agentpassword)
        return self

    def inputdevusername(self,agentusername):
        self.send_keys_clear(self.devusername,agentusername)
        return self

    def inputdevpassword(self,agentpassword):
        self.send_keys_clear(self.devpassword,agentpassword)
        return self

    def loginagent(self):
        self.click(self.loginclick)
        return Mainpage()

    def selectdev(self):
        self.click(self.devcenter)
        return self


