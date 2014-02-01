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
        if r.ok:
        #need fix
            self.login_status = True
        return r

    def get_grade(self, semester):
        if self.login:
            query_data = {
                'xuenian': semester,
                'px': 1,
                'zd': 0
                }
            r = self.s.post(USTCMis.url + 'querycjxx.do', data=query_data)
            return r.content
