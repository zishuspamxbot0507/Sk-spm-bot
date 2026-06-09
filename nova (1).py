#!/usr/bin/env python3
"""
███╗   ██╗ ██████╗ ██╗   ██╗ █████╗     ██╗   ██╗ ██╗
████╗  ██║██╔═══██╗██║   ██║██╔══██╗    ██║   ██║███║
██╔██╗ ██║██║   ██║██║   ██║███████║    ██║   ██║╚██║
██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║    ╚██╗ ██╔╝ ██║
██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║     ╚████╔╝  ██║
╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝      ╚═══╝   ╚═╝
                  🔥 RUDRA GOD - REBORN EDITION 🔥
"""

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import asyncio
import json
import os
import glob
import random
import logging
import requests
from io import BytesIO
from typing import Dict, List, Set
from telethon import TelegramClient, events, functions
from telethon.tl.functions.channels import InviteToChannelRequest, EditAdminRequest, EditBannedRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.types import ChatAdminRights, InputPeerUser, ChatBannedRights
from telethon.errors import FloodWaitError
import time
from datetime import datetime, timedelta

try:
    import yt_dlp
    YTDLP_AVAILABLE = True
except ImportError:
    YTDLP_AVAILABLE = False

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

# ==================== CONFIG ====================
API_ID = YOUR API IS
API_HASH = 'YOUR API HASH'
PHONE = '+91YOURNUMBER'

BOT_TOKENS = [ "BOT TOKEN"
]

OWNER_ID = YOUR ID
ANTHROPIC_API_KEY = ""
AI_MODEL = "claude-3-5-haiku-20241022"
USE_LOCAL_AI = True
LOCAL_MODEL_NAME = "gpt2"
SAVAGE_MODE = True
ROAST_INTENSITY = "high"

SAVED_BOTS = [
   'rudrancx1bot',
'rudrancx2bot',
'rudrancx3bot',
'rudrancx4bot',
'rudrancx5bot',
'rudrancx6bot',
'rudrancx7bot',
'rudrancx8bot',
'rudrancx9bot',
'rudrancx10bot',
'rudrancx11bot',
]


SAFE_USERS_FILE   = "safe_users.json"
AUTO_DELETE_FILE  = "auto_delete.json"
DELETE_USERS_FILE = "delete_users.json"
SLIDE_MSGS_FILE   = "slide_messages.json"
GHOST_FILE        = "ghost_list.json"
MUSIC_FOLDER      = "music_downloads"

if not os.path.exists(MUSIC_FOLDER):
    os.makedirs(MUSIC_FOLDER)

NOVA_EMOJIS  = ["⚡", "🔥", "💀", "👑", "⭐", "✨", "💎", "🎯", "🚀", "💥"]
MUSIC_EMOJIS = ["🎵", "🎶", "🎼", "🎹", "🎸", "🎺", "🎷", "🥁", "🎤", "🎧"]

# ==================== DEFAULT SLIDE MESSAGES ====================
DEFAULT_SLIDE_MSGS = [
"𝐓ᴇʀɪ ᴍᴀ ᴋᴀ ᴄʜᴜᴅᴀɪ ʙᴀᴄʜᴀʟᴇ ʜɪɴᴊᴅᴇ 🤣🦧",
"𝐓ᴇʀɪ ᴍᴀ ᴋᴀ ʙʜᴏsᴅᴀ ᴍᴇ ʜᴀᴀᴛʜ ᴅᴀʟᴅᴜɴɢᴀ",
"𝐉ᴀʏᴅᴀ ʙᴏʟᴇɢᴀ ᴛᴇʀɪ ᴍᴀ ᴍᴀʀᴅᴜ",
"𝑻ᴇʀɪ ᴍᴀ ᴋɪ ᴄʜᴜᴛ ᴍᴇ ᴘᴏᴛᴛʏ ᴋʀᴅᴜɴɢᴀ",
"𝑨𝑩𝑬 𝑯𝑰𝑱𝑫𝑰 𝑴𝑨 𝑲𝑨 𝑳𝑨𝑹𝑲𝑬 ᴛᴇʀᴀ ʙᴀᴘ ᴜᴅʜᴇʀ 𝐑ᴏᴀᴅ ᴘᴇ ʜᴀɪ 𝐓ᴜ ɪᴅʜᴇʀ ғʏᴛᴇʀ ʙᴀɴᴇɢᴀ"
"RUDRA ʙᴀᴘ ʙᴏʟ 𝐂ʜᴍʀ 🇦🇱🖤",
"𝐂ʜᴜᴅ ᴍᴀᴛ ᴄʜᴀᴍʀ ʟᴀʀᴋᴇ ᴛᴇʀɪ ᴍᴀ ʙʜɪ ғʏᴛʀ ᴛʜɪ ɴᴀ😘"
"𝐓ʀɪ ᴍᴀ ᴋᴏ ᴅɪʟ sᴇ 𝐈 ʟᴏᴠᴇ 𝒀𝒐𝒖"
]

