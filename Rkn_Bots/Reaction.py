import requests, httpx
from pyrogram import Client, filters, errors, types
from config import Rkn_Bots, AUTH_CHANNEL
import asyncio, re, time, sys, random
from .database import total_user, getid, delete, addCap, updateCap, insert, chnl_ids
from pyrogram.errors import *
from pyrogram.types import *
from utils import react_msg 
from Script import script
import aiohttp

buttons = [[
        InlineKeyboardButton('✇ Uᴘᴅᴀᴛᴇs ✇', url="https://t.me/HGBOTZ"),
        InlineKeyboardButton('✨ 𝙲𝙾𝙽𝚃𝙰𝙲𝚃 ✨', url="https://t.me/Harshit_contact_bot")
    ]]

group_buttons = [[InlineKeyboardButton('✇ Click To Start Me ✇', url="http://t.me/Reaction_99bot?start=True")
               ],[
                  InlineKeyboardButton('✇ Uᴘᴅᴀᴛᴇs ✇', url="https://t.me/HGBOTZ")
                ]] 


back_button = [[
                 InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/HGBOTZ_support'),
                 InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://telegram.me/hgbotz')
              ],[
                 InlineKeyboardButton('🔙 back', callback_data='back')
              ]]

about_buttons = [[
        InlineKeyboardButton('🙂 𝐎𝐖𝐍𝐄𝐑', url='https://t.me/Harshit_contact_bot')
        ],[
        InlineKeyboardButton('❗️ʜᴇʟᴘ', callback_data='help'), 
        InlineKeyboardButton('🦋 𝙷𝙾𝙼𝙴', callback_data='back')
        ],[
        InlineKeyboardButton('📜 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/HGBOTZ_support'),
        InlineKeyboardButton('📢 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://telegram.me/hgbotz')
        ]]


async def is_subscribed(bot, query, channel):
    btn = []
    for id in channel:
        chat = await bot.get_chat(int(id))
        try:
            await bot.get_chat_member(id, query.from_user.id)
        except UserNotParticipant:
            btn.append([InlineKeyboardButton(f'Join {chat.title}', url=chat.invite_link)])
        except Exception as e:
            pass
    return btn

@Client.on_message(filters.private & filters.user(Rkn_Bots.ADMIN)  & filters.command(["stats"]))
async def all_db_users_here(client, message):
    start_t = time.time()
    rkn = await message.reply_text("Processing...")
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - client.uptime))    
    total_users = await total_user()
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rkn.edit(text=f"**--Bot Processed--** \n\n**Bot Started UpTime:** {uptime} \n**Bot Current Ping:** `{time_taken_s:.3f} ᴍꜱ` \n**All Bot Users:** `{total_users}`")


@Client.on_message(filters.private & filters.user(Rkn_Bots.ADMIN) & filters.command(["broadcast"]))
async def broadcast(bot, message):
    if (message.reply_to_message):
        rkn = await message.reply_text("Bot Processing.\nI am checking all bot users.")
        all_users = await getid()
        tot = await total_user()
        success = 0
        failed = 0
        deactivated = 0
        blocked = 0
        await rkn.edit(f"bot ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ started...")
        async for user in all_users:
            try:
                time.sleep(1)
                await message.reply_to_message.copy(user['_id'])
                success += 1
            except errors.InputUserDeactivated:
                deactivated +=1
                await delete({"_id": user['_id']})
            except errors.UserIsBlocked:
                blocked +=1
                await delete({"_id": user['_id']})
            except Exception as e:
                failed += 1
                await delete({"_id": user['_id']})
                pass
            try:
                await rkn.edit(f"<u>ʙʀᴏᴀᴅᴄᴀsᴛ ᴘʀᴏᴄᴇssɪɴɢ</u>\n\n• ᴛᴏᴛᴀʟ ᴜsᴇʀs: {tot}\n• sᴜᴄᴄᴇssғᴜʟ: {success}\n• ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: {blocked}\n• ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: {deactivated}\n• ᴜɴsᴜᴄᴄᴇssғᴜʟ: {failed}")
            except FloodWait as e:
                await asyncio.sleep(t.x)
        await rkn.edit(f"<u>ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</u>\n\n• ᴛᴏᴛᴀʟ ᴜsᴇʀs: {tot}\n• sᴜᴄᴄᴇssғᴜʟ: {success}\n• ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: {blocked}\n• ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: {deactivated}\n• ᴜɴsᴜᴄᴄᴇssғᴜʟ: {failed}")
        
