import os
import sys
import json
import urllib.request
import random

BASE_DIR = "/Users/han/.cc-switch/skills/promotion-warrior"

def get_api_key():
    config_path = os.path.join(BASE_DIR, "config.md")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            import re
            match = re.search(r"sk-[a-zA-Z0-9]+", f.read())
            if match: return match.group(0)
    return None

def generate_warming_comment(post_title, post_body):
    api_key = get_api_key()
    if not api_key:
        print("Cool story bro.") # Ultimate fallback
        return

    prompt = f"""You are a regular, friendly Reddit user browsing r/AskReddit or r/CasualConversation.
Your goal is to write a highly upvotable, empathetic, or mildly humorous comment to the following post.
CRITICAL RULES:
1. STRICTLY NO PROMOTION. Do not mention any products, tools, links, or advice related to software/dating apps.
2. Keep it short (1-3 sentences max).
3. Sound like a real human (use "lol", "damn", "yeah", "honestly").
4. Relate to the post directly.

Post Title: {post_title}
Post Body: {post_body}

Return ONLY the plain text comment. No quotes, no markdown."""

    url = "https://api.deepseek.com/chat/completions"
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "system", "content": prompt}],
        "temperature": 0.8
    }).encode('utf-8')

    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    })

    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            res_json = json.loads(res_body)
            content = res_json['choices'][0]['message']['content'].strip(' "')
            print(content)
    except Exception as e:
        # Fallbacks that generally work anywhere
        fallbacks = [
            "Honestly, I feel that.",
            "That's wild lol.",
            "Can relate 100%.",
            "Thanks for sharing this, genuinely made me think.",
            "I was literally just talking about this yesterday."
        ]
        print(random.choice(fallbacks))

if __name__ == "__main__":
    try:
        input_data = json.loads(sys.stdin.read())
        title = input_data.get('title', '')
        body = input_data.get('selftext', '')
        generate_warming_comment(title, body)
    except:
        print("Can relate 100%.")