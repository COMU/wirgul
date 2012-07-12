#!/usr/bin/env python
#-*- coding: UTF-8 -*-

def createhtmlmail (html, text, subject, fromEmail):
    """Create a mime-message that will render HTML in popular
    MUAs, text in better ones"""
    import MimeWriter
    import mimetools
    import cStringIO

    out = cStringIO.StringIO() # output buffer for our message
    htmlin = cStringIO.StringIO(html)
    txtin = cStringIO.StringIO(text)

    writer = MimeWriter.MimeWriter(out)
    #
    # set up some basic headers... we put subject here
    # because smtplib.sendmail expects it to be in the
    # message body
    #
    writer.addheader("From", fromEmail)
    writer.addheader("Subject", subject)
    writer.addheader("MIME-Version", "1.0")
    #
    # start the multipart section of the message
    # multipart/alternative seems to work better
    # on some MUAs than multipart/mixed
    #
    writer.startmultipartbody("alternative")
    writer.flushheaders()
    #
    # the plain text section
    #
    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    pout = subpart.startbody("text/plain", [("charset", 'utf-8')])
    mimetools.encode(txtin, pout, 'quoted-printable')
    txtin.close()
    #
    # start the html subpart of the message
    #
    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    #
    # returns us a file-ish object we can write to
    #
    pout = subpart.startbody("text/html", [("charset", 'utf-8')])
    mimetools.encode(htmlin, pout, 'quoted-printable')
    htmlin.close()
    #
    # Now that we're done, close our writer and
    # return the message body
    #
    writer.lastpart()
    msg = out.getvalue()
    out.close()
    #print msg
    return msg

def mailsend(user, link, to):
    import smtplib
    # Create the body of the message (a plain-text and an HTML version).
    link = "http://ldap.comu.edu.tr/akademik/bilgi/?id=" + link
    text = u"Sayın " + user + "," + "\r\n\r\n"
    text += u"Üniversitemizde kullanılmaya başlanan kablosuz ağın Eduroam'a geçişinde sizin için bir kullanıcı adı ve parola oluşturulmuştur.\r\n"
    text += u"Bu geçiş ile tek kullanıcı adı ve parola ile sunulan servislere erişim hedeflenmektedir.\r\n"
    text += u"Lütfen aşağıdaki linki tarayıcınızda açarak kaydınızı tamamlayınız!" + "\r\n"
    text += link + "\r\n\r\n"
    text += u"Eduroam, Education Roaming (Eğitim Gezintisi) kelimelerinin kısaltmasıdır.\r\n"
    text += u"RADIUS tabanlı altyapı üzerinden 802.1x güvenlik standartlarını kullanarak, eduroam üyesi kurumların kullanıcılarının diğer eğitim kurumlarında da sorunsuzca ağ kullanımını amaçlamaktadır.\r\n"
    text += u"Daha fazla bilgiye http://bidb.comu.edu.tr/eduroam/eduroam.htm veya http://www.eduroam.org/ web adreslerinden ulaşabilirsiniz.\r\n"
    text += "\r\n\r\n"
    text += u"Çanakkale Onsekiz Mart Üniversitesi\r\n\
	Bilgi İşlem Dairesi Başkanlığı\r\n\
	Tel : +90 286 218 00 18\r\n\
	Tel - Fax : +90 286 218 05 18\r\n"

    text = text.encode("utf-8")

    html = u"""\
    <html>
      <head>
	  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
      </head>
      <body>
	<p>Sayın, """ + user + u"""<br> \
        Üniversitemiz kullanılmaya başlanan kablosuz ağın Eduroam'a geçişinde sizin için bir kullanıcı adı ve parola oluşturulmuştur. <br>
        Bu geçiş ile tek kullanıcı adı ve parola ile sunulan servislere erişim hedeflenmektedir. <br>
        Lütfen aşağıdaki linki tarayıcınızda açarak kaydınızı tamamlayınız! <br>
	  <a href=\"""" + link + u"""\">Form Erişimi İçin Tıklayınız</a>
	</p>
    <p>
        Eduroam, Education Roaming (Eğitim Gezintisi) kelimelerinin kısaltmasıdır.
        RADIUS tabanlı altyapı üzerinden 802.1x güvenlik standartlarını
        kullanarak, eduroam üyesi kurumların kullanıcılarının diğer eğitim
        kurumlarında da sorunsuzca ağ kullanımını amaçlamaktadır.
        Daha fazla bilgiye http://bidb.comu.edu.tr/eduroam/eduroam.htm veya
        http://www.eduroam.org/ web adreslerinden ulaşabilirsiniz.
    </p>
	<br>
	<p>
	  Çanakkale Onsekiz Mart Üniversitesi<br>
	  Bilgi İşlem Dairesi Başkanlığı<br>
	  Tel : +90 286 218 00 18<br>
	  Tel - Fax : +90 286 218 05 18<br>
	</p
      </body>
    </html>
    """

    html = html.encode("utf-8")

    subject = "Eduroam Bilgi Giris Form Linki"
    message = createhtmlmail(html, text, subject, 'Bilgi Islem Dairesi Baskanligi <yardim@comu.edu.tr>')
    server = smtplib.SMTP('smtp.googlemail.com', 587)
    #server.set_debuglevel(1)
    server.starttls()
    server.login('yardim@comu.edu.tr', 'artemis@nso')
    rtr_code =  server.verify(to)
    server.sendmail('yardim@comu.edu.tr', to, message)
    server.quit()
    #print rtr_code
    return rtr_code[0]

if __name__ == "__main__":
    mailsend("FIKRET CAKIR", "F40p9IHkwZicuPccwfDi6rYh04xnZ5", "fikretcakir@comu.edu.tr")


