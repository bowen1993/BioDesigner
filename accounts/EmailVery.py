import threading
from django.core.mail import send_mail
import datetime
import hashlib
from accounts.models import User, UserSafety

class EmailVerity(threading.Thread):
    def __init__(self, emailAddr, username):
        threading.Thread.__init__(self)
        self.emailAddr = emailAddr
        self.username = username
    def run(self):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:10]
        active_key = hashlib.sha1(self.emailAddr+salt).hexdigest()
        key_expires = datetime.datetime.today() + datetime.timedelta(2)

        # create new user safety
        newSafety = UserSafety(user_id=self.username, activation_key=active_key, key_expires=key_expires)
        newSafety.save()

        #send email with active key
        email_subject = 'BioDesigner Account confirmation'
        email_body = "Hello %s,\nThanks for your registeration.\nTo active you account \
        , please click this link within 48 hours\n\
        http://127.0.0.1:8000/accounts/confirm/%s" % (self.username, active_key)
        send_mail(email_subject, email_body, 'biodesigner@bio.com',
         [self.emailAddr],fail_silently=False)