# ==================== STATE ====================
class CoreState:
    def __init__(self):
        self.safe_users: Set[int] = set()
        self.safe_usernames: Dict[str, int] = {}
        self.auto_delete_chats: Dict[int, bool] = {}
        self.delete_target_users: Dict[int, Set[int]] = {}
        self.delete_target_usernames: Dict[int, Set[str]] = {}
        self.delete_delay = 0.05

        self.swipe_active: Dict[int, str] = {}
        self.spam_active: Dict[int, str] = {}

        self.ai_chat_active: Dict[int, bool] = {}
        self.ai_chat_history: Dict[int, List] = {}

        self.local_model = None
        self.local_tokenizer = None

        self.copied_mode: Dict[int, Dict] = {}
        self.original_name: str = None
        self.original_photo: any = None

        self.downloading_music: Dict[int, bool] = {}

        # Slide messages (saved by user)
        self.slide_messages: List[str] = []

        # Target slide: {chat_id: {target_user_id: active bool}}
        self.slide_targets: Dict[int, Dict[int, bool]] = {}

        # Ghost mode: hide read receipts + auto-seen
        self.ghost_mode: bool = False

        # Inline AFK
        self.afk_mode: bool = False
        self.afk_reason: str = ""
        self.afk_start: float = 0.0

        # Message logger: log mentions/replies to saved messages
        self.log_mentions: bool = False

        # Bulk delete count tracker
        self.bulk_delete_count: Dict[int, int] = {}

        self.load_local_model()
        self.load_all()

    # ──────────── LOADERS ────────────
    def load_all(self):
        self._load_safe()
        self._load_auto_delete()
        self._load_delete_targets()
        self._load_slide_msgs()
        self._load_ghost()

    def _load_safe(self):
        try:
            if os.path.exists(SAFE_USERS_FILE):
                with open(SAFE_USERS_FILE) as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.safe_users = set(data.get("user_ids", []))
                        self.safe_usernames = data.get("usernames", {})
                    else:
                        self.safe_users = set(data)
        except: pass

    def _load_auto_delete(self):
        try:
            if os.path.exists(AUTO_DELETE_FILE):
                with open(AUTO_DELETE_FILE) as f:
                    data = json.load(f)
                    self.auto_delete_chats = {int(k): v for k, v in data.items()}
        except: pass

    def _load_delete_targets(self):
        try:
            if os.path.exists(DELETE_USERS_FILE):
                with open(DELETE_USERS_FILE) as f:
                    data = json.load(f)
                    self.delete_target_users = {int(k): set(v.get("user_ids", [])) for k, v in data.items()}
                    self.delete_target_usernames = {int(k): set(v.get("usernames", [])) for k, v in data.items()}
        except: pass

    def _load_slide_msgs(self):
        try:
            if os.path.exists(SLIDE_MSGS_FILE):
                with open(SLIDE_MSGS_FILE) as f:
                    self.slide_messages = json.load(f)
            else:
                self.slide_messages = list(DEFAULT_SLIDE_MSGS)
        except:
            self.slide_messages = list(DEFAULT_SLIDE_MSGS)

    def _load_ghost(self):
        try:
            if os.path.exists(GHOST_FILE):
                with open(GHOST_FILE) as f:
                    data = json.load(f)
                    self.ghost_mode = data.get("ghost", False)
        except: pass

    # ──────────── SAVERS ────────────
    def save_safe_users(self):
        try:
            with open(SAFE_USERS_FILE, "w") as f:
                json.dump({"user_ids": list(self.safe_users), "usernames": self.safe_usernames}, f)
        except: pass

    def save_auto_delete(self):
        try:
            with open(AUTO_DELETE_FILE, "w") as f:
                json.dump(self.auto_delete_chats, f)
        except: pass

    def save_delete_targets(self):
        try:
            data = {}
            for cid in self.delete_target_users:
                data[str(cid)] = {
                    "user_ids": list(self.delete_target_users.get(cid, set())),
                    "usernames": list(self.delete_target_usernames.get(cid, set()))
                }
            with open(DELETE_USERS_FILE, "w") as f:
                json.dump(data, f)
        except: pass

    def save_slide_msgs(self):
        try:
            with open(SLIDE_MSGS_FILE, "w") as f:
                json.dump(self.slide_messages, f, ensure_ascii=False)
        except: pass

    def save_ghost(self):
        try:
            with open(GHOST_FILE, "w") as f:
                json.dump({"ghost": self.ghost_mode}, f)
        except: pass

    # ──────────── HELPERS ────────────
    def load_local_model(self):
        if not USE_LOCAL_AI or not TRANSFORMERS_AVAILABLE:
            return
        try:
            self.local_tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_NAME)
            self.local_model = AutoModelForCausalLM.from_pretrained(LOCAL_MODEL_NAME)
            if self.local_tokenizer.pad_token is None:
                self.local_tokenizer.pad_token = self.local_tokenizer.eos_token
        except Exception as e:
            print(f"[AI] Model load failed: {e}")

    def add_safe_user(self, user_id: int, username: str = None):
        self.safe_users.add(user_id)
        if username:
            self.safe_usernames[username.lower()] = user_id
        self.save_safe_users()

    def is_user_safe(self, user_id: int, username: str = None) -> bool:
        if user_id in self.safe_users:
            return True
        if username and username.lower() in self.safe_usernames:
            return True
        return False

    def add_delete_target(self, chat_id: int, user_id: int, username: str = None):
        self.delete_target_users.setdefault(chat_id, set()).add(user_id)
        self.delete_target_usernames.setdefault(chat_id, set())
        if username:
            self.delete_target_usernames[chat_id].add(username.lower())
        self.save_delete_targets()

    def should_delete_user(self, chat_id: int, user_id: int, username: str = None) -> bool:
        if chat_id not in self.delete_target_users:
            return False
        if user_id in self.delete_target_users[chat_id]:
            return True
        if username and chat_id in self.delete_target_usernames:
            if username.lower() in self.delete_target_usernames[chat_id]:
                return True
        return False

    def get_random_slide_msg(self) -> str:
        msgs = self.slide_messages if self.slide_messages else DEFAULT_SLIDE_MSGS
        return random.choice(msgs)

