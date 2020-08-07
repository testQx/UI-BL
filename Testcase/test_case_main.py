import allure

from Config import readconfig
from page.Loginpage import Loginpage



class Test_main():

    def setup(self):
        self.page=Loginpage()

    @allure.feature("登陆模块")
    @allure.story("输入正确用户名密码")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.testcase(url="www.baidu.com",name='该用例bug')
    @allure.description("测试输入错误用户名密码登陆")
    def test_login_1(self):
        title=self.page.inputusername(readconfig.username).inputpassword(readconfig.password).loginagent().loginjid()
        try:
            assert title=='进入技能组成功'
        except Exception as e:
            print("进入技能组失败")
            raise e