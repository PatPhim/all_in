#!/usr/bin/python
# _*_ coding:utf-8 _*_
import requests
import datetime
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

API_ELV = (config['DEFAULT']["api_emaillistverify"])

class one():

    def __init__(self, email):
        self.key = API_ELV
        self.email = email
        self.verif = "https://apps.emaillistverify.com/api/verifEmail?secret="
        self.url = self.verif + self.key + "&email=" + self.email

    def control(self):
        r = requests.get(self.url)
        return r.text


class bulk():
    def __init__(self, user_file):
        datenow = datetime.datetime.now()
        self.key = API_ELV
        self.name = 'File' + datenow.strftime("%Y-%m-%d %H:%M")
        self.user_file = user_file
        self.url = 'https://apps.emaillistverify.com/api/verifApiFile?secret=' + API_ELV + '&filename=%s' % self.name

    def upload(self):
        import pycurl

        infile = open('id_file', 'w')
        c = pycurl.Curl()

        c.setopt(pycurl.URL, self.url)
        c.setopt(pycurl.SSL_VERIFYPEER, 1)
        c.setopt(pycurl.SSL_VERIFYHOST, 2)
        c.setopt(pycurl.CAINFO, "/path/to/updated-certificate-chain.crt")
        c.perform()

        c.setopt(c.POST, 1)
        c.setopt(c.URL, self.url)
        c.setopt(c.HTTPPOST, [('file_contents', (
            c.FORM_FILE, self.user_file,
            c.FORM_CONTENTTYPE, 'text/plain',
            c.FORM_FILENAME, self.name.replace(' ', '_'),)), ])
        c.setopt(c.WRITEFUNCTION, infile.write)
        c.setopt(c.VERBOSE, 1)
        c.perform()
        c.close()

    def get_info(self):
        with open('id_file', 'r') as f:
            ids = f.read()
        url = 'https://apps.emaillistverify.com/api/getApiFileInfo?secret=' + self.key + '&id=%s' % ids
        r = requests.get(url)
        with open('result.txt', 'a') as res:
            res.write(r.content + '\n')
        print
        r.content


if __name__ == '__main__':
    pass