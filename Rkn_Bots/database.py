import motor.motor_asyncio
from config import Rkn_Bots

client = motor.motor_asyncio.AsyncIOMotorClient(Rkn_Bots.DB_URL)
db = client[Rkn_Bots.DB_NAME]
chnl_ids = db.chnl_ids
users = db.users
fancode_data = db.fancode_data  # New collection for fancode status and messages
sonyliv_data = db.sonyliv_data
willow_data = db.willow_data
# Insert user data
async def insert(user_id):
    user_det = {"_id": user_id}
    try:
        await users.insert_one(user_det)
    except:
        pass
        
# Total User
async def total_user():
    user = await users.count_documents({})
    return user

async def getid():
    all_users = users.find({})
    return all_users

async def delete(id):
    await users.delete_one(id)

# Fancode functions
async def get_fancode_status(chat_id):
    data = await fancode_data.find_one({"_id": chat_id})
    return data.get("status", False) if data else False

async def set_fancode_status(chat_id, status):
    await fancode_data.update_one(
        {"_id": chat_id},
        {"$set": {"status": status}},
        upsert=True
    )

async def get_fancode_messages(chat_id):
    data = await fancode_data.find_one({"_id": chat_id})
    return data.get("messages", []) if data else []

async def set_fancode_messages(chat_id, messages):
    await fancode_data.update_one(
        {"_id": chat_id},
        {"$set": {"messages": messages}},
        upsert=True
    )

async def delete_fancode_messages(chat_id):
    await fancode_data.update_one(
        {"_id": chat_id},
        {"$set": {"messages": []}},
        upsert=True
    )

# Add this to Database.py
async def get_active_fancode_chats():
    active_chats = []
    async for doc in fancode_data.find({"status": True}):  # Direct async iteration
        active_chats.append(doc["_id"])
    return active_chats



async def get_sonyliv_status(chat_id):
    data = await sonyliv_data.find_one({"_id": chat_id})
    return data.get("status", False) if data else False

async def set_sonyliv_status(chat_id, status):
    await sonyliv_data.update_one(
        {"_id": chat_id},
        {"$set": {"status": status}},
        upsert=True
    )

async def get_sonyliv_messages(chat_id):
    data = await sonyliv_data.find_one({"_id": chat_id})
    return data.get("messages", []) if data else []

async def set_sonyliv_messages(chat_id, messages):
    await sonyliv_data.update_one(
        {"_id": chat_id},
        {"$set": {"messages": messages}},
        upsert=True
    )

async def delete_sonyliv_messages(chat_id):
    await sonyliv_data.update_one(
        {"_id": chat_id},
        {"$set": {"messages": []}},
        upsert=True
    )

# Add this to Database.py
async def get_active_sonyliv_chats():
    active_chats = []
    async for doc in sonyliv_data.find({"status": True}):  # Direct async iteration
        active_chats.append(doc["_id"])
    return active_chats


async def get_willow_status(chat_id):
    data = await willow_data.find_one({"_id": chat_id})
    return data.get("status", False) if data else False

async def set_willow_status(chat_id, status):
    await willow_data.update_one(
        {"_id": chat_id},
        {"$set": {"status": status}},
        upsert=True
    )

async def get_willow_messages(chat_id):
    data = await willow_data.find_one({"_id": chat_id})
    return data.get("messages", []) if data else []

async def set_willow_messages(chat_id, messages):
    await willow_data.update_one(
        {"_id": chat_id},
        {"$set": {"messages": messages}},
        upsert=True
    )

async def delete_willow_messages(chat_id):
    await willow_data.update_one(
        {"_id": chat_id},
        {"$set": {"messages": []}},
        upsert=True
    )

# Add this to Database.py
async def get_active_willow_chats():
    active_chats = []
    async for doc in willow_data.find({"status": True}):  # Direct async iteration
        active_chats.append(doc["_id"])
    return active_chats

