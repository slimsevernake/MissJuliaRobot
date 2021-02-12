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


    gmail = tmail.find({})
    # print(secret)
    for c in gmail:
        if event.sender_id == c["user"]:
            await event.reply(
                "You have already registered your account for this service."
            )
            return
    email = tm.get_email_address()
    tmail.insert_one({"user": event.sender_id, "email": })

#print(email)

__help__ = """
 - /registermail: Registers your account for the tempmail service (one time only)
 - /sendmail <email>: Send the replied message to the email provided (must be a valid one)
 - /checkinbox: Checks the inbox associated with the account for new emails
"""
