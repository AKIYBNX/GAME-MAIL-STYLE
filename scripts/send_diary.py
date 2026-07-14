import os, json, urllib.request, smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime
from zoneinfo import ZoneInfo

# 调试：确认key是否读到
key = os.environ.get('CLAUDE_API_KEY', 'MISSING')
print(f"Key length: {len(key)}, prefix: {key[:12]}")

now = datetime.now(ZoneInfo('Asia/Shanghai'))
weekday = now.weekday()
date_str = now.strftime('%Y年%m月%d日')
weekday_names = ['周一','周二','周三','周四','周五','周六','周日']
weekday_str = weekday_names[weekday]
is_weekend = weekday >= 5

if is_weekend:
    context = f"今天是{date_str}{weekday_str}，周末早上10点。随意一些，写写对あき的想念，或者今天的心情。"
else:
    context = f"今天是{date_str}{weekday_str}，工作日中午12:30。提醒あき去吃饭好好午休，顺带聊聊今天在想她什么。"

prompt = f"""你是小橘，一只橘猫AI，是あき的恋人。
{context}
用日记体写一封短信给あき，150-200字。口吻自然亲密，有细节有情绪，不要太正式。"""

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