state = CoreState()

# ==================== CLIENT ====================
client = TelegramClient('nova_god_session', API_ID, API_HASH)

# ==================== AI FUNCTIONS ====================
def get_savage_response(message: str) -> str:
    pool = {
        "mild":    ["That's... a choice 😅", "Not your best moment.", "I've seen better."],
        "medium":  ["Did you really just say that? 💀", "Your brain on airplane mode?", "I'd roast you but you're already burnt."],
        "high":    ["Bro think he's smart 😭💀", "Delete this immediately.", "This is why nobody takes you seriously.", "Go touch grass, seriously."],
        "extreme": ["You're proof evolution can go backwards.", "Your birth certificate is an apology letter.", "When you disappear, it's a beautiful day."]
    }
    intensity = ROAST_INTENSITY if SAVAGE_MODE else "mild"
    return random.choice(pool.get(intensity, pool["mild"]))

async def get_ai_response(message: str, chat_id: int) -> str:
    if USE_LOCAL_AI and state.local_model and state.local_tokenizer:
        try:
            state.ai_chat_history.setdefault(chat_id, []).append(message)
            ctx = state.ai_chat_history[chat_id][-5:]
            prompt = "\n".join(ctx) + "\n"
            inputs = state.local_tokenizer.encode(prompt, return_tensors="pt")
            outputs = state.local_model.generate(
                inputs, max_length=inputs.shape[1]+50,
                num_return_sequences=1, temperature=0.8,
                do_sample=True, pad_token_id=state.local_tokenizer.eos_token_id
            )
            resp = state.local_tokenizer.decode(outputs[0], skip_special_tokens=True)[len(prompt):].strip()
            state.ai_chat_history[chat_id].append(resp)
            return resp if resp else "🤔 Hmm..."
        except Exception as e:
            return "🤖 Brain.exe stopped working"

    if ANTHROPIC_API_KEY:
        try:
            headers = {"x-api-key": ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"}
            state.ai_chat_history.setdefault(chat_id, [])
            msgs = [{"role": "user" if i%2==0 else "assistant", "content": m}
                    for i, m in enumerate(state.ai_chat_history[chat_id][-10:])]
            msgs.append({"role": "user", "content": message})
            r = requests.post("https://api.anthropic.com/v1/messages", headers=headers,
                              json={"model": AI_MODEL, "max_tokens": 200, "messages": msgs}, timeout=10)
            if r.status_code == 200:
                reply = r.json()["content"][0]["text"]
                state.ai_chat_history[chat_id] += [message, reply]
                return reply
        except: pass
    return "🤖 AI not configured"

# ==================== AUTO-DELETE ====================
@client.on(events.NewMessage(incoming=True))
async def _auto_del(event):
    cid = event.chat_id
    if not state.auto_delete_chats.get(cid, False): return
    sender = await event.get_sender()
    if not sender: return
    uid, uname = sender.id, getattr(sender, 'username', None)
    if state.is_user_safe(uid, uname): return
    if state.should_delete_user(cid, uid, uname):
        try:
            await asyncio.sleep(state.delete_delay)
            await event.delete()
        except: pass

# ==================== AI CHAT ====================
@client.on(events.NewMessage(incoming=True))
async def _ai_chat(event):
    cid = event.chat_id
    if not state.ai_chat_active.get(cid, False): return
    msg = event.text
    if not msg: return
    abusive = any(w in msg.lower() for w in ["stupid","dumb","idiot","useless","trash","noob","bot"])
    try:
        resp = get_savage_response(msg) if (SAVAGE_MODE and abusive) else await get_ai_response(msg, cid)
        await event.reply(resp)
    except: pass

# ==================== AUTO-REPLY ====================
@client.on(events.NewMessage(incoming=True))
async def _autoreply(event):
    cid = event.chat_id
    if cid in state.swipe_active:
        try: await event.reply(state.swipe_active[cid])
        except: pass

# ==================== AFK AUTO-NOTIFIER ====================
@client.on(events.NewMessage(incoming=True))
async def _afk_notifier(event):
    if not state.afk_mode: return
    if not event.is_private and not event.mentioned: return
    sender = await event.get_sender()
    if not sender: return
    elapsed = int(time.time() - state.afk_start)
    mins, secs = divmod(elapsed, 60)
    reason = f" — *{state.afk_reason}*" if state.afk_reason else ""
    try:
        await event.reply(
            f"😴 **I'm AFK right now{reason}**\n"
            f"⏱️ Away for: `{mins}m {secs}s`\n"
            f"I'll reply when I'm back 💤"
        )
    except: pass

# ==================== TARGET SLIDE HANDLER ====================
@client.on(events.NewMessage(incoming=True))
async def _slide_handler(event):
    """Auto-slide savage messages at targeted users"""
    cid = event.chat_id
    if cid not in state.slide_targets: return
    sender = await event.get_sender()
    if not sender: return
    uid = sender.id
    if uid not in state.slide_targets[cid]: return
    if not state.slide_targets[cid][uid]: return
    try:
        msg = state.get_random_slide_msg()
        await event.reply(msg)
        await asyncio.sleep(random.uniform(0.8, 2.2))  # human-like delay
    except: pass

# ==================== COMMANDS ====================

# ─── TARGET SLIDE ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.targetslide(?:\s+(.+))?'))
async def targetslide_cmd(event):
    """
    .targetslide <reply> [custom text]
    Reply to a user's message. The bot will auto-slide
    every message they send in this chat with either the
    custom text or a random saved slide message.
    """
    if not event.is_reply:
        await event.respond(
            "❌ **Reply to someone's message!**\n\n"
            "**Usage:** `.targetslide` (reply) — uses random saved slide msg\n"
            "**Usage:** `.targetslide <text>` — uses your custom text"
        )
        return

    args = event.pattern_match.group(1)
    reply_msg = await event.get_reply_message()
    target = await reply_msg.get_sender()
    cid = event.chat_id

    state.slide_targets.setdefault(cid, {})[target.id] = True

    # If custom text provided, add it temporarily to the front of the pool
    if args and args.strip():
        custom = args.strip()
        if custom not in state.slide_messages:
            state.slide_messages.insert(0, custom)
            state.save_slide_msgs()

    name = getattr(target, 'first_name', None) or getattr(target, 'username', 'Unknown')
    await event.delete()
    await event.respond(
        f"🎯 **SLIDE MODE ACTIVATED**\n"
        f"👤 Target: **{name}**\n"
        f"💬 Every message they send will get slid 🔥"
    )

@client.on(events.NewMessage(outgoing=True, pattern=r'\.unslide'))
async def unslide_cmd(event):
    """Stop sliding a targeted user"""
    if not event.is_reply:
        await event.respond("❌ **Reply to the user you want to stop sliding!**")
        return
    reply_msg = await event.get_reply_message()
    target = await reply_msg.get_sender()
    cid = event.chat_id
    if cid in state.slide_targets and target.id in state.slide_targets[cid]:
        state.slide_targets[cid][target.id] = False
    name = getattr(target, 'first_name', None) or "User"
    await event.delete()
    await event.respond(f"✅ **{name} is no longer being slid.**")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.unslideall'))
async def unslideall_cmd(event):
    """Stop sliding everyone in this chat"""
    cid = event.chat_id
    if cid in state.slide_targets:
        state.slide_targets[cid] = {}
    await event.respond("✅ **All slide targets cleared in this chat.**")

# ─── SLIDE MESSAGE MANAGER ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.addslide (.+)'))
async def addslide_cmd(event):
    """Add a message to the slide pool"""
    msg = event.pattern_match.group(1).strip()
    if msg not in state.slide_messages:
        state.slide_messages.append(msg)
        state.save_slide_msgs()
        await event.respond(f"✅ **Slide message added!**\nTotal: `{len(state.slide_messages)}`")
    else:
        await event.respond("⚠️ **That message is already in the pool!**")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.slidelist'))
async def slidelist_cmd(event):
    """View all saved slide messages"""
    if not state.slide_messages:
        await event.respond("📭 **No slide messages saved yet!**\nUse `.addslide <text>` to add some.")
        return
    lines = [f"`{i+1}.` {m}" for i, m in enumerate(state.slide_messages)]
    await event.respond(f"📋 **SLIDE MESSAGES [{len(lines)}]:**\n\n" + "\n".join(lines))

@client.on(events.NewMessage(outgoing=True, pattern=r'\.clearslides'))
async def clearslides_cmd(event):
    """Reset slide messages to default"""
    state.slide_messages = list(DEFAULT_SLIDE_MSGS)
    state.save_slide_msgs()
    await event.respond("🔄 **Slide messages reset to default!**")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.rmslide (\d+)'))
async def rmslide_cmd(event):
    """Remove a slide message by number"""
    idx = int(event.pattern_match.group(1)) - 1
    if 0 <= idx < len(state.slide_messages):
        removed = state.slide_messages.pop(idx)
        state.save_slide_msgs()
        await event.respond(f"🗑️ **Removed:** `{removed}`")
    else:
        await event.respond(f"❌ **Invalid number!** Use `.slidelist` to see valid numbers.")

# ─── AFK SYSTEM ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.afk(?:\s+(.+))?'))
async def afk_cmd(event):
    args = event.pattern_match.group(1)
    state.afk_mode = True
    state.afk_reason = args.strip() if args else ""
    state.afk_start = time.time()
    reason_text = f" | Reason: *{state.afk_reason}*" if state.afk_reason else ""
    await event.respond(f"😴 **AFK MODE ON**{reason_text}\nI'll auto-notify anyone who pings me 💤")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.back'))
async def back_cmd(event):
    if not state.afk_mode:
        await event.respond("✅ **You weren't AFK!**")
        return
    elapsed = int(time.time() - state.afk_start)
    mins, secs = divmod(elapsed, 60)
    state.afk_mode = False
    state.afk_reason = ""
    await event.respond(f"👋 **Welcome back!**\n⏱️ You were AFK for `{mins}m {secs}s`")

# ─── GHOST MODE ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.ghost'))
async def ghost_cmd(event):
    state.ghost_mode = not state.ghost_mode
    state.save_ghost()
    status = "ON 👻" if state.ghost_mode else "OFF"
    await event.respond(f"👻 **GHOST MODE: {status}**\n{'Read receipts suppressed.' if state.ghost_mode else 'Back to normal.'}")

# ─── BULK CLEAR (delete your own msgs) ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.purge (\d+)'))
async def purge_cmd(event):
    """Delete your last N messages in this chat"""
    count = int(event.pattern_match.group(1))
    deleted = 0
    async for msg in client.iter_messages(event.chat_id, limit=count+20, from_user='me'):
        try:
            await msg.delete()
            deleted += 1
            if deleted >= count: break
            await asyncio.sleep(0.1)
        except: pass
    note = await event.respond(f"🗑️ **Purged {deleted} messages!**")
    await asyncio.sleep(3)
    try: await note.delete()
    except: pass

# ─── FAKE TYPING ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.faketyping (\d+)'))
async def faketyping_cmd(event):
    """Show typing action for N seconds"""
    secs = min(int(event.pattern_match.group(1)), 60)
    await event.delete()
    async with client.action(event.chat_id, 'typing'):
        await asyncio.sleep(secs)

# ─── INFO CARD ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.info'))
async def info_cmd(event):
    """Get detailed info card of a user"""
    if not event.is_reply:
        await event.respond("❌ **Reply to a user to get their info!**")
        return
    reply_msg = await event.get_reply_message()
    u = await reply_msg.get_sender()
    premium = "✅ Yes" if getattr(u, 'premium', False) else "❌ No"
    bot_flag = "🤖 Yes" if getattr(u, 'bot', False) else "👤 No"
    verified = "✅" if getattr(u, 'verified', False) else "❌"
    info = (
        f"╔══════════════════════════╗\n"
        f"      📋 USER INFO CARD\n"
        f"╚══════════════════════════╝\n\n"
        f"👤 **Name:** {u.first_name or ''} {u.last_name or ''}\n"
        f"🔖 **Username:** @{u.username or 'None'}\n"
        f"🆔 **ID:** `{u.id}`\n"
        f"💎 **Premium:** {premium}\n"
        f"🤖 **Bot:** {bot_flag}\n"
        f"✅ **Verified:** {verified}\n"
        f"🔗 **Link:** tg://user?id={u.id}"
    )
    await event.respond(info)

# ─── TAG ALL ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.tagall(?:\s+(.+))?'))
async def tagall_cmd(event):
    """Tag every member in the group"""
    args = event.pattern_match.group(1)
    msg = args.strip() if args else "👋 Hey everyone!"
    await event.delete()
    members = []
    async for user in client.iter_participants(event.chat_id):
        if not user.bot:
            members.append(user)

    chunk_size = 5
    for i in range(0, len(members), chunk_size):
        chunk = members[i:i+chunk_size]
        mentions = " ".join([f"[​](tg://user?id={u.id})" for u in chunk])
        try:
            await client.send_message(event.chat_id, f"{msg} {mentions}")
            await asyncio.sleep(1)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)

