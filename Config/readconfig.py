import configparser
import os

proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "Config.cfg")
path = os.path.abspath(configPath)

#Todo
# 读取配置文件
# ChromeconfigPath = os.path.join(proDir, "ChromeConfig.cfg")
# Chromepath =os.path.abspath(ChromeconfigPath)

#读取文件
conf = configparser.ConfigParser()
conf.read(path)

#Todo
# 读取chrome文件
# Chromeconf=configparser.ConfigParser()
# Chromeconf.read(Chromepath)

#账号、密码
username = conf.get("login", "username")
password = conf.get("login", "password")

#url
url = conf.get("platform", "url")

#浏览器驱动
driver = conf.get("driver","driver")

#Todo
# Chrome浏览器配置文件
# option = Chromeconf.get("option","option")
# print(option)
# 不允许在option里配置多个Option，找寻其他方法实现

#日志等级
log_level = conf.get("log_level","log_level")
