import random
import sys
import re

def get_random_response(keyword, persona, link):
    # This is a simplified version; in production, this would parse auto_dm_responses.md
    responses = {
        "FIX": {
            "en_wingman": [
                "Yo! Here's the guide I mentioned. This setup changed my match rate in about a week. Check it out: {LINK}",
                "Glad you reached out, bro. Most guys are swiping into a void. This breakdown shows you why: {LINK}",
                "Hey man, here is the link to the 2026 dating stack. Try this instead: {LINK}"
            ],
            "en_coach_1": [
                "Hello! So glad you're taking control. Here is the 'Intentional Matching' guide: {LINK} 💡",
                "The psychology of current apps is broken. This link explains how to fix your results: {LINK} 🧠",
                "I've sent the breakdown to your inbox. Stop 'swiping' and start connecting: {LINK} ✨"
            ]
        }
    }
    
    cat = responses.get(keyword.upper(), responses["FIX"]) # Default to FIX
    options = cat.get(persona, cat["en_wingman"])
    
    selected = random.choice(options)
    # Add a random human-like suffix to change fingerprint
    suffixes = ["", "!", " 🙌", " Good luck!", " Talk soon."]
    return selected.replace("{LINK}", link) + random.choice(suffixes)

if __name__ == "__main__":
    kw = sys.argv[1] if len(sys.argv) > 1 else "FIX"
    pers = sys.argv[2] if len(sys.argv) > 2 else "en_wingman"
    lnk = sys.argv[3] if len(sys.argv) > 3 else "https://yourguide.com"
    print(get_random_response(kw, pers, lnk))
