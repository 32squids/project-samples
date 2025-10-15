import requests
import bs4 as bsoup
import random

# Get a requests object with the link to is:commander on Scryfall
commanders_link = requests.get("https://scryfall.com/search?q=is%3Acommander&unique=cards&as=text&order=edhrec&dir=")
soup = bsoup.BeautifulSoup(commanders_link.content, "html.parser")

# Get the names of the commanders
commander_names = []
for tag in soup.find_all("h6", class_ = "card-text-title"):
    # Get the text after the tag
    commander_title = tag.get_text()
    # Strip white space from commander title
    commander_title = commander_title.strip()
    commander_names += [commander_title]

# Pick a random commander
commander_spot = random.randint(0, 59) # 60 cards per page
commander_full = commander_names[commander_spot]


# Get mana cost
i = -1
full_mana_cost = ""
while commander_full[i] != " ":
    full_mana_cost = commander_full[i] + full_mana_cost
    i -= 1

# Get color identity
ID = ""
for letter in full_mana_cost:
    if letter in ["W", "U", "B", "R", "G"]:
        ID += letter

# Get commander name alone. i is the same as when we got the mana cost. By doing the mana cost first, it allows us to go
# from the back to the front, until we hit a non-whitespace character
while commander_full[i] == " ":
    i -= 1
commander = commander_full[:i]
print(commander)

# Initialize full deck list
deck = "1 " + commander + "\n"\
        + "1 Sol Ring\n"\
        + "1 Arcane Signet\n"\
        + "1 Swiftfoot Boots\n"\
        + "1 Mind Stone\n"\
        + "1 Lightning Greaves\n"\
        + "1 Fellwar Stone\n"

# Get top 60 cards by first going to the link with the correct search terms
cards_link = requests.get(f"https://scryfall.com/search?q=id%3C%3D{ID}+-id%3Ac+-t%3Aland&unique=cards&as=text&order=edhrec&dir=asc")
# Create soup object
soup = bsoup.BeautifulSoup(cards_link.content, "html.parser")
# Find all card titles
tags = soup.find_all("h6", class_ = "card-text-title")
# Create a list of cards
cards = []
for tag in tags:
    # Get card text and strip white space
    card = tag.get_text()
    card = card.strip()
    cards += [card]

# Get the card name alone, and add it to the decklist.
for card in cards:
    i = -1
    while card[i] != " ": # Strip non-essential non-whitespace characters
        i -= 1
    card = card[:i]
    card = card.strip()
    if card != commander:
        deck += "1 " + card + "\n"


# Create land balance
total_w, total_u, total_b, total_r, total_g = 0,0,0,0,0
total_lands = [total_w, total_u, total_b, total_r, total_g]
for color in ID:
    if color == "W":
        total_w += 34//len(ID)
    if color == "U":
        total_u += 34//len(ID)
    if color == "B":
        total_b += 34//len(ID)
    if color == "R":
        total_r += 34//len(ID)
    if color == "G":
        total_g += 34//len(ID)

total = total_w + total_u + total_b + total_r + total_g
if total != 34:
    for color in ID:
        while total < 34:
            if color == "W":
                total_w += 1
            if color == "U":
                total_u += 1
            if color == "B":
                total_b += 1
            if color == "R":
                total_r += 1
            if color == "G":
                total_g += 1
            total = total_w + total_u + total_b + total_r + total_g
        while total > 34:
            if color == "W":
                total_w -= 1
            if color == "U":
                total_u -= 1
            if color == "B":
                total_b -= 1
            if color == "R":
                total_r -= 1
            if color == "G":
                total_g -= 1
            total = total_w + total_u + total_b + total_r + total_g

# Add the basic lands to the deck
land_types = ["Plains", "Island", "Swamp", "Mountain", "Forest"]
lands = ""

for i, land in enumerate([total_w, total_u, total_b, total_r, total_g]):
    if land:
        lands += f"{land} {land_types[i]}\n"
deck += lands
print(deck)