# -*- coding: utf-8 *-*
import requests


class USTCMis:
    url = 'http://mis.teach.ustc.edu.cn/'

    def __init__(self):
        self.s = requests.Session()
        self.login_status = False

    def get_check_code(self):
        self.s.post(USTCMis.url + 'userinit.do', data={'userbz': 's'})
        r = self.s.get(USTCMis.url + 'randomImage.do')
        img = r.content.encode('base64').replace('\n', '')
        return img

    def login(self, user_code, pwd, check_code):
        login_info = {
            'userbz': 's',
            'hidjym': '',
            'userCode': user_code,
            'passWord': pwd,
            'check': check_code
            }
        r = self.s.post(USTCMis.url + 'login.do', data=login_info)
        check_login()
        return r

    def check_login(self):
        r = self.s.get(USTCMis.url + 'left.do')
        self.login_status = (r.text.find("个性化选课") != -1)
        return self.login

    def get_grade(self, semester):
        if check_login():
            query_data = {
                'xuenian': semester,
                'px': 1,
                'zd': 0
                }
            r = self.s.post(USTCMis.url + 'querycjxx.do', data=query_data)
            return r.text
