import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
""""__**𝐈'𝐦 📌𝐀𝐉𝐄𝐄𝐓 𝐓𝐚𝐠𝐀𝐥𝐥 𝐁𝐨𝐭**, 𝐢 𝐂𝐚𝐧 𝐌𝐞𝐧𝐭𝐢𝐨𝐧 𝐀𝐥𝐥 𝐌𝐞𝐦𝐛𝐞𝐫𝐬 𝐈𝐧 𝐆𝐫𝐨𝐮𝐩 𝐎𝐫 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 👻\n𝐂𝐥𝐢𝐜𝐤 **/help** 𝐅𝐨𝐫 𝐌𝐨𝐫𝐞 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧__\n\n 𝐅𝐨𝐥𝐥𝐨𝐰 [𝐀𝐣𝐞𝐞𝐭𝐆𝐨𝐧𝐝](https://t.me/papa_bol_sakteho) 𝗢𝗻 𝐓𝐞𝐥𝐞𝐆𝐫𝐚𝐦 ",
ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ TAGALL ʏᴏᴜʀ ɢʀᴏᴜᴘꜱ ᴀɴᴅ ɪ ᴍ ᴠᴇʀʏ ᴘᴏᴡᴇʀꜰᴜʟʟ ʙᴏᴛ! 
*𝐇𝐄𝐘! ,*
┏━━━━━━━━━━━━━━━━
┣ ₪ *ADD ME YOUR GROUP* `
┣ ₪ IAM POWER FULL TAGGER BOT
┣ ₪ __\n\n ᴄʀᴇᴀᴛᴇᴅ ʙʏ [𝐀𝐣𝐞𝐞𝐭𝐆𝐨𝐧𝐝](https://t.me/papa_bol_sakteho)
┗━━━━━━━━━━━━━━━━━
 
  ʜɪᴛ /help **FOR MORE**
 [❤](https://te.legra.ph/file/0f738af80bd579c37624a.jpg),
""",
    link_preview=False,
    buttons=(
       [
        Button.url(' support', 'https://t.me/The_professor_network'),
        Button.url('creater', 'https://t.me/Papa_bol_sakteho')
    ],
    )
  )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "COMMANDS:@all,/cancel. excample @all hi add me your groups iam best tagger pro bot"
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url(' support', 'https://t.me/Tpn_chatroom'),
        Button.url('creater', 'https://t.me/Papa_bol_sakteho')
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^@all ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__This command can be use in groups and channels!__")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__Only admins can mention all!__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__Give me one argument!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("__I can't mention members for older messages! (messages which are sent before I'm added to group)__")
  else:
    return await event.respond("__Reply to a message or give me some text to mention others!__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__There is no proccess on going...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__Stopped.__')

print(">> 📌🄰🄹🄴🄴🅃 🆃🅰🅶 🄱🄾🅃 <<")
client.run_until_disconnected()
