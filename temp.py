import threading
from time import sleep,time
from selenium import webdriver
from multiprocessing import current_process

from selenium.webdriver.common.by import By


def user_login(username,password):
    """
    单终端多线程登录
    :param username:
    :param password:
    :return:
    """

    url = "https://pass.sdu.edu.cn/cas/login?service=https%3A%2F%2Fscenter.sdu.edu.cn%2Ftp_fp%2Findex.jsp"
    driver = webdriver.Chrome(r'G:\auto_order\chromedriver.exe')
    procName = current_process().name
    print("当前进程:",procName)
    sleep(1)
    start = time()
    print("session_id: " + driver.session_id)
    try:
        driver.get(url)
        driver.maximize_window()
        wd = driver
        # 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
        wd.get('https://pass.sdu.edu.cn/cas/login?service=https%3A%2F%2Fscenter.sdu.edu.cn%2Ftp_fp%2Findex.jsp')
        # 根据id选择元素，返回的就是该元素对应的WebElement对象
        un = wd.find_element(By.ID, 'un')
        pw = wd.find_element(By.ID, 'pd')

        un.send_keys(username)
        pw.send_keys(username + '\n')
    except Exception as e:
        raise e

    end = time()
    print("Task run %0.2f seconds." % (end - start))

def list_of_groups(list_info, per_list_len):
    '''
    将列表分割成指定长度的子列表，每个列表长度为当前测试并发数
    :param list_info:   列表，需要进行参数化的总列表
    :param per_list_len:  每个小列表的长度
    :return:
    '''
    list_of_group = zip(*(iter(list_info),) *per_list_len)
    end_list = [list(i) for i in list_of_group] # i is a tuple
    count = len(list_info) % per_list_len
    end_list.append(list_info[-count:]) if count !=0 else end_list
    return end_list

if __name__ == '__main__':
    userinfo = [
        {"username": "202034533", "password": "wuweimeng123"},
        {"username": "202036955", "password": "wzh168169"},
        {"username": "201916202", "password": "dzthang96102"},
        {"username": "202016949", "password": "980206zxh"}
    ]
    threads = []
    split_user_list = list_of_groups(userinfo,2)  # 这里只需要修改分割的数量即可实现循环登录和并发登录的数量
    print(split_user_list)
    for user_list in split_user_list:
        threads = [threading.Thread(target=user_login, args=(i["username"], i["password"])) for i in user_list]

        for t in threads:
            t.start()

        for t in threads:
            t.join()