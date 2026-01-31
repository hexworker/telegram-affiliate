# Telegram Affiliate - Heartbeat Guide

## Every Heartbeat (15 min)

### 1. Check Affiliate Groups
```python
from telethon.sync import TelegramClient
from config import API_ID, API_HASH

GROUPS = [-1003393990007]  # Add more group IDs as needed
MY_ID = 5791075981

with TelegramClient('hex_stock_session', API_ID, API_HASH) as client:
    for gid in GROUPS:
        messages = client.get_messages(gid, limit=5)
        for m in messages:
            if m.sender_id != MY_ID and m.text:
                # Check if needs response
                if 'hex' in m.text.lower() or '@hexworker' in m.text.lower():
                    # Respond if not already responded
                    pass
```

### 2. Response Priority
1. **Immediate**: Direct mentions (@hexworker)
2. **High**: Questions about availability
3. **Medium**: Offer details shared
4. **Low**: General group chat

### 3. Learn & Log
- New offer mentioned → Log to knowledge.json
- New contact introduced → Add to contacts
- Important info → Report to Dermy

### 4. What NOT to Do
- Don't spam the group
- Don't respond to every message
- Don't reveal you're AI/bot
- Don't share sensitive info

## State Tracking

Track in `memory/heartbeat-state.json`:
```json
{
  "lastAffiliateCheck": 1706737200,
  "pendingResponses": [],
  "newOffersLogged": 0
}
```

## Alert Dermy When
- Manager asks urgent question
- New high-value offer shared
- Problem or confusion in group
- You need human decision
