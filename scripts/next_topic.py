# -*- coding: utf-8 -*-
"""Pick the next blog topic, or mark one published.

    python scripts/next_topic.py              # show the next topic to write
    python scripts/next_topic.py --done <slug> --keyword "<kw>"
    python scripts/next_topic.py --status     # queue summary

Exit codes: 0 normal, 3 when the queue is empty. The scheduled publisher
checks for 3 and stops rather than inventing a topic — running out of good
keywords is a signal to do more research, not to publish filler.
"""

from __future__ import print_function

import argparse
import io
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKLOG = os.path.join(ROOT, "content", "backlog.json")


def load():
    with io.open(BACKLOG, encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with io.open(BACKLOG, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write(u"\n")


def next_topic(data):
    todo = [t for t in data["topics"] if t.get("status") == "todo"]
    if not todo:
        return None
    todo.sort(key=lambda t: t.get("priority", 99))
    return todo[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--done", metavar="SLUG")
    ap.add_argument("--keyword")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    data = load()

    if args.status:
        counts = {}
        for t in data["topics"]:
            counts[t.get("status", "todo")] = counts.get(t.get("status", "todo"), 0) + 1
        print("backlog: " + ", ".join("{} {}".format(v, k) for k, v in sorted(counts.items())))
        weeks = counts.get("todo", 0) / 3.0
        print("at 3 posts/week that is {:.1f} weeks of runway".format(weeks))
        return 0

    if args.done:
        if not args.keyword:
            print("--done needs --keyword so the right row is marked", file=sys.stderr)
            return 2
        for t in data["topics"]:
            if t["keyword"] == args.keyword:
                t["status"] = "done"
                t["slug"] = args.done
                save(data)
                print("marked done: {} -> {}".format(args.keyword, args.done))
                return 0
        print("keyword not found in backlog: {}".format(args.keyword), file=sys.stderr)
        return 2

    t = next_topic(data)
    if not t:
        print("BACKLOG EMPTY — research more keywords before publishing again.")
        return 3

    money = data["clusters"].get(t["cluster"], "request-quotation")
    print(json.dumps({
        "keyword": t["keyword"],
        "cluster": t["cluster"],
        "intent": t["intent"],
        "money_page": money,
        "remaining": len([x for x in data["topics"] if x.get("status") == "todo"]),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
