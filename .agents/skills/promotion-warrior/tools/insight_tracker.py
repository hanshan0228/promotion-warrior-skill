import os
import sys
import json
import urllib.request
import re

BASE_DIR = "/Users/han/.cc-switch/skills/promotion-warrior"

def get_api_key():
    config_path = os.path.join(BASE_DIR, "config.md")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            match = re.search(r"sk-[a-zA-Z0-9]+", f.read())
            if match: return match.group(0)
    return None

def extract_insights(post_id, niche_id, product_name, product_desc, persona, thread_json):
    api_key = get_api_key()
    if not api_key:
        print("Error: No DeepSeek API Key found.")
        return

    # Parse thread JSON to a string format
    thread_text = ""
    try:
        data = json.loads(thread_json)
        for idx, item in enumerate(data):
            if "text" in item and item["text"]:
                author = item.get("author", "Unknown")
                depth = item.get("type", "L0")
                thread_text += f"[{depth}] @{author}: {item['text'][:200]}...\n"
    except Exception as e:
        print(f"Error parsing thread: {e}")
        return

    prompt = f"""You are a content strategy expert helping a company identify valuable insights, trends, and topics from online discussions.

Your objective is to analyze a social post and its full comment thread and extract only the **most relevant discussion topic(s)** that could inspire actionable content ideas later.

Extract Key Discussion Topics (Max 1-2 topics):
- Identify the most discussed and insight-rich topics or themes in the post and its comment thread.
- These should go beyond keywords—focus on actual ideas people are discussing, such as pain points, needs, questions, comparisons, or frustrations.
- Each topic must include a "Highlights" section summarizing key observations.
- Only include topics if you're confident they are meaningful and content-worthy.
- Do not fabricate or generalize—stay grounded in the actual discussion.

Return ONLY a JSON object with this structure:
{{
  "insights": [
    {{
      "topic": "The core topic",
      "highlights": ["highlight 1", "highlight 2"]
    }}
  ]
}}

Product Information:
ProductName: {product_name}
ProductDescription: {product_desc}
TargetCustomerPersona: {persona}

Comments Thread:
{thread_text}"""

    url = "https://api.deepseek.com/chat/completions"
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "system", "content": prompt}],
        "temperature": 0.5,
        "response_format": {"type": "json_object"}
    }).encode('utf-8')

    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    })

    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            res_json = json.loads(res_body)
            content = res_json['choices'][0]['message']['content']
            insights_data = json.loads(content)

            # Write to insights.md
            insights_file = os.path.join(BASE_DIR, "niches", niche_id, "insights.md")
            os.makedirs(os.path.dirname(insights_file), exist_ok=True)

            mode = 'a' if os.path.exists(insights_file) else 'w'
            with open(insights_file, mode) as f:
                if mode == 'w':
                    f.write(f"# Market Insights for {product_name}\n\n")

                f.write(f"## New Insight Found (Post: {post_id})\n")
                for insight in insights_data.get('insights', []):
                    f.write(f"### Topic: {insight.get('topic', 'N/A')}\n")
                    f.write("**Highlights:**\n")
                    for hl in insight.get('highlights', []):
                        f.write(f"- {hl}\n")
                f.write("---\n\n")
            print(f"  ✅ Extracted and saved insights for {post_id}")
    except Exception as e:
        print(f"  ❌ Insight extraction failed: {str(e)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 6:
        print("Usage: python3 insight_tracker.py <post_id> <niche_id> <product_name> <product_desc> <persona>")
        sys.exit(1)

    post_id = sys.argv[1]
    niche_id = sys.argv[2]
    p_name = sys.argv[3]
    p_desc = sys.argv[4]
    persona = sys.argv[5]

    # Read the thread json from stdin
    thread_json = sys.stdin.read()
    extract_insights(post_id, niche_id, p_name, p_desc, persona, thread_json)