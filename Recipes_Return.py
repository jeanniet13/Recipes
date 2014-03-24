# -*- coding: utf8 -*-
## This version has no recipe transformation functionality. See Recipes.py for that.
import urllib2
import re
import fractions
import json
import random
from bs4 import BeautifulSoup

from vegTransformation import vegsub
from vegTransformation import meatsub
from vegTransformation import vegrank

from cuisineTransformation import *

from LowFatTransformation import lfingsub
from LowFatTransformation import lfcooksub
from LowFatTransformation import hfingsub

cmp_list = open('cookingmethods_primary.txt', 'rb').read().split('\n')
cms_list = open('cookingmethods_secondary.txt', 'rb').read().split('\n')
tool_list = open('tools.txt','rb').read().split('\n')
veg_list = open('vegetables.txt', 'rb').read().split('\n')
meat_list = open('meat.txt', 'rb').read().split('\n')
oil_list = open('oil.txt', 'rb').read().split('\n')
liquid_list = open('liquid.txt', 'rb').read().split('\n')
spice_list = open('spices.txt', 'rb').read().split('\n')
sauce_list = open('sauce.txt', 'rb').read().split('\n')

sour_list = open('sour.txt','rb').read().split('\n')
hot_list = open('hot.txt', 'rb').read().split('\n')
sweet_list = open('sweet.txt', 'rb').read().split('\n')
salty_list = open('salty.txt','rb').read().split('\n')
soft_list = open('soft.txt', 'rb').read().split('\n')
hard_list = open('hard.txt','rb').read().split('\n')
east_asian = open('eastasian.txt','rb').read().split('\n')
italian = open('italian.txt','rb').read().split('\n')
french = open('french.txt','rb').read().split('\n')

class Recipe:
    def __init__(self):
        self._ingredients = [] # list of Ingredients
        self._directions = [] # list of Steps
        self._cooking_methods = []
        self._preparation_methods = []
        self._tools = []        

class Ingredient:
    def __init__(self):
        self._quantity = 0
        self._measurement = ''
        self._name = ''
        self._descriptor = ''
        self._preparation = ''
        self._type = '' #meat, spice, liquid, veggie, oil, sauce

class Step:
    def __init__(self):
        self._text = []
        self._cooking_methods = []
        self._tools = []
        self._ingredients = []
        self._cooking_time = 0.0

def parse(link, recipe):
    recipe_url = urllib2.urlopen(link)
    recipe_html = recipe_url.read()
    soup = BeautifulSoup(recipe_html)

    ings = soup.find_all(id='liIngredient')
    for i in range(0,len(ings)):
        newIngredient = Ingredient()
        quantity = ings[i].select('span#lblIngAmount')
        ingredient = ings[i].select('span#lblIngName')

        if len(quantity) > 0:
            quantity = quantity[0].contents[0].encode('utf-8').split(' ', 1)
            newIngredient._quantity = float(fractions.Fraction(quantity[0]))
            if len(quantity) > 1:
                newIngredient._measurement = quantity[1].lower()
            
        ingredient = ingredient[0].contents[0].encode('utf-8').lower().split(', ',1)
            
        ingname = " " + ''.join(ingredient)
        tempname = ""
        for liquid in liquid_list:
            if (" " + liquid) in ingname:
                newIngredient._type = 'liquid'
                tempname = liquid
                break

        if newIngredient._type == '':
            for sauce in sauce_list:
                if (" " + sauce) in ingname:
                    newIngredient._type = 'sauce'
                    tempname = sauce
                    break
            
        if newIngredient._type == '':
            for spice in spice_list:
                if (" " + spice) in ingname:
                    newIngredient._type = 'spice'
                    tempname = spice
                    break
                
        if newIngredient._type == '':
            for veg in veg_list:
                if (" " + veg) in ingname:
                    newIngredient._type = 'veggie'
                    tempname = veg
                    break

        if newIngredient._type == '':
            for oil in oil_list:
                if (" " + oil) in ingname:
                    newIngredient._type = 'oil'
                    tempname = oil
                    break

        if newIngredient._type == '':
            for meat in meat_list:
                if (" " + meat) in ingname:
                    newIngredient._type = 'meat'
                    tempname = meat
                    break       

        if newIngredient._type == '':
            tempname = ingredient[0]
        
        newIngredient._name = tempname
        #newIngredient.name = ingredient[0]
        if len(ingredient) > 1:
            #newIngredient.preparation = ingredient[1]
            if tempname in ingredient[0]:            
                newIngredient._descriptor = ingredient[0].replace(tempname, "")
                newIngredient._preparation = ingredient[1]
            elif tempname in ingredient[1]:
                newIngredient._descriptor = ingredient[1].replace(tempname, "")
                newIngredient._preparation = ingredient[0]
        elif len(ingredient) == 1:
            if tempname in ingredient[0]:            
                newIngredient._descriptor = ingredient[0].replace(tempname, "")
      
        recipe._ingredients.append(newIngredient)
        #ingredients.append(((quantity.contents)[0].encode('utf-8'), (ingredient.contents)[0].encode('utf-8')))

