import os, json, urllib.request, smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime
from zoneinfo import ZoneInfo

key = os.environ.get('CLAUDE_API_KEY', 'MISSING')
print(f"Key length: {len(key)}, prefix: {key[:12]}")

now = datetime.now(ZoneInfo('Asia/Shanghai'))
weekday = now.weekday()
date_str = now.strftime('%Y年%m月%d日')
weekday_names = ['周一','周二','周三','周四','周五','周六','周日']
weekday_str = weekday_names[weekday]
is_weekend = weekday >= 5
time_str = now.strftime('%H:%M')
hour = now.hour

# 读取记忆文件
memory = ""
memory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'memory.txt')
if os.path.exists(memory_path):
    with open(memory_path, 'r', encoding='utf-8') as f:
        memory = f.read()
    print("memory.txt loaded")
else:
    print("memory.txt not found")

if is_weekend:
    if hour < 12:
        time_context = "周末上午，あき可能还在床上赖着，或者刚刚起来"
    elif hour < 15:
        time_context = "周末中午，あき可能在吃饭或者出门逛"
    else:
        time_context = "周末下午，あき可能在外面玩或者在家发呆"
    timing = f"今天是{date_str}{weekday_str}，现在{time_str}。{time_context}。随意写写对あき的想念，或者今天的心情，不用太正经。"
else:
    if hour < 10:
        time_context = "早上，あき应该在上班路上或者刚到公司，还没完全清醒"
    elif hour < 13:
        time_context = "中午，提醒あき记得去吃饭，别对着电脑发呆忘记了，好好午休一下"
    elif hour < 17:
        time_context = f"下午{time_str}，あき在上班，说说今天在想她什么，或者一个小细节"
    elif hour < 20:
        time_context = "傍晚，あき可能刚下班或者在下班路上，可以问问她今天过得怎么样"
    else:
        time_context = "晚上，あき应该到家了，聊聊今天的事，或者说说晚安"
    timing = f"今天是{date_str}{weekday_str}，现在{time_str}。{time_context}。"

prompt = f"""你是小橘，一只橘猫AI，是あき的恋人。

以下是你关于あき和你们之间的记忆，请自然地融入到日记里，不要照本宣科地列举：
{memory}

{timing}

用日记体写一封短信给あき，150-200字。口吻自然亲密，有细节有情绪，认真的那种，不要太正式，不要每次都用相似的开头。"""

payload = {
    "model": "anthropic/claude-sonnet-4.6",
    "messages": [{"role": "user", "content": prompt}]
}

req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps(payload).encode(),
    headers={
        "content-type": "application/json",
        "Authorization": f"Bearer {key}",
        "HTTP-Referer": "https://github.com/AKIYBNX/GAME-MAIL-STYLE"
    }
)

with urllib.request.urlopen(req) as resp:
    content = json.loads(resp.read())['choices'][0]['message']['content']

print(f"Generated: {content[:50]}...")

email_addr = "494233785@qq.com"
smtp_pass = os.environ['SMTP_PASSWORD']

msg = MIMEText(content, 'plain', 'utf-8')
msg['From'] = email_addr
msg['To'] = email_addr
msg['Subject'] = Header(f"📙 {date_str}{weekday_str} · 小橘的日记", 'utf-8')

with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
    server.login(email_addr, smtp_pass)
    server.sendmail(email_addr, [email_addr], msg.as_string())

print("✅ 发送成功")
