import json
import random
import os
from send_email import AutoEmail
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import datetime
import re
import requests
import info

init_name = ['马化腾', '耿妙妙', '劳洁玉', '高皓月', '孙忆远', '厍觅波', '史慕儿', '蒙新月', '巢思慧', '辛安波', '尚思溪',
             '戴颖', '杨滢', '吕嫱', '尹涵', '蔡鸾', '相娇', '杨育', '马馥', '孙涵', '牛文', '吕震', '蒋琩', '蔚促', '余学',
             '傅朋', '甘清', '沈偿', '乜乒', '闻利', '武频', '程稼', '厍峙', '张书', '易铿', '董琒', '段英飙', '孔俊誉', '杨正雅',
             '方凯康', '陆和安', '屠宏胜', '靳雅惠', '郝修诚', '李晗昱', '邹鹏翼', '漕俊民', '吴鸿信', '益安民', '赖温文', '尚弘伟',
             '芮修远', '满阳文', '陆永思', '容远航', '糜兴贤', '聂和泽', '芮坚秉', '白浩瀚', '班安平', '靳乐语', '邹哲茂', '姚正文']
order_page_url = 'https://scenter.sdu.edu.cn/tp_fp/view?m=fp#from=hall&serveID=755b2443-dda6-47b6-ba0c-13f5f1e39574&act=fp/serveapply'
commit_url = 'https://scenter.sdu.edu.cn/tp_fp/formParser?status=update&formid=408225d8-1abe-4cdd-8a0d-fd8b1c6f&workflowAction=startProcess&seqId=&unitId=&workitemid=&process=2ff0b7de-9c31-4898-94ac-adfd3e3eebca'
form_url = 'https://scenter.sdu.edu.cn/tp_fp/formParser?status=select&formid=408225d8-1abe-4cdd-8a0d-fd8b1c6f&service_id=755b2443-dda6-47b6-ba0c-13f5f1e39574&process=2ff0b7de-9c31-4898-94ac-adfd3e3eebca&seqId=&seqPid=&privilegeId=711549755616fbc517757f5036364348'


def logger(content):
    logger_content = '================ ({time}) {content} ================' \
        .format(time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), content=content)
    print(logger_content)


