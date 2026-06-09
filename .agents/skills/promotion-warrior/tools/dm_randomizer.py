import random
import sys
import re
import yaml

def get_random_response(keyword, persona, link, config_data):
    # Default responses inspired by RedoraAI's anti-AI organic patterns
    responses = {
        "FIX": {
            "en_wingman": [
                "I was in the exact same spot a while ago — felt like I was swiping into a void. Tried a bunch of profile tweaks, but what actually worked was optimizing for how the algorithm ranks new users. I pinned a breakdown on my profile if you want to check it out.",
                "Honestly, the app that works best is the one where the algorithm doesn't shadowban average guys. I switched to a different setup and my match rate finally started to click. Happy to share the diagnostic tool I used if you check my bio.",
                "We've all been there man. It's not you, it's the pay-to-win mechanics. I put together a quick checklist on my profile of the 3 things that actually trigger the algorithm to show your profile in 2026. Give it a look.",
                "Are you using the same photos you used last year? The current algorithm penalizes stale content heavily. I've pinned a free diagnostic tool on my profile that helps identify exactly why you're being hidden. Might save you some time."
            ],
            "en_coach_1": [
                "And this is exactly why the psychology of current apps is broken. But you can optimize for it. I've pinned a detailed 'Intentional Matching' guide to my profile. Highly recommend giving it a read.",
                "It's not you, it's the algorithm. I've put a free diagnostic tool link in my bio that helps identify exactly why your profile is being hidden. Check it out.",
                "Stop swiping aimlessly. I wrote a breakdown on my profile of how to bypass the pay-to-win mechanics of these apps. Check my bio."
            ]
        }
    }

    # Override with config responses if available
    custom_responses = config_data.get('responses', {})
    if custom_responses:
        responses = custom_responses

    cat = responses.get(keyword.upper(), responses.get("FIX", {}))
    # Fallback if FIX or keyword isn't present properly
    if not cat and responses:
        cat = list(responses.values())[0]

    options = cat.get(persona)
    if not options and cat:
        options = list(cat.values())[0]
    if not options:
        options = ["Check out my bio for a quick guide on this!"]

    selected = random.choice(options)
    suffixes = ["", "!", " 🙌", " Good luck!", " Talk soon.", " Let me know if it helps."]
    return selected.replace("{LINK}", link) + random.choice(suffixes)

if __name__ == "__main__":
    kw = sys.argv[1] if len(sys.argv) > 1 else "FIX"
    pers = sys.argv[2] if len(sys.argv) > 2 else "en_wingman"
    lnk = sys.argv[3] if len(sys.argv) > 3 else "https://dating-diagnostic-tool.surge.sh/"
    config_path = sys.argv[4] if len(sys.argv) > 4 else None

    config_data = {}
    if config_path:
        try:
            with open(config_path, 'r') as f:
                content = f.read()
            match = re.search(r'```(?:yaml)?\n(.*?)\n```', content, re.DOTALL)
            yaml_str = match.group(1) if match else content
            config_data = yaml.safe_load(yaml_str) or {}
        except:
            pass

    print(get_random_response(kw, pers, lnk, config_data))
