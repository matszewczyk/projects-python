from item import Item
import numpy as np

#20 przedmiotow o wartosci i wadze 0 - 100
# items = [Item(np.random.randint(0,100), np.random.randint(0,100)) for x in range(0,20)]

#ile maksymalnie moze zmiescic walizka
capacity = 100

#ilosc przedmiotow z ktorych wybieramy
items_number = 20

items = []
for i in range(0,items_number):
    item = Item(np.random.randint(0,100), np.random.randint(0,100))
    items.append(item)

items = [Item(10,10), Item(25,5), Item(37,42), Item(1,18), Item(35,15), Item(81,37)]

suma_wartosci = 0
suma_wag = 0

for i in range(0, len(items)):
    suma_wartosci = suma_wartosci + items[i].getValue()
    suma_wag = suma_wag + items[i].getWeight()

print("Suma wartosci: ", suma_wartosci)
print("Suma wag: ", suma_wag)

osobnik = [np.random.randint(0,2) for x in range(0,items_number)]

osobnik1 = [1,1,1,1,1,1]
osobnik2 = [0,0,0,0,0,0]

osobniki = [osobnik1, osobnik2]


def krzyzowanie(osobnik1, osobnik2):
    zarodek1 = osobnik1[:3] + osobnik2[3:]
    zarodek2 = osobnik2[:3] + osobnik1[3:]
    return zarodek1, zarodek2


zarodek1, zarodek2 = krzyzowanie(osobnik1, osobnik2)

print("Zarodki: ")
print(zarodek1)
print(zarodek2)


def mutacja(zarodek):
    p_zmutowania = 4
    r = np.random.randint(0,10)
    if r < p_zmutowania:
        mutuj = True
    else:
        mutuj = False

    if mutuj:
        locus = np.random.randint(0, len(zarodek) - 1)
        if zarodek[locus] == 1:
            zarodek[locus] = 0
        else:
            zarodek[locus] = 1

    osobnik = zarodek
    return osobnik


nowy_osobnik1 = mutacja(zarodek1)
nowy_osobnik2 = mutacja(zarodek2)

print("osobniki: ")
print(nowy_osobnik1)
print(nowy_osobnik2)


def check_fitness(osobnik):
    total_weight = 0
    total_value = 0

    for i in range(len(osobnik)):
        if osobnik[i] == 1:
            if (total_weight + items[i].getWeight()) <= capacity:
                total_value = total_value + items[i].getValue()
                total_weight = total_weight + items[i].getWeight()
                # print("Wartosc x: ", osobnik[i], " Wartosc total_value: ", total_value, " Wartosc total_weight: ", total_weight)

    return total_value, total_weight


fitness_osobnik1 = check_fitness(osobnik1)
fitness_osobnik2 = check_fitness(osobnik2)
fitness_nowy_osobnik1 = check_fitness(nowy_osobnik1)
fitness_nowy_osobnik2 = check_fitness(nowy_osobnik2)

print(fitness_osobnik1)
print(fitness_osobnik2)
print(fitness_nowy_osobnik1)
print(fitness_nowy_osobnik2)


# print(osobnik)
# print("Wartosc wybranych: ", total_value)
# print("Waga wybranych: ", total_weight)


#def check_fitness
#def mutate
#def populate
#def main




