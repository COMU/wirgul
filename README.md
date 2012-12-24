wirgul (Wireless account creation for GUests and others with Ldap backend)
==========================================================================

Bu proje kullanıcıların kablosuz hesaplarını kendi başvuruları ile otomatik oluşturmak için oluşturuldu.
Yapılan başvurulara e-posta onayı gönderme prensibiyle çalışmaktadır. Eposta hesaplarına gelen bağlantıya tıklandığında
yapılan istekler gerçeklenmekte ve bilgilendirme epostası kullanıcıya gönderilmektedir.


KURULUM
=======

Kurulum adımları Debian tabanlı sistem için açıklanmıştır.

Gereksinimler
-------------

Wirgul Django web çatısı kullanılarak geliştirilmişti. Onun için ilk olarak Django kurulumu gerekmektedir.

    $ sudo apt-get install python-django

Wirgul, Django 1.3 ile uyumlu olarak yazılmıştır.

Wirgul çalışması sırasında MySQL veri tabanı kullanmaktadır. MySQL veri tabanı ayarları settings.py içerisinde tanımlanmıştır.

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'wirguldb',                      # Or path to database file if using sqlite3.
            'USER': 'wirguldbusr',                      # Not used with sqlite3.
            'PASSWORD': 'w1rg3l',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

Burada NAME veritabanı adı, USER o veri tabanı üzerinde yetkilendirilmiş kullanıcı, PASSWORD ise kullanıcını veritabanı
erişimi sırasında kullandığı parolayı içerir. Bu alanları kendi ayarlarınıza göre güncelleyiniz.
HOST ve PORT kısmı varsayılan olarak localhost ve 3306'dır. Farklı makine ve porttan çalışan MySQL sunucular için bu
ayarları da güncellemeniz gerekmektedir.

Python ile MySQL sunucu etkileşimi için MySQL eklentisi kurulmalıdır

    $ sudo apt-get install python-mysqldb

Wirgul kullanıcı hesaplarının LDAP üzerinde olduğunu varsaymaktadır. Python-LDAP etkileşimi için LDAP eklentisi kurulmalıdır.

    $ sudo apt-get install python-ldap

Wirgul içerisindeki form alanlarında insan girişinin kontrolü için Captcha kullanılmaktadır.
Django için simple-captcha eklentisi kurulmalıdır.

    $ sudo apt-get install python-pip
    $ pip install django-simple-captcha

Ayarlar
-------

Gereksinimler kurulduktan sonra git kullanarak Github üzerinden Wirgul kaynak kodları edinilmelidir. Git kurulu olmayan
sistemler için, önce git komutu çalıştırmak için gerekli paket kurulabilir.

    $ sudo apt-get install git-core
    $ git clone https://github.com/COMU/wirgul.git

Kopyalama işleminden sonra wirgul isimli dizin içerisinde kaynak kodları görebilirsiniz. İlk iş olarak bu dizin içerisindeki
**settings.py** bir metin düzenleyici ile açılmalı ve gerekli değişiklikler yapılmalıdır. **settings.py** içerisinde SMTP,
MySQL sunucu, LDAP, dipnot ve alan adı ayarları bulunmaktadır. Bu ayarlar kullanmak istediğiniz uygun karşılıklar ile
değiştirilmelidir.

Veritabanı ayarları yapıldıktan sonra tabloların tanımlı veritabanı üzerinde oluşturulması gerekmektedir. Bunun için
settings.py dosyası ile aynı dizinde takip eden komut çalıştırılabilir:

    $ python manage.py syncdb

Admin için sorulan tablo isteklerine **n** seçilerek devam edilebilir.

Sonrasında Django uygulamasının mod_wsgi ile çalışabilmesi için Apache kurulumu ve uygun wsgi ayarları gerekmektedir.
Apache kurulumu için:

    $ sudo apt-get install apache2

yeterlidir. Apache üzerinden mod_wsgi kullanımı için:

    $ sudo apt-get install libapache2-mod-wsgi

komutu verilmelidir. Bu aşamadan sonra Apache artık Python dosyalarını işleyebilir hale gelecektir. Hangi dizin için
Python ile işleme yapılması gerektiğini tanımlamak içinse bir sanal konak dosyası oluşturulması gerekmektedir.
Örnek bir dosya wsgi dizini içerisinde bulunmaktadır. Bu dosya içerisindeki yolları kendi sunucunuzdakilere göre
değiştirdikten sonra dosyayı Apache2 sanal konak dosyalarının olduğu dizine kopyalayınız

    $ sudo cp kablosuz /etc/apache2/site-available/
    $ a2ensite kablosuz
    $ /etc/init.d/apache2 reload

 Apache ayarında ilgili konağın aktif hale getirilmesi ve ayarların yeniden yüklenmesi ile artık tanımladığınız adrese
 erişimde Wirgul uygulama ekranını görüyor olmalısınız.

 Bu işlemi yaparken *kablosuz* isimli dosya içerisindeki yol tanımlarınızı kendi diskinizdekine göre güncellemeyi unutmayın.
 Bu dosya içerisindeki ServerName kısmı da uygulamaya erişirken kullanacağınız tam adresi içermektedir (FQDN).
 Kurulum sırasında Linux makinelerde /etc/hosts dosyasına elle test için bir alan adı tanımlayabilirsiniz.

 *kablosuz* isimli sanal tanım içerisinde ayrıca projenizle ilgili bir wsgi betiği tanımı da bulunmaktadır.
 Buradaki yol tanımlarının da kendi diskinizdeki yol tanımına göre yapılması gerekmektedir.

 Uygulamanın çalışır hali için: http://kablosuz.comu.edu.tr adresini ziyaret ediniz.


 LİSANS
=======

[cc-nc-sa]: http://i.creativecommons.org/l/by-nc-sa/3.0/88x31.png "Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License"

![Creative Commons License][cc-nc-sa]

Bu çalışma [Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported](http://creativecommons.org/licenses/by-nc-sa/3.0/deed.en_US) Lisansı ile lisanslanmıştır.
