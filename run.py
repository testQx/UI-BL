import json
import logging
import os
import sys

import pytest

from Common.Fileoption import Fileoption
from Common.Publicmethod import Publicmethod

root_dir = os.path.dirname(__file__)
# config_yaml = Fileoption.read_yaml("./Conf/config.yaml")
thread_num = 0


# Todo
# 增加allure环境变量说明
# 修改allure环境变量
# def modify_report_environment_file(report_widgets_dir):
#     """
#     向environment.json文件添加测试环境配置，展现在allure测试报告中
#     @return:
#     """
#     environment_info = [
#         {"name": '测试地址', "values": [config_yaml['allure_environment']['URL']]},
#         {"name": '测试版本号', "values": [config_yaml['allure_environment']["version"]]},
#         {"name": '测试账户', "values": [config_yaml['allure_environment']['username']]},
#         {"name": '测试说明', "values": [config_yaml['allure_environment']['description']]}
#     ]
#     # 确保目录存在
#     Fileoption.create_dirs(os.path.join(report_widgets_dir, 'widgets'))
#     with open(report_widgets_dir + '/widgets/environment.json', 'w', encoding='utf-8') as f:
#         json.dump(environment_info, f, ensure_ascii=False, indent=4)


# 保存历史数据
def save_history(history_dir, dist_dir):
    if not os.path.exists(os.path.join(dist_dir, "history")):
        Fileoption.create_dirs(os.path.join(dist_dir, "history"))
    else:
        # 遍历报告report下allure-report下的history目录下的文件
        for file in os.listdir(os.path.join(dist_dir, "history")):
            old_data_dic = {}
            old_data_list = []
            # 1、从report下allure-report下的history目录下的文件读取最新的历史纪录
            with open(os.path.join(dist_dir, "history", file), 'rb') as f:
                new_data = json.load(f)
            # 2、从Report下的history(历史文件信息存储目录)读取老的历史记录
            try:
                with open(os.path.join(history_dir, file), 'rb') as fr:
                    old_data = json.load(fr)

                    if isinstance(old_data, dict):
                        old_data_dic.update(old_data)
                    elif isinstance(old_data, list):
                        old_data_list.extend(old_data)
            except Exception as fe:
                print("{}文件查找失败信息：{}，开始创建目标文件！！！".format(history_dir, fe))
                Fileoption.create_file(os.path.join(history_dir, file))
                # 3、合并更新最新的历史纪录到report下的history目录对应浏览器目录中
            with open(os.path.join(history_dir, file), 'w') as fw:
                if isinstance(new_data, dict):
                    old_data_dic.update(new_data)
                    json.dump(old_data_dic, fw, indent=4)
                elif isinstance(new_data, list):
                    old_data_list.extend(new_data)
                    json.dump(old_data_list, fw, indent=4)
                else:
                    print("旧历史数据异常")


# Todo
# 导入历史数据
def import_history_data(history_save_dir, result_dir):
    if not os.path.exists(history_save_dir):
        print("未初始化历史数据！！！进行首次数据初始化!!!")
    else:
        # 读取历史数据
        for file in os.listdir(history_save_dir):
            # 读取最新的历史纪录
            with open(os.path.join(history_save_dir, file), 'rb') as f:
                new_data = json.load(f)
            # 写入目标文件allure-result中，用于生成趋势图
            Fileoption.create_file(os.path.join(result_dir, "history", file))
            try:
                with open(os.path.join(result_dir, "history", file), 'w') as fw:
                    json.dump(new_data, fw, indent=4)
            except Exception as fe:
                print("文件查找失败信息：{}，开始创建目标文件".format(fe))


# 运行命令参数配置
def run_all_case(browser, nloops):
    """
    @param browser:传入浏览器，chrome/firefox/ie
    """
    # 测试结果文件存放目录
    global thread_num
    thread_num = nloops
    print(thread_num)
    result_dir = os.path.abspath("./Report/{}/allure-result{}".format(browser, nloops))
    # 测试报告文件存放目录
    report_dir = os.path.abspath("./Report/{}/allure-report{}".format(browser, nloops))
    # 本地测试历史结果文件存放目录，用于生成趋势图
    history_dir = os.path.abspath("./Report/history/{}/{}".format(browser, nloops))
    # 定义测试用例features集合
    # allure_features = ["--allure-features"]
    # allure_features_list = [
    #     'Register_page_case',
    #     'Login_page_case'
    # ]
    # allure_features_args = ",".join(allure_features_list)
    # # 定义stories集合
    # allure_stories = ["--allure-stories"]
    # allure_stories_args = ['']
    allure_path_args = ['--alluredir', result_dir, '--clean-alluredir']
    test_args = ['-s', '-q']
    run_args = test_args + allure_path_args
    print(f"run_args的完整参数：{run_args}")
    # 使用pytest.main
    pytest.main(run_args)
    # 导入历史数据
    import_history_data(history_dir, result_dir)
    # 生成allure报告，需要系统执行命令--clean会清楚以前写入environment.json的配置
    cmd = 'allure generate ./Report/{}/allure-result{} -o ./Report/{}/allure-report{} --clean'.format(
        browser.replace(" ", "_"), nloops,
        browser.replace(" ", "_"), nloops)
    logging.info("命令行执行cmd:{}".format(cmd))
    print(f"cmd的命令:{cmd}")
    try:
        os.system(cmd)
    except Exception as e:
        logging.error('命令【{}】执行失败！'.format(cmd))
        sys.exit()
    # 定义allure报告环境信息
    # modify_report_environment_file(report_dir)
    # 保存历史数据
    save_history(history_dir, report_dir)


@Publicmethod.thread
def thread_main(i):
    run_all_case("chrome", i)


if __name__ == "__main__":
    thread_main(count=2)

# Todo
# 将thread方法封装一层，不直接写在run.py中 -->over
# 全局增加默认值，非并发模式存储某文档中，并发模式时分开指明文档存储-->后续处理，目前使用xdist解决并发
# 处理并发时日志写入混乱-->后续处理，目前使用xdist解决并发
# 处理并发时登录不同账号-->
# 处理allure报告合并成一份，处理histroy文件
# 处理并发时，不同线程执行不同测试用例
# 处理并发时分发至不同浏览器（兼容性）
# 增加错误重设机制
