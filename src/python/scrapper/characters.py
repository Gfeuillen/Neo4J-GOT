import requests
from bs4 import BeautifulSoup
import pandas as pd

print("hi")

charactersURL = "https://en.wikipedia.org/wiki/List_of_Game_of_Thrones_characters?oldformat=true"

r = requests.get(charactersURL,  stream=True)
soup = BeautifulSoup(r.text, 'html.parser')

# Find the tables
tables = soup.find_all("table", attrs={"class":"wikitable"})

# The two firsts ones are of interest
mainCast = tables[0]
supportingCast = tables[1]

# Get each line
mainCastLines = mainCast.find_all("tr")
supportingCastLines = supportingCast.find_all("tr")

print(mainCastLines[2].contents)

# For each line, extract name
characterNames = [line.contents[3].text for line in mainCastLines[2:] + supportingCastLines[2:]]

rows = [name.split(" ") for name in characterNames]
maxLength = max([len(row) for row in rows])

characterNamesDf = pd.DataFrame(rows, columns=["name{:d}".format(i) for i in range(maxLength)])

characterNamesDf.to_csv("../../../data/character_names.csv", index=False)

