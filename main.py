from upemtk import *
import upemtk
from random import *
from time import *
import copy
import sys
import os
from fonctions import *


def main(nomPreRempli=None, isSave=False, ver="Normal"):

    if "-l" in sys.argv:
        ver = "Low"
        sys.argv.remove("-l")

    taillecase = 50

    if len(sys.argv) == 2 and sys.argv[1] == "-s":
        with open('./niveaux/lastSave.txt') as lastSave:
            nomNiveau = lastSave.read().replace("\n", "") + "Save.txt"
    else:
        nomNiveau = OuvNiveau(nomPreRempli)

    sauvegarde = False
    if len(sys.argv) > 2 and sys.argv[2] == "-s":
        if not os.path.isfile('./niveaux/' + sys.argv[1] + "Save.txt"):
            print('./niveaux/' + sys.argv[1] + "Save.txt")
            sys.exit("ErrCMD : Il n'y a pas de sauvegarde pour ce niveau !")
        sauvegarde = True
    elif isSave:
        if not os.path.isfile('./niveaux/' + nomPreRempli + "Save.txt"):
            print('./niveaux/' + nomPreRempli + "Save.txt")
            sys.exit("ErrMenu : Il n'y a pas de sauvegarde pour ce niveau !")
        sauvegarde = True

    if sauvegarde:
        with open('./niveaux/' + nomNiveau[:-4] + "Save.txt") as niveau:
            niv = niveau.read()
    else:
        with open('./niveaux/' + nomNiveau) as niveau:
            niv = niveau.read()

    fichierscore(nomNiveau, sauvegarde)

    # On initialise d'abord le jeu
    tempsInit = int(time())
    tempsTimerInit = int(niv[0:niv.find('s')])
    nombreDiamantsVictoire = int(niv[niv.find('s') + 2: len(niv.splitlines()[0]) - 1])

    print('temps = ', tempsTimerInit)
    print('diamants = ', nombreDiamantsVictoire)
    score = 0

    carte = setCarte(niv)
    carteReset = copy.deepcopy(carte)
    largeurfenetre = taillecase * len(carte[0])
    longfenetre = taillecase * len(carte) + 50

    cree_fenetre(largeurfenetre, longfenetre)
    debug = False
    rockford = posRF(carte)
    direction = ""
    faireEboulement = 0
    tempsEboulement = 0
    result = False
    porteOuvertes = False
    diamantsRecoltes = 0
    nombreDiamants = comptediamants(carte)

    oops = ''
    for ligne in carte:
        oops += ''.join(ligne) + '\n'
    print(oops)

    while True:

        for i in range(len(upemtk.__canevas.eventQueue)):
            if upemtk.__canevas.eventQueue[i][0] == "Touche":
                del upemtk.__canevas.eventQueue[i + 2:]
                break

        carte = stopEboulement(carte)

        tempsTimer = tempsTimerInit - (int(time()) - tempsInit)
        if tempsTimer < 0:
            break

        diamantsPresents = comptediamants(carte)
        if diamantsPresents < nombreDiamants:
            tempsTimerInit += 10
            score += 100
            diamantsRecoltes += 1
            nombreDiamants = diamantsPresents

        if not porteOuvertes and diamantsRecoltes >= nombreDiamantsVictoire:
            carte = ouvrePortes(carte)
            porteOuvertes = True

        if not posRF(carte):
            resulat = False
            break

        direction = entree()
        if direction == 'stop':
            break
        elif direction == "d":
            if debug:
                debug = False
            else:
                debug = True
        elif direction == "r":
            carte = copy.deepcopy(carteReset)
            rockford = posRF(carte)
            tempsInit = int(time())
            tempsTimerInit = int(niv[0:niv.find('s')])
            nombreDiamants = nombreDiamantsVictoire

        if debug:
            direction = deplacement_debug()

        rockford = DeplacementRockford(rockford, direction, carte)
        if rockford is True:
            efface_tout()
            if ver != "Normal":
                affiche_elements_lq(carte, taillecase, largeurfenetre, longfenetre)
            else:
                affiche_elements(carte, taillecase, largeurfenetre, longfenetre)
            result = True
            break

        if time() - tempsEboulement > 0.25 and faireEboulement:
            carte = eboulement(carte)
            tempsEboulement = time()

        if peutEbouler(carte):
            faireEboulement = True
        else:
            faireEboulement = False

        efface_tout()
        if ver != "Normal":
            affiche_elements_lq(carte, taillecase, largeurfenetre, longfenetre)
        else:
            affiche_elements(carte, taillecase, largeurfenetre, longfenetre)
        texte(10, longfenetre - 45, str(tempsTimer) + ' secondes', "white")
        if nombreDiamantsVictoire >= 0:
            texte(largeurfenetre - 265, longfenetre - 45, 'Diamants : ' + str(diamantsRecoltes) + ' sur ' + str(nombreDiamantsVictoire), "white")
        else:
            texte(largeurfenetre - 265, longfenetre - 45, 'Diamants : ' + str(diamantsRecoltes), "white")
        mise_a_jour()

        sleep(0.001)

    finjeu(score, carte, direction, result, tempsTimer, nomNiveau, largeurfenetre, longfenetre, nombreDiamantsVictoire, diamantsRecoltes)


if __name__ == "__main__":
    main()
