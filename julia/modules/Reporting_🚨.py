import html
from julia import tbot
from julia import CMD_HELP
from telethon import events
from telethon.tl import functions
from telethon.tl import types
from pymongo import MongoClient
from julia import MONGO_DB_URI
from julia.events import register
from julia.modules.sql import reporting_sql as sql

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

@register(pattern="^/reports (.*)")
async def _(event):
    if event.is_private:
       return
    chat = event.chat_id
    args = event.pattern_match.group(1)
    if args:
            if args == "on":
                sql.set_chat_setting(chat, True)
                await event.reply(
                    "Turned on reporting!\nAdmins who have turned on reports will be notified when /report or @admin is called."
                )

            elif args == "off":
                sql.set_chat_setting(chat, False)
                await event.reply(
                    "Turned off reporting!\nNo admins will be notified on /report or @admin."
                )
            else:
                await event.reply(
                    "Wrong option!\nEither say on or off."
                )                         
    else:
            await event.reply(
                f"This group's current setting is: `{sql.chat_should_report(chat)}`",
                parse_mode="markdown",
            )

