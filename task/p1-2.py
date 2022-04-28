import datetime
import info
from auto_order import AutoOrder
from send_email import AutoEmail
'''
    此处是预约账号数组，每个元素是一个字典，包含账号、密码、预约时间
    周一到周日对应数组下标为0-6
    username: '-' 代表当天不约场地
'''
login_info = [
    {'username': '-', 'password': 'Zz837868!', 'name': '郑永健', 'order_time': '16:00-17:30'}, # 4
    {'username': '-', 'password': 'Zz837868!', 'name': '郑永健', 'order_time': '16:00-17:30'}, # 5
    {'username': '202016949', 'password': '.980206zxh.', 'name': '赵小涵', 'order_time': '16:00-17:30'}, #6
    {'username': '202016949', 'password': '.980206zxh.', 'name': '赵小涵', 'order_time': '16:00-17:30'},#7
    {'username': '202016949', 'password': '.980206zxh.', 'name': '赵小涵', 'order_time': '16:00-17:30'},#1
    {'username': '-', 'password': '.980206zxh.', 'name': '赵小涵', 'order_time': '16:00-17:30'},#2
    {'username': '202034533', 'password': 'wuweimeng123', 'name': '武维蒙', 'order_time': '16:00-17:30'},#3
]
preference = [11, 12, 9, 10, 1, 2, 3, 8, 5, 7, 4, 6]
'''
    邮件模块
'''
email_module = AutoEmail(
        sender='wzh_7076@163.com', # 发件人邮箱
        receiver='as456741@qq.com',# 收件人邮箱
        smtp_server='smtp.163.com',# 发件人smtp服务器
        username='wzh_7076', # 发件人邮箱账号
        password='ETTTWIGAEHOJSRAP' # 发件人邮箱绑定码
)

if __name__ == '__main__':
    email_content = ''
    today = datetime.datetime.now().weekday()
    if login_info[today]['username'] != '-':
        new_task = AutoOrder(info.driver_path,
                             preference,
                             login_info[today],
                             display=False,
                             email=email_module)
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
