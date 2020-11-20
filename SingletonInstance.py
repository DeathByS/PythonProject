import requests
import smtplib
from email.mime.text import MIMEText

# 
#  DB에서 데이터를 읽어오는 singleton Class
# 
# 


class SingletonInstane:
  __instance = None

  @classmethod
  def __getInstance(cls):
    return cls.__instance

  @classmethod
  def instance(cls, *args, **kargs):
    cls.__instance = cls(*args, **kargs)
    cls.instance = cls.__getInstance
    return cls.__instance

class GetDataFromDB(SingletonInstane):
    
    def __init__(self):

        self.url = 'http://kwtkorea.iptime.org:8080/%s/'

    def print(self):
        
        print(self.url)

    def getDataInRange(self, tableName, colName, start, end, machineName):

        url = self.url%tableName+'?%s__range=%s,%s&machineName=%s'%(colName, start, end, machineName)

        print(url)

        response = requests.get(url=url)
        
        print(response.status_code)
        # print(response.text)
        # print(response[0]['sludgeInput'])

        if response.status_code != 200:
            return response.status_code
        else: 
            return response.json()

    def getDataAll(self, tableName, machineName):

        url = self.url%tableName+'?machineName=%s'%(machineName)

        print(url)

        response = requests.get(url=url)

        if response.status_code != 200:
            return response.status_code
        else: 
            return response.json()

# c = GetDataFromDB.instance()

# c.getDataInRange('InfoData', '서울_A', 'timeData', '2020-02-14 00:00:00', '2020-02-17 00:00:00')

# # c.print()

class EmailSender(SingletonInstane):

    def __init__(self):
        self.s = None
        
    
    def openSMTP(self, smtpName = "smtp.naver.com", smtpPort = 587):
        self.s = smtplib.SMTP(smtpName, smtpPort) #메일 서버 연결

    def emailSend(self, sender = "ghwhrlf@naver.com", reciver = ["ghwhrlf@gmail.com",], 
    password = "w1r1g1w1w!", smtpName = "smtp.naver.com", smtpPort = 587, subject='', msg = ''):

        print('emailSend In', subject, msg)

        text = msg
        msg = MIMEText(text, _charset = "utf8") #MIMEText(text , _charset = "utf8")

        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ", ".join(reciver)
        print(msg.as_string())
        self.s = smtplib.SMTP(smtpName, smtpPort) #메일 서버 연결
        self.s.starttls() #TLS 보안 처리
        self.s.login(sender, password)
        self.s.sendmail(sender, reciver, msg.as_string()) #메일 전송, 문자열로 변환하여 보냅니다.
        self.s.quit()
    
    def quitSMTP(self):
        if self.s is not None:
            self.s.quit()    
