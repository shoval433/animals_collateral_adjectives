#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re
from flask import Flask, render_template
# CONST
MINIMAL_NUMBER_OF_CELLS_IN_RELEVANT_ROW = 6
COLLATERAL_ADJECTIVE_CELLS = 5
ANIMAL_CELLS_TABLE1 = 0
ANIMAL_CELLS_TABLE2 = MINIMAL_NUMBER_OF_CELLS_IN_RELEVANT_ROW
NUMBER_OF_WORDS = 2
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
    brackets=['[',']','(',')']
    flag_insert=True
    bracketsIndex=0
    for char in string:
        if char.isalpha() and flag_insert:
            letters_only += char
        # takes everything inside the brackets and ignores it and puts spaces
        elif char in brackets and flag_insert:
            flag_insert=False
            bracketsIndex=brackets.index(char)+1
        elif char == brackets[bracketsIndex] and flag_insert is False:
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

def Capital_letters_in_name(name):
    # Delete all the animals that have a capital letter in the middle of a word
    for i in range(1, len(name)):
        if name[i].isupper():
            name = name[:i]
            break
    return name 

def checkName(name):
    # Removes everything that is not letters
    name=remove_non_letters(name)
    name=name.replace("family", "").strip()
    name=Capital_letters_in_name(name)
    #converts the name to a list with has several names
    if "," in name:
       name= [n.strip() for n in name.split(",")]
    return name

def addToDictionary(Animals,collateral_adjective,animal):
    if collateral_adjective not in Animals:
        Animals[collateral_adjective.capitalize()]=list()
    animal=checkName(animal)
    if isinstance(animal, list):
        for a in animal:
            Animals[collateral_adjective.capitalize()].append(a)
    else:
        Animals[collateral_adjective.capitalize()].append(animal)
    return Animals

def wikiAnimal():
    # start souping
    url = "https://en.wikipedia.org/wiki/List_of_animal_names"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    Animals={}
    #go to big table
    table = soup.find_all("table", {"class": "wikitable"})[1]
    l=[]
    # run in O(n) (one for) Because we know exactly where the names are (if it is not possible to go over column 0)
    for row in table.find_all("tr")[1:]:# starting from one 
        cells = row.find_all("td")
        #not to go out of range
        if len(cells) < MINIMAL_NUMBER_OF_CELLS_IN_RELEVANT_ROW:
            continue
        # handle animals without collateral -> others
        elif "?" in cells[COLLATERAL_ADJECTIVE_CELLS].text.strip() :
            animal = cells[ANIMAL_CELLS_TABLE1].text.strip()
            collateral_adjective = "others"
            Animals=addToDictionary(Animals,collateral_adjective,animal)
        else:
            # handle many in one <tr><br>
            ####################################################################
            # <td>anguine<br>elapine<br>ophidian<br>serpentine<br>viperine</td>
            manyIn=cells[COLLATERAL_ADJECTIVE_CELLS].find_all("br")
            flag_isOne=True
            if len(manyIn) > 0:## Here we know that there are some names separated by <br>
                collateral_adjectives = []
                for tag in cells[COLLATERAL_ADJECTIVE_CELLS].contents:
                    if tag.name == "br":
                        try:
                            collateral_adjectives.append(tag.nextSibling.strip())
                        except:
                            continue
                flag_isOne=False
                collateral_adjective= ' '.join(collateral_adjectives)
            #####################################################################
            animal = cells[ANIMAL_CELLS_TABLE1].text.strip()
            if flag_isOne:
                collateral_adjective = cells[COLLATERAL_ADJECTIVE_CELLS].text.strip()
            if len(collateral_adjective) > NUMBER_OF_WORDS:
                collateral_adjective=checkAdjective(collateral_adjective)
                if isinstance(collateral_adjective, list):
                    for one_collateral_adjective in collateral_adjective:
                        Animals= addToDictionary(Animals,one_collateral_adjective,animal)
                      
                else:
                    Animals= addToDictionary(Animals,collateral_adjective,animal)
                    


    #go to first table
    table = soup.find("table", {"class": "wikitable"})

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) < MINIMAL_NUMBER_OF_CELLS_IN_RELEVANT_ROW:
            continue
        collateral_adjective = cells[COLLATERAL_ADJECTIVE_CELLS].text.strip()
        animal = cells[ANIMAL_CELLS_TABLE2].text.strip()
        if len(collateral_adjective) > NUMBER_OF_WORDS:
                collateral_adjective=checkAdjective(collateral_adjective)
                if isinstance(collateral_adjective, list):
                    for one_collateral_adjective in collateral_adjective:
                        Animals= addToDictionary(Animals,one_collateral_adjective,animal)
                    
                else:
                    Animals= addToDictionary(Animals,collateral_adjective,animal)
                   
    Animals=remove_duplicates(Animals)
    return Animals

def remove_duplicates(dict_obj):
    result_dict = {}
    for key, value in dict_obj.items():
        unique_values = set()
        for val in value:
            if val.lower() not in unique_values:
                unique_values.add(val.lower())
                result_dict.setdefault(key, []).append(val)
    return result_dict

app = Flask(__name__)

@app.route('/')
def display_animals():
    animals = wikiAnimal()
    headers = ["Collateral_Adjective", "Animal"]
    rows = []
    for animal, classification in animals.items():
        rows.append([animal, ", ".join(classification)])
    return render_template('animals.html', headers=headers, rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
