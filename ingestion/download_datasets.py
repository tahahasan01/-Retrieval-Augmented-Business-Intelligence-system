import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Ensure directories exist
os.makedirs("data/structured", exist_ok=True)
os.makedirs("data/unstructured", exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0"}

# 1A. Global CO2 Emissions by Country (CSV)
co2_url = 'https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv'
co2_df = pd.read_csv(co2_url)
co2_df.to_csv("data/structured/global_co2_emissions.csv", index=False)
print("Saved global_co2_emissions.csv")

# 1B. Titanic Dataset (CSV)
titanic_url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'
titanic_df = pd.read_csv(titanic_url)
titanic_df.to_csv("data/structured/titanic.csv", index=False)
print("Saved titanic.csv")

# 1C. Nobel Prize Winners (HTML Table)
nobel_url = 'https://en.wikipedia.org/wiki/List_of_Nobel_laureates'
nobel_response = requests.get(nobel_url, headers=headers)
nobel_response.raise_for_status()
nobel_tables = pd.read_html(nobel_response.text)
# Save the first table as an example
nobel_tables[0].to_csv("data/structured/nobel_laureates.csv", index=False)
print("Saved nobel_laureates.csv")

# 2A. Wikipedia Article (HTML)
ai_url = 'https://en.wikipedia.org/wiki/Artificial_intelligence'
ai_response = requests.get(ai_url, headers=headers)
ai_response.raise_for_status()
with open("data/unstructured/artificial_intelligence.html", "w", encoding="utf-8") as f:
    f.write(ai_response.text)
print("Saved artificial_intelligence.html")

# 2B. Alice in Wonderland (TXT)
alice_url = 'https://www.gutenberg.org/cache/epub/11/pg11.txt'
alice_response = requests.get(alice_url, headers=headers, verify=False)
alice_response.raise_for_status()
with open("data/unstructured/alice_in_wonderland.txt", "w", encoding="utf-8") as f:
    f.write(alice_response.text)
print("Saved alice_in_wonderland.txt")

# 2C. US IRS Tax Guide (PDF)
pdf_url = 'https://www.irs.gov/pub/irs-pdf/p17.pdf'
pdf_response = requests.get(pdf_url, headers=headers)
pdf_response.raise_for_status()
with open("data/unstructured/irs_tax_guide.pdf", "wb") as f:
    f.write(pdf_response.content)
print("Saved irs_tax_guide.pdf") 