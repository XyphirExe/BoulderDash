import upemtk
from upemtk import *
from random import *
from time import *
import copy
import sys
import os
from main import main


if __name__ == '__main__':
    cree_fenetre(400, 400)
    with open("config.txt") as config:
        quality = config.read().split(":")[1].replace("\n", "")[1:-1]

    print(quality)

    with open("./niveaux/lastSave.txt") as derniere_save:
        last_save = derniere_save.read().replace("\n", "")

    # Bouton "Jouer"
    rectangle(150, 100, 250, 150, "black", tag='Jouer')
    texte(200, 125, "Jouer", "black", "center", tag='Jouer')
    hover_jouer = False

    # Bouton "Sauvegarde"
    rectangle(260, 100, 290, 150, "black", tag='Save')
    texte(275, 125, "S", "black", "center", tag='Save')
    hover_save = False
    save_existe = False
    save_couleur = "red"

    # Bouton "Niveaux"
    rectangle(140, 175, 260, 225, "black", tag='Niveaux')
    texte(200, 200, "Niveaux", "black", "center", tag='Niveaux')
    hover_niveaux = False

    # Bouton "Qualité"
    if quality == "Normal":
        rectangle(10, 10, 60, 60, "black", "black", tag='Qualité')
        texte(35, 35, "HD", "white", "center", tag='Qualité')
        active_quality = True
    elif quality != "Normal":
        rectangle(10, 10, 60, 60, "black", tag='Qualité')
        texte(35, 35, "LD", "black", "center", tag='Qualité')
        active_quality = False
    hover_quality = False

    mise_a_jour()

    # Entrée nom niveau
    string = ''
    texte(200, 300, string, "black", tag='entreeNiv')
    menu_niveau = False
    niveau_existe = False
    niveau_couleur = "red"

    end = False
    while not end:
        temps = time()
        ev = donne_evenement()
        type_ev = type_evenement(ev)
        mise_a_jour()

        for i in range(len(upemtk.__canevas.eventQueue)):
            if upemtk.__canevas.eventQueue[i][0] == "Deplacement":
                del upemtk.__canevas.eventQueue[i:]
                break

        if not type_ev == "RAS":

            print(type_ev)

            if type_ev == "Quitte":
                end = True

            elif type_ev == "Touche" and menu_niveau:
                t = touche(ev)
                print(t)
                if t == "space":
                    string += ' '
                elif t == "BackSpace" and len(string) > 0:
                    string = string[:-1]
                elif t == "underscore":
                    string += '_'
                elif t == "minus":
                    string += "-"
                elif len(t) == 1:
                    string += t

                if os.path.isfile("./niveaux/" + string + '.txt'):
                    niveau_couleur = "green"
                    niveau_existe = True
                else:
                    niveau_couleur = "red"
                    niveau_existe = False

                if os.path.isfile("./niveaux/" + string + 'Save.txt'):
                    save_couleur = "green"
                    save_existe = True
                else:
                    save_couleur = "red"
                    save_existe = False

                if menu_niveau and hover_save:
                    efface("Save")
                    rectangle(260, 100, 290, 150, "black", save_couleur, tag='Save')
                    texte(275, 125, "S", "white", "center", tag='Save')
                elif menu_niveau and not hover_save:
                    efface("Save")
                    rectangle(260, 100, 290, 150, "black", save_couleur, tag='Save')
                    texte(275, 125, "S", "black", "center", tag='Save')

                efface("entreeNiv")
                texte(200, 300, string, niveau_couleur, "center", tag='entreeNiv')

            elif type_ev in ["ClicGauche", "ClicDroit", "Deplacement"]:
                ev_x, ev_y = clic_x(ev), clic_y(ev)

                if type_ev == "ClicGauche":

                    # Lancer le jeu
                    if 150 < ev_x < 250 and 100 < ev_y < 150:
                        print("Clic gauche au point", ev_x, ev_y)
                        ferme_fenetre()
                        if string != "" and niveau_existe:
                            print("yes")
                            if menu_niveau:
                                main(string, ver=quality)
                            else:
                                main(ver=quality)
                        else:
                            main(ver=quality)
                        sys.exit()

                    # Lancer la dernière sauvegarde
                    if 260 < ev_x < 290 and 100 < ev_y < 150:
                        if menu_niveau and not save_existe:
                            pass
                        else:
                            ferme_fenetre()
                            if not menu_niveau:
                                main(last_save, isSave=True, ver=quality)
                            elif menu_niveau and save_existe:
                                main(string, isSave=True, ver=quality)
                            else:
                                pass
                            sys.exit()

                    # Menu sélection de niveau
                    if 140 < ev_x < 260 and 175 < ev_y < 225:
                        if menu_niveau:
                            menu_niveau = False
                            efface('entreeNiv')
                            efface('RetourNiv')
                            efface('Niveaux')
                            efface("Save")
                            efface("entreeNiv")
                            rectangle(260, 100, 290, 150, "black", tag='Save')
                            texte(275, 125, "S", "black", "center", tag='Save')
                            rectangle(140, 175, 260, 225, "black", "black", tag='Niveaux')
                            texte(200, 200, "Niveaux", "white", "center", tag='Niveaux')
                        elif not menu_niveau:
                            menu_niveau = True
                            efface('Niveaux')
                            efface('RetourNiv')
                            efface("Save")
                            efface("entreeNiv")
                            texte(200, 300, string, niveau_couleur, "center", tag='entreeNiv')
                            rectangle(260, 100, 290, 150, "black", save_couleur, tag='Save')
                            texte(275, 125, "S", "black", "center", tag='Save')
                            rectangle(140, 175, 260, 225, "black", "black", tag='RetourNiv')
                            texte(200, 200, "Retour", "white", "center", tag='RetourNiv')

                    # Changer la qualité du jeu:
                    if 10 < ev_x < 60 and 10 < ev_y < 60:
                        if active_quality:
                            active_quality = False
                            with open("config.txt", "w") as config:
                                config.write("Quality:\"Low\"")
                            quality="Low"
                            efface("Qualité")
                            rectangle(10, 10, 60, 60, "black", tag='Qualité')
                            texte(35, 35, "LD", "black", "center", tag='Qualité')
                            efface("HoverQuality")
                            rectangle(11, 11, 59, 59, "white", tag="HoverQuality")
                            rectangle(12, 12, 58, 58, "black", tag="HoverQuality")
                        elif not active_quality:
                            active_quality = True
                            with open("config.txt", "w") as config:
                                config.write("Quality:\"Normal\"")
                            quality = "Normal"
                            efface("Qualité")
                            rectangle(10, 10, 60, 60, "black", "black", tag='Qualité')
                            texte(35, 35, "HD", "white", "center", tag='Qualité')
                            efface("HoverQuality")
                            rectangle(11, 11, 59, 59, "white", tag="HoverQuality")
                            rectangle(12, 12, 58, 58, "black", tag="HoverQuality")

                if type_ev == "Deplacement":
                    print(ev_x, ev_y)

                    # Animaton bouton "Jouer"
                    if 150 < ev_x < 250 and 100 < ev_y < 150:
                        hover_jouer = True
                    elif hover_jouer:
                        hover_jouer = False

                    if hover_jouer:
                        efface("Jouer")
                        rectangle(150, 100, 250, 150, "black", "black", tag='Jouer')
                        texte(200, 125, "Jouer", "white", "center", tag='Jouer')
                    else:
                        efface("Jouer")
                        rectangle(150, 100, 250, 150, "black", tag='Jouer')
                        texte(200, 125, "Jouer", "black", "center", tag='Jouer')

                    # Animation bouton "Niveau"
                    if 140 < ev_x < 260 and 175 < ev_y < 225:
                        hover_niveaux = True
                    elif hover_niveaux:
                        hover_niveaux = False

                    if hover_niveaux and not menu_niveau:
                        efface('RetourNiv')
                        efface('Niveaux')
                        rectangle(140, 175, 260, 225, "black", "black", tag='Niveaux')
                        texte(200, 200, "Niveaux", "white", "center", tag='Niveaux')
                    elif hover_niveaux and menu_niveau:
                        efface('Niveaux')
                        efface('RetourNiv')
                        rectangle(140, 175, 260, 225, "black", "black", tag='RetourNiv')
                        texte(200, 200, "Retour", "white", "center", tag='RetourNiv')
                    elif not menu_niveau:
                        efface('RetourNiv')
                        efface('Niveaux')
                        rectangle(140, 175, 260, 225, "black", tag='Niveaux')
                        texte(200, 200, "Niveaux", "black", "center", tag='Niveaux')
                    elif menu_niveau:
                        efface('Niveaux')
                        efface('RetourNiv')
                        rectangle(140, 175, 260, 225, "black", tag='RetourNiv')
                        texte(200, 200, "Retour", "black", "center", tag='RetourNiv')

                    # Animation bouton "Sauvegarde"
                    if 260 < ev_x < 290 and 100 < ev_y < 150:
                        hover_save = True
                    elif hover_save:
                        hover_save = False

                    if hover_save and not menu_niveau:
                        efface("Save")
                        rectangle(260, 100, 290, 150, "black", "black", tag='Save')
                        texte(275, 125, "S", "white", "center", tag='Save')
                    elif not menu_niveau:
                        efface("Save")
                        rectangle(260, 100, 290, 150, "black", tag='Save')
                        texte(275, 125, "S", "black", "center", tag='Save')
                    elif menu_niveau:
                        if hover_save:
                            efface("Save")
                            rectangle(260, 100, 290, 150, "black", save_couleur, tag='Save')
                            texte(275, 125, "S", "white", "center", tag='Save')
                        elif not hover_save:
                            efface("Save")
                            rectangle(260, 100, 290, 150, "black", save_couleur, tag='Save')
                            texte(275, 125, "S", "black", "center", tag='Save')

                    # Animation du bouton de qualité
                    if 10 < ev_x < 60 and 10 < ev_y < 60:
                        hover_quality = True
                    elif hover_quality:
                        hover_quality = False

                    if hover_quality:
                        efface("HoverQuality")
                        rectangle(11, 11, 59, 59, "white", tag="HoverQuality")
                        rectangle(12, 12, 58, 58, "black", tag="HoverQuality")
                    elif not hover_quality:
                        efface("HoverQuality")

        mise_a_jour()
