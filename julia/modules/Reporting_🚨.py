import html
from julia import tbot
from julia import CMD_HELP
from telethon import events
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from pymongo import MongoClient
from julia import MONGO_DB_URI
from julia.events import register
from julia.modules.sql import reporting_sql as sql

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

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

async def can_ban_users(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users
    )

async def can_del(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.delete_messages
    )

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

@tbot.on(events.CallbackQuery(pattern=r"report_(.*?)"))
async def _(event):
    query = event.pattern_match.group(1)
    splitter = query.replace("report_", "").split("=")
    if splitter[1] == "kick":
        try:
            await tbot.kick_participant(splitter[0], splitter[2])            
            await event.answer("✅ Succesfully kicked")
            return
        except Exception as err:
            await event.answer("🛑 Failed to kick")
            print (err)
    elif splitter[1] == "banned":
        try:
            await tbot(EditBannedRequest(splitter[0], splitter[2], BANNED_RIGHTS)) 
            await event.answer("✅  Succesfully Banned")
            return
        except Exception as err:
            print (err)
            await event.answer("🛑 Failed to Ban")
    elif splitter[1] == "delete":
        try:
            await tbot.delete_messages(splitter[0], splitter[3])
            await event.answer("✅ Message Deleted")
            return
        except Exception as err:
            print (err)
            await event.answer("🛑 Failed to delete message!")

