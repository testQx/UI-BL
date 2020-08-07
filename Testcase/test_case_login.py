from page.Loginpage import Loginpage
import allure
from Config import readconfig

class Test_login():

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



    # @allure.feature("登陆模块")
    # @allure.story("输入错误用户名密码")
    # @allure.severity(allure.severity_level.BLOCKER)
    # @allure.testcase(url="www.baidu.com",name='该用例bug')
    # @allure.description("测试输入错误用户名密码登陆")
    # def test_s2(self):
    #     info = [{"name":"测试用户名1","password":"测试密码1"},{"name":"测试用户名2","password":"测试密码2"}]
    #     with allure.step("测试用例2步骤一{}".format(info[0]["name"])):
    #         print("执行步骤一")
    #     with allure.step("测试用例2步骤二{}".format(info[1]["name"])):
    #         print("执行步骤二")
    #         file = open(r'C:\Users\罗富权\Desktop\图片\test.jpg', mode='rb').read()
    #         allure.attach( file,'步骤二图片', allure.attachment_type.JPG)