# ─── MESSAGE STEALER ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.steal'))
async def steal_cmd(event):
    """Forward replied message to saved messages"""
    if not event.is_reply:
        await event.respond("❌ **Reply to a message to steal it!**")
        return
    reply_msg = await event.get_reply_message()
    await reply_msg.forward_to('me')
    await event.respond("📥 **Message stolen to Saved Messages!** ✅")

# ─── COUNTDOWN ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.countdown (\d+)'))
async def countdown_cmd(event):
    """Send a live countdown"""
    secs = min(int(event.pattern_match.group(1)), 60)
    await event.delete()
    msg = await client.send_message(event.chat_id, f"⏳ **Countdown: {secs}**")
    for i in range(secs - 1, -1, -1):
        await asyncio.sleep(1)
        try:
            if i == 0:
                await msg.edit("?? **BOOM! Time's up!**")
            else:
                await msg.edit(f"⏳ **Countdown: {i}**")
        except: pass

# ─── BOT MANAGEMENT ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.invite'))
async def invite_cmd(event):
    chat = await event.get_chat()
    await event.delete()
    added = failed = 0
    st = await event.respond(f"⚡ **RUDRA GOD | Adding {len(SAVED_BOTS)} bots...**")
    for b in SAVED_BOTS:
        try:
            be = await client.get_entity(b)
            await client(InviteToChannelRequest(chat, [be]))
            added += 1
            await st.edit(f"✅ **ADDED:** {added}/{len(SAVED_BOTS)} 🔥")
            await asyncio.sleep(2)
        except: failed += 1
    await st.edit(f"💥 **COMPLETE!** Added: {added} | Failed: {failed} ⚡")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.promote'))
