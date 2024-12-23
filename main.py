from Fuzzy_system import FuzzySet, LingVariable, FuzzyRule, FuzzySystem, triangle

# Definice vstupních fuzzy proměnných
vzdalenost = LingVariable('Vzdalenost')
vzdalenost.add_set(FuzzySet('Blizko', lambda x: triangle(x, 0, 0, 40)))
vzdalenost.add_set(FuzzySet('Stredne', lambda x: triangle(x, 20, 60, 100)))
vzdalenost.add_set(FuzzySet('Daleko', lambda x: triangle(x, 80, 120, 120)))

relativni_rychlost = LingVariable('RelativniRychlost')
relativni_rychlost.add_set(FuzzySet('VelmiPomale', lambda x: triangle(x, -100, -100, -50)))
relativni_rychlost.add_set(FuzzySet('Pomale', lambda x: triangle(x, -75, -25, 0)))
relativni_rychlost.add_set(FuzzySet('Stejne', lambda x: triangle(x, -10, 0, 10)))
relativni_rychlost.add_set(FuzzySet('Rychle', lambda x: triangle(x, 0, 25, 75)))
relativni_rychlost.add_set(FuzzySet('VelmiRychle', lambda x: triangle(x, 50, 100, 100)))

intenzita_dopravy = LingVariable('IntenzitaDopravy')
intenzita_dopravy.add_set(FuzzySet('Nizka', lambda x: triangle(x, 0, 0, 3)))
intenzita_dopravy.add_set(FuzzySet('Stredni', lambda x: triangle(x, 2, 5, 8)))
intenzita_dopravy.add_set(FuzzySet('Vysoka', lambda x: triangle(x, 7, 10, 10)))

# Definice výstupní fuzzy proměnné
zrychleni = LingVariable('Zrychleni')
zrychleni.add_set(FuzzySet('Brzdeni', lambda x: triangle(x, -5, -5, -2.5)))
zrychleni.add_set(FuzzySet('Zadne', lambda x: triangle(x, -2.5, 0, 2.5)))
zrychleni.add_set(FuzzySet('Akcelerace', lambda x: triangle(x, 2.5, 5, 5)))

# Pravidla fuzzy systému
rules = [
    # Pokud je vzdálenost blízko, relativní rychlost velmi pomalá a intenzita dopravy vysoká -> brzdit
    FuzzyRule([('Vzdalenost', 'Blizko'), ('RelativniRychlost', 'VelmiPomale'), ('IntenzitaDopravy', 'Vysoka')], ('Zrychleni', 'Brzdeni')),
    # Pokud je vzdálenost blízko, relativní rychlost stejná a intenzita dopravy střední -> brzdit
    FuzzyRule([('Vzdalenost', 'Blizko'), ('RelativniRychlost', 'Stejne'), ('IntenzitaDopravy', 'Stredni')], ('Zrychleni', 'Brzdeni')),
    # Pokud je vzdálenost střední, relativní rychlost pomalá a intenzita dopravy nízká -> žádné zrychlení
    FuzzyRule([('Vzdalenost', 'Stredne'), ('RelativniRychlost', 'Pomale'), ('IntenzitaDopravy', 'Nizka')], ('Zrychleni', 'Zadne')),
    # Pokud je vzdálenost daleko, relativní rychlost rychlá a intenzita dopravy střední -> akcelerovat
    FuzzyRule([('Vzdalenost', 'Daleko'), ('RelativniRychlost', 'Rychle'), ('IntenzitaDopravy', 'Stredni')], ('Zrychleni', 'Akcelerace')),
    # Pokud je vzdálenost daleko, relativní rychlost velmi rychlá a intenzita dopravy nízká -> akcelerovat
    FuzzyRule([('Vzdalenost', 'Daleko'), ('RelativniRychlost', 'VelmiRychle'), ('IntenzitaDopravy', 'Nizka')], ('Zrychleni', 'Akcelerace'))
]

# Vytvoření fuzzy systému
fuzzy_system = FuzzySystem()
fuzzy_system.add_variable(vzdalenost)
fuzzy_system.add_variable(relativni_rychlost)
fuzzy_system.add_variable(intenzita_dopravy)
fuzzy_system.add_variable(zrychleni, is_output=True)

for rule in rules:
    fuzzy_system.add_rule(rule)

# Testování systému pro různé kombinace vstupů
test_inputs = [
    {'Vzdalenost': 10, 'RelativniRychlost': -90, 'IntenzitaDopravy': 9},
    {'Vzdalenost': 50, 'RelativniRychlost': 0, 'IntenzitaDopravy': 5},
    {'Vzdalenost': 100, 'RelativniRychlost': 60, 'IntenzitaDopravy': 2},
    {'Vzdalenost': 30, 'RelativniRychlost': -20, 'IntenzitaDopravy': 7},
    {'Vzdalenost': 80, 'RelativniRychlost': 90, 'IntenzitaDopravy': 1}
]

for inputs in test_inputs:
    aggregated_output = fuzzy_system.infer(inputs)
    final_output = fuzzy_system.defuzzify(aggregated_output)
    print(f"Inputs: {inputs}, Aggregated Output: {aggregated_output}, Final Output: {final_output}")