# Restart to cancell all process 
@Client.on_message(filters.private & filters.user(Rkn_Bots.ADMIN) & filters.command("restart"))
async def restart_bot(b, m):
    rkn_msg = await b.send_message(text="**🔄 𝙿𝚁𝙾𝙲𝙴𝚂𝚂𝙴𝚂 𝚂𝚃𝙾𝙿𝙴𝙳. 𝙱𝙾𝚃 𝙸𝚂 𝚁𝙴𝚂𝚃𝙰𝚁𝚃𝙸𝙽𝙶...**", chat_id=m.chat.id)       
    await asyncio.sleep(3)
    await rkn_msg.edit("**✅️ 𝙱𝙾𝚃 𝙸𝚂 𝚁𝙴𝚂𝚃𝙰𝚁𝚃𝙴𝙳. 𝙽𝙾𝚆 𝚈𝙾𝚄 𝙲𝙰𝙽 𝚄𝚂𝙴 𝙼𝙴**")
    os.execl(sys.executable, sys.executable, *sys.argv)
    
NOTIFICATION_CHANNEL_ID = -1002346166150
@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(bot, message):
    client = bot
    if AUTH_CHANNEL:
        try:
            btn = await is_subscribed(client, message, AUTH_CHANNEL)
            if btn:
                username = (await client.get_me()).username
                if message.command:
                    btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{username}?start=true")])
                else:
                    btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{username}?start=true")])
                await message.reply_text(text=f"<b>👋 Hello {message.from_user.mention},\n\nPlease join the channel then click on try again button. 😇</b>", reply_markup=InlineKeyboardMarkup(btn))
                return
        except Exception as e:
            print(e)
    user_id = int(message.from_user.id)
    reply_markup=InlineKeyboardMarkup(buttons)
    await insert(user_id)
    notification_text = f"🎉 New user started the bot: {message.from_user.mention} (ID: {user_id})"
    await bot.send_message(NOTIFICATION_CHANNEL_ID, notification_text)
    await message.reply_photo(photo=Rkn_Bots.RKN_PIC,
        caption=script.START_TXT.format(message.from_user.mention),
        has_spoiler=True, 
        reply_markup=reply_markup)




FANCODE_URL = "https://raw.githubusercontent.com/drmlive/fancode-live-events/main/fancode.json"

@Client.on_message(filters.command("fancode") & filters.private)
async def fancode_handler(client, message):
    try:
        async with httpx.AsyncClient() as http:
            response = await http.get(FANCODE_URL)
            data = response.json()

        live_matches = [m for m in data.get("matches", []) if m.get("status") == "LIVE"]

        if not live_matches:
            await message.reply("No live matches right now.")
            return

        for match in live_matches:
            text = (f"<b>{match['match_name']} ({match['event_name']})</b>\n\n"
                f"🔴 <b>FROM:</b> Fancode\n"
                f"🏟 <b>Event:</b> {match['event_name']}\n"
                f"🕒 <b>Start Time:</b> {match['startTime']}\n"
                f"👥 <b>Teams:</b> {match['team_1']} vs {match['team_2']}\n"
                f"<blockquote><b>Stream info </b>\n🌐 <b>Normal Stream:</b> {match['dai_url']}\n🚫 <b>Ad-Free Stream:</b> {match['adfree_url']}</blockquote>\n\n"
                f"<b>Note: Copy and paste the url in NS player or VLC media player to play stream</b>"
            )

            await message.reply_photo(photo=match['src'], caption=text)

    except Exception as e:
        await message.reply("Something went wrong while fetching Fancode data.")
        print(e)





FANCODE_URL = "https://raw.githubusercontent.com/drmlive/fancode-live-events/main/fancode.json"

fancode_status = {}  # chat_id: True/False
fancode_messages = {}  # chat_id: list of msg ids

async def fetch_f_live_matches():
    async with httpx.AsyncClient() as http:
        resp = await http.get(FANCODE_URL)
        data = resp.json()
    return [m for m in data.get("matches", []) if m.get("status") == "LIVE"]

async def send_f_live_matches(client, chat_id):
    live_matches = await fetch_f_live_matches()
    if chat_id in fancode_messages:
        # delete old messages
        for msg_id in fancode_messages[chat_id]:
            try:
                await client.delete_messages(chat_id, msg_id)
            except:
                pass

    sent_msg_ids = []
    for match in live_matches:
        text = (f"<b>{match['match_name']} ({match['event_name']})</b>\n\n"
                f"🔴 <b>FROM:</b> Fancode\n"
                f"🏟 <b>Event:</b> {match['event_name']}\n"
                f"🕒 <b>Start Time:</b> {match['startTime']}\n"
                f"👥 <b>Teams:</b> {match['team_1']} vs {match['team_2']}\n"
                f"<blockquote><b>Stream info </b>\n🌐 <b>Normal Stream:</b> {match['dai_url']}\n🚫 <b>Ad-Free Stream:</b> {match['adfree_url']}</blockquote>\n\n"
                f"<b>Note: Copy and paste the url in NS player or VLC media player to play stream</b>"
            )
        try:
            sent = await client.send_photo(
                chat_id,
                photo=match['src'], 
                caption=text
            )
            sent_msg_ids.append(sent.id)
        except Exception as e:
            print(f"Error sending message: {e}")

    fancode_messages[chat_id] = sent_msg_ids

