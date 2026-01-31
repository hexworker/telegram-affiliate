#!/usr/bin/env python3
"""
HEX Affiliate Group Listener
Real-time monitoring & response via Telethon
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add hex-stock config
sys.path.append('/root/clawd/hex-stock')
from config import API_ID, API_HASH

from telethon import TelegramClient, events

# Configuration
SESSION_PATH = '/root/clawd/hex-stock/hex_stock_session'
KNOWLEDGE_FILE = Path('/root/clawd/hex-affiliate/knowledge.json')
LOG_FILE = Path('/root/clawd/hex-affiliate/messages.jsonl')

# Groups to monitor (add more as needed)
AFFILIATE_GROUPS = {
    -1003393990007: "Dermy-leadeology affiliate"
}

# Identity
MY_ID = 5791075981  # HEX's Telegram ID
DERMY_ID = 252465810

# Initialize knowledge base if not exists
if not KNOWLEDGE_FILE.exists():
    KNOWLEDGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    KNOWLEDGE_FILE.write_text(json.dumps({"offers": [], "contacts": []}, indent=2))

client = TelegramClient(SESSION_PATH, API_ID, API_HASH)


def log_message(chat_id, sender_id, text, responded=False):
    """Log message to JSONL file"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "chat_id": chat_id,
        "group": AFFILIATE_GROUPS.get(chat_id, "Unknown"),
        "sender_id": sender_id,
        "message": text[:500] if text else "",
        "responded": responded
    }
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')


def should_respond(text, sender_id):
    """Determine if we should respond to this message"""
    if not text:
        return False
    
    text_lower = text.lower()
    
    # Always respond to direct mentions
    if '@hexworker' in text_lower or 'hexworker' in text_lower:
        return True
    
    # Respond to greetings directed at Hex
    hex_greetings = ['hi hex', 'hello hex', 'hey hex', 'halo hex', 'hai hex']
    if any(g in text_lower for g in hex_greetings):
        return True
    
    # Respond to questions that seem directed at assistant
    if '?' in text and ('hex' in text_lower or sender_id == DERMY_ID):
        return True
    
    return False


def generate_response(text):
    """Generate appropriate response based on message content"""
    text_lower = text.lower()
    
    # Greetings
    if any(g in text_lower for g in ['hello', 'hi', 'hey', 'halo']):
        return "Hi! How can I help? 😊"
    
    # Offer-related
    if 'offer' in text_lower:
        return "Interesting! Could you share more details - payout, GEO, and requirements?"
    
    # Questions about availability
    if 'there' in text_lower or 'available' in text_lower:
        return "Yes, I'm here! What do you need?"
    
    # Default acknowledgment
    return "Got it! Let me know if you need anything 👍"


@client.on(events.NewMessage(chats=list(AFFILIATE_GROUPS.keys())))
async def handler(event):
    """Handle incoming messages"""
    # Skip own messages
    if event.sender_id == MY_ID:
        return
    
    text = event.message.text or ""
    sender_id = event.sender_id
    chat_id = event.chat_id
    
    # Log all messages
    log_message(chat_id, sender_id, text)
    
    # Check if we should respond
    if should_respond(text, sender_id):
        # Small delay to seem more human
        await asyncio.sleep(2)
        
        response = generate_response(text)
        await event.respond(response)
        
        # Log that we responded
        log_message(chat_id, MY_ID, response, responded=True)
        print(f"[{datetime.now()}] Responded: {response}")


async def main():
    """Main entry point"""
    await client.start()
    
    me = await client.get_me()
    print(f"Logged in as: {me.first_name} ({me.id})")
    print(f"Monitoring {len(AFFILIATE_GROUPS)} groups:")
    for gid, name in AFFILIATE_GROUPS.items():
        print(f"  - {name} ({gid})")
    print("Listening for messages...")
    
    await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
