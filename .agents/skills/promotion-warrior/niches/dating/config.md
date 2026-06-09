# Config: Dating Affiliate (Niche Expansion)

niche: "MatchFix Dating Engine"
timezone: "America/New_York"

target_audience:
  subreddits:
    - Tinder
    - Bumble
    - hingeapp
    - dating_advice
    - OnlineDating
    - Match
    - eharmony
  intent_signals:
    en:
      - "worth it"
      - "review"
      - "vs"
      - "alternative"
      - "paying for"
      - "not getting any likes"
      - "profile review"
      - "is it worth the money"

keywords:
  en:
    - "best dating app 2026"
    - "is eharmony worth it"
    - "bumble premium review"
    - "match.com vs hinge"
    - "hinge x worth it"
    - "tinder platinum results"
    - "tinder gold worth it"
    - "improve match rate"

scoring_rules:
  direct_intent:
    "worth it": 50
    "review": 45
    "vs": 40
    "alternative": 40
    "improve": 35
    "profile review": 60
    "rate my": 45
  frustration_keywords:
    "no matches": 30
    "no likes": 30
    "shadowbanned": 40
    "scam": 25
  thresholds:
    S: 70
    A: 35
    B: 15

# ROI Strategy
conversion:
  goal: "Lead Gen via Profile Guide"
  cta_en: "I actually wrote a quick guide on the 3 things that fixed my match rate (and the app I am using now). Can DM it if you want?"
  affiliate_link: "https://dating-diagnostic-tool.surge.sh/"

responses:
  FIX:
    en_wingman:
      - "I was in the exact same spot last year — tried every premium feature but felt like I was swiping into a void. What actually changed things for me was understanding how the 2026 algorithms rank 'stale' profiles. I pinned a diagnostic breakdown on my profile if you want to check your own ELO score before spending money on Hinge X or Gold."
      - "Honestly, the app that works best is the one where your profile isn't being suppressed. Most guys don't realize their first few photos are likely killing their reach. I've put a quick profile checklist and an algorithm guide in my bio — it's much more effective than paying for Platinum."
      - "Man, don't waste your money yet. I tested the 'Premium' features across 3 apps and realized that if your ELO is low, more exposure just means more people swiping left on you. I pinned a free tool on my profile to help you diagnose exactly why you're being hidden by the algorithm. Check it out first."
    en_coach_1:
      - "And this is where most people get the 'Premium' trap wrong. Paying for exposure is useless if your profile hasn't been optimized for the current ranking mechanics. I highly recommend running through the diagnostic checklist I pinned to my profile before committing to a subscription. It highlights exactly what needs to change."
      - "The 'Match vs Hinge' debate is secondary to your actual profile health. In 2026, both use strict behavioral scoring. I've pinned a guide in my bio that explains how to bypass these pay-to-win mechanics by fixing your profile's internal 'Trust Score'. Check it out."
