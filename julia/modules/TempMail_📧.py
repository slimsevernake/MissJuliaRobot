import tempmail
from julia import *
from julia.events import register
from pymongo import MongoClient
from telethon import types, events
from telethon.tl import *
from telethon.tl.types import *

client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve
tmail = db.tempmail

tm = TempMail()
api_host = 'privatix-temp-mail-v1.p.rapidapi.com'
api_key=TEMP_MAIL_KEY
tm.set_header(api_host,api_key)

async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):          
        return True


email = tm.get_email_address()
#print(email)