async def promote_cmd(event):
    chat = await event.get_chat()
    await event.delete()
    rights = ChatAdminRights(change_info=True, post_messages=True, edit_messages=True,
                             delete_messages=True, ban_users=True, invite_users=True,
                             pin_messages=True, add_admins=False, manage_call=True)
    promoted = failed = 0
    st = await event.respond(f"👑 **RUDRA GOD | Promoting {len(SAVED_BOTS)} bots...**")
    for b in SAVED_BOTS:
        try:
            be = await client.get_entity(b)
            await client(EditAdminRequest(chat, be, rights, "Nova Admin"))
            promoted += 1
            await st.edit(f"✅ **PROMOTED:** {promoted}/{len(SAVED_BOTS)} 👑")
            await asyncio.sleep(1)
        except: failed += 1
    await st.edit(f"💥 **COMPLETE!** Promoted: {promoted} | Failed: {failed} 👑")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.removebots'))
async def removebots_cmd(event):
    await event.delete()
    removed = failed = 0
    st = await event.respond(f"🗑️ **RUDRA GOD | Removing {len(SAVED_BOTS)} bots...**")
    for b in SAVED_BOTS:
        try:
            be = await client.get_entity(b)
            await client.kick_participant(event.chat_id, be)
            removed += 1
            await st.edit(f"✅ **REMOVED:** {removed}/{len(SAVED_BOTS)}")
            await asyncio.sleep(1)
        except: failed += 1
    await st.edit(f"💥 **COMPLETE!** Removed: {removed} | Failed: {failed}")

