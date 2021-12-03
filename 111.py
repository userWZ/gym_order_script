from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
import time
from email.mime.image import MIMEImage
temp_date = datetime.datetime.now()
order_time = (temp_date + datetime.timedelta(days=+6)).strftime("%Y-%m-%d")
print(temp_date, order_time)
sender = 'wzh_7076@163.com'
receiver = 'as456741@qq.com'

#主题
"""**主题如果是纯中文或纯英文则字符数必须大于等于5个，
不然会报错554 SPM被认为是垃圾邮件或者病毒** """
subject = str(temp_date.strftime("%Y-%m-%d")) + '预约结果'
#内容
contents='预约成功:' + '\n' + '预约场次3场' + '\n' + '完成时间' + str(temp_date)
#服务器地址
smtpserver = 'smtp.163.com'
#用户名（不是邮箱）
username = 'wzh_7076'
#163授权码
password = 'ETTTWIGAEHOJSRAP'
msg = MIMEMultipart('mixed')
content = MIMEText(contents, 'plain', 'utf-8')  # 中文需参数‘utf-8'，单字节字符不需要
msg.attach(content)
msg['Subject'] = Header(subject, 'utf-8')
msg['From'] = sender
msg['To'] = receiver

sendimagefile = open(r'D:\test\a.jpg', 'rb').read()
image = MIMEImage(sendimagefile)
image.add_header('Content-ID', '<image1>')
image["Content-Disposition"] = 'attachment; filename="testimage.png"'
msg.attach(image)

#服务器地址和端口25
smtp = smtplib.SMTP(smtpserver,25)
# smtp.set_debuglevel(1)
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()