##    for ingredient in recipe._ingredients:
##        print ingredient._quantity, ";", ingredient._measurement, ";", ingredient._preparation, ";", ingredient._descriptor, ";", ingredient._name, ";", ingredient._type

    directions_html = soup.find_all(class_='directLeft')
    directions_span = directions_html[0].select('span')
    for direction in directions_span:
        direction = re.sub(r'<.*?>', "", str(direction))
        recipe._directions.append(direction)

    for direction in recipe._directions:
        for sentence in direction.split('.'):
            for word in cmp_list:
                sentence2 = sentence.lower()
                if word in sentence2 and word not in recipe._cooking_methods:
                    recipe._cooking_methods.append(word)
            for word in cms_list:
                sentence2 = sentence.lower()
                if word in sentence2 and word not in recipe._preparation_methods:
                    recipe._preparation_methods.append(word)
            for tool in tool_list:
                sentence2 = sentence.lower()
                tool = tool.lower()
                if tool in sentence2 and tool not in recipe._tools:
                    recipe._tools.append(tool)

def toLowFat(recipe):
    print "Low-fat version"
    ishealthy = 1
    for ingredient in recipe._ingredients:
        for key in lfingsub.keys():
            if key in ingredient._name:
                print "Substitue "+ingredient._name+" with "+lfingsub[key]
                ishealthy = 0
                break
    for method in recipe.cooking_methods:
        for key in lfcooksub.keys():
            if key in method:
                print "Substitute "+method+" with "+lfcooksub[key]
                ishealthy = 0
                break
    if ishealthy==1:
        print "Recipe already healthy, no substitutions made."
        
def toHighFat(recipe):
    print "Normal, non-low-fat version"
    isNOThealthy = 1
    for ingredient in recipe._ingredients:
        for key in hfingsub.keys():
            if key in ingredient._name:
                print "Substitue "+ingredient._name+" with "+hfingsub[key]
                isNOThealthy = 0
                break
    if isNOThealthy==1:
        print "Recipe already high-fat, no substitutions made."
        

def toVeg(recipe):
    print "Vegetarian version"
    if isVeg(recipe):
        print "Recipe is already vegetarian."
        return
    else:
        for ingredient in recipe._ingredients:
            if ingredient._type == 'meat':
                for key in sorted(meatsub.keys()):
                    if key in ingredient._name:
                        print "Substitute", ingredient._name, "with", meatsub[key] 
                        break
            elif ingredient._type == 'liquid' and 'vegetable' not in ingredient._name:
                if "stock" in ingredient._name:
                    print "vegetable stock"
                else:
                    print "vegetable broth"
            else:
                print ingredient._name

