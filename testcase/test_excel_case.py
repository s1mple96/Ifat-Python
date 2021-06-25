from config.Conf import ConfigYaml
from config import Conf
import os
from common.ExcelData import Data
from utils.LogUtil import my_log
from common import ExcelConfig
from utils.RequestsUtil import Request
import json
import pytest
from common import Base
from utils.AssertUtil import AssertUtil
import allure

# 1、初始化信息
# 1）.初始化测试用例文件
case_file = os.path.join(Conf.get_data_path(), ConfigYaml().get_excel_file())
# 2）.测试用例sheet名称
sheet_name = ConfigYaml().get_excel_sheet()
# 3）.获取运行测试用例列表
data_init = Data(case_file, sheet_name)
run_list = data_init.get_run_data()

# 4）.日志
log = my_log()
# 初始化dataconfig
data_key = ExcelConfig.DataConfig


# 2、测试用例方法，参数化运行
# 一个用例的执行
class TestExcel:
    # 1、增加Pyest
    # 2、修改方法参数
    # 3、重构函数内容
    # 4、pytest.main

    def run_api(self, url, method, params=None, header=None, cookie=None):
        """
        发送请求api
        :return:
        """
        # 2）.接口请求
        request = Request()
        # params 转义json
        # 验证params有没有内容
        if len(str(params).strip()) is not 0:
            params = json.loads(params)
        # method post/get
        if str(method).lower() == "get":
            # 2.增加Headers
            res = request.get(url, json=params, headers=header, cookies=cookie)
        elif str(method).lower() == "post":
            res = request.post(url, json=params, headers=header, cookies=cookie)
        else:
            log.error("错误请求method: %s" % method)

        return res

    def run_pre(self, pre_case):
        # 初始化数据
        pass
        url = ConfigYaml().get_conf_url() + pre_case[data_key.url]
        method = pre_case[data_key.method]
        params = pre_case[data_key.params]
        headers = pre_case[data_key.headers]
        cookies = pre_case[data_key.cookies]

        # 1.判断headers是否存在，json转义，无需
        # if headers:
        #     header = json.loads(headers)
        # else:
        #     header = headers
        header = Base.json_parse(headers)
        # 3.增加cookies
        # if cookies:
        #     cookie = json.loads(cookies)
        # else:
        #     cookie = cookies
        cookie = Base.json_parse(cookies)
        res = self.run_api(url, method, params, header)
        print("前置用例执行：%s" % res)
        return res

    # 1）.初始化信息，url,data

    # 1、增加Pyest
    @pytest.mark.parametrize("case", run_list)
    # 2、修改方法参数
    def test_run(self, case):
        # 3、重构函数内容
        # data_key = ExcelConfig.DataConfig
        # run_list第1个用例，用例，key获取values
        url = ConfigYaml().get_conf_url() + case[data_key.url]
        print(url)
        case_id = case[data_key.case_id]
        case_model = case[data_key.case_model]
        case_name = case[data_key.case_name]
        pre_exec = case[data_key.pre_exec]
        method = case[data_key.method]
        params_type = case[data_key.params_type]
        params = case[data_key.params]
        expect_result = case[data_key.expect_result]
        headers = case[data_key.headers]
        cookies = case[data_key.cookies]
        code = case[data_key.code]
        db_verify = case[data_key.db_verify]

        # 1、验证前置条件
        if pre_exec:
            pass
            # 2、找到执行用例
            # 前置测试用例
            pre_case = data_init.get_case_pre(pre_exec)
            print("前置条件信息为：%s" % pre_case)
            pre_res = self.run_pre(pre_case)
            headers, cookies = self.get_correlation(headers, cookies, pre_res)

        header = Base.json_parse(headers)
        cookie = Base.json_parse(cookies)
        res = self.run_api(url, method, params, header, cookie)
        print("测试用例执行：%s" % res)

        # allure
        # sheet名称  feature 一级标签
        allure.dynamic.feature(sheet_name)
        # 模块   story 二级标签
        allure.dynamic.story(case_model)
        # 用例ID+接口名称  title
        allure.dynamic.title(case_id + case_name)
        # 请求URL  请求类型 期望结果 实际结果描述
        desc = "<font color='red'>请求URL: </font> {}<Br/>" \
               "<font color='red'>请求类型: </font>{}<Br/>" \
               "<font color='red'>期望结果: </font>{}<Br/>" \
               "<font color='red'>实际结果: </font>{}".format(url, method, expect_result, res)
        allure.dynamic.description(desc)

        # 断言验证
        # 状态码，返回结果内容，数据库相关的结果的验证
        # 状态码
        assert_util = AssertUtil()
        assert_util.assert_code(int(res["code"]), int(code))
        # 返回结果内容断言
        assert_util.assert_in_body(str(res["body"]), str(expect_result))
        # 数据库结果断言
        # Base.assert_db("db_1", res["body"], db_verify)

        # 1、初始化数据库
        # from common.Base import init_db
        # sql = init_db("db_1")
        # #2、查询sql，excel定义好的
        # db_res = sql.fetchone(db_verify)
        # log.debug("数据库查询结果：{}".format(str(db_res)))
        # #3、数据库的结果与接口返回的结果验证
        # #获取数据库结果的key
        # verify_list = list(dict(db_res).keys())
        # #根据key获取数据库结果，接口结果
        # for line in verify_list:
        #     res_line = res["body"][line]
        #     res_db_line = dict(db_res)[line]
        # #验证
        #     assert_util.assert_body(res_line,res_db_line)
        # 1.判断headers是否存在，json转义，无需
        # if headers:
        #     header = json.loads(headers)
        # else:
        #     header = headers
        # # 3.增加cookies
        # if cookies:
        #     cookie = json.loads(cookies)
        # else:
        #     cookie = cookies

        # #2）.接口请求
        # request = Request()
        # #params 转义json
        # #验证params有没有内容
        # if len(str(params).strip()) is not 0:
        #     params = json.loads(params)
        # #method post/get
        # if str(method).lower()=="get":
        #     # 2.增加Headers
        #     res = request.get(url,json=params,headers = header,cookies=cookie)
        # elif str(method).lower()=="post":
        #     res = request.post(url, json=params,headers = header,cookies=cookie)
        # else:
        #     log.error("错误请求method: %s"%method)
        # print(res)

    # TestExcel().test_run()

    def get_correlation(self, headers, cookies, pre_res):
        """
        关联
        :param headers:
        :param cookies:
        :param pre_res:
        :return:
        """
        # 验证是否有关联
        headers_para, cookies_para = Base.params_find(headers, cookies)
        # 有关联，执行前置用例，获取结果
        if len(headers_para):
            headers_data = pre_res["body"]["data"][headers_para[0]]
            # 结果替换
            headers = Base.res_sub(headers, headers_data)
        if len(cookies_para):
            cookies_data = pre_res["body"]["data"][cookies_para[0]]
            # 结果替换
            cookies = Base.res_sub(headers, cookies_data)
        return headers, cookies

