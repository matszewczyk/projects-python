from item import Item
import numpy as np


items = [Item(10,10), Item(25,5), Item(37,42), Item(1,18), Item(35,15), Item(81,37)]
items = [Item(np.random.randint(0,100), np.random.randint(0,100)) for x in range(0,40)]

#ile maksymalnie moze zmiescic walizka
capacity = 500

#ilosc przedmiotow z ktorych wybieramy
items_number = len(items)

#ilosc osobnikow w populacji
wielkosc_populacji = 30


def generujPopulacje(wielkosc_populacji):

    populacja = []
    for i in range(wielkosc_populacji):
        osobnik = [np.random.randint(0, 1) for x in range(0, items_number)]
        populacja.append(osobnik)

    return populacja


def krzyzowanie(osobnik1, osobnik2):

    #losowanie locus podzialu
    l = np.random.randint(0,items_number)
    l = 3
    zarodek1 = osobnik1[:l] + osobnik2[l:]
    zarodek2 = osobnik2[:l] + osobnik1[l:]

    return zarodek1, zarodek2


def mutacja(zarodek):
    p_zmutowania = 10
    r = np.random.randint(0,10)
    if r < p_zmutowania:
        mutuj = True
    else:
        mutuj = False

    if mutuj:
        locus = np.random.randint(0, len(zarodek))
        if zarodek[locus] == 1:
            zarodek[locus] = 0
        else:
            zarodek[locus] = 1
    osobnik = zarodek
    return osobnik

# def przystosowanie(osobnik):
#     waga = 0
#     wartosc = 0
#
#     for gen in osobnik:
#         if gen == 1:
#             waga +=


def check_fitness(osobnik):
    total_weight = 0
    total_value = 0

    for i in range(len(osobnik)):
        if osobnik[i] == 1:
            if (total_weight + items[i].getWeight()) <= capacity:
                total_value = total_value + items[i].getValue()
                total_weight = total_weight + items[i].getWeight()
                # print("Wartosc x: ", osobnik[i], " Wartosc total_value: ", total_value, " Wartosc total_weight: ", total_weight)

    return total_value


# MAIN
populacja = generujPopulacje(wielkosc_populacji)
print(populacja)
for j in range(10):
    zarodki = []
    for i in range(0, wielkosc_populacji, 2):

        if i == wielkosc_populacji - 1:
            zarodek1, zarodek2 = krzyzowanie(populacja[i], populacja[0])
        else:
            zarodek1, zarodek2 = krzyzowanie(populacja[i], populacja[i+1])

        zarodki.append(zarodek1)
        zarodki.append(zarodek2)
    # print("Zarodki: ", zarodki)
    for zarodek in zarodki:
        populacja.append(mutacja(zarodek))

    # print(populacja)
    oceny_osobnikow = []
    for osobnik in populacja:
        wartosc = check_fitness(osobnik)
        oceny_osobnikow.append(wartosc)
    # print(oceny_osobnikow)
    populacja_oceny = zip(oceny_osobnikow, populacja)

    populacja_oceny = sorted(populacja_oceny)
    # print(populacja_oceny)
    populacjaPosortowana = [populacja for oceny_osobnikow, populacja in populacja_oceny]
    nowaPopulacja = populacjaPosortowana[-wielkosc_populacji:]
    # print(nowaPopulacja)
    najlepszyOsobnik = max(oceny_osobnikow)
    # print(najlepszyOsobnik)

    print("Numer iteracji: ", j, " Najlepszy osobnik: ", najlepszyOsobnik)
    print(nowaPopulacja[-1])

    populacja = nowaPopulacja
#

suma = 0
for i in range(len(items)):
    suma += (items[i].getWeight()*nowaPopulacja[-1][i])

print(suma)


