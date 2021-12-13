import random
import os
from send_email import AutoEmail
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import datetime

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
        self.old_date = []

    def login(self, un, pd):
        """
            登录部分
        """
        # 创建 WebDriver 对象，指明使用chrome浏览器驱动
        wd = self.driver
        # 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
        wd.get('https://pass.sdu.edu.cn/')
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

    def send_email(self, content, email_img=''):
        self.email.create_email()
        self.email.add_content(content)
        if email_img != '':
            self.email.add_img(r'.\img\%s.png' % email_img)
        self.email.login_and_send()

    def judge_in_404(self):
        """
        判断是否是在404界面
        :return: result --> boolean
        """
        result = False
        wd = self.driver
        try:
            if wd.find_element(By.CLASS_NAME, 'title-01').text == '服务不在有效期':
                print()
                logger('当前时间还没有开放预约')
                result = True
            else:
                email_content = '预约开放时间{time}'.format(time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                self.send_email(email_content)
        except:
            pass
        return result

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
        scheduled_time_opts = self.get_opt_info('JHYYSJ')
        if len(scheduled_time_opts) > 1:
            scheduled_time_opts.remove('')
            scheduled_time_opt = scheduled_time_opts[len(scheduled_time_opts) - 1]
            print('选择预约时间%s' % scheduled_time_opt)
            wd.find_element(By.XPATH, "//button[@data-id='JHYYSJ']").click()
            wd.find_element(By.XPATH, "//button[@data-id='JHYYSJ']/following-sibling::div/ul/li[%s]" %
                            str(len(scheduled_time_opts) + 1)).click()
            # 开始选择场地
            time.sleep(1)
            place_opts = self.get_opt_info('FYCCBH')
            if len(place_opts) > 1:
                place_opts.remove('')
                for place_index in reversed(range(0, len(place_opts)-3)):
                    place_opt = place_opts[place_index]
                    print('选择预约场地%s' % place_opt)
                    wd.find_element(By.XPATH, "//button[@data-id='FYCCBH']").click()
                    wd.find_element(By.XPATH,
                                    "//button[@data-id='FYCCBH']/following-sibling::div/ul/li[%s]" %
                                    str(place_index + 2)).click()
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
            self.old_date = scheduled_time_opts
        
    def get_screenshot(self):
        time.sleep(5)
        try:
            '''
            调用get_screenshot_as_file(filename)方法，对浏览器当前打开页面
            进行截图,并保为e盘下的screenPicture.png文件。
            '''
            img_name = datetime.datetime.now().strftime("%Y-%m-%d")
            result = self.driver.get_screenshot_as_file('./img/{}.png'.format(str(img_name)))
            if result:
                print('截图保存成功')
                return img_name
        except IOError as e:
            print(e)


if __name__ == '__main__':
    email_module = AutoEmail(
        sender='wzh_7076@163.com',
        receiver='as456741@qq.com',
        smtp_server='smtp.163.com',
        username='wzh_7076',
        password='ETTTWIGAEHOJSRAP'
    )
    login_info = [
        ['201936225', 'Zz837868!'],     # 周一
        ['202034533', 'wuweimeng123'],  # 周二
        ['202036955', 'wzh168169'],     # 周三
        ['202016948', 'ladida52459'],   # 周四
        ['202016944', 'gsk199938'],     # 周五
        ['202016949', '.980206zxh.']    # 周六
    ]
    email_content = ''
    new_task = AutoOrder(r'E:\driver\chromedriver.exe', email_module)
    # order_list = ['16:00-17:30']
    order_list = ['8:00-9:30']
    today = datetime.datetime.now().weekday()
    new_task.login(login_info[today][0], login_info[today][1])
    new_task.jump(
        'https://scenter.sdu.edu.cn/tp_fp/view?m=fp#from=hall&serveID=755b2443-dda6-47b6-ba0c-13f5f1e39574&act=fp/serveapply')
    wd = new_task.driver
    in_404 = False
    # while True:
    #     cur_time = datetime.datetime.now().strftime("%H:%M:%S")
    #     in_404 = new_task.judge_in_404()
    #     if not in_404:
    #         # new_task.send_email(cur_time + '终于开放了')
    #         email_content += str(cur_time) + '终于开放了\n'
    #         break
    #     else:
    #         new_task.jump(
    #             'https://scenter.sdu.edu.cn/tp_fp/view?m=fp#from=hall&serveID=755b2443-dda6-47b6-ba0c-13f5f1e39574&act=fp/serveapply')
    #         time.sleep(600)
    if not in_404:
        for index in range(len(order_list)):
            # time.sleep(5)
            wd.switch_to.frame('formIframe')
            # new_task.complete_form('202036955', '王子豪')
            new_task.complete_select(order_list[index],)
            if new_task.has_place:
                # 切换回原来的主html
                print('找到场地', new_task.find_place)
                print(new_task.order_res)
                wd.switch_to.default_content()
                wd.find_element(By.ID, 'commit').click()
                print('申请了这块场地')
                if index != len(order_list) - 1:
                    time.sleep(3)
                    wd.back()
            else:
                print('没球打了，洗洗睡吧')
        print('有球打了ohhhhhhhhhhhh')

    new_task.jump('https://scenter.sdu.edu.cn/tp_fp/view?m=fp#act=fp/myserviceapply/indexFinish')
    if wd.current_url == 'https://scenter.sdu.edu.cn/tp_fp/view?m=fp#act=fp/myserviceapply/indexFinish':
        img = new_task.get_screenshot()
        new_task.send_email(email_content + new_task.order_res, img)
    else:
        new_task.send_email(email_content + new_task.order_res)
    new_task.logout()
    wd.quit()
