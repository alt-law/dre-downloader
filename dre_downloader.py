from bs4 import BeautifulSoup
import urllib
import requests

"""
    output objetctive:

    {
    "law-id": {
        "title": "the law's title"
        "document-type": "decreto-lei" # might alctualy involve extra processing
        "url": "www.dre.pt/....../"
        "tags": ['Economics','Agriculture',...]
        "description": "description of the law"
        }
    }

"""


##### Extra functions #####
def remove_linguagem_clara(documents):
    i = 0
    while i < len(documents):
        if documents[i].find('a', {"class": "clara"}):
            documents.pop(i) # remove linguagem clara
            continue         # continuma se incrementar i

        i = i + 1 # passa ao elemento seguinte

    return documents


def csv_to_list(string):
    """ converts a string of csv to a list of strings """
    tail = head = 0
    lst = []
    while head < len(string):
        if string[head] != ',':
            head += 1
        else:
            lst.append(string[tail+1:head])
            tail = head + 1 # to discount for the " " after the comma
            head = head + 1
    lst.append(string[tail+1:head-1])

    return lst


##### Script #####
urlbase = "https://dre.pt/web/guest/home/-/dre/calendar/normal/I"

html = urllib.request.urlopen(urlbase + "?day=2017-06-09")
page = BeautifulSoup(html, "lxml")

# obtains all law titles
documents = page.findAll("h4",  {"class":"headerdiploma"})
documents = remove_linguagem_clara(documents)
summaries = page.findAll("div", {"class":"summary"})
tags = page.findAll("div", {"class":"author"})

for doc in range(len(documents)):
    print(documents[doc].find('a').text.replace("\t", "").replace("\n", ""))
    print(summaries[doc].text.replace("\t", "").replace("\n", ""))
    print(csv_to_list(tags[doc].text.replace("\t", "").replace("\n", "")))
    print("\n")
