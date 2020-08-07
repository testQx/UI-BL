import pytest
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import Remote
import logging
import threading
logging.basicConfig(level=logging.INFO)



class TestGrid:
    @pytest.mark.parametrize("cap",["CHROME","FIREFOX"])
    def test_griod(self,cap):
        hub_url="http://127.0.0.1:4444/wd/hub"

        capability=eval(f'DesiredCapabilities.{cap}.copy()')
        # capability1=DesiredCapabilities.FIREFOX.copy()
        self.loops=[1]
        threads = []
        nloops = range(len(self.loops))
        for i in nloops:
            t = threading.Thread(target=self.loop,args=(hub_url,capability))
            threads.append(t)
        for i in nloops:
            threads[i].start()
        for i in nloops:
            threads[i].join()

    def loop(self,hub_url,capability):
        driver = Remote(command_executor=hub_url, desired_capabilities=capability)
        driver.get("https://www.baidu.com")
        driver.quit()


