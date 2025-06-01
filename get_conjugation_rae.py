# pip install cloudscraper beautifulsoup4
import cloudscraper
from bs4 import BeautifulSoup

BASE  = "https://dle.rae.es"
verb  = "amar"

# 1️⃣  create a Cloudflare-aware session
scraper = cloudscraper.create_scraper(           # same API as requests
    browser={"browser": "firefox", "platform": "windows", "desktop": True},
    delay=1.0,                                   # polite throttle (seconds)
)

# 2️⃣  grab the conjugation fragment
table_html = scraper.get(f"{BASE}/{verb}", timeout=10).text
soup       = BeautifulSoup(table_html, "html.parser")

# 3️⃣  identical parsing loop
data = {}
# for block in soup.select("table"):
#     mood = block.find_previous("h2").get_text(strip=True)
#     for row in block.select("tr"):
#         cells = [c.get_text(" ", strip=True) for c in row.select("th,td")]
#         if len(cells) == 1:
#             tense = cells[0]
#             data.setdefault(mood, {})[tense] = {}
#         elif cells:
#             person, *forms = cells
#             data[mood][tense][person] = forms[0]

print(soup.body.prettify())   # or json.dumps(data, ensure_ascii=False, indent=2)
