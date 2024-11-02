#!/usr/bin/env python3
from os import listdir, makedirs, walk
from os.path import isfile, join, exists, basename

challenge_categories = list(set([
    "Azure", "OnSite", "boot2root", "Crypto", "Forensics", "Misc", "Pwn", "RealWorld", "Reversing", "Web"
    ]))
challenge_categories = sorted(challenge_categories, key=str.lower)
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

"""

for category in listdir("./writeups"):
    if category.startswith(".") or isfile(category):
        continue
    text += f'### {category}\n'
    for chall in listdir(f'./writeups/{category}'):
        text += (f' - **{chall}**\n')
        print(text)
        for writeup in next(walk(f'./writeups/{category}/{chall}'))[1]:
            url = f'/writeups/{category}/{chall}/{writeup}'.replace(' ', '%20')
            text += f"\t - [{writeup}]({url})  \n"
            print(text)

with open('README.md', 'w') as f:
    f.write(text)
