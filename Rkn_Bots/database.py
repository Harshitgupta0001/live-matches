import motor.motor_asyncio
from config import Rkn_Bots

client = motor.motor_asyncio.AsyncIOMotorClient(Rkn_Bots.DB_URL)
db = client[Rkn_Bots.DB_NAME]
chnl_ids = db.chnl_ids
users = db.users
fancode_data = db.fancode_data  # New collection for fancode status and messages

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
    cursor = fancode_data.find({"status": True})
    active_chats = []
    async for doc in await cursor.to_list(length=None):
        active_chats.append(doc["_id"])
    return active_chats
