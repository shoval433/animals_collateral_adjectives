#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re
url = "https://en.wikipedia.org/wiki/List_of_animal_names"
response = requests.get(url)


# Check that each collateral_adjective contains only one name
def checkAdjective(name):
    name=remove_non_letters_forAdjective(name)
    #(+ is one or more) So I replaced all the spaces with one space
    clean_name = re.sub(' +', ' ', name)
    listName=clean_name.split(' ')
    if len(listName)>1:
        return listName
    else:
        return name
    
def remove_non_letters_forAdjective(string):
    letters_only = ""
    trash=['[',']','(',')']
    flag_insert=True
    trashIndex=0
    for char in string:
        if char.isalpha() and flag_insert:
            letters_only += char
        # takes everything inside the brackets and ignores it and puts spaces
        elif char in trash and flag_insert:
            flag_insert=False
            trashIndex=trash.index(char)+1
        elif char == trash[trashIndex] and flag_insert is False:
            flag_insert=True
            letters_only += " "
        else:
            letters_only += " "
    return letters_only.strip()

def remove_non_letters(string):
    letters_only = ""
    flag=True
    for char in string:
        if char ==',':
            return string
        if char.isalpha():
            letters_only += char
        # If there is an animal only if two words it will pass
        elif char==' ':
            if flag:
                flag=False
                letters_only += char
            else:
                return letters_only.strip()
        else:
            return letters_only.strip()
    return letters_only.strip()

def checkName(name):
    # Removes everything that is not letters
    name=remove_non_letters(name)
    name=name.replace("family", "").strip()
    #converts the name to a list with has several names
    if "," in name:
       name= [n.strip() for n in name.split(",")]
    return name

def addToDictionary(Animals,collateral_adjective,animal):
    
    if collateral_adjective not in Animals:
        Animals[collateral_adjective]=list()
    animal=checkName(animal)
    if isinstance(animal, list):
        for a in animal:
            Animals[collateral_adjective].append(a)
    else:
        Animals[collateral_adjective].append(animal)
    return Animals
def main(response):
    # start souping
    soup = BeautifulSoup(response.content, "html.parser")
    Animals={}
    #go to big table
    table = soup.find_all("table", {"class": "wikitable"})[1]
    l=[]
    # run in n(o) (one for) Because we know exactly where the names are (if it is not possible to go over column 0)
    for row in table.find_all("tr")[1:]:# starting from one 
        cells = row.find_all("td")
        #not to go out of range
        if len(cells) < 6:
            continue
        # handle animals without collateral -> others
        elif "?" in cells[5].text.strip() :
            animal = cells[0].text.strip()
            collateral_adjective = "others"
            Animals=addToDictionary(Animals,collateral_adjective,animal)
        else:
            
            animal = cells[0].text.strip()
            collateral_adjective = cells[5].text.strip()
            if len(collateral_adjective) >2:
                collateral_adjective=checkAdjective(collateral_adjective)
                if isinstance(collateral_adjective, list):
                    for one_collateral_adjective in collateral_adjective:
                        Animals= addToDictionary(Animals,one_collateral_adjective,animal)
                    # print(collateral_adjective+"->"+ str(Animals[collateral_adjective]))   
                else:
                    Animals= addToDictionary(Animals,collateral_adjective,animal)
                    # print(collateral_adjective+"->"+ str(Animals[collateral_adjective]))


    #go to first table
    table = soup.find("table", {"class": "wikitable"})

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        collateral_adjective = cells[5].text.strip()
        animal = cells[6].text.strip()
        if len(collateral_adjective) >2:
                collateral_adjective=checkAdjective(collateral_adjective)
                if isinstance(collateral_adjective, list):
                    for one_collateral_adjective in collateral_adjective:
                        Animals= addToDictionary(Animals,one_collateral_adjective,animal)
                    
                else:
                    Animals= addToDictionary(Animals,collateral_adjective,animal)
                   
    Animals=remove_duplicates(Animals)
    for key, values in Animals.items():
        print(key + ": " + ", ".join(values))

def remove_duplicates(dict_obj):
    result_dict = {}
    for key, value in dict_obj.items():
        unique_values = set()
        for val in value:
            if val.lower() not in unique_values:
                unique_values.add(val.lower())
                result_dict.setdefault(key, []).append(val)
    return result_dict

response = requests.get(url)
if response.ok:
    main(response)
else:
    print("There was an error with the url : " +url)
