import random
import os
from send_email import AutoEmail
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from info import *
import time
import datetime
import re

init_name = ['马化腾', '耿妙妙', '劳洁玉', '高皓月', '孙忆远', '厍觅波', '史慕儿', '蒙新月', '巢思慧', '辛安波', '尚思溪',
             '戴颖', '杨滢', '吕嫱', '尹涵', '蔡鸾', '相娇', '杨育', '马馥', '孙涵', '牛文', '吕震', '蒋琩', '蔚促', '余学',
             '傅朋', '甘清', '沈偿', '乜乒', '闻利', '武频', '程稼', '厍峙', '张书', '易铿', '董琒', '段英飙', '孔俊誉', '杨正雅',
             '方凯康', '陆和安', '屠宏胜', '靳雅惠', '郝修诚', '李晗昱', '邹鹏翼', '漕俊民', '吴鸿信', '益安民', '赖温文', '尚弘伟',
             '芮修远', '满阳文', '陆永思', '容远航', '糜兴贤', '聂和泽', '芮坚秉', '白浩瀚', '班安平', '靳乐语', '邹哲茂', '姚正文']


def logger(content):
    logger_content = '================ ({time}) {content} ================' \
        .format(time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), content=content)
    print(logger_content)


class AutoOrder:
    def __init__(self, driver_path, email):
        self.driver = webdriver.Chrome(driver_path)
        self.email = email
        self.driver.implicitly_wait(10)
        self.res = dict()
        self.order_res = ''
        self.has_place = False
        self.find_place = ''
        self.order_number = 0
        self.img = []
        self.open_time = ''

    def login(self, un, pd):
        """
            登录部分
        """
        # 创建 WebDriver 对象，指明使用chrome浏览器驱动
        wd = self.driver
        # 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
        wd.get('https://pass.sdu.edu.cn/cas/login?service=https%3A%2F%2Fscenter.sdu.edu.cn%2Ftp_fp%2Findex.jsp')
        # 根据id选择元素，返回的就是该元素对应的WebElement对象
        username = wd.find_element(By.ID, 'un')
        password = wd.find_element(By.ID, 'pd')

        username.send_keys(un)
        password.send_keys(pd + '\n')

    def logout(self):
        """
             退出登录部分
         """
        self.driver.get('https://scenter.sdu.edu.cn/tp_fp/logout')

    def jump(self, url):
        wd = self.driver
        wd.get(url)
        # 切换iframe

    def get_opt_info(self, select_ID):
        wd = self.driver
        option_info = []
        select_ele = wd.find_element(By.ID, select_ID)
        select = Select(select_ele)
        options_list = select_ele.find_elements_by_tag_name('option')
        for option in options_list:
            # 获取下拉框的value和text
            option_info.append(option.get_attribute("value"))
            # print("Value is:%s " % (option.get_attribute("value")))
        return option_info

    def send_email(self, content, email_img=None):
        self.email.create_email()
        self.email.add_content(content)
        if email_img:
            self.email.add_img(email_img)
        self.email.login_and_send()

    def judge_in_404(self):
        """
        判断是否是在404界面
        :return: result --> boolean
        """
        wd = self.driver
        try:
            wd.find_element(By.CLASS_NAME, 'building-box')
            print('当前预约没有开放')
            self.open_time = 'wait'
            return True
        except:
            print('预约开放了')
            if self.open_time == 'wait':
                self.open_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.send_email('预约开放时间' + self.open_time)
            return False

    def complete_form(self, number, name):
        wd = self.driver
        wd.find_element(By.CLASS_NAME, 'swiper-slide-active').click()
        wd.switch_to.default_content()
        stu_number = wd.find_element(By.ID, 'XGH')
        stu_name = wd.find_element(By.ID, 'XM')
        stu_number.send_keys(number)
        stu_name.send_keys(name)
        wd.find_element(By.XPATH, "//button[@data-id='SF']").click()
        wd.find_element(By.XPATH, "//button[@data-id='SF']/following-sibling::div/ul/li[3]").click()
        wd.find_element(By.NAME, 'ok').click()
        # 随机填入后三位同学的信息
        random_name = random.sample(init_name, 3)
        random_number = [random.sample(['2020', '2021', '2019'], 1)[0] + str(random.randint(14000, 99000)) for _ in
                         range(10)]
        for index in range(0, 3):
            time.sleep(1)
            wd.switch_to.frame('formIframe')
            wd.find_element(By.CLASS_NAME, 'swiper-slide-active').click()
            wd.switch_to.default_content()
            stu_number = wd.find_element(By.ID, 'XGH')
            stu_name = wd.find_element(By.ID, 'XM')
            stu_number.send_keys(random_number[index])
            stu_name.send_keys(random_name[index])
            wd.find_element(By.XPATH, "//button[@data-id='SF']").click()
            wd.find_element(By.XPATH, "//button[@data-id='SF']/following-sibling::div/ul/li[3]").click()
            wd.find_element(By.NAME, 'ok').click()
        wd.switch_to.frame('formIframe')

    def complete_select(self, expect):
        wd = self.driver
        time.sleep(1)
        # 提取时间选项
        scheduled_time_opts = self.get_opt_info('JHYYSJ')
        if len(scheduled_time_opts) > 1:
            scheduled_time_opts.remove('')
            scheduled_time_opt = scheduled_time_opts[len(scheduled_time_opts) - 1]
            print('选择预约时间%s' % scheduled_time_opt + ' ' + expect)
            wd.find_element(By.XPATH, "//button[@data-id='JHYYSJ']").click()
            wd.find_element(By.XPATH, "//button[@data-id='JHYYSJ']/following-sibling::div/ul/li[%s]" %
                            str(len(scheduled_time_opts) + 1)).click()
            # 开始选择场地
            time.sleep(1)
            place_opts = self.get_opt_info('FYCCBH')
            time.sleep(1)
            if len(place_opts) > 1:

                place_opts.remove('')
                place_list = []
                for item in place_opts:
                    place_list.append(int(re.findall(r"\d+\.?\d*", item)[-1]))
                # 选择场地 根据优先级列表顺序来[]
                for place_index in preference:
                    if place_index in place_list:
                        order_number = place_list.index(place_index)
                        place_opt = place_opts[order_number]
                        print('选择预约场地%s' % place_opt)
                        wd.find_element(By.XPATH, "//button[@data-id='FYCCBH']").click()
                        # 拿到可预约的场地列表
                        wd.find_element(By.XPATH,
                                        "//button[@data-id='FYCCBH']/following-sibling::div/ul/li[%s]" %
                                        str(order_number + 2)).click()
                        # 开始选择使用时间段
                        time.sleep(1)
                        consultant_opts = self.get_opt_info('XZSYSD')
                        expect_full_info = place_opt + expect
                        if expect_full_info in consultant_opts:
                            expect_index = consultant_opts.index(expect_full_info)
                            wd.find_element(By.XPATH, "//button[@data-id='XZSYSD']").click()
                            wd.find_element(By.XPATH,
                                            "//button[@data-id='XZSYSD']/following-sibling::div/ul/li[%s]" % str(
                                                expect_index + 1)).click()
                            self.has_place = True
                            self.find_place = expect_full_info
                            self.order_res += str(expect_full_info) + '\n'
                            logger('找到场地: 时间段{t}'.format(t=expect_full_info))
                            break
                        else:
                            logger(place_opt + '没有想要的时间段了')
                    else:
                        print('今天没有' + str(place_index) + '号场地')
                        continue

    def get_screenshot(self):

        '''
        调用get_screenshot_as_file(filename)方法，对浏览器当前打开页面
        进行截图,并保为e盘下的screenPicture.png文件。
        '''
        img_name = datetime.datetime.now().strftime("%Y%m%d") + 'p' + str(self.order_number)
        result = self.driver.get_screenshot_as_file(u'G:\\auto_order\\img\\%s.png' % img_name)
        if result:
            print('截图保存成功')
            self.img.append(r'G:\auto_order\img\%s.png' % img_name)
        else:
            print('截图失败')

    def order(self, order_list):
        wd = self.driver
        self.jump(
            'https://scenter.sdu.edu.cn/tp_fp/view?m=fp#from=hall&serveID=755b2443-dda6-47b6-ba0c-13f5f1e39574&act=fp/serveapply')
        while self.judge_in_404():
            time.sleep(5)
            self.jump(
                'https://scenter.sdu.edu.cn/tp_fp/view?m=fp#from=hall&serveID=755b2443-dda6-47b6-ba0c-13f5f1e39574&act=fp/serveapply')
        for index in range(len(order_list)):
            wd.switch_to.frame('formIframe')
            self.complete_select(order_list[index])
            if self.has_place:
                # 切换回原来的主html
                print('找到场地', self.find_place)
                print(self.order_res)
                wd.switch_to.default_content()
                wd.find_element(By.ID, 'commit').click()
                if index != len(order_list) - 1:
                    time.sleep(2)
                    wd.back()
            else:
                wd.switch_to.default_content()
                print(order_list[index] + '没球打了，洗洗睡吧')
        self.order_number += 1
        self.jump('https://scenter.sdu.edu.cn/tp_fp/view?m=fp#act=fp/myserviceapply/indexFinish')
        time.sleep(3)
        if wd.current_url == 'https://scenter.sdu.edu.cn/tp_fp/view?m=fp#act=fp/myserviceapply/indexFinish':
            self.get_screenshot()
        self.logout()

