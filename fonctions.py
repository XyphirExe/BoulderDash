from upemtk import *
from random import *
from time import *
import copy
import sys
import os

def niveaualeat():
    '''Cette fonction va créer un fichier contenant une carte générée aléatoirement'''

    # Nous choisissons les dimensions de la carte aléatoirement, le nombre de diamants est fixe, 5% du nombre de cases
    NbLongueur = randint(10, 20)
    NbLargeur = randint(5, 10)
    Nbcase = NbLongueur*NbLargeur
    nbDiamants = int(Nbcase * 0.05)

    # On crée dans un premier temps le niveau sous forme de liste qu'on recopie plus tard dans le fichier txt
    niveau = []

    # Le choix se fera dans cette liste, plus l'élement y est présent, plus il y en aura dans le niveau
    listeElem = ["G"] * 10 + ["."] * 3 + ["B"] * 2

    niveau.append(["W"] * NbLongueur)
    # On fait NbLargeur-2 car les extremitées seront toujours des murs
    for i in range(NbLargeur - 2):
        ligne = ["W"]
        for j in range(NbLongueur - 2):
            ligne.append(choice(listeElem))

        ligne.append("W")

        niveau.append(ligne)

    niveau.append(["W"]*NbLongueur)


    # On ajoute ensuite la sortie et les diamants qui ont chacun un nombre fixe
    listeElem = ["R", "E"] + ["D"] * nbDiamants
    while len(listeElem) != 0:
        # Il faut faire attention à ce que l'on ne remplace pas un des éléments de cette liste
        coord = (randint(1, NbLargeur - 1), randint(1, NbLongueur - 1))
        if niveau[coord[0]][coord[1]] not in ("R", "D", "E", "W"):
            niveau[coord[0]][coord[1]] = listeElem[0]
            listeElem.pop(0)


    # On l'écrit ensuite dans un fichier
    with open("./niveaux/NivAlea.txt", "w") as fichier:
        fichier.write(str(randint(120, 180))+"s"+" "+str(int(nbDiamants - randint(0, nbDiamants - 1)))+"d"+"\n")
        for element in niveau:
            fichier.write("".join(element)+"\n")


def setCarte(niveau):
    '''Cette fonction doit à partir d'un fichier entré en paramètre, créer une matrice correspondant au niveau'''
    matrice = []

    # Avec splitlines on lit chaque ligne du fichier une à une en oubliant la première car elle ne nous interesse pas
    listNiveau = niveau.splitlines()[1:]
    lenNiv = len(listNiveau[0])
    larNiv = len(listNiveau)

    # On construit ensuite la matrice
    for i in range(larNiv):
        ligne = []
        for j in range(lenNiv):
            ligne.append(listNiveau[i][j])
        matrice.append(ligne)

    return matrice


def posRF(mat):
    '''Cette fonction doit renvoyer les coordonnées de Rockford ou False si il n'est pas dans la matrice'''
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == "R":
                return (j, i)
    return False


def affiche_elements(mat, taillecase, largeurfenetre, longfenetre):
    '''Cette fonction affiche chaque élément de la matrice un à un'''
    rectangle(0, 0, largeurfenetre, longfenetre, "Black", "Black")
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            pos = mat[i][j]
            if pos == 'W':
                image(j*taillecase + taillecase/2, i*taillecase + taillecase/2, './images/wall.gif')
            elif pos == 'R':
                image(j*taillecase + taillecase/2, i*taillecase + taillecase/2, './images/rockford.gif')
            elif pos == "B" or pos == "F":
                image(j*taillecase + taillecase/2, i*taillecase + taillecase/2, './images/rock.gif')
            elif pos == "G":
                image(j*taillecase + taillecase/2, i*taillecase + taillecase/2, './images/dirtblock.gif')
            elif pos == "E":
                image(j*taillecase + taillecase/2, i*taillecase + taillecase/2, './images/wayout.gif')
            elif pos == "S":
                image(j*taillecase + taillecase/2, i*taillecase + taillecase/2, './images/wayoutOpen.gif')
            elif pos == "D" or pos == "T":
                image(j*taillecase + taillecase/2, i*taillecase + taillecase/2, './images/diamond.gif')


