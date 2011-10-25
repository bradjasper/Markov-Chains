#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pull company names from CrunchBase and write to a text file
import string
import requests
from BeautifulSoup import BeautifulSoup

def names_from_letter(letter):
    print "Getting CrunchBase names starting with '%s'" % letter
    req = requests.get("http://www.crunchbase.com/companies?c=" + letter)
    soup = BeautifulSoup(req.content)
    items = soup.find("table", **{"class": "col2_table_listing"}).findAll("li")
    return (item.text for item in items)


def all_names():
    for letter in string.ascii_lowercase:
        for name in names_from_letter(letter):
            yield name

if __name__ == "__main__":
    names = list(all_names())
    with open("crunchbase.txt", "w") as file:
        file.write(" ".join(names).encode("utf-8"))

    print "Wrote %d names" % len(names)
