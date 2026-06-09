#!/usr/bin/env python3
"""Build the matrix queue JSON.

Inputs (files in cwd, both optional):
  queue.txt      - one Drive video filename per line
  links_raw.txt  - lines of "N url" (N = retry attempt) or plain "url"
Prints a JSON array of {"kind","ref","try"} objects.
"""
import json
import os

items = []
if os.path.exists("queue.txt"):
    for line in open("queue.txt", encoding="utf-8"):
        line = line.strip()
        if line:
            items.append({"kind": "file", "ref": line, "try": "0"})
if os.path.exists("links_raw.txt"):
    seen = set()
    for line in open("links_raw.txt", encoding="utf-8", errors="ignore"):
        line = line.strip()
        if not line:
            continue
        attempt = "0"
        parts = line.split(None, 1)
        if len(parts) == 2 and parts[0].isdigit():
            attempt, line = parts[0], parts[1].strip()
        if line.lower().startswith(("http://", "https://")) and line not in seen:
            seen.add(line)
            items.append({"kind": "url", "ref": line, "try": attempt})
print(json.dumps(items))
