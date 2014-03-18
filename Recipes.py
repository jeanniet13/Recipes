# -*- coding: utf8 -*-
import nltk
import urllib2
import re
import fractions
from bs4 import BeautifulSoup

cmp_list = open('cookingmethods_primary.txt', 'rb').read().split('\r\n')
cms_list = open('cookingmethods_secondary.txt', 'rb').read().split('\r\n')
tool_list = open('tools.txt','rb').read().split('\r\n')
veg_list = open('vegetables.txt', 'rb').read().split('\r\n')
meat_list = open('meat.txt', 'rb').read().split('\r\n')
oil_list = open('oil.txt', 'rb').read().split('\r\n')
liquid_list = open('liquid.txt', 'rb').read().split('\r\n')
spice_list = open('spices.txt', 'rb').read().split('\r\n')

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
    itype = '' #meat, spice, liquid, veggie, oil

class Step:
    text = []
    cooking_methods = []
    tools = []
    ingredients = []
    cooking_time = 0.0

def parse(link, recipe):
    recipe_url = urllib2.urlopen("http://allrecipes.com/Recipe/Quinoa-and-Black-Beans/Detail.aspx?evt19=1")
    recipe_html = recipe_url.read()
    soup = BeautifulSoup(recipe_html)

    for quantity, ingredient in zip(soup.find_all(id='lblIngAmount'), soup.find_all(id='lblIngName')):
        quantity = quantity.contents[0].encode('utf-8').split(' ', 1)
        newIngredient = Ingredient()
        newIngredient.quantity = float(fractions.Fraction(quantity[0]))
        if len(quantity) > 1:
            newIngredient.measurement = quantity[1]
        newIngredient.name = (ingredient.contents)[0].encode('utf-8')
        for liquid in liquid_list:
            if liquid.lower() in newIngredient.name.lower():
                newIngredient.itype = 'liquid'
                break
        if newIngredient.itype == '':
            for spice in spice_list:
                if spice.lower() in newIngredient.name.lower():
                    newIngredient.itype = 'spice'
                    break
        if newIngredient.itype == '':
            for veg in veg_list:
                if veg.lower() in newIngredient.name.lower():
                    newIngredient.itype = 'veggie'
                    break
        if newIngredient.itype == '':
            for oil in oil_list:
                if oil.lower() in newIngredient.name.lower():
                    newIngredient.itype = 'oil'
                    break
        if newIngredient.itype == '':
            for meat in meat_list:
                if meat.lower() in newIngredient.name.lower():
                    newIngredient.itype = 'meat'
                    break
        recipe.ingredients.append(newIngredient)
        #ingredients.append(((quantity.contents)[0].encode('utf-8'), (ingredient.contents)[0].encode('utf-8')))

    for ingredient in recipe.ingredients:
        print ingredient.quantity, ingredient.measurement, ingredient.name, ",", ingredient.itype

    directions_html = soup.find_all(class_='directLeft')
    directions_span = directions_html[0].select('span')
    for direction in directions_span:
        direction = re.sub(r'<.*?>', "", str(direction))
        recipe.directions.append(direction)

    ##print recipe.directions

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
            for tool in tool_list:
                sentence2 = sentence.lower()
                tool = tool.lower()
                if tool in sentence2 and tool not in recipe.tools:
                    recipe.tools.append(tool)

    print recipe.cooking_methods
    print recipe.preparation_methods
    print recipe.tools

def toVeg(recipe):
    if isVeg(recipe):
        print "Recipe is already vegetarian."
        return
    else:
        meatveg = open('toVeg.txt', 'rb').read().split('\r\n')
        for ingredient in recipe.ingredients:
            if ingredient.itype == 'meat':
                print "replace with veg"
            elif ingredient.itype == 'liquid' and 'vegetable' not in ingredient.name.lower():
                print "replace soup stocket with vegetable"
        print "not done yet"

def toMeat(recipe):
    vegmeat = open('toMeat.txt', 'rb').read().split('\r\n')
    print "not done yet"

def isVeg(recipe):
    for ingredient in recipe.ingredients:
        if ingredient.itype is 'meat' or (ingredient.itype is 'liquid' and 'vegetable' not in ingredient.name):
            return False
    return True

def main():
    link = raw_input("What is the URL for the recipe? ")
    recipe = Recipe()
    parse(link, recipe)
    toVeg(recipe)
    toMeat(recipe)

main()

#text = nltk.word_tokenize("chopped fresh parsley")
#print nltk.pos_tag(text)
