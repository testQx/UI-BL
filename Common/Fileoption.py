import os
import sys
from datetime import datetime

import yaml
from loguru import logger

class Fileoption:
    @staticmethod
    def empty_local_dir(local_file_dir):
        files = os.listdir(local_file_dir)
        if len(files) > 0:
            for file in os.listdir(local_file_dir):
                file_path = os.path.join(local_file_dir, file)
                if 'ovpn' in file or 'json' or 'test_result' or 'png' in file:
                    os.remove(file_path)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '本地文件夹清空成功！', local_file_dir)

        else:
            print('%s此文件夹没有待清除文件！' % local_file_dir)

    @staticmethod
    def read_yaml(file):
        if os.path.isfile(file):
            fr = open(file, 'r', encoding='utf-8')
            yaml_info = yaml.safe_load(fr)
            fr.close()
            return yaml_info
        else:
            logger.error(file, '文件不存在')


    @staticmethod
    def create_file(file_path):
        """
        创建文件，当目录不存在时自动创建
        :param file_path:
        :return:
        """
        dir_path = os.path.split(file_path)[0]
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if not os.path.isfile(file_path):
            f = open(file_path, mode='w', encoding='utf-8')
            f.close()

    @staticmethod
    def create_dirs(file_dir):
        """
        创建文件路径,先判断目录是否存在
        :param file_dir:
        :return:
        """
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)