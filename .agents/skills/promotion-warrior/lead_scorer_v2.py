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

    # Get rules from config, fallback to default dating rules
    scoring_rules = config_data.get('scoring_rules', {})

    frustration_keywords = scoring_rules.get('frustration_keywords', {
        'giving up': 40,
        'shadowbanned': 35,
        'zero matches': 35,
        'no matches': 30,
        'didn\'t even get any matches': 35,
        'sucks': 20,
        'lonely': 25,
        'waste of time': 20,
        'scam': 30,
        'disgusted': 25,
        'tired of this': 25,
        'ghosted': 20,
        'no likes': 30,
        'am i ugly': 40,
        'doing wrong': 30,
        'hard time': 20,
        'profile review': 25
    })

    body_lower = comment_body.lower()
    for kw, val in frustration_keywords.items():
        if kw in body_lower:
            score += val
            factors.append(f"Frustration Signal: {kw}")
            break # Avoid over-scoring on multiple synonyms

    # Influence / Account Age (Trust Factors)
    followers = int(user_data.get('followers', 0))
    if followers > 500:
        score += 15
        factors.append("Micro-Influencer (Good for social proof)")

    # Direct Intent (Asking for help)
    intent_keywords = scoring_rules.get('intent_keywords', [
        'how', 'help', 'recommend', 'which app', 'tips', 'advice', 'improve', 'what to change'
    ])

    if any(kw in body_lower for kw in intent_keywords):
        score += 25
        factors.append("Direct Intent Signal")

    # Thresholds
    thresholds = scoring_rules.get('thresholds', {'S': 70, 'A': 45, 'B': 20})

    # Final Grade Calculation
    if score >= thresholds.get('S', 70):
        grade = 'S' # Immediate Sniping
    elif score >= thresholds.get('A', 45):
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
