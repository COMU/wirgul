#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import ldap
from ldifparser import Parse
import ldap.modlist as modlist
import random
import string

class Operations:

    def __init__(self):
        self.servername = "".join(["ldap://","server_ip_addres"])
        self.admin_dn = "admin_dn"
        self.admin_passwd = "admin_passwd"

    def makePassword(self,minlength=5,maxlength=10):
        length1=random.randint(minlength,maxlength)
        letters=string.ascii_letters+string.digits
        use0 = letters.partition("l")
        part = use0[2]
        use1 = part.partition("o")
        part = use1[2]
        use2 = part.partition("I")
        part = use2[2]
        use3 = part.partition("O")
        part = use3[2]
        use4 = part.partition("0")
        letters = "".join([use0[0], use1[0], use2[0], use3[0], use4[0], use4[2]])
        letters = letters.partition("-")[0]
        return ''.join([random.choice(letters) for _ in range(length1)])

    def connect(self):
        self.server = ldap.initialize(self.servername)
        self.server.protocol_version = ldap.VERSION3

    def bind(self):
        self.server.bind_s(self.admin_dn, self.admin_passwd)

    def unbind(self):
        self.server.unbind_s()

    def add(self, filename):
        p = Parse(filename)
        p.parse()
        dn,user_attributes =  p.format()
        print dn
        print user_attributes
        try:
            self.server.add_s(dn, user_attributes)
            return True
        except Exception, ex:
            print ex
            return False

    def add_formatted(self, dn, ldif):
        '''
        add_record = [
                    ('objectclass', ['person','organizationalperson','inetorgperson']),
                    ('uid', ['francis']),
                    ('cn', ['Francis Bacon'] ),
                    ('sn', ['Bacon'] ),
                    ('userpassword', ['secret']),
                    ('ou', ['users'])
                   ]
        [(dn1, attribute_of_this_dn1), (dn2, attribute_of__this_dn2), ...]
        '''
        self.server.add_s(dn, ldif)

    def del_user(self, mail, member_type="personel"):
        if member_type == "":
            s = "".join(["mail=",mail,",","ou=people,dc=comu,dc=edu,dc=tr"])
        if member_type == "personel" or member_type == "ogrenci":
            s = "".join(["mail=",mail,",","ou=",member_type,",","ou=people,dc=comu,dc=edu,dc=tr"])
        #print s
        try:
            self.server.delete_s(s)
            return True
        except:
            return False

    def search(self, mail, member_type="personel"):
        '''
            return value
            [('mail=alpertekinalp@comu.edu.tr,ou=ogrenci,ou=people,dc=comu,dc=edu,dc=tr',
  {'cn': ['Alper Tekinalp'],
   'givenName': ['Alper'],
   'mail': ['alpertekinalp@comu.edu.tr'],
   'objectClass': ['organizationalPerson',
                   'radiusprofile',
                   'person',
                   'inetOrgPerson'],
   'sn': ['Tekinalp'],
   'uid': ['alpertekinalp'],
   'userPassword': ['alper123']})]
        '''
        if not member_type:
            s = "".join(["mail=",mail,",","ou=people,dc=comu,dc=edu,dc=tr"])
        if member_type == "personel" or member_type == "ogrenci":
            s = "".join(["mail=",mail,",","ou=",member_type,",","ou=people,dc=comu,dc=edu,dc=tr"])
        try:
            return self.server.search_s(base=s, scope=ldap.SCOPE_BASE)
        except:
            return False

    def modify_personel(self, email, old_password, new_password):

        # The dn of our existing entry/object
        dn="mail="+email+",ou=personel,ou=people,dc=comu,dc=edu,dc=tr"

        # Some place-holders for old and new values
        old = {'userPassword': old_password}
        new = {'userPassword': new_password}

        # Convert place-holders for modify-operation using modlist-module
        ldif = modlist.modifyModlist(old,new)

        # Do the actual modification
        print self.server.modify_s(dn,ldif)

        # Its nice to the server to disconnect and free resources when done
        #self.server.unbind_s()

    def modify_ogrenci(self, email, old_password, new_password):

        # The dn of our existing entry/object
        dn="mail="+email+",ou=ogrenci,ou=people,dc=comu,dc=edu,dc=tr"

        # Some place-holders for old and new values
        old = {'userPassword': old_password}
        new = {'userPassword': new_password}

        # Convert place-holders for modify-operation using modlist-module
        ldif = modlist.modifyModlist(old,new)

        # Do the actual modification
        print self.server.modify_s(dn,ldif)

        # Its nice to the server to disconnect and free resources when done
        #self.server.unbind_s()

if __name__ == "__main__":
    op = Operations()
    op.connect()
    op.bind()
    #op.add("test.ldif")
    #print op.modify_ogrenci("080401018@comu.edu.tr", "M1Quw", "engine123")
    op.modify_personel("akgun@comu.edu.tr", "ArmFYa", "143014qazxsw")
    #op.modify_ogrenci("user1@comu.edu.tr", "XX3WtjgW", "G8NiU")
    #print op.search("user1@comu.edu.tr", member_type="ogrenci")
    op.unbind()

