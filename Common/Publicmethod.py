import string
import threading
import time
from random import random

import allure
import docker
from loguru import logger

from Common.Fileoption import Fileoption

class Publicmethod:

    @staticmethod
    def random_string(strings=string.ascii_letters, length=15):
        #获取随机字符串
        values = ''.join(random.choices(strings, k=length))
        return values

    @staticmethod
    def screen_picture(driver):
        """
        截图操作
        @return:
        """
        try:
            logger.info("正在进行截图操作：")
            picture_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
            file_path = "screenshot/picture"
            file_name = picture_time + ".png"
            Fileoption.create_file(file_path)
            res = driver.get_screenshot_as_file(file_path + '/' + file_name)
            picture_url = file_path + '/' + file_name
            allure.attach.file(picture_url, attachment_type=allure.attachment_type.PNG)
            logger.info("截图成功，picture_url为：{}".format(picture_url))
        except Exception as e:
            logger.error("截图失败，错误信息为：{}".format(e))
        finally:
            return picture_url

    @staticmethod
    def create_docker_hub_container(base_url, image, name, ports):
        """
        创建selenium的hub节点
        @param base_url:
        @param image:
        @param name:
        @param ports:
        @return:
        """
        client = docker.DockerClient(base_url=base_url)
        try:
            client.containers.run(
                image=image,
                detach=True,
                tty=True,
                stdin_open=True,
                restart_policy={'Name': 'always'},
                name=name,
                ports=ports,
                privileged=True
            )
        except Exception as e:
            print("创建容器失败，错误信息：{}".format(e))

    @staticmethod
    def create_docker_node_container(base_url, image, name, ports, links):
        """
        在docker中创建selenium的node节点
        @param base_url: docker的URL
        @param image: 镜像
        @param name: 命名
        @param ports: 端口
        @param links: 连接
        @return:
        """
        client = docker.DockerClient(base_url=base_url)
        try:
            client.containers.run(
                image=image,
                detach=True,
                tty=True,
                stdin_open=True,
                restart_policy={'Name': 'always'},
                name=name,
                ports=ports,
                links=links,
                privileged=True
            )
        except Exception as e:
            print("创建容器失败，错误信息：{}".format(e))

    @staticmethod
    def thread(func):
        threads = []
        # *args在实现函数时正常传参进入
        def thread_loop(count=1):
            try:
                nloops = range(0,count)
                for i in nloops:
                    t = threading.Thread(target=func,args=(i,))
                    #若t =threading.Thread(target=func,args=(args[0],))
                    #args=(args[0],)需要传值进入被调函数中
                    threads.append(t)
                for i in nloops:
                    threads[i].start()
                    # import time
                    # time.sleep(1)
                for i in nloops:
                    threads[i].join()
            except Exception as e :
                logger.error("count次数输入错误"+e)
        return thread_loop
