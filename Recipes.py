# -*- coding: utf8 -*-
import nltk
import urllib2
import re
import fractions
from bs4 import BeautifulSoup

class Recipe:
    ingredients = [] # list of Ingredients
    directions = [] # list of Steps
    cooking_methods = []
    preparation_methods = []
    tools = []

class Ingredient:
    quantity = 1.0
    measurement = ''
    name = 'none'
    descriptor = ''
    preparation = ''
    itype = ''

class Step:
    text = []
    cooking_methods = []
    tools = []
    ingredients = []
    cooking_time = 0.0

def Parse():
    cmp_list = open('cookingmethods_primary.txt', 'rb').read().split('\r\n')
    cms_list = open('cookingmethods_secondary.txt', 'rb').read().split('\r\n')

    recipe_url = urllib2.urlopen("http://allrecipes.com/Recipe/Worlds-Best-Lasagna/Detail.aspx?evt19=1")
    recipe_html = recipe_url.read()
    soup = BeautifulSoup(recipe_html)

    recipe = Recipe()

    for quantity, ingredient in zip(soup.find_all(id='lblIngAmount'), soup.find_all(id='lblIngName')):
        quantity = quantity.contents[0].encode('utf-8').split(' ', 1)
        newIngredient = Ingredient()
        newIngredient.quantity = float(fractions.Fraction(quantity[0]))
        if len(quantity) > 1:
            newIngredient.measurement = quantity[1]
        newIngredient.name = (ingredient.contents)[0].encode('utf-8')
        recipe.ingredients.append(newIngredient)
        #ingredients.append(((quantity.contents)[0].encode('utf-8'), (ingredient.contents)[0].encode('utf-8')))

    for ingredient in recipe.ingredients:
        print ingredient.quantity, ingredient.measurement, ingredient.name

    directions_html = soup.find_all(class_='directLeft')
    directions_span = directions_html[0].select('span')
    for direction in directions_span:
        direction = re.sub(r'<.*?>', "", str(direction))
        recipe.directions.append(direction)

    print recipe.directions

    for direction in recipe.directions:
        for sentence in direction.split('.'):
            for word in cmp_list:
                sentence2 = sentence.lower()
                if word in sentence2 and word not in recipe.cooking_methods:
                    recipe.cooking_methods.append(word)
            for word in cms_list:
                sentence2 = sentence.lower()
                if word in sentence2 and word not in recipe.preparation_methods:
                    recipe.preparation_methods.append(word)

    print recipe.cooking_methods
    print recipe.preparation_methods

def ToVeg():
    print "not done yet"

def FromVeg():
    print "not done yet"

#text = nltk.word_tokenize("chopped fresh parsley")
#print nltk.pos_tag(text)