async def auto_send_f_loop(client, chat_id):
    while fancode_status.get(chat_id, False):
        await send_f_live_matches(client, chat_id)
        await asyncio.sleep(1800)  # 30 minutes

@Client.on_message(filters.command("fan") & filters.user(Rkn_Bots.ADMIN))
async def fancode(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage:\n/fan on [channel_id]\n/fan off [channel_id]")

    arg = message.command[1].lower()
    
    # Check if channel ID is provided
    if len(message.command) > 2 and message.command[2].lstrip('-').isdigit():
        chat_id = int(message.command[2])
    else:
        chat_id = message.chat.id

    if arg == "on":
        if fancode_status.get(chat_id, False):
            await message.reply(f"Fancode auto updates are already ON for {'this chat' if chat_id == message.chat.id else 'the specified channel'}.")
            return
        fancode_status[chat_id] = True
        await message.reply(f"Fancode auto updates started for {'this chat' if chat_id == message.chat.id else 'the specified channel'}. Updates every 30 minutes.")
        asyncio.create_task(auto_send_f_loop(client, chat_id))

    elif arg == "off":
        if not fancode_status.get(chat_id, False):
            await message.reply(f"Fancode auto updates are already OFF for {'this chat' if chat_id == message.chat.id else 'the specified channel'}.")
            return
        fancode_status[chat_id] = False
        await message.reply(f"Fancode auto updates stopped for {'this chat' if chat_id == message.chat.id else 'the specified channel'}.")
        # delete old messages
        if chat_id in fancode_messages:
            for msg_id in fancode_messages[chat_id]:
                try:
                    await client.delete_messages(chat_id, msg_id)
                except:
                    pass
            fancode_messages.pop(chat_id)

    else:
        await message.reply("Unknown option. Use:\n/fan on [channel_id]\n/fan off [channel_id]")



WILLOW_URL = "https://hgbotz.serv00.net/willow.php"

@Client.on_message(filters.command("willow") & filters.private)
async def willow(client, message):
    try:
        async with httpx.AsyncClient() as http:
            response = await http.get(WILLOW_URL)
            data = response.json()

        live_matches = [m for m in data.get("matches", []) if m.get("status", "").lower() == "live"]

        if not live_matches:
            await message.reply("No live matches currently on Willow TV.")
            return

        for match in live_matches:
            # Extract teams from title
            teams = match['title'].split('vs')
            team1 = teams[0].split('-')[-1].strip() if len(teams) > 0 else "Team 1"
            team2 = teams[1].split('-')[0].strip() if len(teams) > 1 else "Team 2"
          
            # Format CDN URLs
            cdn_urls = "\n".join([f"🌐 {url['cdn']}: {url['url']}" 
                                for url in match.get('playback_data', {}).get('urls', [])])
        
            # Format decryption keys
            keys = "\n".join([f"🔑 {key}" for key in match.get('playback_data', {}).get('keys', [])])

            text = (f"<a href='{match['cover']}'>ㅤ</a> <b>{match['title']}</b>\n"
                        f"🏆 <b>Event Type:</b> {match.get('contentType', 'Cricket Match')}\n"
                        f"🕒 <b>Start Time:</b> {match['startTime']}\n"
                        f"👥 <b>Teams:</b> {team1} vs {team2}\n"
                        f"<blockquote expandable> Stream URLs:</b>\n{cdn_urls}\n</blockquote>"
                        f"<b>Decryption Keys:</b>\n{keys}\n\n"
                        f"<b>Note: Copy and paste the url in NS player or VLC media player in android and Autho iptv in pc to play stream</b>")

            await message.reply_text(
                text=text, 
                disable_web_page_preview=False, 
                invert_media=True
            )

    except Exception as e:
        await message.reply(f"Failed to fetch Willow TV data. Please try again later. {e} ")
        print(f"Willow TV error: {e}")


WILLOW_URL = "https://hgbotz.serv00.net/willow.php"
willow_status = {}  # chat_id: True/False
willow_messages = {}  # chat_id: list of msg ids

async def fetch_w_live_matches():
    async with httpx.AsyncClient() as http:
        resp = await http.get(WILLOW_URL)
        data = resp.json()
    return [m for m in data.get("matches", []) if m.get("status", "").lower() == "live"]

async def send_w_live_matches(client, chat_id):
    live_matches = await fetch_w_live_matches()
    if chat_id in willow_messages:
        for msg_id in willow_messages[chat_id]:
            try:
                await client.delete_messages(chat_id, msg_id)
            except:
                pass

    sent_msg_ids = []
    for match in live_matches:
        # Extract teams from title
        teams = match['title'].split('vs')
        team1 = teams[0].split('-')[-1].strip() if len(teams) > 0 else "Team 1"
        team2 = teams[1].split('-')[0].strip() if len(teams) > 1 else "Team 2"
        
        # Format CDN URLs
        cdn_urls = "\n".join([f"🌐 {url['cdn']}: {url['url']}" 
                            for url in match.get('playback_data', {}).get('urls', [])])
        
        # Format decryption keys
        keys = "\n".join([f"🔑 {key}" for key in match.get('playback_data', {}).get('keys', [])])

        text = (f"<a href='{match['cover']}'>ㅤ</a> <b>{match['title']}</b>\n"
                    f"🏆 <b>Event Type:</b> {match.get('contentType', 'Cricket Match')}\n"
                    f"🕒 <b>Start Time:</b> {match['startTime']}\n"
                    f"👥 <b>Teams:</b> {team1} vs {team2}\n"
                    f"<blockquote expandable> Stream URLs:</b>\n{cdn_urls}\n</blockquote>"
                    f"<b>Decryption Keys:</b>\n{keys}\n\n"
                    f"<b>Note: Copy and paste the url in NS player or VLC media player in android and Autho iptv in pc to play stream</b>")

        try:
            sent = await client.send_message(
                chat_id,
                text=text, 
                disable_web_page_preview = False, 
                invert_media = True 
            )
            sent_msg_ids.append(sent.id)
        except Exception as e:
            print(f"Error sending message: {e}")

    willow_messages[chat_id] = sent_msg_ids

async def auto_send_w_loop(client, chat_id):
    while willow_status.get(chat_id, False):
        await send_w_live_matches(client, chat_id)
        await asyncio.sleep(1800)  # 30 minutes

@Client.on_message(filters.command("wtv") & filters.user(Rkn_Bots.ADMIN))
async def wtv_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage:\n/willow on [channel_id]\n/willow off [channel_id]")

    arg = message.command[1].lower()
    
    # Handle channel ID parameter
    if len(message.command) > 2 and message.command[2].lstrip('-').isdigit():
        chat_id = int(message.command[2])
    else:
        chat_id = message.chat.id

    if arg == "on":
        if willow_status.get(chat_id, False):
            await message.reply(f"Willow updates already active for {'this chat' if chat_id == message.chat.id else 'specified channel'}")
            return
        willow_status[chat_id] = True
        await message.reply(f"🚦 Willow live updates activated for {'this chat' if chat_id == message.chat.id else 'specified channel'}!\nUpdates every 30 minutes")
        asyncio.create_task(auto_send_w_loop(client, chat_id))

    elif arg == "off":
        if not willow_status.get(chat_id, False):
            await message.reply(f"Willow updates already inactive for {'this chat' if chat_id == message.chat.id else 'specified channel'}")
            return
        willow_status[chat_id] = False
        await message.reply(f"🚫 Willow updates stopped for {'this chat' if chat_id == message.chat.id else 'specified channel'}")
        if chat_id in willow_messages:
            for msg_id in willow_messages[chat_id]:
                try:
                    await client.delete_messages(chat_id, msg_id)
                except:
                    pass
            willow_messages.pop(chat_id)

    else:
        await message.reply("Invalid command. Use:\n/willow on [channel_id]\n/willow off [channel_id]")


SONYLIV_URL = "https://hgbotz.serv00.net/sliv.json"

@Client.on_message(filters.command("sonyliv") & filters.private)
async def sliv(client, message):
    try:
        async with httpx.AsyncClient() as http:
            response = await http.get("https://hgbotz.serv00.net/sliv.php")
            data = response.json()

        live_matches = [m for m in data.get("matches", []) if m.get("isLive")]

        if not live_matches:
            await message.reply("No live events currently on Sony LIV.")
            return

        for match in live_matches:
            # Collect all available servers
            servers = []
            for key in match:
                if key.startswith("Server"):
                    servers.append(f"🔗 {key}: {match[key]}")

            text = (f"<b>📺 {match['event']}</b>\n\n"
                    f"🏆 <b>Match:</b> {match['match']}\n"
                    f"📡 <b>Channel:</b> {match.get('TVchannel', 'N/A')}\n"
                    f"🎬 <b>Genre:</b> {match.get('genre', 'Sports')}\n"
                    f"🖥 <b>Quality:</b> {match.get('MaxResolution', 'HD')}\n\n"
                    f"<b>Available Streams:</b>\n" + "\n".join(servers) + "\n\n"
                    f"<b>Note: Copy and paste the url in NS player or VLC media player in android and Autho iptv in pc to play stream</b>")

            await message.reply_photo(
                photo=match['poster'],
                caption=text
            )

    except Exception as e:
        await message.reply(f"Fail to Fatch {e}")
        print(f"Sony LIV error: {e}")

SONYLIV_URL = "https://hgbotz.serv00.net/sliv.json"
sonyliv_status = {}  # chat_id: True/False
sonyliv_messages = {}  # chat_id: list of msg ids

async def fetch_sonyliv_live():
    async with httpx.AsyncClient() as http:
        resp = await http.get("https://hgbotz.serv00.net/sliv.php")
        data = resp.json()
    return [m for m in data.get("matches", []) if m.get("isLive")]

async def send_sonyliv_updates(client, chat_id):
    live_events = await fetch_sonyliv_live()
    
    # Delete old messages
    if chat_id in sonyliv_messages:
        for msg_id in sonyliv_messages[chat_id]:
            try:
                await client.delete_messages(chat_id, msg_id)
            except:
                pass

    sent_msg_ids = []
    for event in live_events:
        # Collect all server links
        servers = []
        for key in event:
            if key.startswith("Server"):
                servers.append(f"🌐 {key}: {event[key]}")
        
        text = (f"<b>🔴 LIVE: {event['event']}</b>\n\n"
                f"🏆 <b>Match:</b> {event['match']}\n"
                f"📡 <b>Channel:</b> {event.get('TVchannel', 'Sony LIV')}\n"
                f"🎬 <b>Genre:</b> {event.get('genre', 'Sports')}\n"
                f"🖥 <b>Quality:</b> {event.get('MaxResolution', 'HD')}\n\n"
                f"<b>Stream Links:</b>\n" + "\n".join(servers) + "\n\n"
                f"<b>Note: Copy and paste the url in NS player or VLC media player in android and Autho iptv in pc to play stream</b>")

        try:
            sent = await client.send_photo(
                chat_id,
                photo=event['poster'],
                caption=text
            )
            sent_msg_ids.append(sent.id)
        except Exception as e:
            print(f"Sony LIV send error: {e}")

    sonyliv_messages[chat_id] = sent_msg_ids

async def sonyliv_auto_loop(client, chat_id):
    while sonyliv_status.get(chat_id, False):
        await send_sonyliv_updates(client, chat_id)
        await asyncio.sleep(1800)  # 30 minutes

@Client.on_message(filters.command("sliv")  & filters.user(Rkn_Bots.ADMIN))
async def sonyliv_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage:\n/sonyliv on [channel_id]\n/sonyliv off [channel_id]")

    arg = message.command[1].lower()
    
    # Handle channel ID parameter
    if len(message.command) > 2 and message.command[2].lstrip('-').isdigit():
        chat_id = int(message.command[2])
    else:
        chat_id = message.chat.id

    if arg == "on":
        if sonyliv_status.get(chat_id, False):
            await message.reply(f"Sony LIV updates already active for {'this chat' if chat_id == message.chat.id else 'channel'}")
            return
        sonyliv_status[chat_id] = True
        await message.reply(f"🎬 Sony LIV LIVE updates activated for {'this chat' if chat_id == message.chat.id else 'channel'}!\nUpdates every 30 minutes")
        asyncio.create_task(sonyliv_auto_loop(client, chat_id))

    elif arg == "off":
        if not sonyliv_status.get(chat_id, False):
            await message.reply(f"Sony LIV updates already inactive for {'this chat' if chat_id == message.chat.id else 'channel'}")
            return
        sonyliv_status[chat_id] = False
        await message.reply(f"⏹ Sony LIV updates stopped for {'this chat' if chat_id == message.chat.id else 'channel'}")
        if chat_id in sonyliv_messages:
            for msg_id in sonyliv_messages[chat_id]:
                try:
                    await client.delete_messages(chat_id, msg_id)
                except:
                    pass
            sonyliv_messages.pop(chat_id)

    else:
        await message.reply("Invalid command. Use:\n/sonyliv on [channel_id]\n/sonyliv off [channel_id]")
