import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import time
init_name = ['马化腾', '耿妙妙', '劳洁玉', '高皓月', '孙忆远', '厍觅波', '史慕儿', '蒙新月', '巢思慧', '辛安波', '尚思溪',
             '戴颖', '杨滢', '吕嫱', '尹涵', '蔡鸾', '相娇', '杨育', '马馥', '孙涵', '牛文', '吕震', '蒋琩', '蔚促', '余学',
             '傅朋', '甘清', '沈偿', '乜乒', '闻利', '武频', '程稼', '厍峙', '张书', '易铿', '董琒', '段英飙', '孔俊誉', '杨正雅',
             '方凯康', '陆和安', '屠宏胜', '靳雅惠', '郝修诚', '李晗昱', '邹鹏翼', '漕俊民', '吴鸿信', '益安民', '赖温文', '尚弘伟',
             '芮修远', '满阳文', '陆永思', '容远航', '糜兴贤', '聂和泽', '芮坚秉', '白浩瀚', '班安平', '靳乐语', '邹哲茂', '姚正文']


class AutoOrder:
    def __init__(self):
        self.diver = webdriver.Chrome(r'G:\chromedriver\chromedriver.exe')
        self.diver.implicitly_wait(10)
        self.res = dict()
        self.has_place = False
        self.find_place = ''
        self.old_date = []

    def login(self, un, pd):
        """
            登录部分
        """
        # 创建 WebDriver 对象，指明使用chrome浏览器驱动
        wd = self.diver
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
        self.diver.get('https://scenter.sdu.edu.cn/tp_fp/logout')

    def jump_and_switch(self):
        wd = self.diver
        wd.get(
            'https://scenter.sdu.edu.cn/tp_fp/view?m=fp#from=hall&serveID=755b2443-dda6-47b6-ba0c-13f5f1e39574&act=fp/serveapply')
        # 切换iframe
        wd.switch_to.frame('formIframe')

    def get_opt_info(self, select_ID):
        wd = self.diver
        option_info = []
        select_ele = wd.find_element(By.ID, select_ID)
        select = Select(select_ele)
        options_list = select_ele.find_elements_by_tag_name('option')
        for option in options_list:
            # 获取下拉框的value和text
            option_info.append(option.get_attribute("value"))
            # print("Value is:%s " % (option.get_attribute("value")))
        return option_info

    def complete_form(self, number, name):
        wd = self.diver
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
        random_number = [random.sample(['2020', '2021', '2019'], 1)[0] + str(random.randint(14000, 99000)) for _ in range(10)]
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
        wd = self.diver
        time.sleep(1)
        scheduled_time_opts = self.get_opt_info('JHYYSJ')
        if len(scheduled_time_opts) > 1:
            scheduled_time_opts.remove('')
            for index in range(0, len(scheduled_time_opts)):
                scheduled_time_opt = scheduled_time_opts[len(scheduled_time_opts) - 1 - index]
                print('选择预约时间%s' % scheduled_time_opt)
                wd.find_element(By.XPATH, "//button[@data-id='JHYYSJ']").click()
                wd.find_element(By.XPATH, "//button[@data-id='JHYYSJ']/following-sibling::div/ul/li[%s]" %
                                str(len(scheduled_time_opts) + 1 - index)).click()
                # 开始选择场地
                time.sleep(1)
                place_opts = self.get_opt_info('FYCCBH')
                if len(place_opts) > 1:
                    place_opts.remove('')
                    for place_index in range(0, len(place_opts)):
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
                            print('================ 找到场地: 时间段{t} ================'.format(t=expect_full_info))
                            break
                        else:
                            print('================ ', place_opt, '没有想要的时间段了', ' ================')
                    if self.has_place:
                        break
                    else:
                        print('================ ', scheduled_time_opt, '没有想要的时间段了', ' ================')
        self.old_date = scheduled_time_opts


if __name__ == '__main__':
    new_task = AutoOrder()
    # new_task.login('202036955', 'wzh168169')
    # new_task.login('202016948', 'ladida52459')
    new_task.login('202016944', 'gsk199938')
    # new_task.login('202034533', 'wuweimeng123')
    # new_task.login('202016949', '.980206zxh.')
    # new_task.login('201936225', 'Zz837868!')
    while True:
        new_task.jump_and_switch()
        new_task.complete_form('202036955', '王子豪')
        wd = new_task.diver
        # new_task.complete_select('20:00-21:30')
        new_task.complete_select('16:00-17:30')
        # new_task.complete_select('18:30-20:00')
        if new_task.has_place:
            # 切换回原来的主html
            print('找到场地', new_task.find_place)
            print('有球打了ohhhhhhhhhhhh')
            wd.switch_to.default_content()
            wd.find_element(By.ID, 'commit').click()
            break
        else:
            print('没球打了，洗洗睡吧')
            new_task.diver.refresh()
    new_task.logout()
    wd.quit()
    print('')