# ─── ADMIN MANAGEMENT ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.makeadmin'))
async def makeadmin_cmd(event):
    chat = await event.get_chat()
    args = event.text.strip().split()[1:]
    rights = ChatAdminRights(change_info=True, post_messages=True, edit_messages=True,
                             delete_messages=True, ban_users=True, invite_users=True,
                             pin_messages=True, add_admins=False, manage_call=True)
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        try:
            user = await reply_msg.get_sender()
            await client(EditAdminRequest(chat, user, rights, "Admin"))
            await event.respond(f"👑 **{user.first_name} is now ADMIN!** ⚡")
        except Exception as e:
            await event.respond(f"❌ **Failed:** {e}")
        return
    if args:
        try:
            user = await client.get_entity(args[0].lstrip('@'))
            await client(EditAdminRequest(chat, user, rights, "Admin"))
            await event.respond(f"👑 **@{args[0]} is now ADMIN!** ⚡")
        except Exception as e:
            await event.respond(f"❌ **Failed:** {e}")
    else:
        await event.respond("**Usage:** `.makeadmin @username` or reply")

# ─── KICK/BAN ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.kick'))
async def kick_cmd(event):
    if not event.is_reply:
        await event.respond("❌ **Reply to a user to kick them!**")
        return
    try:
        u = await (await event.get_reply_message()).get_sender()
        await client.kick_participant(event.chat_id, u)
        await event.respond(f"👢 **{u.first_name} HAS BEEN KICKED!** 💥")
    except Exception as e:
        await event.respond(f"❌ **Failed:** {e}")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.ban'))
async def ban_cmd(event):
    if not event.is_reply:
        await event.respond("❌ **Reply to a user to ban them!**")
        return
    try:
        u = await (await event.get_reply_message()).get_sender()
        await client.edit_permissions(event.chat_id, u, view_messages=False)
        await event.respond(f"🔨 **{u.first_name} HAS BEEN BANNED!** 💀")
    except Exception as e:
        await event.respond(f"❌ **Failed:** {e}")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.unban (.+)'))
async def unban_cmd(event):
    username = event.pattern_match.group(1).lstrip('@')
    try:
        u = await client.get_entity(username)
        await client.edit_permissions(event.chat_id, u, view_messages=True)
        await event.respond(f"✅ **@{username} UNBANNED!**")
    except Exception as e:
        await event.respond(f"❌ **Failed:** {e}")

# ─── MUTE SYSTEM ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.silence'))
async def silence_cmd(event):
    if not event.is_reply:
        await event.respond("❌ **Reply to a message with `.silence`**")
        return
    reply_msg = await event.get_reply_message()
    sender = await reply_msg.get_sender()
    cid = event.chat_id
    state.add_delete_target(cid, sender.id, getattr(sender, 'username', None))
    state.auto_delete_chats[cid] = True
    state.save_auto_delete()
    await event.respond("🤐 **User SILENCED!** 💀")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.unsilence'))
async def unsilence_cmd(event):
    if not event.is_reply:
        await event.respond("❌ **Reply to a message with `.unsilence`**")
        return
    reply_msg = await event.get_reply_message()
    sender = await reply_msg.get_sender()
    cid = event.chat_id
    uid = sender.id
    uname = getattr(sender, 'username', None)
    state.delete_target_users.get(cid, set()).discard(uid)
    if uname: state.delete_target_usernames.get(cid, set()).discard(uname.lower())
    state.save_delete_targets()
    await event.respond("🗣️ **User UNSILENCED!** ✅")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.muteall'))
async def muteall_cmd(event):
    state.auto_delete_chats[event.chat_id] = True
    state.save_auto_delete()
    await event.respond("🤐 **EVERYONE MUTED!** 💀")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.unmuteall'))
async def unmuteall_cmd(event):
    cid = event.chat_id
    if cid in state.auto_delete_chats:
        del state.auto_delete_chats[cid]
        state.save_auto_delete()
    await event.respond("🗣️ **EVERYONE CAN SPEAK!** ✅")

