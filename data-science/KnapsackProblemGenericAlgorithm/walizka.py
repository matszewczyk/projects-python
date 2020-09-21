import numpy as np


class Przedmiot(object):
    def __init__(self, wartosc, objetosc):
        self.wartosc = wartosc
        self.objetosc = objetosc

#ile maksymalnie moze zmiescic walizka
pojemnosc = 1000

#ilosc przedmiotow z ktorych wybieramy (równa ilosci genow osobnika)
iloscPrzedmiotow = 50

#liczba osobnikow w populacji
wielkoscPopulacji = 30

#liczba pokolen
liczbaPokolen = 50

#prawdopodobienstwo mutacji
p_mutacji = 7

przedmioty = [Przedmiot(np.random.randint(1, 101), np.random.randint(1, 101)) for x in range(iloscPrzedmiotow)]


def generujPopulacje(wielkoscPopulacji):

    populacja = []
    for i in range(wielkoscPopulacji):
        osobnik = [np.random.randint(0, 1) for x in range(0, iloscPrzedmiotow)]
        populacja.append(osobnik)

    return populacja


def krzyzowanie(osobnik1, osobnik2):

    #losowanie locus podzialu
    locus = np.random.randint(0, iloscPrzedmiotow)

    zarodek1 = osobnik1[:locus] + osobnik2[locus:]
    zarodek2 = osobnik2[:locus] + osobnik1[locus:]

    return zarodek1, zarodek2


def mutacja(zarodek, p_mutacji):
    r = np.random.randint(0,10)
    if r < p_mutacji:
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


def sprawdzDostosowanie(osobnik):
    objCalkowita = 0
    wartoscCalkowita = 0
    indeks = 0
    for i in osobnik:
        if (i == 1):
            wartoscCalkowita += przedmioty[indeks].wartosc
            objCalkowita += przedmioty[indeks].objetosc
        indeks += 1

    if objCalkowita > pojemnosc:
        return 0
    else:
        return wartoscCalkowita


def pokazWyniki(przedmioty, najlepszyOsobnik):
    sumaObj = 0
    sumaWartosci = 0
    objPrzed = []
    wartoscPrzed = []
    for i in range(len(przedmioty)):
        objPrzed.append(przedmioty[i].objetosc)
        wartoscPrzed.append(przedmioty[i].wartosc)
        sumaObj += przedmioty[i].objetosc * najlepszyOsobnik[i]
        sumaWartosci += przedmioty[i].wartosc * najlepszyOsobnik[i]

    print("Wylosowane wagi: ", objPrzed)
    print("Wylosowane wartosci: ", wartoscPrzed)
    print("Najlepszy osobnik")
    print(" 1. Genotyp: ", najlepszyOsobnik)
    print(" 2. Wartosc: ", sumaWartosci)
    print(" 3. Objetosc: ", sumaObj)


def optymalizuj(populacja):

    for j in range(liczbaPokolen):

        zarodki = []
        for i in range(0, wielkoscPopulacji, 2):
            if i == wielkoscPopulacji - 1:
                zarodek1, zarodek2 = krzyzowanie(populacja[i], populacja[0])
            else:
                zarodek1, zarodek2 = krzyzowanie(populacja[i], populacja[i+1])
            zarodki.append(zarodek1)
            zarodki.append(zarodek2)

        for zarodek in zarodki:
            populacja.append(mutacja(zarodek, p_mutacji))

        ocenyOsobnikow = []
        for osobnik in populacja:
            wartosc = sprawdzDostosowanie(osobnik)
            ocenyOsobnikow.append(wartosc)

        populacjaOceny = sorted(zip(populacja, ocenyOsobnikow), key=lambda x:x[1])
        najlepszyOsobnik = populacjaOceny[-1][0]
        populacja, populacjaOceny = map(list, zip(*populacjaOceny))
        populacja= populacja[-wielkoscPopulacji:]

    return najlepszyOsobnik


populacjaPoczatkowa = generujPopulacje(wielkoscPopulacji)
najlepszyOsobnik = optymalizuj(populacjaPoczatkowa)
pokazWyniki(przedmioty, najlepszyOsobnik)

