import ldap
import ldap.modlist as modlist
from django.conf import settings
from web.models import FirstTimeUser

class LdapHandler:

    def __init__(self):
        self.servername = "".join(["ldap://",settings.LDAP_SERVER])  # 127.0.0.1
        self.admin_dn = settings.LDAP_ADMIN_DN  # dn
        self.admin_passwd = settings.LDAP_PASSWORD  # passwd

    def connect(self):
        try:
            self.server = ldap.initialize(self.servername)  # ldap.open()
            self.server.protocol_version = ldap.VERSION3
            return True
        except Exception, ex:
            return False

    def bind(self):
        try:
            self.server.bind_s(self.admin_dn, self.admin_passwd)
            return True
        except Exception, ex:
            return False

    def unbind(self):
        self.server.unbind_s()

    def add(self,name,middle_name,surname,email,passwd):
        attrs = {}
        if email.find("@gmail.com") != -1:
                mail_adr = email.split("@")
                email = mail_adr[0]
                dn= "".join(["mail=",email,"@comu.edu.tr,ou=personel,ou=people,dc=comu,dc=edu,dc=tr"])
                attrs['mail'] = "".join([email,"@comu.edu.tr"])
        else:
            dn="mail="+email+"comu.edu.tr,ou=personel,ou=people,dc=comu,dc=edu,dc=tr"
            attrs['mail'] = email
        attrs['objectclass'] = ['organizationalPerson','person','inetOrgPerson']
        attrs['givenName'] = " ".join([name,middle_name])
        attrs['sn'] = surname
        attrs['cn'] = " ".join([name,middle_name,surname])
        attrs['userPassword'] = passwd
        try :
            ldif = modlist.addModlist(attrs)
            self.server.add_s(dn,ldif)
            return True
        except :
            return False

    def search(self, email): # sadece mail adresine gore ldapta arama yapmak icin
        base_dn = "ou=people,dc=comu,dc=edu,dc=tr"
        if email.find("@gmail.com") != -1:
            mail_username = email.split("@")[0]
            email = "".join([mail_username,"@comu.edu.tr"])
        filter = "".join(['mail=',email])
        self.results = self.server.search_s(base_dn, ldap.SCOPE_SUBTREE, filter) # tek elemanli bir list
        return len(self.results)

    def get_cn(self,email): # sadece mail adresine gore kisinin adini soyadini getirir
        base_dn = "ou=people,dc=comu,dc=edu,dc=tr"
        if email.find("@gmail.com") != -1:
            mail_adr = email.split("@")
            email = mail_adr[0]
            email = "".join([email,"@comu.edu.tr"])
        filter = "".join(['mail=',email])
        attr = ['cn']
        self.results = self.server.search_s(base_dn,ldap.SCOPE_SUBTREE,filter,attr) # tek elemanli bir list
        s = str(self.results) # icinden cn cekebilmek icin strige cevirdik.
        array = s.split('\'') # tek tirnaga gore ayirdik. bir diziye atadik
        cn = array[5]  # array in 5. elemanina denk geliyo kullanici common name i
        return cn



    def modify(self,password,email):
        self.mod_atr = [( ldap.MOD_REPLACE, 'userPassword', password )]
        if email.find("@gmail.com") != -1:
            mail_adr = email.split("@")
            email = mail_adr[0]
            email = "".join([email,"@comu.edu.tr"])
        try:
            self.server.modify_s("".join(['mail=',email,',ou=personel,ou=people,dc=comu,dc=edu,dc=tr']),self.mod_atr)
            return True
        except :
            return False


