import requests, httpx
from pyrogram import Client, filters, errors, types
from config import Rkn_Bots, AUTH_CHANNEL
import asyncio, re, time, sys, random
from .database import total_user, getid, delete, insert, chnl_ids, get_fancode_status, set_fancode_status, get_fancode_messages, set_fancode_messages, delete_fancode_messages, get_active_fancode_chats, get_sonyliv_status, set_sonyliv_status, get_sonyliv_messages, set_sonyliv_messages, delete_sonyliv_messages, get_active_sonyliv_chats, get_active_willow_chats, delete_willow_messages, set_willow_messages, get_willow_messages, set_willow_status, get_willow_status
from pyrogram.errors import *
from pyrogram.types import *
from utils import react_msg 
from Script import script
import aiohttp

buttons = [[
        InlineKeyboardButton('✇ Movie Zone ✇', url="https://t.me/eera_Search_Zone"),
        InlineKeyboardButton('✨ Crick Zone ✨', url="https://t.me/CricDynasty")
    ],[
        InlineKeyboardButton('❗️ʜᴇʟᴘ', callback_data='help'), 
        InlineKeyboardButton('🦋 𝙰𝙱𝙾𝚄𝚃', callback_data='about')
    ]]


back_button = [[
                 InlineKeyboardButton('MOVIE ɢʀᴏᴜᴘ', url='https://t.me/Eera_Search_Zone'),
                 InlineKeyboardButton('crick ᴄʜᴀɴɴᴇʟ', url='https://telegram.me/CricDynasty')
              ],[
                 InlineKeyboardButton('🔙 back', callback_data='back')
              ]]

