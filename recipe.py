# pylint: disable=missing-docstring,line-too-long
import sys
from os import path
from turtle import ht
from bs4 import BeautifulSoup
import requests
import csv

def parse(html):
    ''' return a list of dict {name, difficulty, prep_time} '''
    soup = BeautifulSoup(html, "html.parser")
    parse_result = []
    for recipe in soup.find_all('div', class_= 'recipe-details'):
        parse_result.append(parse_recipe(recipe))
    return parse_result

def parse_recipe(article):
    ''' return a dict {name, difficulty, prep_time} modelising a recipe'''
    prep_time = article.find("span", class_= "recipe-cooktime")
    difficulty = article.find("span", class_= "recipe-difficulty")
    name = article.find("p", class_= "recipe-name")
    result = {"name": name.text, "difficulty": difficulty.text, "prep_time": prep_time.text}
    return result

def write_csv(ingredient, recipes):
    ''' dump recipes to a CSV file `recipes/INGREDIENT.csv` '''
    file = open(f'recipes/{ingredient}.csv', 'w', newline ='')
    with file:
        header = ['name', 'difficulty', 'prep_time']
        writer = csv.DictWriter(file, fieldnames = header)
        writer.writeheader()
        for recipe in recipes:
            writer.writerow(recipe)

def scrape_from_internet(ingredient, start=1):
    ''' Use `requests` to get the HTML page of search results for given ingredients. '''
    response = requests.get(f"https://recipes.lewagon.com/?search[query]={ingredient}&page={start}")

    if len(response.history) == 0:
        return response.text
    else:
        return ""

def scrape_from_file(ingredient):
    file = f"pages/{ingredient}.html"
    if path.exists(file):
        return open(file)
    print("Please, run the following command first:")
    print(f'curl -g "https://recipes.lewagon.com/?search[query]={ingredient}" > pages/{ingredient}.html')
    sys.exit(1)


def main():
    if len(sys.argv) > 1:
        ingredient = sys.argv[1]
        # TODO: Replace scrape_from_file with scrape_from_internet and implement pagination (more than 2 pages needed)
        recipes = []
        for i in range(1,4):
            html = scrape_from_internet(ingredient, i)
            if html == "":
                break
            each_recipes = parse(html)

            recipes = recipes + each_recipes
        write_csv(ingredient, recipes)
    else:
        print('Usage: python recipe.py INGREDIENT')
        sys.exit(0)


if __name__ == '__main__':
    main()
