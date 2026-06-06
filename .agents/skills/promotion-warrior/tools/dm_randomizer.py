import random
import sys
import re
import yaml

def get_random_response(keyword, persona, link, config_data):
    # Default responses
    responses = {
        "FIX": {
            "en_wingman": [
                "Bro, your first photo might be killing your ELO score. I pinned a breakdown on my profile of how I bypassed the algorithm to get out of the 'zero matches' bucket. Check my bio, might save you some time.",
                "Man, the algorithm right now is brutal if you don't optimize specifically for it. I put together a quick guide on my profile on the 3 things that actually work in 2026. Give it a look.",
                "Most guys are swiping into a void because of how the apps are monetized now. Check the pinned post on my profile—I explained how to fix your match rate without paying for Platinum."
            ],
            "en_coach_1": [
                "The psychology of current apps is broken, but you can optimize for it. I've pinned a detailed 'Intentional Matching' guide to my profile. Highly recommend giving it a read! 💡",
                "It's not you, it's the algorithm. I've put a free diagnostic tool link in my bio that helps identify exactly why your profile is being hidden. Check it out. 🧠",
                "Stop 'swiping' aimlessly. I wrote a breakdown on my profile of how to bypass the pay-to-win mechanics of these apps. Check my bio! ✨"
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
