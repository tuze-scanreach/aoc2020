from collections import defaultdict
from copy import deepcopy

ingredients = set()
ingredients_count = defaultdict(int)
allergens = defaultdict(list)
allergens_unique = defaultdict(list)
with open('aoc21.txt') as f:

    input_txt = f.readlines()
#kfcds, nhms, sbzzf, or trh
for txt in input_txt:
    txt = txt[:len(txt) - 2]
    allergens_list = txt[txt.find("contains") + len("contains "):].split(', ')
    ingredients_list = txt[:txt.find('(') - 1].split()
    ingredients.update(ingredients_list)
    for ing in ingredients_list:
        ingredients_count[ing] += 1
    for al in allergens_list:
        relevant_ingredients = deepcopy(ingredients_list)
        if len(allergens[al]) > 0:
            relevant_ingredients = list(
                set(allergens[al]) & set(relevant_ingredients))
        allergens[al] = relevant_ingredients

#print(allergens)
for al in allergens:
    allergens_unique[al] = deepcopy(allergens[al])
    for al2 in allergens:
        if al != al2:
            second_set_of_allergens = set(allergens[al2])
            if al2 in allergens_unique:
                second_set_of_allergens = set(allergens_unique[al2])
            unique_allergens = list(
                set(allergens_unique[al]) ^ second_set_of_allergens)
            unique_allergens = [
                allergen for allergen in unique_allergens
                if allergen in allergens_unique[al]
            ]
            if len(unique_allergens):
                allergens_unique[al] = list(unique_allergens)

allergen_free = ingredients ^ set(
    [i[0] for i in list(allergens_unique.values())])

sum_of_allergen_free_ing_occurences = sum(ingredients_count[ingredient]
                                          for ingredient in allergen_free)

print(sum_of_allergen_free_ing_occurences)

canonical_dangerous_ingredient_list = ""
for key, value in sorted(allergens_unique.items()):
    canonical_dangerous_ingredient_list += value[0] + ","
print(canonical_dangerous_ingredient_list)