class AutoOrder:
    def __init__(self, driver_path, email, preference, login_info, display=False, send_img=False, ):
        if display:
            self.driver = webdriver.Chrome(driver_path)
        else:
            # 无界面运行，不显示浏览器
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            # 不启动界面显示- linux下命令行模式必须启用
            chrome_options.add_argument('--headless')
            self.driver = webdriver.Chrome(driver_path, options=chrome_options)
        self.email = email
        self.login_info = login_info
        self.driver.implicitly_wait(10)
        self.order_res = ''
        self.has_place = False
        self.img = []
        self.preference = preference
        self.send_img = send_img
        self.cookies = None
        self.session = None
        self.place_info = {'18:30-20:00': [], '20:00-21:30': [], '16:00-17:30': [], '8:00-9:30': []}
        self.order_date = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")

    def login(self):
        """
            登录部分
        """
        # 创建 WebDriver 对象，指明使用chrome浏览器驱动
        wd = self.driver
        # 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
        wd.get('https://pass.sdu.edu.cn/cas/login?service=https%3A%2F%2Fscenter.sdu.edu.cn%2Ftp_fp%2Findex.jsp')
        # 根据id选择元素，返回的就是该元素对应的WebElement对象
        un = self.login_info['username']
        pd = self.login_info['password']
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

    def complete_select(self, place_index):
        wd = self.driver
        time.sleep(1)
        wd.switch_to.frame('formIframe')
        # 展示隐藏的select
        wd.execute_script("document.getElementById('JHYYSJ').style='display:block'")
        wd.execute_script("document.getElementById('FYCCBH').style='display:block'")
        wd.execute_script("document.getElementById('XZSYSD').style='display:block'")
        # 选择器元素
        JHYYSJ = Select(wd.find_element(By.ID, 'JHYYSJ'))
        FYCCBH = Select(wd.find_element(By.ID, 'FYCCBH'))
        XZSYSD = Select(wd.find_element(By.ID, 'XZSYSD'))
        # 选择日期
        order_date = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        JHYYSJ.select_by_value(order_date)
        # 选择场地
        order_place = order_date + '青岛校区' + str(place_index) + '号场地'
        time.sleep(2)
        print(FYCCBH.options[0].text)

        try:
            FYCCBH.select_by_value(order_place)
            print('场地选择成功')
        except:
            print(place_index, '号场地已经被抢')
            return False
        # 选择时间
        order_time = order_place + self.login_info['order_time']
        self.order_res = order_time
        # 判断选择的时间是否可用
        res = self.check_place_status(order_time)
        if res:
            try:
                XZSYSD.select_by_value(order_time)
                print(order_time, '选择成功')
            except:
                print(order_time, '已经被抢')
                return False
            return True
        else:
            print('赶紧重新选择')
            return False

    def get_screenshot(self):
        '''
        调用get_screenshot_as_file(filename)方法，对浏览器当前打开页面
        进行截图,并保为e盘下的screenPicture.png文件。
        '''
        img_name = datetime.datetime.now().strftime("%Y%m%d")
        result = self.driver.get_screenshot_as_file(u'G:\\auto_order\\img\\%s.png' % img_name)
        if result:
            print('截图保存成功')
            self.img.append(r'G:\auto_order\img\%s.png' % img_name)
        else:
            print('截图失败')

    def get_place_info(self):
        self.place_info = {'18:30-20:00': [], '20:00-21:30': [], '16:00-17:30': [], '8:00-9:30': []}
        self.cookies = self.driver.get_cookies()
        self.session = requests.Session()
        c = requests.cookies.RequestsCookieJar()
        for item in self.cookies:
            c.set(item["name"], item["value"])
        self.session.cookies.update(c)  # 载入cookie
        # 获取到了预约场地，时间信息
        data = {'codelist_type': 'pbrq_fyccbh_sj_qd_4', 'formid': '408225d8-1abe-4cdd-8a0d-fd8b1c6f'}
        place_json = self.session.post(url='https://scenter.sdu.edu.cn/tp_fp/formParser?status=codeList',
                                       data=data).text
        place_info = json.loads(place_json)
        for item in place_info:
            if item['NAME'] in self.place_info and item['VALUE'][0:10] == self.order_date:
                index = int(re.findall(r'区(.*)号', item['VALUE'])[0])
                self.place_info[item['NAME']].append(index)
        return place_info

    def check_place_status(self, params):
        status_json = {
            "presetKey": "310499157438464",
            "param": {"XZSYSD": "2022-04-25青岛校区8号场地16:00-17:30"}
        }
        status_json['param']['XZSYSD'] = params
        res = self.session.post(url='https://scenter.sdu.edu.cn/tp_fp/fp/Uniformcommon/selectOnePresetData',
                                json=status_json).text
        res = json.loads(res)
        if res['PD'] != '0':
            print('场地已被预约')
            return False
        return True

    def judgeSuccess(self):
        data = {
            "serviceName": "",
            "startTime": "",
            "endTime": "",
            "assess": "",
            "result": "",
            "completestart_time": "",
            "completeend_time": "",
            "procinst_id": "",
            "summary": "",
            "pageNum": "1",
            "pageSize": "1"
        }
        res = self.session.post(url='https://scenter.sdu.edu.cn/tp_fp/fp/myserviceapply/getBJSXList', json=data).text
        res = json.loads(res)
        res_time = res['list'][0]['START_TIME_DATE']
        res_name = res['list'][0]['service_name']
        res_time = time.strftime("%Y-%m-%d", time.localtime(res_time / 1000))
        if res_time == datetime.datetime.now().strftime("%Y-%m-%d") and res_name == "青岛校区风雨操场预约":
            print('预约成功')
            return True
        else:
            return False

    def order(self):
        wd = self.driver
        self.get_place_info()
        system_open = self.session.post(url='https://scenter.sdu.edu.cn/tp_fp/fp/serveapply/checkService',
                                        json={'serveID': "755b2443-dda6-47b6-ba0c-13f5f1e39574"})
        while system_open.text != '0':
            time.sleep(0.3)
            print('系统还没开放')
            system_open = self.session.post(url='https://scenter.sdu.edu.cn/tp_fp/fp/serveapply/checkService',
                                            json={'serveID': "755b2443-dda6-47b6-ba0c-13f5f1e39574"})
        print('系统开放了')
        time.sleep(1)
        self.jump(order_page_url)
        # 根据优先顺序选择场地
        place_set = self.place_info[self.login_info['order_time']]
        suitable_place = [val for val in self.preference if val in place_set]
        for place in suitable_place:
            if self.complete_select(place):
                wd.switch_to.default_content()
                wd.find_element(By.ID, 'commit').click()
            time.sleep(1)
            res = self.judgeSuccess()
            print(res)
            if res:
                print('预约成功')
                self.has_place = True
                break
            else:
                print('预约失败')
                self.has_place = False
                self.jump(order_page_url)
                continue


        # 如果预约成功，并且需要保存截图
        if self.send_img and self.has_place:
            self.jump('https://scenter.sdu.edu.cn/tp_fp/view?m=fp#act=fp/myserviceapply/indexFinish')
            time.sleep(3)
            if wd.current_url == 'https://scenter.sdu.edu.cn/tp_fp/view?m=fp#act=fp/myserviceapply/indexFinish':
                self.get_screenshot()
        self.logout()


login_info = [
    {'username': '202036955', 'password': 'wzh168169', 'name': '王子豪', 'order_time': '18:30-20:00'},
    {'username': '202036955', 'password': 'wzh168169', 'name': '王子豪', 'order_time': '18:30-20:00'},
    {'username': '201916207', 'password': 'my412427', 'name': '米楠', 'order_time': '18:30-20:00'},
    {'username': '201916207', 'password': 'my412427', 'name': '米楠', 'order_time': '18:30-20:00'},
    {'username': '201916207', 'password': 'my412427', 'name': '米楠', 'order_time': '18:30-20:00'},
    {'username': '202036955', 'password': 'wzh168169', 'name': '王子豪', 'order_time': '18:30-20:00'},
    {'username': '202034533', 'password': 'wuweimeng123', 'name': '武维蒙', 'order_time': '18:30-20:00'},
]
preference = [9, 12, 7, 6, 1, 2, 3, 8, 5, 11, 4, 10]

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
    new_task = AutoOrder(r'G:\auto_order\chromedriver.exe',
                         email_module,
                         preference,
                         login_info[today],
                         display=False)
    new_task.login()
    new_task.order()
    # 发送邮件
    if new_task.has_place:
        print('预约成功', new_task.order_res)
        print('邮件发送成功')
        email_content = new_task.login_info['name'] + new_task.order_res
        new_task.send_email(email_content, new_task.img)
    else:
        delta = datetime.timedelta(days=3)
        new_task.send_email('周' + str((datetime.datetime.now() + delta).weekday() + 1) + '没有球打了')

    new_task.driver.quit()
