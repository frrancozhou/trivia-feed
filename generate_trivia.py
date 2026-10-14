import json
from datetime import datetime

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_trivia():
    try:
        with open("trivia.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_trivia(trivia_list):
    with open("trivia.json", "w", encoding="utf-8") as f:
        json.dump(trivia_list, f, ensure_ascii=False, indent=2)

def generate_with_copilot(prompt):
    # QUI colleghi Copilot / modello AI via API.
    # Per ora metti un placeholder per test:
    return "Stars whisper quietly above cities that have forgotten to look up."

def is_duplicate_exact(new_text, trivia_list):
    texts = [t["text"] for t in trivia_list]
    return new_text in texts

def update_feed(trivia_list):
    latest = trivia_list[-20:] if len(trivia_list) > 20 else trivia_list
    items_xml = ""
    for t in latest:
        items_xml += f"""
    <item>
      <title>{t["text"]}</title>
    </item>"""

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Random Trivia Feed</title>
    <link>https://frrancozhou.github.io/trivia-feed/feed.xml</link>
    <description>Short curiosities in English, updated every 12 hours.</description>
{items_xml}
  </channel>
</rss>
"""
    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(feed)

def main():
    config = load_config()
    trivia_list = load_trivia()

    prompt = config["prompt"]
    new_text = generate_with_copilot(prompt).strip()

    if not new_text:
        return

    if is_duplicate_exact(new_text, trivia_list):
        return

    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    new_entry = {
        "id": len(trivia_list) + 1,
        "text": new_text,
        "created_at": now,
        "source": "copilot"
    }
    trivia_list.append(new_entry)
    save_trivia(trivia_list)
    update_feed(trivia_list)

if __name__ == "__main__":
    main()
