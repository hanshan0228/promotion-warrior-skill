import json
import sys
import re

def score_dating_user(comment_body, user_data):
    """
    Score a dating lead based on emotional frustration and intent.
    Returns a grade (S, A, B, C) and a score (0-100).
    """
    score = 0
    factors = []

    # 1. Emotional Frustration Level (High Priority for Dating)
    frustration_keywords = {
        'giving up': 40,
        'shadowbanned': 35,
        'zero matches': 35,
        'no matches': 30,
        'sucks': 20,
        'lonely': 25,
        'waste of time': 20,
        'tinder is a scam': 30,
        'bumble is a scam': 30
    }
    
    body_lower = comment_body.lower()
    for kw, val in frustration_keywords.items():
        if kw in body_lower:
            score += val
            factors.append(f"Frustration Signal: {kw}")
            break # Avoid over-scoring on multiple synonyms

    # 2. Influence / Account Age (Trust Factors)
    followers = int(user_data.get('followers', 0))
    if followers > 500:
        score += 15
        factors.append("Micro-Influencer (Good for social proof)")
    
    # 3. Direct Intent (Asking for help)
    intent_keywords = ['how', 'help', 'recommend', 'which app', 'tips']
    if any(kw in body_lower for kw in intent_keywords):
        score += 25
        factors.append("Direct Intent Signal")

    # Final Grade Calculation
    if score >= 70:
        grade = 'S' # Immediate Sniping
    elif score >= 45:
        grade = 'A' # High value
    elif score >= 20:
        grade = 'B' # Standard
    else:
        grade = 'C' # Low priority

    return {
        'grade': grade,
        'score': score,
        'factors': factors,
        'recommendation': 'INSTANT_DM' if grade == 'S' else 'AUTO_COMMENT'
    }

if __name__ == "__main__":
    try:
        input_data = json.load(sys.stdin)
        comment = input_data.get('comment', '')
        user_info = input_data.get('user_info', {})
        result = score_dating_user(comment, user_info)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
