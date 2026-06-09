import json
import sys
import re
import yaml

def score_user(comment_body, user_data, config_data):
    """
    Score a lead based on emotional frustration and intent.
    Returns a grade (S, A, B, C) and a score (0-100).
    """
    score = 0
    factors = []

    # Get rules from config, fallback to global strategic defaults
    scoring_rules = config_data.get('scoring_rules', {})

    # 1. Direct Intent Signals (High Priority - Decision Moments)
    # These are users actively looking for a solution RIGHT NOW.
    intent_keywords = scoring_rules.get('direct_intent', {
        '求推荐': 60,
        '求路标': 60,
        '求梯子': 65,
        '机场': 40,
        '哪家强': 45,
        '稳定吗': 35,
        '求助': 30,
        'recommend': 50,
        'which app': 45,
        'best alternative': 50,
        'is it worth it': 45,
        'any tips': 30,
        'looking for': 40,
        'profile review': 40,
        'rate my profile': 40,
        'coupon': 55,
        'discount code': 55,
        'promo code': 55,
        'promo code': 55
    })

    # NEW: High-Conversion Intent (The "Credit Card Out" Moment)
    purchase_intent_keywords = {
        'about to buy': 40,
        'checking out': 45,
        'in my cart': 45,
        'ready to purchase': 40,
        'is it worth the money': 35,
        'buying now': 40
    }

    # 2. Emotional Frustration Level (Secondary Priority)
    frustration_keywords = scoring_rules.get('frustration_keywords', {
        'giving up': 30,
        'shadowbanned': 35,
        'zero matches': 35,
        'sucks': 20,
        'scam': 30,
        'disgusted': 25,
        'tired of this': 25,
        'ghosted': 20,
        'no likes': 30,
        'am i ugly': 40,
        'doing wrong': 30,
        'hard time': 20,
        '挂了': 45,
        '跑路': 50,
        '封了': 40,
        '太贵': 30
    })

    body_lower = comment_body.lower()

    # Process Purchase Intent (Multiplier effect)
    purchase_signal = False
    for kw, val in purchase_intent_keywords.items():
        if kw in body_lower:
            score += val
            factors.append(f"🔥 Purchase Intent: {kw}")
            purchase_signal = True

    # Process Direct Intent
    for kw, val in intent_keywords.items():
        if kw in body_lower:
            score += val
            factors.append(f"Intent Signal: {kw}")

    # If both purchase intent and direct intent match, multiply the total
    if purchase_signal:
        score = int(score * 1.5)
        factors.append("Conversion Multiplier: High Probability Lead")

    # Process Frustration Second (Accumulative)
    for kw, val in frustration_keywords.items():
        if kw in body_lower:
            score += val
            factors.append(f"Frustration Signal: {kw}")

    # 3. Influence / Account Age (Trust Factors)
    followers = int(user_data.get('followers', 0))
    if followers > 500:
        score += 15
        factors.append("Micro-Influencer (Good for social proof)")

    # Thresholds - Optimized for immediate action on Intent
    thresholds = scoring_rules.get('thresholds', {'S': 75, 'A': 40, 'B': 20})

    # Final Grade Calculation
    if score >= thresholds.get('S', 75):
        grade = 'S' # Immediate Sniping
    elif score >= thresholds.get('A', 40):
        grade = 'A' # High value
    elif score >= thresholds.get('B', 20):
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
        config_path = sys.argv[1] if len(sys.argv) > 1 else None
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

        input_data = json.load(sys.stdin)
        comment = input_data.get('comment', '')
        user_info = input_data.get('user_info', {})
        result = score_user(comment, user_info, config_data)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
