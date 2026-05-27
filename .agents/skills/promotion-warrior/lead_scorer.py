import json
import sys
import re

def score_user(platform, user_data):
    """
    Score a user based on their profile data.
    Returns a grade (S, A, B, C) and a score (0-100).
    """
    score = 0
    factors = []

    # 1. Influence Check (Followers)
    followers = int(user_data.get('followers', 0))
    if followers > 10000:
        score += 40
        factors.append("High Influence (10k+)")
    elif followers > 1000:
        score += 20
        factors.append("Moderate Influence (1k+)")
    
    # 2. Professional Identity (Bio/Description)
    bio = user_data.get('bio', '').lower()
    pro_keywords = ['ceo', 'cto', 'founder', 'marketing', 'agency', 'director', 'producer', 'content creator', 'learning']
    if any(kw in bio for kw in pro_keywords):
        score += 30
        factors.append("Professional Persona")
    
    # 3. Engagement (Verified Status or Activity)
    if user_data.get('verified', False):
        score += 20
        factors.append("Verified Account")

    # Final Grade Calculation
    if score >= 80:
        grade = 'S'
    elif score >= 50:
        grade = 'A'
    elif score >= 20:
        grade = 'B'
    else:
        grade = 'C'

    return {
        'grade': grade,
        'score': score,
        'factors': factors,
        'recommendation': 'MANUAL_REVIEW' if grade == 'S' else 'AUTO_REPLY'
    }

if __name__ == "__main__":
    # Expects JSON string from stdin
    try:
        input_data = json.load(sys.stdin)
        platform = input_data.get('platform', 'unknown')
        user_info = input_data.get('user_info', {})
        result = score_user(platform, user_info)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