about_buttons = [[
        InlineKeyboardButton('Maintainer 🙂‍↔️', url='https://t.me/Harshit_contact_bot')
        ],[
        InlineKeyboardButton('❗️ʜᴇʟᴘ', callback_data='help'), 
        InlineKeyboardButton('🦋 𝙷𝙾𝙼𝙴', callback_data='back')
        ],[
        InlineKeyboardButton('❗️ Movie ɢʀᴏᴜᴘ', url='https://t.me/eera_Search_Zone'),
        InlineKeyboardButton('❗️ crick ᴄʜᴀɴɴᴇʟ', url='https://telegram.me/CricDynasty')
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
@Client.on_message(filters.command("start") & filters.private )
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
    await message.reply_text(
        text=script.START_TXT.format(message.from_user.mention),
        disable_web_page_preview = False, 
        invert_media = True, 
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
                f"<blockquote><b>Stream info </b>\n🌐 <b>Normal Stream:</b> {match['dai_url']}\n🚫 <b>Ad-Free Stream:</b> {match['adfree_url']}</blockquote>\n"
                f"<b>Note: Copy and paste the url in NS player or VLC media player to play stream</b>"
            )

            await message.reply_photo(photo=match['src'], caption=text)

    except Exception as e:
        await message.reply("Something went wrong while fetching Fancode data.")
        print(e)






FANCODE_URL = "https://raw.githubusercontent.com/drmlive/fancode-live-events/main/fancode.json"

async def fetch_f_live_matches():
    async with httpx.AsyncClient() as http:
        resp = await http.get(FANCODE_URL)
        data = resp.json()
    return [m for m in data.get("matches", []) if m.get("status") == "LIVE"]

async def send_f_live_matches(client, chat_id):
    live_matches = await fetch_f_live_matches()
    old_msg_ids = await get_fancode_messages(chat_id)
    
    # delete old messages
    for msg_id in old_msg_ids:
        try:
            await client.delete_messages(chat_id, msg_id)
        except:
            pass

    sent_msg_ids = []
    for match in live_matches:
        text = (f"<b>{match['match_name']} ({match['event_name']})</b>\n\n"
                f"🔴 <blockquote expandable <b>Provider: Fancode </b>\n"
                f"🏟 <b>Event:</b> {match['event_name']}\n"
                f"🕒 <b>Start Time:</b> {match['startTime']}\n"
                f"👥 <b>Teams:</b> {match['team_1']} vs {match['team_2']}</blockquote>\n"
                f"<blockquote expandable <b>Stream info </b>\n🌐 <b>Normal Stream:</b> {match['dai_url']}\n🚫 <b>Ad-Free Stream:</b> {match['adfree_url']}</blockquote>\n"
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

    await set_fancode_messages(chat_id, sent_msg_ids)

async def auto_send_f_loop(client, chat_id):
    while await get_fancode_status(chat_id):
        await send_f_live_matches(client, chat_id)
        await asyncio.sleep(1800)  # 30 minutes

# Add this function to initialize loops
async def init_fancode_loops(client):
    active_chats = await get_active_fancode_chats()
    for chat_id in active_chats:
        asyncio.create_task(auto_send_f_loop(client, chat_id))
        print(f"Restarted Fancode loop for chat {chat_id}")

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
        current_status = await get_fancode_status(chat_id)
        if current_status:
            await message.reply(f"Fancode auto updates are already ON for {'this chat' if chat_id == message.chat.id else 'the specified channel'}.")
            return
        await set_fancode_status(chat_id, True)
        await message.reply(f"Fancode auto updates started for {'this chat' if chat_id == message.chat.id else 'the specified channel'}. Updates every 30 minutes.")
        asyncio.create_task(auto_send_f_loop(client, chat_id))

    elif arg == "off":
        current_status = await get_fancode_status(chat_id)
        if not current_status:
            await message.reply(f"Fancode auto updates are already OFF for {'this chat' if chat_id == message.chat.id else 'the specified channel'}.")
            return
        await set_fancode_status(chat_id, False)
        await message.reply(f"Fancode auto updates stopped for {'this chat' if chat_id == message.chat.id else 'the specified channel'}.")
        # delete old messages
        old_msg_ids = await get_fancode_messages(chat_id)
        for msg_id in old_msg_ids:
            try:
                await client.delete_messages(chat_id, msg_id)
            except:
                pass
        await delete_fancode_messages(chat_id)

    else:
        await message.reply("Unknown option. Use:\n/fan on [channel_id]\n/fan off [channel_id]")




SONYLIV_URL = "https://terapi-git-main-hgbotz-s-projects.vercel.app"

@Client.on_message(filters.command("sonyliv") & filters.private)
async def sliv(client, message):
    try:
        async with httpx.AsyncClient() as http:
            response = await http.get(SONYLIV_URL)
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
                    f"<b>Provider: SONY LIV 🔴</b>\n"
                    f"🏆 <b>Match:</b> {match['match']}\n"
                    f"📡 <b>Channel:</b> {match.get('TVchannel', 'N/A')}\n"
                    f"🎬 <b>Genre:</b> {match.get('genre', 'Sports')}\n"
                    f"🖥 <b>Quality:</b> {match.get('MaxResolution', 'HD')}\n"
                    f"<blockquote expandable><b>Available Streams:</b>\n" + "\n".join(servers) + "\n\n</blockquote>"
                    f"<b>Note: Copy and paste the url in NS player or VLC media player in android and Autho iptv in pc to play stream</b>")

            await message.reply_photo(
                photo=match['poster'],
                caption=text
            )

    except Exception as e:
        await message.reply(f"Fail to Fatch {e}")
        print(f"Sony LIV error: {e}")



SONYLIV_URL = "https://terapi-git-main-hgbotz-s-projects.vercel.app"

async def fetch_sonyliv_live():
    async with httpx.AsyncClient() as http:
        resp = await http.get(SONYLIV_URL)
        data = resp.json()
    return [m for m in data.get("matches", []) if m.get("isLive")]

async def send_sonyliv_updates(client, chat_id):
    live_events = await fetch_sonyliv_live()
    old_msg_ids = await get_sonyliv_messages(chat_id)
    
    # Delete old messages
    for msg_id in old_msg_ids:
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
                f"<b>Provider: SONY LIV🔴</b>\n"
                f"🏆 <b>Match:</b> {event['match']}\n"
                f"📡 <b>Channel:</b> {event.get('TVchannel', 'Sony LIV')}\n"
                f"🎬 <b>Genre:</b> {event.get('genre', 'Sports')}\n"
                f"🖥 <b>Quality:</b> {event.get('MaxResolution', 'HD')}\n"
                f"<blockquote expandable><b>Stream Links:</b>\n" + "\n".join(servers) + "\n\n</blockquote>"
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

    await set_sonyliv_messages(chat_id, sent_msg_ids)

async def sonyliv_auto_loop(client, chat_id):
    while await get_sonyliv_status(chat_id):
        await send_sonyliv_updates(client, chat_id)
        await asyncio.sleep(1800)  # 30 minutes

async def init_sonyliv_loops(client):
    active_chats = await get_active_sonyliv_chats()
    for chat_id in active_chats:
        asyncio.create_task(sonyliv_auto_loop(client, chat_id))
        print(f"♻️ Restarted Sony LIV updates for chat {chat_id}")

@Client.on_message(filters.command("sliv") & filters.user(Rkn_Bots.ADMIN))
async def sonyliv_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage:\n/sliv on [channel_id]\n/sliv off [channel_id]")

    arg = message.command[1].lower()
    
    # Handle channel ID parameter
    if len(message.command) > 2 and message.command[2].lstrip('-').isdigit():
        chat_id = int(message.command[2])
    else:
        chat_id = message.chat.id

    if arg == "on":
        current_status = await get_sonyliv_status(chat_id)
        if current_status:
            await message.reply(f"Sony LIV updates already active for {'this chat' if chat_id == message.chat.id else 'channel'}")
            return
        await set_sonyliv_status(chat_id, True)
        await message.reply(f"🎬 Sony LIV LIVE updates activated for {'this chat' if chat_id == message.chat.id else 'channel'}!\nUpdates every 30 minutes")
        asyncio.create_task(sonyliv_auto_loop(client, chat_id))

    elif arg == "off":
        current_status = await get_sonyliv_status(chat_id)
        if not current_status:
            await message.reply(f"Sony LIV updates already inactive for {'this chat' if chat_id == message.chat.id else 'channel'}")
            return
        await set_sonyliv_status(chat_id, False)
        await message.reply(f"⏹ Sony LIV updates stopped for {'this chat' if chat_id == message.chat.id else 'channel'}")
        
        # Delete old messages
        old_msg_ids = await get_sonyliv_messages(chat_id)
        for msg_id in old_msg_ids:
            try:
                await client.delete_messages(chat_id, msg_id)
            except:
                pass
        await delete_sonyliv_messages(chat_id)

    else:
        await message.reply("Invalid command. Use:\n/sliv on [channel_id]\n/sliv off [channel_id]")


WILLOW_URL = "https://raw.githubusercontent.com/drmlive/willow-live-events/main/willow.json"

@Client.on_message(filters.command("willow") & filters.private)
async def willow_handler(client, message):
    try:
        async with httpx.AsyncClient() as http:
            response = await http.get(WILLOW_URL)
            data = response.json()

        live_matches = data.get("matches", []) 

        if not live_matches:
            await message.reply("No live matches currently on Willow TV.")
            return

        for match in live_matches:
            # Extract teams from title
            teams = match['title'].split('vs')
            team1 = teams[0].split('-')[-1].strip() if len(teams) > 0 else "Team 1"
            team2 = teams[1].split('-')[0].strip() if len(teams) > 1 else "Team 2"
            
            # Format DRM URLs with keys
            drm_streams = []
            playback_data = match.get('playback_data', {})
            
            for url in playback_data.get('urls', []):
                for key in playback_data.get('keys', []):
                    drm_url = f"{url['url']}?|drmScheme=clearkey&drmLicense={key}"
                    drm_streams.append(f"🌐 {url['cdn']}: <code>{drm_url}</code>")

            text = (f"<a href='{match['cover']}'>ㅤ</a><b>{match['title']}</b>\n\n"
                    f"<b>Provider: Willow Tv 🔴</b>\n"
                    f"🏆 <b>Event Type:</b> {match.get('contentType', 'Cricket Match')}\n"
                    f"🕒 <b>Start Time:</b> {match['startTime']}\n"
                    f"👥 <b>Teams:</b> {team1} vs {team2}\n"
                    f"<blockquote expandable><b>DRM Stream URLs:</b>\n" + "\n".join(drm_streams) + "\n\n</blockquote>"
                    f"<b>Note: Copy and paste the url in NS player or VLC media player in android and Autho iptv in pc to play stream</b>")

            await message.reply_text(
                
                text=text,
                disable_web_page_preview =False, 
                invert_media =True 
            )

    except httpx.HTTPError:
        await message.reply("⚠️ Couldn't connect to Willow TV servers. Try again later.")
    except json.JSONDecodeError:
        await message.reply("⚠️ Invalid data received from Willow TV.")
    except Exception as e:
        await message.reply("❌ Error fetching match data.")
        print(f"Willow TV error: {e}")






WILLOW_URL = "https://raw.githubusercontent.com/drmlive/willow-live-events/main/willow.json"

async def fetch_w_live_matches():
    async with httpx.AsyncClient() as http:
        resp = await http.get(WILLOW_URL)
        data = resp.json()
    return data.get("matches", [])

async def send_w_live_matches(client, chat_id):
    live_matches = await fetch_w_live_matches()
    old_msg_ids = await get_willow_messages(chat_id)
    
    # Delete old messages
    for msg_id in old_msg_ids:
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
        
        # Format DRM URLs with keys
        drm_streams = []
        playback_data = match.get('playback_data', {})
            
        for url in playback_data.get('urls', []):
            for key in playback_data.get('keys', []):
                drm_url = f"{url['url']}?|drmScheme=clearkey&drmLicense={key}"
                drm_streams.append(f"🌐 {url['cdn']}: <code>{drm_url}</code>")

        text = (f"<a href='{match['cover']}'>ㅤ</a><b>{match['title']}</b>\n\n"
                f"<b>Provider: Willow Tv 🔴</b>\n"
                f"🏆 <b>Event Type:</b> {match.get('contentType', 'Cricket Match')}\n"
                f"🕒 <b>Start Time:</b> {match['startTime']}\n"
                f"👥 <b>Teams:</b> {team1} vs {team2}\n"
                f"<blockquote expandable><b>DRM Stream URLs:</b>\n" + "\n".join(drm_streams) + "\n\n</blockquote>"
                f"<b>Note: Copy and paste the url in NS player or VLC media player in android and Autho iptv in pc to play stream</b>")

        try:
            sent = await client.send_message(
                chat_id,
                text=text, 
                disable_web_page_preview=False, 
                invert_media=True
            )
            sent_msg_ids.append(sent.id)
        except Exception as e:
            print(f"Willow TV send error: {e}")

    await set_willow_messages(chat_id, sent_msg_ids)

async def auto_send_w_loop(client, chat_id):
    while await get_willow_status(chat_id):
        await send_w_live_matches(client, chat_id)
        await asyncio.sleep(1800)  # 30 minutes

async def init_willow_loops(client):
    active_chats = await get_active_willow_chats()
    for chat_id in active_chats:
        asyncio.create_task(auto_send_w_loop(client, chat_id))
        print(f"♻️ Restarted Willow TV updates for chat {chat_id}")

@Client.on_message(filters.command("willowtv") & filters.user(Rkn_Bots.ADMIN))
async def willow_tv_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage:\n/willowtv on [channel_id]\n/willowtv off [channel_id]")

    arg = message.command[1].lower()
    
    # Handle channel ID parameter
    if len(message.command) > 2 and message.command[2].lstrip('-').isdigit():
        chat_id = int(message.command[2])
    else:
        chat_id = message.chat.id

    if arg == "on":
        current_status = await get_willow_status(chat_id)
        if current_status:
            await message.reply(f"Willow updates already active for {'this chat' if chat_id == message.chat.id else 'specified channel'}")
            return
        await set_willow_status(chat_id, True)
        await message.reply(f"🚦 Willow live updates activated for {'this chat' if chat_id == message.chat.id else 'specified channel'}!\nUpdates every 30 minutes")
        asyncio.create_task(auto_send_w_loop(client, chat_id))

    elif arg == "off":
        current_status = await get_willow_status(chat_id)
        if not current_status:
            await message.reply(f"Willow updates already inactive for {'this chat' if chat_id == message.chat.id else 'specified channel'}")
            return
        await set_willow_status(chat_id, False)
        await message.reply(f"🚫 Willow updates stopped for {'this chat' if chat_id == message.chat.id else 'specified channel'}")
        
        # Delete old messages
        old_msg_ids = await get_willow_messages(chat_id)
        for msg_id in old_msg_ids:
            try:
                await client.delete_messages(chat_id, msg_id)
            except:
                pass
        await delete_willow_messages(chat_id)

    else:
        await message.reply("Invalid command. Use:\n/willowtv on [channel_id]\n/willowtv off [channel_id]")



@Client.on_callback_query(filters.regex('help'))
async def show_help_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()  # Acknowledge the callback
    await callback_query.message.edit_text(text=script.HELP_TXT, disable_web_page_preview=False, invert_media=True, reply_markup=InlineKeyboardMarkup(back_button))

@Client.on_callback_query(filters.regex('back'))
async def back_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()  # Acknowledge the callback
    await callback_query.message.edit_text(text=script.HOME_TXT, disable_web_page_preview=False, invert_media=True, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex('about'))
async def about_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()# Acknowledge the callback
    await callback_query.message.edit_text(text=script.ABOUT_TXT, disable_web_page_preview=False, invert_media=True, reply_markup=InlineKeyboardMarkup(about_buttons))
