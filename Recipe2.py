# -*- coding: utf8 -*-
# -*- coding: utf8 -*-
import nltk
import urllib2
import re
import fractions
import json
import random
from bs4 import BeautifulSoup
from vegTransformation import vegsub
from vegTransformation import meatsub
from vegTransformation import vegrank
from cuisineTransformation import eastasianSauce
from cuisineTransformation import eastasianSpice
from cuisineTransformation import eastasianOil
from cuisineTransformation import eastasianLiquid
from cuisineTransformation import eastasianVegetable
from cuisineTransformation import frenchSauce
from cuisineTransformation import frenchSpice
from cuisineTransformation import frenchOil
from cuisineTransformation import frenchLiquid
from cuisineTransformation import frenchVegetable
from cuisineTransformation import italianSauce
from cuisineTransformation import italianSpice
from cuisineTransformation import italianOil
from cuisineTransformation import italianLiquid
from cuisineTransformation import italianVegetable


from LowFatTransformation import lfingsub


cmp_list = open('cookingmethods_primary.txt', 'rb').read().split('\r\n')
cms_list = open('cookingmethods_secondary.txt', 'rb').read().split('\r\n')
tool_list = open('tools.txt','rb').read().split('\r\n')
veg_list = open('vegetables.txt', 'rb').read().split('\r\n')
meat_list = open('meat.txt', 'rb').read().split('\r\n')
oil_list = open('oil.txt', 'rb').read().split('\r\n')
liquid_list = open('liquid.txt', 'rb').read().split('\r\n')
spice_list = open('spices.txt', 'rb').read().split('\r\n')
sauce_list = open('sauce.txt', 'rb').read().split('\r\n')
sour_list = open('sour.txt','rb').read().split('r\n')
hot_list = open('hot.txt', 'rb').read().split('\r\n')
sweet_list = open('sweet.txt', 'rb').read().split('\r\n')
salty_list = open('salty.txt','rb').read().split('r\n')
soft_list = open('soft.txt', 'rb').read().split('\r\n')
hard_list = open('hard.txt','rb').read().split('r\n')
east_asian = open('eastasian.txt','rb').read().split('r\n')
italian = open('italian.txt','rb').read().split('r\n')
french = open('eastasian.txt','rb').read().split('r\n')


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
    itype = '' #meat, spice, liquid, veggie, oil, sauce

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
            
        ingname = " " + ''.join(ingredient)
        tempname = ""
        for liquid in liquid_list:
            if (" " + liquid) in ingname:
                newIngredient.itype = 'liquid'
                tempname = liquid
                break

        if newIngredient.itype == '':
            for sauce in sauce_list:
                if (" " + sauce) in ingname:
                    newIngredient.itype = 'sauce'
                    tempname = sauce
                    break
            
        if newIngredient.itype == '':
            for spice in spice_list:
                if (" " + spice) in ingname:
                    newIngredient.itype = 'spice'
                    tempname = spice
                    break
                
        if newIngredient.itype == '':
            for veg in veg_list:
                if (" " + veg) in ingname:
                    newIngredient.itype = 'veggie'
                    tempname = veg
                    break

        if newIngredient.itype == '':
            for oil in oil_list:
                if (" " + oil) in ingname:
                    newIngredient.itype = 'oil'
                    tempname = oil
                    break

        if newIngredient.itype == '':
            for meat in meat_list:
                if (" " + meat) in ingname:
                    newIngredient.itype = 'meat'
                    tempname = meat
                    break
       

        if newIngredient.itype == '':
            tempname = ingredient[0]

        newIngredient.name = tempname
        #newIngredient.name = ingredient[0]
        if len(ingredient) > 1:
            #newIngredient.preparation = ingredient[1]
            if tempname in ingredient[0]:            
                newIngredient.descriptor = ingredient[0].replace(tempname, "")
                newIngredient.preparation = ingredient[1]
            elif tempname in ingredient[1]:
                newIngredient.descriptor = ingredient[1].replace(tempname, "")
                newIngredient.preparation = ingredient[0]
                
        recipe.ingredients.append(newIngredient)
        #ingredients.append(((quantity.contents)[0].encode('utf-8'), (ingredient.contents)[0].encode('utf-8')))

    for ingredient in recipe.ingredients:
        print ingredient.quantity, ";", ingredient.measurement, ";", ingredient.preparation, ";", ingredient.name, ";", ingredient.itype

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



def toLowFat(recipe):
    for ingredient in recipe.ingredients:
        for key in lfingsub.keys():
            if key in ingredient.name:
                print lfingsub[key]
                break
    print "Recipe already healthy, no substitutions made."


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


    #sweetEastAsianSauce=[]
    #for string in eastasianSauce:
        #if string is 'sweet':
            #sweetEastAsianSauce.append(string)
    #print sweetEastAsianSauce