def affiche_elements_lq(mat, taillecase, largeurfenetre, longfenetre):
    '''Cette fonction affiche chaque élément de la matrice un à un'''
    rectangle(0, 0, largeurfenetre, longfenetre, "Black", "Black")
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            pos = mat[i][j]
            if pos == 'W':
                rectangle(j*taillecase, i*taillecase, j*taillecase + taillecase, i*taillecase + taillecase, 'black', 'red')
            elif pos == 'R':
                image(j*taillecase + taillecase/2, i*taillecase + taillecase/2, './images/rockford.gif')
            elif pos == "B" or pos == "F":
                cercle(j*taillecase + taillecase/2, i*taillecase + taillecase/2, taillecase/2, 'black', 'grey')
            elif pos == "G":
                rectangle(j*taillecase, i*taillecase, j*taillecase + taillecase, i*taillecase + taillecase, 'black', 'brown')
            elif pos == "E":
                image(j*taillecase + taillecase/2, i*taillecase + taillecase/2, './images/wayout.gif')
            elif pos == "S":
                image(j*taillecase + taillecase/2, i*taillecase + taillecase/2, './images/wayoutOpen.gif')
            elif pos == "D" or pos == "T":
                polygone([(j*taillecase + taillecase/2, i*taillecase), (j*taillecase + taillecase, i*taillecase + taillecase/2), (j*taillecase + taillecase/2, i*taillecase + taillecase), (j*taillecase, i*taillecase + taillecase/2)], 'black', 'blue')


def ouvrePortes(mat):
    '''Cette fonction permet de sortir une fois qu'il n'y a plus de diamant dans le jeu'''
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            pos = mat[i][j]
            # Pour différencier quand le joueur peut sortir ou non, il y a deux types d'objets, E qui est la porte fermée
            # Et S qui est la porte ouverte
            if pos == "E":
                mat[i][j] = "S"

    return copy.deepcopy(mat)


def DeplacementRockford(rockford, direction, mat):
    '''Cette fonction doit permettre de donner de nouvelles coordonnées à rockford en fonction du déplacement.'''

    oldRockford = rockford
    ''' On calcule les nouvelles coordonnées de Rockford suite au déplacement'''
    if direction == "Left":
        rockford = (rockford[0]-1, rockford[1])
    elif direction == "Right":
        rockford = (rockford[0]+1, rockford[1])
    elif direction == "Up":
        rockford = (rockford[0], rockford[1]-1)
    elif direction == "Down":
        rockford = (rockford[0], rockford[1]+1)
    else:
        return oldRockford

    if not 0 <= rockford[0] < len(mat[0])and 0 <= rockford[1] < len(mat):
        return oldRockford

    if mat[rockford[1]][rockford[0]] in ['B', 'F']:
        return deplacementcaillou(rockford, oldRockford, mat)

    if mat[rockford[1]][rockford[0]] in ['W', 'B', 'F']:
        return oldRockford

    if mat[rockford[1]][rockford[0]] == 'E':
        return oldRockford

    if mat[rockford[1]][rockford[0]] == 'S':
        mat[oldRockford[1]][oldRockford[0]] = '.'
        return True

    mat[rockford[1]][rockford[0]] = 'R'
    mat[oldRockford[1]][oldRockford[0]] = '.'

    return rockford


def deplacementcaillou(rockford, oldrockford, mat):
    '''Cette fonction permet à Rockford de pousser les rochers'''

    # On regarde de quel coté vient rockford puis si la place est vide
    if oldrockford == (rockford[0] - 1, rockford[1]):
        if mat[rockford[1]][rockford[0] + 1] == '.':
            mat[rockford[1]][rockford[0] + 1] = 'B'
            mat[rockford[1]][rockford[0]] = 'R'
            mat[oldrockford[1]][oldrockford[0]] = '.'
            return rockford

    if oldrockford == (rockford[0] + 1, rockford[1]):
        if mat[rockford[1]][rockford[0] - 1] == '.':
            mat[rockford[1]][rockford[0] - 1] = 'B'
            mat[rockford[1]][rockford[0]] = 'R'
            mat[oldrockford[1]][oldrockford[0]] = '.'
            return rockford

    return oldrockford


def entree():
    '''Cette fonction doit permettre de lire une direction ou une touche de l'utilisateur'''
    ev = donne_evenement()
    type_ev = type_evenement(ev)
    if type_ev == "Touche":
        t = touche(ev)
        return t
    elif type_ev == "Quitte":
        return 'stop'


def deplacement_debug():
    '''Si l'utilisateur ne fait rien on retourne une direction au hasard'''
    return choice(('Up', 'Right', 'Left', 'Down'))


def peutEbouler(mat):
    '''Cette fonction a pour but de verifier si il existe des objets dans le jeu qui peuvent ébouler'''
    for i in range(len(mat)-1):
        for j in range(len(mat[i])):
            if mat[i][j] in ['B', 'F', 'E', 'T'] and (mat[i + 1][j] in ['.'] or mat[i + 1][j + 1] in ['.', 'R'] or mat[i + 1][j - 1] in ['.', 'R']):
                return True
    return False


