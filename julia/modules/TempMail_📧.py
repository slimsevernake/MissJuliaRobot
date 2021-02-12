import tempmail
from julia import *
from julia.events import register

tm = TempMail()
api_host = 'privatix-temp-mail-v1.p.rapidapi.com'
api_key=TEMP_MAIL_KEY
tm.set_header(api_host,api_key)




email = tm.get_email_address()
#print(email)
