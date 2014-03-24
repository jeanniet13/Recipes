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
        else:
            print ingredient._name