def stopEboulement(mat):
    '''Cette fonction doit vérifier quand un objet doit cesser d'etre en eboulement'''

    matrice = copy.deepcopy(mat)

    for i in range(len(mat)-1):
        for j in range(len(mat[i])):
            # Le "f" correspond au rocher en chute, on regarde si la case en dessous est prise
            if mat[i][j] == 'F' and mat[i + 1][j] in ['E', 'T', 'G', 'D', 'S', 'W', 'B']:
                matrice[i][j] = 'B'

            # Le "T" correspond au Diamant en chute, on regarde si la case en dessous est prise
            elif mat[i][j] == 'T' and mat[i + 1][j] in ['E', 'F', 'G', 'D', 'S', 'W', 'B']:
                matrice[i][j] = 'D'

    return copy.deepcopy(matrice)


def eboulement(mat):
    '''Cette fonction permet de faire tomber les objets qui doivent l'etre'''
    matrice = copy.deepcopy(mat)

    for i in range(len(mat)-1):
        for j in range(len(mat[i])):

            if mat[i][j] == 'B':
                # On regarde si le rocher peut ébouler verticalement
                if mat[i + 1][j] in ['.']:
                    # Pour modeliser un rocher en chute, il devient un autre type "F" qui peut désormais écraser rockford
                    matrice[i + 1][j] = 'F'
                    matrice[i][j] = '.'

                    # On regarde sinon si il peut ébouler latéralement
                elif mat[i][j + 1] == '.' and mat[i + 1][j + 1] and matrice[i + 1][j + 1] == '.':
                    matrice[i + 1][j + 1] = 'F'
                    matrice[i][j] = '.'
                elif mat[i][j - 1] == '.' and mat[i + 1][j - 1] and matrice[i + 1][j - 1] == '.':
                    matrice[i + 1][j - 1] = 'F'
                    matrice[i][j] = '.'

            # On effecture le même travail pour les rochers en chute, désormais, si Rockford est en dessous il peut etre écrasé
            if mat[i][j] == 'F':
                if mat[i + 1][j] in ['.', 'R']:
                    matrice[i + 1][j] = 'F'
                    matrice[i][j] = '.'
                elif mat[i][j + 1] == '.' and mat[i + 1][j + 1] and matrice[i + 1][j + 1] == '.':
                    matrice[i + 1][j + 1] = 'F'
                    matrice[i][j] = '.'
                elif mat[i][j - 1] == '.' and mat[i + 1][j - 1] and matrice[i + 1][j - 1] == '.':
                    matrice[i + 1][j - 1] = 'F'
                    matrice[i][j] = '.'

            # La chute des diamants fonctionne comme celle des rochers vue ci-dessus
            if mat[i][j] == 'D':
                if mat[i + 1][j] in ['.']:
                    matrice[i + 1][j] = 'T'
                    matrice[i][j] = '.'
                elif mat[i][j + 1] == '.' and mat[i + 1][j + 1] and matrice[i + 1][j + 1] == '.':
                    matrice[i + 1][j + 1] = 'T'
                    matrice[i][j] = '.'
                elif mat[i][j - 1] == '.' and mat[i + 1][j - 1] and matrice[i + 1][j - 1] == '.':
                    matrice[i + 1][j - 1] = 'T'
                    matrice[i][j] = '.'
            if mat[i][j] == 'T':
                if mat[i + 1][j] in ['.', 'R']:
                    matrice[i + 1][j] = 'T'
                    matrice[i][j] = '.'
                elif mat[i][j + 1] == '.' and mat[i + 1][j + 1] and matrice[i + 1][j + 1] == '.':
                    matrice[i + 1][j + 1] = 'T'
                    matrice[i][j] = '.'
                elif mat[i][j - 1] == '.' and mat[i + 1][j - 1] and matrice[i + 1][j - 1] == '.':
                    matrice[i + 1][j - 1] = 'T'
                    matrice[i][j] = '.'

    return copy.deepcopy(matrice)