def toMeat(recipe):
    print "Non-vegetarian version"
    if not isVeg(recipe):
        print "Recipe already has meat in it."
        return
    else:
        rank = 100
        repkey = ''
        reping = ''
        for ingredient in recipe._ingredients:
            for key in vegrank.keys():
                if key in ingredient._name and vegrank[key] < rank:
                    rank = vegrank[key]
                    repkey = key
                    reping = ingredient._name
        for ingredient in recipe._ingredients:
            if ingredient._name == reping:
                print "Substitute", ingredient._name, "with", vegsub[repkey]
            else:
                print ingredient._name
        if rank < 100:
            "Recipe was not modified. There are no common meat substitutes in the recipe."

def isVeg(recipe):
    for ingredient in recipe._ingredients:
        print ingredient._type
        if ingredient._type != 'meat' or (ingredient._type != 'liquid' and 'veggie' not in ingredient._name):
            return False
    return True


def toEastasian(recipe):
    print "East Asian version"
    for ingredient in recipe._ingredients:
        if ingredient._name not in east_asian:
            if (ingredient._type is 'spice') or (ingredient._type is 'sauce') or (ingredient._type is 'liquid'):

                if ingredient._name in sweet_list:
                    if ingredient._type is 'sauce':
                        print "Substitute", ingredient._name, "with", sweetEastasianSauce[random.randrange(len(sweetEastasianSauce))]
                    elif ingredient._type is 'spice':
                        print "Substitute", ingredient._name, "with", sweetEastasianSpice[random.randrange(len(sweetEastasianSpice))]
                    else:
                        print "Substitute", ingredient._name, "with", sweetEastasianLiquid[random.randrange(len(sweetEastasianLiquid))]
               
                elif ingredient._name in sour_list:
                    if ingredient._type is 'sauce':
                        print "Substitute", ingredient._name, "with", sourEastasianSauce[random.randrange(len(sourEastasianSauce))]
                    elif ingredient._type is 'spice':
                        print "Substitute", ingredient._name, "with", sourEastasianSpice[random.randrange(len(sourEastasianSpice))]
                    else:
                        print "Substitute", ingredient._name, "with", sourEastasianLiquid[random.randrange(len(sourEastasianLiquid))]


                elif ingredient._name in hot_list:
                    if ingredient._type is 'sauce':
                        print "Substitute", ingredient._name, "with", hotEastasianSauce[random.randrange(len(hotEastasianSauce))]
                    elif ingredient._type is 'spice':
                        print "Substitute", ingredient._name, "with", hotEastasianSpice[random.randrange(len(hotEastasianSpice))]
                    else:
                        print "Substitute", ingredient._name, "with", hotEastasianLiquid[random.randrange(len(hotEastasianLiquid))]


                elif ingredient._name in salty_list:
                    if ingredient._type is 'sauce':
                        print "Substitute", ingredient._name, "with", saltyEastasianSauce[random.randrange(len(saltyEastasianSauce))]
                    elif ingredient._type is 'spice':
                        print "Substitute", ingredient._name, "with", saltyEastasianSpice[random.randrange(len(saltyEastasianSpice))]
                    else:
                        print "Substitute", ingredient._name, "with", saltyEastasianLiquid[random.randrange(len(saltyEastasianLiquid))]

                else:
                        if ingredient._type is 'sauce':
                            print "Substitute", ingredient._name, "with", eastasianSauce[random.randrange(len(eastasianSauce))]
                        elif ingredient._type is 'spice':
                            print "Substitute", ingredient._name, "with", eastasianSpice[random.randrange(len(eastasianSpice))]
                        else :
                            print "Substitute", ingredient._name, "with", eastasianLiquid[random.randrange(len(eastasianLiquid))]

            elif ingredient._type is 'veggie':
                    if ingredient._name in hard_list:
                        print "Substitute", ingredient._name, "with", hardEastasianVegetable[random.randrange(len(hardEastasianVegetable))]
                    elif ingredient._name in soft_list:
                        print "Substitute", ingredient._name, "with", softEastasianVegetable[random.randrange(len(softEastasianVegetable))]
                    else:
                        print "Substitute", ingredient._name, "with", eastasianVegetable[random.randrange(len(eastasianVegetable))]

            elif ingredient._type is 'oil':
                    print "Substitute", ingredient._name, "with", eastasianOil[random.randrange(len(eastasianOil))]
        else:
            print ingredient._name

                    
