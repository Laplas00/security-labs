#!/usr/bin/env python3
import json

def write_payload(path: str, for_comments_value):
    """
    Write a JSON draft with a given for_comments value.
    """
    draft = {
        "title":       "Type Confusion Attack",
        "content":     "This post tests the for_comments flag.",
        "for_comments": for_comments_value
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(draft, f, indent=2)
    print(f"[+] Payload written to {path} (for_comments={for_comments_value!r})")

if __name__ == "__main__":
    # 1) Boolean false – expected to disable comments
    write_payload("payload_bool_false.draft", False)
