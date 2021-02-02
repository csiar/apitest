import unittest
from common import HTMLTestRunner
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# 当前文件地址
basepath = os.path.realpath(os.path.dirname(__file__))
print(basepath)

def add_case(caseName="case", rule="test*.py"):
    # case存放地址
    casepath = os.path.join(basepath, caseName)
    # 如果不存在case这个文件夹，就自动创建一个
    if not os.path.exists(casepath):os.mkdir(casepath)
    print("test case path:%s"%casepath)
    # 查找用例，三要素:第一看有没用例，第二看用例的路径，第三看匹配规则
    discover = unittest.defaultTestLoader.discover(casepath, pattern=rule)
    # print(discover)
    return discover

def run_case(all_case, reportName="report"):
    now = time.strftime("%Y_%m_%d_%H_%M_%S") # 时间戳
    # 生成html报告的地址
    reportpath = os.path.join(basepath, reportName, "report.html")
    # 生成报告名加上时间戳
    # reportpath = os.path.join(basepath, reportName, "result%s.html"%now)
    print("report path:%s"%reportpath)
    fp = open(reportpath, "wb")
    # 运行器
    runner = HTMLTestRunner.HTMLTestRunner(fp, title="接口测试报告",
                                           description="测试报告详情",
                                           verbosity=2)
    runner.run(all_case)
    fp.close()

def get_report_file(reportpath):
    '''获取最新的测试报告'''
    lists = os.listdir(reportpath)
    lists.sort(key=lambda fn: os.path.getmtime(os.path.join(reportpath, fn)))
    print(u'最新测试生成的报告：'+lists[-1])
    # 找到最新生成的报告文件
    report_file = os.path.join(reportpath, lists[-1])
    return report_file

def send_mail(sender, psw, receiver, smtpserver, report_file, port):
    '''发送最新的测试报告内容'''
    with open(report_file, "rb") as f:
        mail_body = f.read()
    # 定义邮件内容
    msg = MIMEMultipart()
    body = MIMEText(mail_body, _subtype='html', _charset="utf-8")
    msg['Subject'] = u"自动化测试报告"
    msg["from"] = sender
    msg["to"] = ",".join(receiver)  # 只能字符串
    msg.attach(body)

    # 添加附件
    att = MIMEText(open(report_file, "rb").read(), "base64", "utf-8")
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = 'attachment: filename= "report.html"'
    msg.attach(att)

    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(sender, psw)
    except:
        smtp = smtplib.SMTP_SSL(smtpserver, port)
        smtp.login(sender, psw)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print('test report email has send out !')


# def send_email(smtpserver, port, sender, psw, receiver):
#     # 写信模板
#     msg = MIMEMultipart()
#     msg['Subject'] = "这是opa项目的自动化测试报告"
#     msg['From'] = sender
#     msg['to'] = receiver
#
#     # 通过os获取文件路径
#     annex = open(report_file, "r", encoding="utf-8").read()  # 附件，打开并且读取测试报告
#
#     main_body = '<title>接口测试报告</title>'  # 正文的内容
#
#     # 添加正文到容器
#     body = MIMEText(main_body, "html", "utf-8")
#     msg.attach(body)
#
#     # 添加附件到容器
#     att = MIMEText(annex, "base64", "utf-8")
#     att["Content-Type"] = "application/octet-sream"
#     att["Content-Disposition"] = 'attachment;filename="report.html"'  # 附件名称
#     msg.attach(att)
#
#     # 连接发送邮件
#     smtp = smtplib.SMTP_SSL(smtpserver, port)
#     smtp.login(sender, psw)
#     smtp.sendmail(sender, receiver, msg.as_string())
#     smtp.quit()


if __name__ == "__main__":
    all_case = add_case()
    run_case(all_case)
    reportpath = os.path.join(basepath, "report")
    report_file = get_report_file(reportpath)
    sender = "1019073255@qq.com"
    psw = "kbblldwtyfbjbdcb"
    smtp_server = "smtp.qq.com"
    port = 465
    receiver = ["1019073255@qq.com"]

    # smtpserver = "smtp.qq.com"
    # send_email(smtpserver, port, sender, psw, receiver)
    send_mail(sender, psw, receiver, smtp_server, report_file, port)