def toFrench(recipe):
    print "French version"
    for ingredient in recipe._ingredients:
        if ingredient._name not in french:
            if (ingredient._type is 'spice') or (ingredient._type is 'sauce') or (ingredient._type is 'liquid'):

                if ingredient._name in sweet_list:
                    if ingredient._type is 'sauce':
                        print "Substitute", ingredient._name, "with", sweetFrenchSauce[random.randrange(len(sweetFrenchSauce))]
                    elif ingredient._type is 'spice':
                        print "Substitute", ingredient._name, "with", sweetFrenchSpice[random.randrange(len(sweetFrenchSpice))]
                    else:
                        print "Substitute", ingredient._name, "with", sweetFrenchLiquid[random.randrange(len(sweetFrenchLiquid))]
               
                elif ingredient._name in sour_list:
                    if ingredient._type is 'sauce':
                        print "Substitute", ingredient._name, "with", sourFrenchSauce[random.randrange(len(sourFrenchSauce))]
                    elif ingredient._type is 'spice':
                        print "Substitute", ingredient._name, "with", sourFrenchSpice[random.randrange(len(sourFrenchSpice))]
                    else:
                        print "Substitute", ingredient._name, "with", sourFrenchLiquid[random.randrange(len(sourFrenchLiquid))]


                elif ingredient._name in hot_list:
                    if ingredient._type is 'sauce':
                        print "Substitute", ingredient._name, "with", hotFrenchSauce[random.randrange(len(hotFrenchSauce))]
                    elif ingredient._type is 'spice':
                        print "Substitute", ingredient._name, "with", hotFrenchSpice[random.randrange(len(hotFrenchSpice))]
                    else:
                        print "Substitute", ingredient._name, "with", hotFrenchLiquid[random.randrange(len(hotFrenchLiquid))]


                elif ingredient._name in salty_list:
                    if ingredient._type is 'sauce':
                        print "Substitute", ingredient._name, "with", saltyFrenchSauce[random.randrange(len(saltyFrenchSauce))]
                    elif ingredient._type is 'spice':
                        print "Substitute", ingredient._name, "with", saltyFrenchSpice[random.randrange(len(saltyFrenchSpice))]
                    else:
                        print "Substitute", ingredient._name, "with", saltyFrenchLiquid[random.randrange(len(saltyFrenchLiquid))]

                else:
                        if ingredient._type is 'sauce':
                            print "Substitute", ingredient._name, "with", frenchSauce[random.randrange(len(frenchSauce))]
                        elif ingredient._type is 'spice':
                            print "Substitute", ingredient._name, "with", frenchSpice[random.randrange(len(frenchSpice))]
                        else :
                            print "Substitute", ingredient._name, "with", frenchLiquid[random.randrange(len(frenchLiquid))]

            elif ingredient._type is 'veggie':
                    if ingredient._name in hard_list:
                        print "Substitute", ingredient._name, "with", hardFrenchVegetable[random.randrange(len(hardFrenchVegetable))]
                    elif ingredient._name in soft_list:
                        print "Substitute", ingredient._name, "with", softFrenchVegetable[random.randrange(len(softFrenchVegetable))]
                    else:
                        print "Substitute", ingredient._name, "with", frenchVegetable[random.randrange(len(frenchVegetable))]

            elif ingredient._type is 'oil':
                    print "Substitute", ingredient._name, "with", frenchOil[random.randrange(len(frenchOil))]
        else:
            print ingredient._name


