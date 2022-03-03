from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
from email.mime.image import MIMEImage
import time

class AutoEmail:
    def __init__(self, sender, receiver, smtp_server, username, password):
        self.temp_date = datetime.datetime.now()    # 当前时间
        self.order_time = (self.temp_date + datetime.timedelta(days=+6)).strftime("%Y-%m-%d")   # 预约成功时间
        self.sender = sender   # 发件人'wzh_7076@163.com'
        self.receiver = receiver   # 收件人'as456741@qq.com'
        self.smtp_server = smtp_server  # 服务器地址
        self.username = username    # 用户名（不是邮箱）
        self.password = password    # 163授权码
        self.msg = MIMEMultipart('mixed')   # 发文主体
        self.contents = ''
        self.res_content = ''

    def create_email(self):
        # 主题
        """**主题如果是纯中文或纯英文则字符数必须大于等于5个，
        不然会报错554 SPM被认为是垃圾邮件或者病毒** """
        subject = str(self.temp_date.strftime("%Y-%m-%d")) + '预约结果'
        # 内容

        self.msg['Subject'] = Header(subject, 'utf-8')
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver

    def add_content(self, result_content=''):
        self.contents = '预约结果:' + '\n' + '时间' + str(self.temp_date.strftime("%Y-%m-%d %H:%M:%S"))
        result_content = self.contents + '\n' + result_content
        self.res_content = result_content
        content = MIMEText(result_content, 'plain', 'utf-8')  # 中文需参数‘utf-8'，单字节字符不需要
        self.msg.attach(content)

    def add_img(self, images):
        mail_msg = ''
        content = self.res_content
        for i in range(len(images)):
            mail_msg += '<p><img src="cid:image%d" height="240" width="320"></p>' % (i+1)
        self.msg.attach(MIMEText(content + mail_msg, 'html', 'utf-8'))

        for i, img_name in enumerate(images):
            with open(img_name, 'rb') as fp:
                img_data = fp.read()
            msg_image = MIMEImage(img_data)
            msg_image.add_header('Content-ID', '<image%d>' % (i+1))
            self.msg.attach(msg_image)

    def login_and_send(self, debug=False):
        # 服务器地址和端口25
        smtp = smtplib.SMTP(self.smtp_server, 25)
        if debug:
            smtp.set_debuglevel(1)
        smtp.login(self.username, self.password)
        smtp.sendmail(self.sender, self.receiver, self.msg.as_string())
        smtp.quit()


if __name__ == '__main__':
    result_email = AutoEmail(
        sender='wzh_7076@163.com',
        receiver='as456741@qq.com',
        smtp_server='smtp.163.com',
        username='wzh_7076',
        password='ETTTWIGAEHOJSRAP'
    )
    result_email.create_email()
    images = ['.\\img\\2022-03-02-1.png', '.\\img\\2022-03-02-2.png']
    result_email.add_img(images)
    result_email.login_and_send()
