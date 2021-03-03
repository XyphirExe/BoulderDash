PROJET PYTHON ASTIER Yohan, GARCIA CALZADA Alan 

****************************************PHASE 1****************************************

Dans ce projet, nous avons produit un programme reproduisant le jeu Boulder Dash.
Notre programme peut: 

-Lire un niveau à partir d'une variable de type string (Permettre de lire à partir d'un fichier txt ne devrait pas être plus dur.
-Appliquer des textures sur les différents types de blocs.
-Deplacer un personnage.
-Pousser un rocher et le faire tomber si aucun bloc ne se situe en dessous.
-Tuer le personnage si il a un rocher au dessus de lui et qu'il se déplace vers le bas (La solution sera expliquée plus tard dans le document).
-Ramasser des diamants et creuser la terre.
-Aller à la sortie pour finir le niveau.
-Un mode reset qui remet le niveau à 0 en appuyant sur 'r'
-Un mode debug qui fait déplacer le personnage aléatoirement si on appuie sur 'd' et on peut retirer le mode debug en appuyant une nouvelle fois sur 'd'.

Toutes les textures de ce projet ont été réalisées par Alan, qui s'est juste inspiré du jeu 'minecraft' pour la terre. Le reste n'étant pas pris d'images
appartenant à d'autres personnes.

Pour ce qui est du code, pour générer le niveau nous avons décidé de lire la variable string ligne par ligne en mettant les coordonnées de chaque type de bloc rencontré
dans une liste correspondant au type de bloc elle même imbriquée dans une plus grande liste. Nous aurions pu faire une grande liste correspondant au statut de chaque case
mais cette option semblait plus compliquée à mettre en oeuvre.

Pour ce qui est du déplacement du personnage et de l'affichage, nous avons reprit en grande partie le tp de snake. Pour vérifier si il avait bien le droit de se déplacer
sur une case donnée, nous gardions 2 coordonnées du personnage, celles avant le déplacement, celles après le déplacement et nous regardions si il était dans une autre liste
si la case était vide on garde les coordonnées après le déplacement, sinon on garde celles d'avant. Si il arrive sur de la terre nous retirions les coordonnées de rockford après le déplacement 
de la liste terre. Nous faisions la même chose pour savoir si il est possible de pousser un rocher en nous basant sur la direction dans laquelle il était bloqué.

Pour ce qui est de la fin de partie, le joueur gagne uniquement si il arrive à la sortie, nous n'avons pas mis en place de système pour compter les diamants

Pour que le joueur perde, c'était le cas le plus dur à gérer du projet, il doit se situer en dessous d'une case de rocher et descendre vers le bas, en effet, dans ce cas
le rocher l'écrase. Si il se déplace sur le coté il est sauvé. L'idéal aurait été de permettre au joueur de fuir la chute du rocher si il continue de se déplacer vers
le bas mais nous n'avons pas réussit.

Pour réaliser ce programme nous avons eu besoin de 3 modules:
-upemtk pour représenter le jeu et insérer des images.
-time pour ralentir le mode debug et permettre à l'utilisateur de voir les déplacements de son personnage.
-random principalement pour choisir aléatoirement une direction dans le mode debug.

****************************************PHASE 2****************************************

Dans le cadre de cette phase 2, un changement majeur a été éffectué, plutot que de stocker les coordonnées de tous les objets dans une liste. Nous avons décidé de modifier la structure pour qu'une matrice
puisse correspondre à notre niveau et chaque case stock le type d'objet. Qui peuvent être:

-W pour les murs
-R pour rockford
-B pour les rochers
-F pour les rochers en chute (nous reviendrons dessus)
-E pour la sortie fermée
-S pour la sortie ouverte (nous reviendrons aussi dessus)
-D pour le diamants
-T pour le diamants qui tombe (idem)

Ainsi, nous avons mis en place dans le cadre de la phase 2 un systeme permettant à ce que seul un rocher dans un état de chute et d'éboulement puisse tuer notre
personnage. Ainsi, le rocher en état de chute est modélisé par le "F" et nous pouvons plus facilement permettre à l'utilisateur de lui échapper.
Cette fonctionnalité marche de la même manière pour les diamants car nous avons implémenté leur chute.

Comme nouvelle fonctionnalité nous avons aussi permis à l'utilisateur d'entrer le nom d'un fichier niveau en paramètre pour que le programme puisse le lire 
si aucun fichier n'est donné en paramètre ou alors qu'il est introuvable, le programme crée lui même et enregistre dans un fichier à part un niveau aléatoire pour
ensuite pouvoir le lire. Pour se faire, nous créons aléatoirement une matrice qui a une certaine taille choisie aléatoirement dans un intervalle afin d'y ajouter tous
les blocs qui peuvent avoir un nombre variable d'occurences pour ensuite y rajouter ceux qui doivent avoir un nombre fixe (comme Rockford par exemple).

De plus, lorsque l'utilisateur quitte le programme en cliquant sur la croix, nous sauvegardons le niveau dans un fichier sous la forme nomniveausave.txt .

Nous avons aussi inséré un chronomètre et un compteur de diamants, et lorsque l'utilisateur a collecté le nombre minimum de diamants stipulé dans le niveau
il peut emprunter la sortie, d'où l'ajout de 2 types de sorties: sortie ouverte et fermée. Et lors de la fin de jeu (soit le joueur est mort soit il a emprunté
la sortie), nous calculons son score en fonction du temps restant et du nombre de diamants collectés et lui affichons les 10 meilleurs scores pour ce niveau.

Le problème majeur que nous ayons rencontré est que la bibliothèque upemtk semble avoir plus de mal pour afficher des images. Et comme nous demandons à notre programme
de réafficher toutes les cases à chaque tour, cela peut engendrer quelques ralentissements. 3 solutions ont alors été envisagées:
- Afficher certains objets avec des formes simple. Un cercle par exemple pour un rocher.
- Réduire la qualité des images.
- Ne réafficher seulement les blocs ayant été modifié. Cependant, pour cette solution nous devons utiliser les "tags" liés aux images et ils semblent avoir
une limite.

****************************************PHASE 3****************************************

Nous avons introduit dans cette phase 3 un menu principal avec sélection de niveau ainsi que de sauvegardes (dernière sauvegarde effectuée en globale ou pour un niveau précis) (Extension 2.a).
L'extension 1.a a été introduite en phase 2 (les roches et diamants vont prendre un certains temps pour effectuer un éboulement).
Nous avons aussi rajouté une version basse qualité qui peut être activer avec comme paramètre "-l" (pour "l" pour "Low quality") dans la console.
La dernière sauvegarde effectuée peut être accédé avec le paramètre "-s", si un nom de niveau a été spécifié en premier paramètre et "-s" en deuxième alors la dernière sauvegarde de ce niveau sera prise en compte.

Sur le menu, la touche "S" permet de lancer la dernière sauvegarde globale dans le menu principale sinon la dernière sauvegarde d'un niveau spécifié dans le menu "Niveaux" (il suffit d'écrire le nom du niveau dans ce menu).
La touche "HD"/"LD" permet de changer la qualité du jeu ("HD" est la qualité normale avec des images et "LD" est la basse qualité avec des formes au lieu d'images à part pour Rockford et la sortie du niveau)

Nous avons créer ce mode basse qualité car comme spécifié à la fin du Readme Phase 2, nous n'avons pas pu mieux gérer les images.
Il est donc conseillé de jouer en basse qualité pour moins de "ralentissements".
Sinon vous pouvez profitez de nos textures avec le mode "HD".