def toEastAsian(recipe):

    for ingredient in recipe.ingredients:
        print ingredient.name
        if ingredient.itype is 'oil':
            print 1
        else:
            print 0

        if ingredient.name in east_asian:
            break

        else:

            if ingredient.itype is not 'meat':
                if ingredient.itype is not 'oil':
                    if ingredient.itype is not 'veggie':

                        if ingredient.name in sweet_list:
                            if ingredient.itype is 'sauce':
                                print 'is substituted by'+ sweetEastAsianSauce[random.randrange(len(sweetEastAsianSauce))]
                            elif ingredient.itype is 'spice':
                                print "is substituted by" +sweetEastAsianSpice[random.randrange(len(sweetEastAsianSpice))]
                            else:
                                print "is substituted by" +sweetEastAsianLiquid[random.randrange(len(sweetEastAsianLiquid))]
           
                        elif ingredient.name in sour_list:
                            if ingredient.itype is 'sauce':
                                print "is substituted by" +sourEastAsianSauce[random.randrange(len(sourEastAsianSauce))]
                            elif ingredient.itype is 'spice':
                                print "is substituted by"+ sourEastAsianSpice[random.randrange(len(sourEastAsianSpice))]
                            else:
                                print "is substituted by"+ sourEastAsianLiquid[random.randrange(len(sourEastAsianLiquid))]


                        elif ingredient.name in hot_list:
                            if ingredient.itype is 'sauce':
                                print "is substituted by"+ hotEastAsianSauce[random.randrange(len(hotEastAsianSauce))]
                            elif ingredient.itype is 'spice':
                                print "is substituted by"+ hotEastAsianSpice[random.randrange(len(hotEastAsianSpice))]
                            else:
                                print "is substituted by"+ hotEastAsianLiquid[random.randrange(len(hotEastAsianLiquid))]


                        elif ingredient.name in salty_list:
                            if ingredient.itype is 'sauce':
                                print "is substituted by" +saltyEastAsianSauce[random.randrange(len(saltyEastAsianSauce))]
                            elif ingredient.itype is 'spice':
                                print "is substituted by"+ saltyEastAsianSpice[random.randrange(len(saltyEastAsianSpice))]
                            else:
                                print"is substituted by"+ saltyEastAsianLiquid[random.randrange(len(saltyEastAsianLiquid))]

                        else:
                            if ingredient.itype is 'sauce':
                                print "is substituted by" +eastasianSauce[random.randrange(len(eastasianSauce))]
                            elif ingredient.itype is 'spice':
                                print "is substituted by"+ eastasianSpice[random.randrange(len(eastasianSpice))]
                            else :
                                print"is substituted by"+ eastasianLiquid[random.randrange(len(eastasianLiquid))]

                    else:
                        if ingredient.name in hard_list:
                            print "is substituted by" +hardEastAsianVegetable[random.randrange(len(hardEastAsianVegetable))]
                        elif ingredient.name in soft_list:
                            print "is substituted by" +softEastAsianVegetable[random.randrange(len(softEastAsianVegetable))]
                        else:
                            print "is substituted by" + eastasianVegetable[random.randrange(len(eastasianVegetable))]
                else:
                    print "is substituted by" + eastasianOil[random.randrange(len(eastasianOil))]
            else:
                print"Did I get here"
                    
def toFrench(recipe):

    for ingredient in recipe.ingredients:
        print ingredient.name

        if ingredient.name in east_asian:
            break

        else:

            if ingredient.itype is not 'meat':
                if ingredient.itype is not 'oil':
                    if ingredient.itype is not 'vegetable':

                        if ingredient.name in sweet_list:
                            if ingredient.itype is 'sauce':
                                print 'is substituted by'+ sweetFrenchSauce[random.randrange(len(sweetFrenchSauce))]
                            elif ingredient.itype is 'spice':
                                print "is substituted by" +sweetFrenchSpice[random.randrange(len(sweetFrenchSpice))]
                            else:
                                print "is substituted by" +sweetFrenchLiquid[random.randrange(len(sweetFrenchLiquid))]
           
                        elif ingredient.name in sour_list:
                            if ingredient.itype is 'sauce':
                                print "is substituted by" +sourFrenchSauce[random.randrange(len(sourFrenchSauce))]
                            elif ingredient.itype is 'spice':
                                print "is substituted by"+ sourFrenchSpice[random.randrange(len(sourFrenchSpice))]
                            else:
                                print "is substituted by"+ sourFrenchLiquid[random.randrange(len(sourFrenchLiquid))]


                        elif ingredient.name in hot_list:
                            if ingredient.itype is 'sauce':
                                print "is substituted by"+ hotFrenchSauce[random.randrange(len(hotFrenchSauce))]
                            elif ingredient.itype is 'spice':
                                print "is substituted by"+ hotFrenchSpice[random.randrange(len(hotFrenchSpice))]
                            else:
                                print "is substituted by"+ hotFrenchLiquid[random.randrange(len(hotFrenchLiquid))]


                        elif ingredient.name in salty_list:
                            if ingredient.itype is 'sauce':
                                print "is substituted by" +saltyFrenchSauce[random.randrange(len(saltyFrenchSauce))]
                            elif ingredient.itype is 'spice':
                                print "is substituted by"+ saltyFrenchSpice[random.randrange(len(saltyFrenchSpice))]
                            else:
                                print"is substituted by"+ saltyFrenchLiquid[random.randrange(len(saltyFrenchLiquid))]

                        else:
                            if ingredient.itype is 'sauce':
                                print "is substituted by" +frenchSauce[random.randrange(len(frenchSauce))]
                            elif ingredient.itype is 'spice':
                                print "is substituted by"+ frenchSpice[random.randrange(len(frenchSpice))]
                            else :
                                print"is substituted by"+ frenchLiquid[random.randrange(len(frenchLiquid))]

                    else:
                        if ingredient.name in hard_list:
                            print "is substituted by" +hardFrenchVegetable[random.randrange(len(hardFrenchVegetable))]
                        elif ingredient.name in soft_list:
                            print "is substituted by" +softFrenchVegetable[random.randrange(len(softFrenchVegetable))]
                        else:
                            print "is substituted by" + frenchVegetable[random.randrange(len(frenchVegetable))]
                else:
                    print "is substituted by" + frenchOil[random.randrange(len(frenchOil))]


