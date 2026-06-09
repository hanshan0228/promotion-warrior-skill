import sys
import os
import re
from typing import Optional, List, Dict

ACCOUNTS_PATH = "/Users/han/.agents/skills/promotion-warrior/accounts.md"

def get_accounts_for_platform(platform: str) -> List[Dict]:
    if not os.path.exists(ACCOUNTS_PATH):
        return []

    with open(ACCOUNTS_PATH, 'r') as f:
        content = f.read()

    sections = re.split(r'##\s+', content)
    for sec in sections:
        lines = sec.strip().split('\n')
        if not lines: continue
        header = lines[0].strip().lower()
        if platform.lower() in header:
            accounts = []
            for line in lines:
                if line.startswith('|') and '---' not in line and '账号名' not in line:
                    parts = [p.strip() for p in line.split('|')[1:-1]]
                    if len(parts) >= 5:
                        # Parse quota like "0/15"
                        comment_quota = parts[4] if len(parts) > 4 else "0/10"
                        dm_quota = parts[5] if len(parts) > 5 else "0/5"

                        try:
                            c_cur, c_max = map(int, comment_quota.split('/'))
                            d_cur, d_max = map(int, dm_quota.split('/'))
                        except:
                            c_cur, c_max, d_cur, d_max = 0, 10, 0, 5

                        accounts.append({
                            'name': parts[0],
                            'status': parts[1],
                            'persona': parts[2],
                            'comment_cur': c_cur,
                            'comment_max': c_max,
                            'dm_cur': d_cur,
                            'dm_max': d_max,
                            'raw_line': line
                        })
            return accounts
    return []

def pick_account(platform: str, action_type: str = 'comment') -> Optional[Dict]:
    accounts = get_accounts_for_platform(platform)
    active_accounts = [a for a in accounts if a['status'] in ['active', 'warming']]

    for acc in active_accounts:
        if action_type == 'comment':
            if acc['comment_cur'] < acc['comment_max']:
                return acc
        else: # dm
            if acc['dm_cur'] < acc['dm_max']:
                return acc
    return None

def increment_count(platform: str, account_name: str, action_type: str = 'comment'):
    if not os.path.exists(ACCOUNTS_PATH):
        return

    with open(ACCOUNTS_PATH, 'r') as f:
        lines = f.readlines()

    new_lines = []
    in_platform = False
    updated = False

    for line in lines:
        if line.startswith('## '):
            in_platform = platform.lower() in line.lower()

        if in_platform and line.startswith('|') and f"| {account_name} |" in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7:
                idx = 5 if action_type == 'comment' else 6
                try:
                    cur, mx = map(int, parts[idx].split('/'))
                    parts[idx] = f"{cur + 1}/{mx}"
                    new_lines.append('| ' + ' | '.join(parts[1:-1]) + ' |\n')
                    updated = True
                    continue
                except: pass
        new_lines.append(line)

    if updated:
        with open(ACCOUNTS_PATH, 'w') as f:
            f.writelines(new_lines)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "pick":
        plat = sys.argv[2]
        act = sys.argv[3] if len(sys.argv) > 3 else "comment"
        acc = pick_account(plat, act)
        if acc:
            print(f"{acc['name']}|{acc['persona']}|{acc['status']}")
        else:
            sys.exit(1)
    elif cmd == "increment":
        plat = sys.argv[2]
        name = sys.argv[3]
        act = sys.argv[4] if len(sys.argv) > 4 else "comment"
        increment_count(plat, name, act)
