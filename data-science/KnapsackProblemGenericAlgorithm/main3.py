import numpy as np

class Przedmiot(object):
    def __init__(self, wartosc, waga):
        self.wartosc = wartosc
        self.waga = waga

#ile maksymalnie moze zmiescic walizka
pojemnosc = 140

#ilosc przedmiotow z ktorych wybieramy = ilosc genow osobnika
iloscPrzedmiotow = 10

#liczba osobnikow w populacji
wielkoscPopulacji = 100

#liczba pokolen
liczbaIteracji = 5

przedmioty = [Przedmiot(np.random.randint(0, 100), np.random.randint(0, 100)) for x in range(iloscPrzedmiotow)]


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


def mutacja(zarodek):
    p_zmutowania = 7
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


def sprawdzDostosowanie(osobnik):
    wagaCalkowita = 0
    wartoscCalkowita = 0
    indeks = 0
    for i in osobnik:
        if (i == 1):
            wartoscCalkowita += przedmioty[indeks].wartosc
            wagaCalkowita += przedmioty[indeks].waga
        indeks += 1

    if wagaCalkowita > pojemnosc:
        return 0
    else:
        return wartoscCalkowita


def pokazWyniki(przedmioty, najlepszyOsobnik):
    sumaWag = 0
    sumaWartosci = 0
    wagaPrzed = []
    wartoscPrzed = []
    for i in range(len(przedmioty)):
        wagaPrzed.append(przedmioty[i].waga)
        wartoscPrzed.append(przedmioty[i].wartosc)
        sumaWag += przedmioty[i].waga * najlepszyOsobnik[i]
        sumaWartosci += przedmioty[i].wartosc * najlepszyOsobnik[i]

    print("Wylosowane wagi: ", wagaPrzed)
    print("Wylosowane wartosci: ", wartoscPrzed)
    print("Najlepszy osobnik")
    print("Genotyp: ", najlepszyOsobnik)
    print("Wartosc: ", sumaWartosci)
    print("Waga: ", sumaWag)


def optymalizuj():
    populacja = generujPopulacje(wielkoscPopulacji)
    for j in range(liczbaIteracji):

        zarodki = []
        for i in range(0, wielkoscPopulacji, 2):
            if i == wielkoscPopulacji - 1:
                zarodek1, zarodek2 = krzyzowanie(populacja[i], populacja[0])
            else:
                zarodek1, zarodek2 = krzyzowanie(populacja[i], populacja[i+1])
            zarodki.append(zarodek1)
            zarodki.append(zarodek2)

        for zarodek in zarodki:
            populacja.append(mutacja(zarodek))

        ocenyOsobnikow = []
        for osobnik in populacja:
            wartosc = sprawdzDostosowanie(osobnik)
            ocenyOsobnikow.append(wartosc)

        populacjaOceny = sorted(zip(populacja, ocenyOsobnikow), key=lambda x:x[1])
        najlepszyOsobnik = populacjaOceny[-1][0]
        populacja, populacjaOceny = map(list, zip(*populacjaOceny))
        populacja= populacja[-wielkoscPopulacji:]

    return najlepszyOsobnik

najlepszyOsobnik = optymalizuj()
pokazWyniki(przedmioty, najlepszyOsobnik)