def toItalian(recipe):

    for ingredient in recipe.ingredients:
        print ingredient.name

        if ingredient.name in east_asian:
            break

        else:

            if ingredient.itype is not 'meat':
                if ingredient.itype is not 'oil':
                    if ingredient.itype is not 'vegetable':

                        if ingredient.name in sweet_list:
                            if ingredient.itype is 'sauce':
                                print 'is substituted by'+ sweetItalianSauce[random.randrange(len(sweetItalianSauce))]
                            elif ingredient.itype is 'spice':
                                print "is substituted by" +sweetItalianSpice[random.randrange(len(sweetItalianSpice))]
                            else:
                                print "is substituted by" +sweetItalianLiquid[random.randrange(len(sweetItalianLiquid))]
           
                        elif ingredient.name in sour_list:
                            if ingredient.itype is 'sauce':
                                print "is substituted by" +sourItalianSauce[random.randrange(len(sourItalianSauce))]
                            elif ingredient.itype is 'spice':
                                print "is substituted by"+ sourItalianSpice[random.randrange(len(sourItalianSpice))]
                            else:
                                print "is substituted by"+ sourItalianLiquid[random.randrange(len(sourItalianLiquid))]


                        elif ingredient.name in hot_list:
                            if ingredient.itype is 'sauce':
                                print "is substituted by"+ hotItalianSauce[random.randrange(len(hotItalianSauce))]
                            elif ingredient.itype is 'spice':
                                print "is substituted by"+ hotItalianSpice[random.randrange(len(hotItalianSpice))]
                            else:
                                print "is substituted by"+ hotItalianLiquid[random.randrange(len(hotItalianLiquid))]


                        elif ingredient.name in salty_list:
                            if ingredient.itype is 'sauce':
                                print "is substituted by" +saltyItalianSauce[random.randrange(len(saltyItalianSauce))]
                            elif ingredient.itype is 'spice':
                                print "is substituted by"+ saltyItalianSpice[random.randrange(len(saltyItalianSpice))]
                            else:
                                print"is substituted by"+ saltyItalianLiquid[random.randrange(len(saltyItalianLiquid))]

                        else:
                            if ingredient.itype is 'sauce':
                                print "is substituted by" +italianSauce[random.randrange(len(italianSauce))]
                            elif ingredient.itype is 'spice':
                                print "is substituted by"+ italianSpice[random.randrange(len(italianSpice))]
                            else :
                                print"is substituted by"+ italianLiquid[random.randrange(len(italianLiquid))]

                    else:
                        if ingredient.name in hard_list:
                            print "is substituted by" +hardItalianVegetable[random.randrange(len(hardItalianVegetable))]
                        elif ingredient.name in soft_list:
                            print "is substituted by" +softItalianVegetable[random.randrange(len(softItalianVegetable))]
                        else:
                            print "is substituted by" + italianVegetable[random.randrange(len(italianVegetable))]
                else:
                    print "is substituted by" + italianOil[random.randrange(len(italianOil))]



def isVeg(recipe):
    for ingredient in recipe.ingredients:
        if ingredient.itype is 'meat' or (ingredient.itype is 'liquid' and 'veggie' not in ingredient.name):
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
   # print eastasianOil(random.randrange(len(eastasianOil)))
    #print eastasianOil[0]
    #toVeg(recipe)
    #toMeat(recipe)
    #toEastAsian(recipe)
    #toFrench(recipe)
    toItalian(recipe)
    #print eastasianSauce[random.randrange(len(eastasianSauce))]

main()

#text = nltk.word_tokenize("chopped fresh parsley")
#print nltk.pos_tag(text)