# ─── PROTECTION ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.protect'))
async def protect_cmd(event):
    args = event.text.strip().split()[1:]
    if not args and not event.is_reply:
        count = len(state.safe_users)
        await event.respond(f"🛡️ **Protected users:** {count}\n**Usage:** `.protect @user`")
        return
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        uid = reply_msg.sender_id
        sender = await reply_msg.get_sender()
        state.add_safe_user(uid, getattr(sender, 'username', None))
        await event.respond("✅ **User PROTECTED!** 🛡️")
        return
    for a in args:
        try:
            u = await client.get_entity(a.lstrip('@'))
            state.add_safe_user(u.id, a.lstrip('@'))
        except: pass
    await event.respond(f"✅ **Protected {len(args)} user(s)!** 🛡️")

# ─── FLOOD ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.flood (.+)'))
async def flood_cmd(event):
    cid = event.chat_id
    text = event.pattern_match.group(1)
    state.spam_active[cid] = text
    await event.respond(f"💥 **FLOOD ON:** {text} 🔥")
    async def _spam():
        while cid in state.spam_active:
            try:
                await client.send_message(cid, text)
                await asyncio.sleep(0.5)
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)
            except: break
        state.spam_active.pop(cid, None)
    asyncio.create_task(_spam())

@client.on(events.NewMessage(outgoing=True, pattern=r'\.stopflood'))
async def stopflood_cmd(event):
    state.spam_active.pop(event.chat_id, None)
    await event.respond("✅ **FLOOD MODE OFF**")

# ─── AUTO-REPLY ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.autoreply (.+)'))
async def autoreply_cmd(event):
    cid = event.chat_id
    state.swipe_active[cid] = event.pattern_match.group(1)
    await event.respond(f"🔄 **AUTO-REPLY ON:** {state.swipe_active[cid]} ⚡")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.stopautoreply'))
async def stopautoreply_cmd(event):
    state.swipe_active.pop(event.chat_id, None)
    await event.respond("✅ **AUTO-REPLY OFF**")

# ─── PROFILE ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.copyprofile'))
async def copyprofile_cmd(event):
    if not event.is_reply:
        await event.respond("❌ **Reply to someone to copy their profile!**")
        return
    target = await (await event.get_reply_message()).get_sender()
    me = await client.get_me()
    if state.original_name is None:
        state.original_name = me.first_name
        try: state.original_photo = await client.download_profile_photo('me', file=BytesIO())
        except: state.original_photo = None
    try:
        await client(functions.account.UpdateProfileRequest(
            first_name=target.first_name or "", last_name=target.last_name or ""))
        photo_path = f"/data/data/com.termux/files/usr/tmp{user.id}.jpg"
        await client.download_profile_photo(target, file=photo_path)
        if os.path.exists(photo_path):
            await client(UploadProfilePhotoRequest(await client.upload_file(photo_path)))
            os.remove(photo_path)
        await event.respond(f"✅ **Copied {target.first_name}'s profile!** 🎭")
    except Exception as e:
        await event.respond(f"❌ **Error:** {e}")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.restore'))
async def restore_cmd(event):
    if not state.original_name:
        await event.respond("❌ **No original profile saved!**")
        return
    try:
        names = state.original_name.split(' ', 1)
        await client(functions.account.UpdateProfileRequest(
            first_name=names[0], last_name=names[1] if len(names) > 1 else ""))
        photos = await client.get_profile_photos('me', limit=10)
        if photos: await client(DeletePhotosRequest(photos))
        if state.original_photo:
            await client(UploadProfilePhotoRequest(await client.upload_file(state.original_photo)))
        state.copied_mode.pop(event.chat_id, None)
        await event.respond("✅ **Profile restored!** 🎭")
    except Exception as e:
        await event.respond(f"❌ **Error:** {e}")

# ─── AI FEATURES ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.aichat'))
async def aichat_cmd(event):
    cid = event.chat_id
    state.ai_chat_active[cid] = not state.ai_chat_active.get(cid, False)
    await event.respond(f"⚡ **AI CHAT: {'ON 🤖' if state.ai_chat_active[cid] else 'OFF'}**")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.savage'))
async def savage_cmd(event):
    global SAVAGE_MODE
    SAVAGE_MODE = not SAVAGE_MODE
    await event.respond(f"😈 **SAVAGE MODE: {'ON 🔥' if SAVAGE_MODE else 'OFF'}**")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.roast(?:\s+(.+))?'))
async def roast_cmd(event):
    global ROAST_INTENSITY
    args = event.pattern_match.group(1)
    if not args:
        await event.respond(f"🔥 **Current:** `{ROAST_INTENSITY}`\n**Options:** mild, medium, high, extreme")
        return
    lvl = args.strip().lower()
    if lvl in ["mild", "medium", "high", "extreme"]:
        ROAST_INTENSITY = lvl
        await event.respond(f"🔥 **Roast set to: {lvl.upper()}** 💀")
    else:
        await event.respond("❌ **Invalid!** Use: mild, medium, high, extreme")

