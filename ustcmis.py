# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


class USTCMis:
    url = 'http://mis.teach.ustc.edu.cn/'

    def __init__(self):
        self.s = requests.Session()
        self.login_status = False

    def get_check_code(self):
        self.s.post(USTCMis.url + 'userinit.do', data={'userbz': 's'})
        r = self.s.get(USTCMis.url + 'randomImage.do')
        img = r.content
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
        return self.check_login()

    def check_login(self):
        r = self.s.get(USTCMis.url + 'init_xk_ts.do')
        self.login_status = (r.text.find(u'所在院系') != -1)
        return self.login_status

    def get_grade(self, semester):
        if not self.check_login():
            return "login error"
        query_data = {
            'xuenian': semester,
            'px': 1,
            'zd': 0
            }
        r = self.s.post(USTCMis.url + 'querycjxx.do', data=query_data)
        soup = BeautifulSoup(r.text)
        content = {}
        tables = [i.find_all('td') for i in soup.find_all('table')]
        basic = [i.string.strip() for i in tables[0]]
        content['basic'] = dict(zip(basic[::2], basic[1::2]))
        detail_key = [i.string.strip() for i in tables[1]]
        detail_item = [i.string.strip() for i in tables[2]]
        detail = {}
        for i in xrange(len(detail_item) / len(detail_key)):
            n = len(detail_key)
            item = detail_item[i * n: i * n + n]
            detail[i] = dict(zip(detail_key, item))
        content['detail'] = detail
        return content
