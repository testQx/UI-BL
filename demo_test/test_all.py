from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import Remote
import logging
import threading
logging.basicConfig(level=logging.INFO)

class TestGrid:
    def test_griod(self):
        global hub_url
        hub_url="http://127.0.0.1:4444/wd/hub"
        global capability
        capability=DesiredCapabilities.CHROME.copy()
        # capability1=DesiredCapabilities.FIREFOX.copy()
        self.loops=[1,2,3,4]
        threads = []
        nloops = range(len(self.loops))
        for i in nloops:
            t = threading.Thread(target=self.loop)
            threads.append(t)
        for i in nloops:
            threads[i].start()
        for i in nloops:
            threads[i].join()

    def loop(self):
        driver = Remote(command_executor=hub_url, desired_capabilities=capability)
        driver.get("https://www.baidu.com")



