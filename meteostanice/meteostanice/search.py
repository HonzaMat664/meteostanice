import os
import json
from bs4 import BeautifulSoup

# =========================
# NASTAVENÍ
# =========================
WEB_DIR = "../nas-web"   # <-- uprav podle sebe
OUTPUT_FILE = "../nas-web/search.json"

index = []

# =========================
# FUNKCE: čistý text z HTML
# =========================
def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # odstranit rušivé části
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    text = soup.get_text(" ")
    return " ".join(text.split())

# =========================
# PROCHÁZENÍ WEBU
# =========================
for root, dirs, files in os.walk(WEB_DIR):
    for file in files:

        if not (file.endswith(".html") or file.endswith(".htm")):
            continue

        path = os.path.join(root, file)

        try:
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()
        except:
            continue

        soup = BeautifulSoup(html, "html.parser")

        # -------------------------
        # TITLE (SAFE)
        # -------------------------
        title_tag = soup.find("title")

        if title_tag and title_tag.get_text(strip=True):
            title = title_tag.get_text(strip=True)
        else:
            title = file

        # -------------------------
        # TEXT
        # -------------------------
        text = extract_text(html)

        if not text.strip():
            continue

        # -------------------------
        # RELATIVNÍ URL
        # -------------------------
        rel_path = os.path.relpath(path, WEB_DIR).replace("\\", "/")

        index.append({
            "title": title,
            "url": rel_path,
            "text": text[:3000]
        })

# =========================
# ULOŽENÍ JSON
# =========================
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

print(f"Hotovo: {OUTPUT_FILE}")
print(f"Stránek indexováno: {len(index)}")