def toItalian(recipe):
    print "Italian version"
    for ingredient in recipe._ingredients:
        if ingredient._name not in italian:            
            if (ingredient._type is 'spice') or (ingredient._type is 'sauce') or (ingredient._type is 'liquid'):

                if ingredient._name in sweet_list:
                    if ingredient._type is 'sauce':
                        print "Substitute", ingredient._name, "with", sweetItalianSauce[random.randrange(len(sweetItalianSauce))]
                    elif ingredient._type is 'spice':
                        print "Substitute", ingredient._name, "with", sweetItalianSpice[random.randrange(len(sweetItalianSpice))]
                    else:
                        print "Substitute", ingredient._name, "with", sweetItalianLiquid[random.randrange(len(sweetItalianLiquid))]
               
                elif ingredient._name in sour_list:
                    if ingredient._type is 'sauce':
                        print "Substitute", ingredient._name, "with", sourItalianSauce[random.randrange(len(sourItalianSauce))]
                    elif ingredient._type is 'spice':
                        print "Substitute", ingredient._name, "with", sourItalianSpice[random.randrange(len(sourItalianSpice))]
                    else:
                        print "Substitute", ingredient._name, "with", sourItalianLiquid[random.randrange(len(sourItalianLiquid))]


                elif ingredient._name in hot_list:
                    if ingredient._type is 'sauce':
                        print "Substitute", ingredient._name, "with", hotItalianSauce[random.randrange(len(hotItalianSauce))]
                    elif ingredient._type is 'spice':
                        print "Substitute", ingredient._name, "with", hotItalianSpice[random.randrange(len(hotItalianSpice))]
                    else:
                        print "Substitute", ingredient._name, "with", hotItalianLiquid[random.randrange(len(hotItalianLiquid))]


                elif ingredient._name in salty_list:
                    if ingredient._type is 'sauce':
                        print "Substitute", ingredient._name, "with", saltyItalianSauce[random.randrange(len(saltyItalianSauce))]
                    elif ingredient._type is 'spice':
                        print "Substitute", ingredient._name, "with", saltyItalianSpice[random.randrange(len(saltyItalianSpice))]
                    else:
                        print "Substitute", ingredient._name, "with", saltyItalianLiquid[random.randrange(len(saltyItalianLiquid))]

                else:
                        if ingredient._type is 'sauce':
                            print "Substitute", ingredient._name, "with", italianSauce[random.randrange(len(italianSauce))]
                        elif ingredient._type is 'spice':
                            print "Substitute", ingredient._name, "with", italianSpice[random.randrange(len(italianSpice))]
                        else :
                            print "Substitute", ingredient._name, "with", italianLiquid[random.randrange(len(italianLiquid))]

            elif ingredient._type is 'veggie':
                    if ingredient._name in hard_list:
                        print "Substitute", ingredient._name, "with", hardItalianVegetable[random.randrange(len(hardItalianVegetable))]
                    elif ingredient._name in soft_list:
                        print "Substitute", ingredient._name, "with", softItalianVegetable[random.randrange(len(softItalianVegetable))]
                    else:
                        print "Substitute", ingredient._name, "with", italianVegetable[random.randrange(len(italianVegetable))]

            elif ingredient._type is 'oil':
                    print "Substitute", ingredient._name, "with", italianOil[random.randrange(len(italianOil))]
        else:
            print ingredient._name

def printJson(recipe):
    jsonoutput = {}
    ingList = []
    for ingredient in recipe._ingredients:
        tempdict = {}
        tempdict["name"] = ingredient._name
        tempdict["quantity"] = ingredient._quantity
        tempdict["measurement"] = ingredient._measurement
        tempdict["descriptor"] = ingredient._descriptor
        tempdict["preparation"] = ingredient._preparation
        ingList.append(tempdict)
    jsonoutput["ingredients"] = ingList
    jsonoutput["cooking method"] = recipe._cooking_methods
    jsonoutput["cooking tools"] = recipe._tools
    return json.dumps(jsonoutput)

def main(link):
    recipe = Recipe()
    parse(link, recipe)
    return printJson(recipe)