import requests
from bs4 import BeautifulSoup

from requests_html import HTMLSession
if __name__ == '__main__':
    email_module = AutoEmail(
        sender='wzh_7076@163.com',
        receiver='as456741@qq.com',
        smtp_server='smtp.163.com',
        username='wzh_7076',
        password='ETTTWIGAEHOJSRAP'
    )
    email_content = ''

    today = datetime.datetime.now().weekday()
    order_info = [login_info[today], order_list[today]]
    new_task = AutoOrder(r'/chromedriver.exe', email_module)
    new_task.login(order_info[0][0][0], order_info[0][0][1])
    cookies = new_task.driver.get_cookies()
    s = requests.Session()
    c = requests.cookies.RequestsCookieJar()
    for item in cookies:
        c.set(item["name"], item["value"])
    s.cookies.update(c)  # 载入cookie
    # 进入约场界面
    s.get('https://scenter.sdu.edu.cn/tp_fp/view?m=fp#from=hall&serveID=755b2443-dda6-47b6-ba0c-13f5f1e39574&act=fp/serveapply')
    # 获取约场界面的html 表单部分
    r = s.get('https://scenter.sdu.edu.cn/tp_fp/formParser?status=select&formid=408225d8-1abe-4cdd-8a0d-fd8b1c6f&service_id=755b2443-dda6-47b6-ba0c-13f5f1e39574&process=2ff0b7de-9c31-4898-94ac-adfd3e3eebca&seqId=&seqPid=&privilegeId=711549755616fbc517757f5036364348')
    # print(r.text)

    #获取到了预约场地，时间信息
    data = {'codelist_type' : 'pbrq_fyccbh_sj_qd_1', 'formid': '408225d8-1abe-4cdd-8a0d-fd8b1c6f'}
    print(s.post(url='https://scenter.sdu.edu.cn/tp_fp/formParser?status=codeList',data=data).text)
    data1 = {'codelist_type': 'pbrq_fyccbh_sj_qd_2', 'formid': '408225d8-1abe-4cdd-8a0d-fd8b1c6f','codelist_parentValue': '2022-03-18'}
    data2 = {'codelist_type': 'pbrq_fyccbh_sj_qd_3', 'formid': '408225d8-1abe-4cdd-8a0d-fd8b1c6f','codelist_parentValue': '2022-03-18青岛校区6号场地'}

    print(s.post(url='https://scenter.sdu.edu.cn/tp_fp/formParser?status=codeList', data=data1).text)
    print(s.post(url='https://scenter.sdu.edu.cn/tp_fp/formParser?status=codeList', data=data2).text)
    print(s.get('https://scenter.sdu.edu.cn/tp_fp/formParser?status=select&formid=408225d8-1abe-4cdd-8a0d-fd8b1c6f&service_id=755b2443-dda6-47b6-ba0c-13f5f1e39574&process=2ff0b7de-9c31-4898-94ac-adfd3e3eebca&seqId=&seqPid=&SYS_FK=2203151643376540&privilegeId=711549755616fbc517757f5036364348').text)
    # # 获取初始数据
    from info import json
    url = 'https://scenter.sdu.edu.cn/tp_fp/formParser?status=update&formid=408225d8-1abe-4cdd-8a0d-fd8b1c6f&workflowAction=startProcess&seqId=&unitId=&workitemid=&process=2ff0b7de-9c31-4898-94ac-adfd3e3eebca'
    print(s.post(url=url, json=json).text)
    getForm = s.get('https://scenter.sdu.edu.cn/tp_fp/formParser?status=select&formid=408225d8-1abe-4cdd-8a0d-fd8b1c6f&service_id=755b2443-dda6-47b6-ba0c-13f5f1e39574&process=2ff0b7de-9c31-4898-94ac-adfd3e3eebca&seqId=&seqPid=&privilegeId=711549755616fbc517757f5036364348')
    formData = BeautifulSoup(getForm.text, features="lxml")
    print(formData.find('script', id='dcstr').text)
    # time.sleep(5)
