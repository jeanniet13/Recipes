# -*- coding: utf8 -*-
import nltk
import urllib2
import re
from bs4 import BeautifulSoup

ingredients = []
directions = []

recipe_url = urllib2.urlopen("http://allrecipes.com/Recipe/Worlds-Best-Lasagna/Detail.aspx?evt19=1")
recipe_html = recipe_url.read()
soup = BeautifulSoup(recipe_html)

for quantity, ingredient in zip(soup.find_all(id='lblIngAmount'), soup.find_all(id='lblIngName')):
    ingredients.append(((quantity.contents)[0].encode('utf-8'), (ingredient.contents)[0].encode('utf-8')))
print ingredients

#text = nltk.word_tokenize("chopped fresh parsley")
#print nltk.pos_tag(text)
