# -*- coding: utf8 -*-
import nltk
import urllib2
import re
import fractions
import json
from bs4 import BeautifulSoup
from vegTransformation import vegsub
from vegTransformation import meatsub
from vegTransformation import vegrank

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
    recipe_url = urllib2.urlopen(link)
    recipe_html = recipe_url.read()
    soup = BeautifulSoup(recipe_html)

    for quantity, ingredient in zip(soup.find_all(id='lblIngAmount'), soup.find_all(id='lblIngName')):
        newIngredient = Ingredient()
        
        quantity = quantity.contents[0].encode('utf-8').split(' ', 1)        
        newIngredient.quantity = float(fractions.Fraction(quantity[0]))
        if len(quantity) > 1:
            newIngredient.measurement = quantity[1].lower()
            
        ingredient = (ingredient.contents)[0].encode('utf-8').lower().split(', ',1)
        # attempting nltk pos tagger, but it's really bad with short phrases
##        tags = nltk.pos_tag(nltk.word_tokenize(ingredient))
##        for (word, pos) in tags:
##            if "NN" in pos:               
            
        newIngredient.name = ingredient[0]
        if len(ingredient) > 1:
            newIngredient.preparation = ingredient[1]
        
        ingname = " " + newIngredient.name
        for liquid in liquid_list:
            if (" " + liquid) in ingname:
                newIngredient.itype = 'liquid'
                break
            
        if newIngredient.itype == '':
            for spice in spice_list:
                if (" " + spice) in ingname:
                    newIngredient.itype = 'spice'
                    break
                
        if newIngredient.itype == '':
            for veg in veg_list:
                if (" " + veg) in ingname:
                    newIngredient.itype = 'veggie'
                    break
                
        if newIngredient.itype == '':
            for oil in oil_list:
                if (" " + oil) in ingname:
                    newIngredient.itype = 'oil'
                    break
                
        if newIngredient.itype == '':
            for meat in meat_list:
                if (" " + meat) in ingname:
                    newIngredient.itype = 'meat'
                    break
                
        recipe.ingredients.append(newIngredient)
        #ingredients.append(((quantity.contents)[0].encode('utf-8'), (ingredient.contents)[0].encode('utf-8')))

    #for ingredient in recipe.ingredients:
        #print ingredient.quantity, ";", ingredient.measurement, ";", ingredient.preparation, ";", ingredient.name, ";", ingredient.itype

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

    #print recipe.cooking_methods
    #print recipe.preparation_methods
    #print recipe.tools

def toVeg(recipe):
    if isVeg(recipe):
        print "Recipe is already vegetarian."
        return
    else:
        for ingredient in recipe.ingredients:
            if ingredient.itype == 'meat':
                for key in sorted(meatsub.keys()):
                    if key in ingredient.name:
                        print meatsub[key]
                        break
                #print "replace with veg"
            elif ingredient.itype == 'liquid' and 'vegetable' not in ingredient.name:
                if "stock" in ingredient.name:
                    print "vegetable stock"
                else:
                    print "vegetable broth"
                #print "replace soup stock with vegetable"
            else:
                print ingredient.name

def toMeat(recipe):
    if not isVeg(recipe):
        print "Recipe already has meat in it."
        return
    else:
        rank = 100
        repkey = ''
        reping = ''
        for ingredient in recipe.ingredients:
            for key in vegrank.keys():
                if key in ingredient.name and vegrank[key] < rank:
                    rank = vegrank[key]
                    repkey = key
                    reping = ingredient.name
        for ingredient in recipe.ingredients:
            if ingredient.name == reping:
                print vegsub[repkey]
            else:
                print ingredient.name
        if rank < 100:
            "Recipe was not modified. There are no common meat substitutes in the recipe."

def isVeg(recipe):
    for ingredient in recipe.ingredients:
        if ingredient.itype is 'meat' or (ingredient.itype is 'liquid' and 'vegetable' not in ingredient.name):
            return False
    return True

def printJson(recipe):
    jsonoutput = {}
    ingList = []
    for ingredient in recipe.ingredients:
        tempdict = {}
        tempdict["name"] = ingredient.name
        tempdict["quantity"] = ingredient.quantity
        tempdict["measurement"] = ingredient.measurement
        tempdict["descriptor"] = ingredient.descriptor
        tempdict["preparation"] = ingredient.preparation
        ingList.append(tempdict)
    jsonoutput["ingredients"] = ingList
    jsonoutput["cooking method"] = recipe.cooking_methods
    jsonoutput["cooking tools"] = recipe.tools
    print json.dumps(jsonoutput, indent=2, separators=(',',': '))

def main():
    link = raw_input("What is the URL for the recipe? ")
    recipe = Recipe()
    parse(link, recipe)
    printJson(recipe)
    toVeg(recipe)
    toMeat(recipe)

main()

#text = nltk.word_tokenize("chopped fresh parsley")
#print nltk.pos_tag(text)
