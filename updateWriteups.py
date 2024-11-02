#!/usr/bin/env python3
from os import listdir, makedirs, walk
from os.path import isfile, join, exists, basename
map_challenge_category_name = {
    "Boot2root": "boot2root",
    "Onsite": "OnSite",
    "Realworld": "RealWorld"}
challenge_categories = []
writeups = ""
for category in listdir("./writeups"):
    if category.startswith(".") or isfile(category):
        continue
    challenge_category = map_challenge_category_name.get(category.capitalize(), category.capitalize())
    challenge_categories.append(challenge_category)
    writeups += f'### {category}\n'
    for chall in listdir(f'./writeups/{category}'):
        chall_url = f'/writeups/{category}/{chall}'.replace(' ', '%20')
        writeups += (f' - **[{chall}]({chall_url})**\n')
        print(writeups)
        for writeup in next(walk(f'./writeups/{category}/{chall}'))[1]:
            wripteup_url = f'/writeups/{category}/{chall}/{writeup}'.replace(' ', '%20')
            writeups += f"\t - [{writeup}]({wripteup_url})  \n"

challenge_categories = sorted(list(set(challenge_categories)), key=str.lower)
table_of_content = ""
for challenge_category in challenge_categories:
    table_of_content += f"- [{challenge_category}](#{challenge_category.lower()})\n"

text = f"""
# Equinor CTF 2024
Educational guides, writeups and challenges resources for the 2024 Equinor CTF


## Table of content

{table_of_content}
---

## Writeups

{writeups}
"""

with open('README.md', 'w') as f:
    f.write(text)