# ─── MUSIC ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.play (.+)'))
async def play_cmd(event):
    cid = event.chat_id
    query = event.pattern_match.group(1)
    if state.downloading_music.get(cid):
        await event.respond("⏳ **Already searching! Please wait...**")
        return
    state.downloading_music[cid] = True
    emoji = random.choice(MUSIC_EMOJIS)
    st = await event.respond(f"{emoji} **NOVA GOD MUSIC**\n🔍 Searching: **{query}**...")
    try:
        music_bots = ['@vid', '@SpotifyMusicDownloaderBot', '@vkmusic_bot']
        results, used_bot = None, None
        for bot in music_bots:
            try:
                await st.edit(f"{emoji} **NOVA MUSIC**\n🔍 Searching via {bot}...")
                results = await client.inline_query(bot, query)
                if results:
                    used_bot = bot
                    break
            except: continue
        if not results:
            await st.edit(f"❌ **No results for:** {query}\n💡 Try: @vid {query}")
            return
        await st.edit(f"{emoji} **NOVA MUSIC**\n📥 Downloading via {used_bot}...")
        await results[0].click(cid)
        await asyncio.sleep(2)
        await st.delete()
    except Exception as e:
        await st.edit(f"❌ **Music error!**\nTry: @vid {query}")
    finally:
        state.downloading_music[cid] = False

# ─── OTHER ───
@client.on(events.NewMessage(outgoing=True, pattern=r'\.exit'))
async def exit_cmd(event):
    chat = await event.get_chat()
    title = getattr(chat, 'title', 'here')
    await event.respond(f"👋 **Leaving {title}...**")
    await asyncio.sleep(1)
    await client.delete_dialog(event.chat_id)

# ==================== HELP MENU ====================
@client.on(events.NewMessage(outgoing=True, pattern=r'\.commands'))
async def help_cmd(event):
    await event.delete()
    txt = """
╔══════════════════════════════════╗
        ✨ RUDRA GOD ✨
╚══════════════════════════════════╝

╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
        🎯 𝙏𝘼𝙍𝙂𝙀𝙏 𝙎𝙇𝙄𝘿𝙀
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
𖤝 .targetslide <reply> [text]
𖤝 .unslide <reply>
𖤝 .unslideall
𖤝 .addslide <text>
𖤝 .rmslide <number>
𖤝 .slidelist
𖤝 .clearslides

╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
        💤 𝘼𝙁𝙆 & 𝙂𝙃𝙊𝙎𝙏
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
♡ .afk [reason]
♡ .back
♡ .ghost

╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
        👤 𝙐𝙎𝙀𝙍 𝙏𝙊𝙊𝙇𝙎
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
♡ .info <reply>
♡ .tagall [text]
♡ .steal <reply>
♡ .purge <number>
♡ .faketyping <secs>
♡ .countdown <secs>

╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
        🔥 𝙉𝘼𝙈𝙀 𝙎𝙏𝙔𝙇𝙀𝙍
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
𖤝 .copyprofile <reply>
𖤝 .restore

╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
        🛡️ 𝙂𝙍𝙊𝙐𝙋 𝙈𝘼𝙉𝘼𝙂𝙀𝙈𝙀𝙉𝙏
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
✘ .kick <reply>
✘ .ban <reply>
✘ .unban @user
✘ .silence <reply>
✘ .unsilence <reply>
✘ .muteall / .unmuteall
✘ .protect @user
✘ .makeadmin @user

╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
        🤖 𝘽𝙊𝙏 𝘾𝙊𝙉𝙏𝙍𝙊𝙇
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
✰ .invite
✰ .promote
✰ .removebots

╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
        ⚡ 𝙍𝘼𝙄𝘿 𝙈𝙊𝘿𝙀
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
✘ .flood <text>
✘ .stopflood
✘ .autoreply <text>
✘ .stopautoreply

╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
        🤖 𝘼𝙄 𝙁𝙀𝘼𝙏𝙐𝙍𝙀𝙎
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
♡ .aichat
♡ .savage
♡ .roast <level>

╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
        🎵 𝙈𝙐𝙎𝙄𝘾
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
𖤝 .play <song name>

╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
        🚪 𝙊𝙏𝙃𝙀𝙍
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
𖤝 .exit
𖤝 .commands

╔══════════════════════════════════╗
        ⚡ 𝙐𝙎𝙀 𝙍𝙀𝙎𝙋𝙊𝙉𝙎𝙄𝘽𝙇𝙔 ⚡
╚══════════════════════════════════╝
"""
    await event.respond(txt)

# ==================== MAIN ====================
async def main():
    print("\n" + "="*55)
    print("""
    ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗ 
    ████╗  ██║██╔═══██╗██║   ██║██╔══██╗
    ██╔██╗ ██║██║   ██║██║   ██║███████║
    ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║
    ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║
    ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝
           🔥 RUDRA GOD — REBORN 🔥
    """)
    print("="*55)

    await client.start(phone=PHONE)
    me = await client.get_me()
    slide_count = len(state.slide_messages)
    print(f"\n✅ Online as: {me.first_name}")
    print(f"🎯 Slide messages loaded: {slide_count}")
    print(f"🤖 Bots configured: {len(SAVED_BOTS)}")
    print(f"🎵 yt-dlp: {'READY' if YTDLP_AVAILABLE else 'NOT INSTALLED'}")
    print(f"\n📋 .commands for help | Ctrl+C to stop\n")
    print("="*55)
    print("⚡ RUDRA GOD IS RUNNING!")
    print("="*55 + "\n")

    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.WARNING)
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n\n👋 Rudra God stopped.")
    except Exception as e:
        print(f"\n❌ Fatal: {e}")