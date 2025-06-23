#Solutie:
# DFS + pruning(eliminare timpurie ale anumitor trasee daca acestea nu duc la o solutie mai buna decat cea cunoscuta) + sortare euristica(exploreaza vecinii mai "valorosi" mai intai)
# Depth-First Search exploreaza trasee posibile dintr-un punct de start, mergand cat mai adanc pe un traseu pana nu se mai poate continua apoi prin backtracking revine pentru a explora si alte trasee
# Functia 'calculeazaUpperBound' estimeaza un scor maxim posibil pe baza artefactelor ramase disponibile pe muchii nefolosite.
# Aceasta functie este una de bounding in stilul Branch and Bound, permite excluderea ramurilor inutile din arborele de cautare reducand spatiul de cautare
# Vecinii sunt ordonati descrescator dupa valoarea artefactelor din tunelurile adiacente cu scopul de a explora mai intai cele mai promitatoare trasee. Acest lucru creste probabilitatea ca scor_max sa ajunga repede la o valoare mare care va duce ulterior la mai mult pruning.

import csv
import time

# variabile globale
n = 0
graf = []
max_scor = 0
cel_mai_bun_traseu = []
start_time = 0
TIME_LIMIT = 299  # limita de executie maxima impusa in cerinta
artefacte_totale = 0  # suma tuturor artefactelor posibile
stop = False  # flag global pentru timeout

# returneaza numarul de camere, lista cu limitele de vizite si matricea graf cu tuneluri
def citeste_input(nume_fisier):
    with open(nume_fisier, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    n = int(data[0][0])  # numarul de camere = linia 1
    limite = list(map(int, data[1]))  # limitele de vizite pentru fiecare camera = linia 2

    # initializam matricea de adiacenta cu -1 tunel inexistent
    graf = [[-1] * n for _ in range(n)]
    for i in range(n - 1):  # construim matricea pe baza valorilor triunghiulare din fisier
        linie = list(map(int, data[2 + i]))
        for j, val in enumerate(linie):
            if val != -1:
                graf[i][i + j + 1] = val
                graf[i + j + 1][i] = val
    return n, limite, graf

# calculeaza un bound superior pentru scorul posibil ramas
def calculeazaUpperBound(scor_curent, artefacte_folosite):
    artefacte_ramase = []  #lista in care se vor stoca valorile tunelurilor nefolosite

    #parcurgem doar jumatatea superioara a matricei adiacente
    for i in range(n):
        for j in range(i + 1, n):
            #verificam daca exista un tunel intre i si j si daca nu a fost deja folosit
            if graf[i][j] != -1 and (i, j) not in artefacte_folosite:
                artefacte_ramase.append(graf[i][j])  #adaugam valoarea artefactului in lista
    #sortam valorile ramase si le adunam la scorul curent pentru a obtine estimarea maxima posibila
    return scor_curent + sum(sorted(artefacte_ramase, reverse=True)[:n])



# algoritmul DFS cu backtracking, optimizat cu pruning si sortare euristica
def depthFirstSearch(nod_curent, start, vizite_ramase, artefacte_folosite, traseu, scor_curent):
    global max_scor, cel_mai_bun_traseu, graf, n, start_time, TIME_LIMIT, artefacte_totale, stop

    # verificam daca am depasit timpul limita
    if time.time() - start_time > TIME_LIMIT:
        stop = True
        return

    # pruning pe baza scorului maxim estimat ramas
    if calculeazaUpperBound(scor_curent, artefacte_folosite) <= max_scor:
        return  # oprim recursivitatea daca nu putem depasi max_scor

    # daca am revenit in camera initiala si avem cel putin 1 pas efectuat
    if nod_curent == start and len(traseu) > 1:
        if scor_curent > max_scor:
            max_scor = scor_curent  # actualizam scorul maxim
            cel_mai_bun_traseu = traseu.copy()  # salvam traseul optim
        return

    # ordonam vecinii descrescator dupa valoarea artefactelor
    vecini = sorted(
        [(vecin, graf[nod_curent][vecin]) for vecin in range(n)
         if graf[nod_curent][vecin] != -1 and vizite_ramase[vecin] > 0],
        key=lambda x: -x[1]
    )

    for vecin, artefacte in vecini:
        tunel = tuple(sorted((nod_curent, vecin)))  # identificam tunelul indiferent de directie
        artefacte_castigate = 0

        # colectam artefactele doar daca tunelul nu a mai fost folosit
        if tunel not in artefacte_folosite:
            artefacte_castigate = graf[nod_curent][vecin]
            artefacte_folosite.add(tunel)

        traseu.append(vecin)  # adaugam camera in traseu
        vizite_ramase[vecin] -= 1  # scadem o vizita pentru camera vecinului

        # apelam recursiv DFS
        depthFirstSearch(vecin, start, vizite_ramase, artefacte_folosite, traseu, scor_curent + artefacte_castigate)

        # revenim la starea anterioara adica backtracking
        traseu.pop()
        vizite_ramase[vecin] += 1
        if artefacte_castigate > 0:
            artefacte_folosite.remove(tunel)

def main():
    global max_scor, cel_mai_bun_traseu, graf, n, start_time, TIME_LIMIT, artefacte_totale, stop

    nume_fisier = input("Nume fisier: ")
    n, limite, graf = citeste_input(nume_fisier)

    start_time = time.time()

    # calculam suma totala a artefactelor din toate tunelurile
    artefacte_totale = 0
    for i in range(n):
        for j in range(i + 1, n):
            if graf[i][j] != -1:
                artefacte_totale += graf[i][j]

    max_scor = 0
    cel_mai_bun_traseu = []

    # parcurgem toate camerele posibile ca punct de start
    for start in range(n):
        if stop or time.time() - start_time > TIME_LIMIT:
            break  # oprim executia daca am depasit timpul acordat

        if limite[start] >= 2:  # camera de start trebuie sa aiba minim 2 vizite
            vizite_ramase = limite.copy()
            vizite_ramase[start] -= 1  # folosim o vizita din camera de start
            depthFirstSearch(start, start, vizite_ramase, set(), [start], 0)

    with open("rezultat.txt", "w") as f_out:
        if cel_mai_bun_traseu:
            traseu_str = ",".join(str(x + 1) for x in cel_mai_bun_traseu)
            f_out.write(f"{traseu_str}\n")
            f_out.write(f"{max_scor}\n")
        else:
            f_out.write("N-a\n")

    end_time = time.time()
    print(f"Timp de executie: {end_time - start_time:.2f} secunde.")

if __name__ == "__main__":
    main()

