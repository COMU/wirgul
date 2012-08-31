#!/usr/bin/env python
#-*- coding: UTF-8 -*-

__author__ = 'oguz'

from wirgul.utils.ldapmanager import LdapHandler
from wirgul.utils.utils import generate_passwd

import sys

class TemporaryUser:

    def __init__(self):
        self.ldap_handler = LdapHandler()
        status = self.ldap_handler.connect()
        if status:
            try:
                self.ldap_handler.bind()
            except:
                self.ldap_handler.unbind()
                sys.exit(-1)


    def change_password(self, start=1, stop=101):

        f = file("gecisi_kullanicilar.csv", "w")

        for x in range(start, stop):
            email = "".join(["user", str(x), "@comu.edu.tr"])
            if self.ldap_handler.search(email) > 0:
                print email
                passwd = generate_passwd()
                if self.ldap_handler.modify_student(passwd, email):
                    print "Parola degisti", passwd
                    name = "".join(["GECICI KULLANICI", str(x)])
                    username = email
                    line = ",".join([name, username, passwd])
                    f.write(line)
                    f.write("\n")

        f.close()
        self.ldap_handler.unbind()


if __name__ == "__main__":

    temp = TemporaryUser()
    temp.change_password()

