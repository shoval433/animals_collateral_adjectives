
# animals_collateral_adjectives

Using the page https://en.wikipedia.org/wiki/List_of_animal_names, write a python program that will output all of the “collateral adjectives” and all of the “animals” which belong to it. 


## BeautifulSoup Documentation

[Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)


## Acknowledgements

 - [External material that helped me](https://www.geeksforgeeks.org/beautifulsoup-nextsibling/)

## Deployment

To deploy this project run

```bash
  pip install -r requirements.txt
  python3 main.py
```


## Demo

http://localhost:5000


## References to scripting data collection:
### animal:
The treatment of the animal names in that each animal consists of 2 words, cleaning of all the spelling that are not letters, and arrangement of if there is a capital letter in the middle of a word.
If the name contained family he was deleted.
### collateral_adjectives:
It was decided that if there is more than one, we will enter the animal for each one separately, put out parentheses and special characters.
Animals that were without collateral_adjectives enter the other category.