def perdu(largeurfenetre, longfenetre):
    '''Cette fonction affiche à l'utilisateur qu'il a perdu'''
    texte(largeurfenetre//2, longfenetre//2, "Perdu!", "white", "center")
    mise_a_jour()


def gagne(largeurfenetre, longfenetre):
    '''Cette fonction affiche à l'utilisateur qu'il a gagné '''
    texte(largeurfenetre//2, longfenetre//2, "Gagné!", "white", "center")
    mise_a_jour()


def sauvegardeNiv(mat, nomNiveau, tempsTimer, nombreDiamantsVictoire, diamantsRecoltes):
    '''Cette fonction permet de sauvegarder un niveau dans un fichier de type  nomNiveauSave.txt '''

    with open('./niveaux/' + nomNiveau[:-4] + 'Save.txt', 'w') as save:
        texte = str(tempsTimer) + 's ' + str(nombreDiamantsVictoire - diamantsRecoltes) + 'd' + '\n'
        for ligne in mat:
            texte += ''.join(ligne) + '\n'
        print(texte)
        save.write(texte)


    with open('./niveaux/lastSave.txt', 'w') as save:
        save.write(nomNiveau[:-4])


def comptediamants(mat):
    '''Cette fonction a pour but de compter les diamants et verifier si les conditions de victoire sont remplies'''
    compteur = 0
    for i in range(len(mat) - 1):
        for j in range(len(mat[i]) - 1):
            if mat[i][j] == "D" or mat[i][j] == "T":
                compteur += 1
    return compteur


# FONCTION POUR ALLEGER LE MAIN
def OuvNiveau(nomPreRempli):
    '''Cette fonction permet de lire le nom d'un niveau donné en argument ou non'''

    # Si un nom a été donné en argument, on regarde si il existe, si oui, on pourra l'ouvrir
    if len(sys.argv) >= 2:
        if not os.path.isfile('./niveaux/' + sys.argv[1] + '.txt'):
            sys.exit("Ce niveau n'existe pas !")
        return sys.argv[1] + ".txt"

    elif nomPreRempli is not None:
        return nomPreRempli + ".txt"

    # Si aucun fichier n'a été donné en paramètre, on en crée un aléatoirement et on renvoie son nom
    else:
        niveaualeat()
        return 'NivAlea.txt'


def fichierscore(nomNiveau, sauvegarde):
    '''Cette fonction crée un fichier score pour le niveau si il n'existe pas'''
    rmSaveStr = 0
    if sauvegarde:
        rmSaveStr = -4

    # Si il n'y a pas de fichiers de score pour ce niveau on en crée un
    if not os.path.isfile("./scores/" + nomNiveau[:-4 + rmSaveStr] + "Scores.txt") and nomNiveau != 'NivAlea.txt':
        with open("./scores/" + nomNiveau[:-4 + rmSaveStr] + "Scores.txt", "w") as fichier:
            fichier.write("Scores de ce niveau :\n")


def finjeu(score, carte, direction, result, tempsTimer, nomNiveau, largeurfenetre, longfenetre, nombreDiamantsVictoire, diamantsRecoltes):
    '''Cette fonction gère la fin de jeu, la sauvegarde du fichier et l'affichage du score'''

    # Si l'utilisateur a cliqué sur la croix, on sauvegarde le fichier
    if direction == 'stop':
        sauvegardeNiv(carte, nomNiveau, tempsTimer, nombreDiamantsVictoire, diamantsRecoltes)
        ferme_fenetre()
        sys.exit("Partie sauvegardée!\nLancer le programme avec \"save\" en deuxième argument.\n(\"python (nom de niveau) save\")")

    # Sinon, si l'utilisateur a gagné, on calcule le score et on lui affiche qu'il a gagné
    elif result:
        score += tempsTimer * 10
        gagne(largeurfenetre, longfenetre)
        fin = "Gagné !"
        attente_clic()

    # Sinon il a perdu
    else:
        perdu(largeurfenetre, longfenetre)
        fin = "Perdu ..."
        attente_clic()

    efface_tout()
    ferme_fenetre()

    # On s'occupe ensuite d'afficher le tableau des scores
    cree_fenetre(500, 700)
    rectangle(0, 0, 500, 700, "Black", "Black")
    mise_a_jour()
    sleep(0.5)
    texte(250, 70, fin, "white", "center", tag='1')
    mise_a_jour()
    sleep(0.5)

    texte(250, 150, "Votre score : " + str(score), "white", "center", tag='2')
    mise_a_jour()
    sleep(0.5)

    # On affiche ensuite les autres scores de la meme carte
    with open("./scores/" + nomNiveau[:-4] + "Scores.txt") as fichier:

        texteFichier = fichier.read()
        lstTexte = texteFichier.split("\n")

        if '' in lstTexte:
            lstTexte.remove('')

        lstScores = [int(e) for e in lstTexte[1:]]
        lstScores = sorted(lstScores + [int(score)], reverse=True)
        scores = str(lstTexte[0]) + '\n' + '\n'.join([str(e) for e in lstScores])

    with open("./scores/" + nomNiveau[:-4] + "Scores.txt", "w") as fichier:
        fichier.write(scores)

    sleep(1)
    texte(250, 200, str(lstTexte[0]), "white", "center", tag='3')
    mise_a_jour()
    for i in range(len(lstScores[0:10])):
        sleep(i * 0.075 + 0.4)
        texte(250, 660 - i * 45, str(lstScores[len(lstScores[0:10]) - i - 1]), "white", "center", tag=str(4 + i))
        mise_a_jour()

    sleep(3)

    for i in range(14):
        efface(str(14 - i))
        mise_a_jour()
        sleep(0.25 + i * 0.01)

    ferme_fenetre()
