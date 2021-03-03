PROJET PYTHON ASTIER Yohan, GARCIA CALZADA Alan 

****************************************PHASE 1****************************************

Dans ce projet, nous avons produit un programme reproduisant le jeu Boulder Dash.
Notre programme peut: 

-Lire un niveau � partir d'une variable de type string (Permettre de lire � partir d'un fichier txt ne devrait pas �tre plus dur.
-Appliquer des textures sur les diff�rents types de blocs.
-Deplacer un personnage.
-Pousser un rocher et le faire tomber si aucun bloc ne se situe en dessous.
-Tuer le personnage si il a un rocher au dessus de lui et qu'il se d�place vers le bas (La solution sera expliqu�e plus tard dans le document).
-Ramasser des diamants et creuser la terre.
-Aller � la sortie pour finir le niveau.
-Un mode reset qui remet le niveau � 0 en appuyant sur 'r'
-Un mode debug qui fait d�placer le personnage al�atoirement si on appuie sur 'd' et on peut retirer le mode debug en appuyant une nouvelle fois sur 'd'.

Toutes les textures de ce projet ont �t� r�alis�es par Alan, qui s'est juste inspir� du jeu 'minecraft' pour la terre. Le reste n'�tant pas pris d'images
appartenant � d'autres personnes.

Pour ce qui est du code, pour g�n�rer le niveau nous avons d�cid� de lire la variable string ligne par ligne en mettant les coordonn�es de chaque type de bloc rencontr�
dans une liste correspondant au type de bloc elle m�me imbriqu�e dans une plus grande liste. Nous aurions pu faire une grande liste correspondant au statut de chaque case
mais cette option semblait plus compliqu�e � mettre en oeuvre.

Pour ce qui est du d�placement du personnage et de l'affichage, nous avons reprit en grande partie le tp de snake. Pour v�rifier si il avait bien le droit de se d�placer
sur une case donn�e, nous gardions 2 coordonn�es du personnage, celles avant le d�placement, celles apr�s le d�placement et nous regardions si il �tait dans une autre liste
si la case �tait vide on garde les coordonn�es apr�s le d�placement, sinon on garde celles d'avant. Si il arrive sur de la terre nous retirions les coordonn�es de rockford apr�s le d�placement 
de la liste terre. Nous faisions la m�me chose pour savoir si il est possible de pousser un rocher en nous basant sur la direction dans laquelle il �tait bloqu�.

Pour ce qui est de la fin de partie, le joueur gagne uniquement si il arrive � la sortie, nous n'avons pas mis en place de syst�me pour compter les diamants

Pour que le joueur perde, c'�tait le cas le plus dur � g�rer du projet, il doit se situer en dessous d'une case de rocher et descendre vers le bas, en effet, dans ce cas
le rocher l'�crase. Si il se d�place sur le cot� il est sauv�. L'id�al aurait �t� de permettre au joueur de fuir la chute du rocher si il continue de se d�placer vers
le bas mais nous n'avons pas r�ussit.

Pour r�aliser ce programme nous avons eu besoin de 3 modules:
-upemtk pour repr�senter le jeu et ins�rer des images.
-time pour ralentir le mode debug et permettre � l'utilisateur de voir les d�placements de son personnage.
-random principalement pour choisir al�atoirement une direction dans le mode debug.

****************************************PHASE 2****************************************

Dans le cadre de cette phase 2, un changement majeur a �t� �ffectu�, plutot que de stocker les coordonn�es de tous les objets dans une liste. Nous avons d�cid� de modifier la structure pour qu'une matrice
puisse correspondre � notre niveau et chaque case stock le type d'objet. Qui peuvent �tre:

-W pour les murs
-R pour rockford
-B pour les rochers
-F pour les rochers en chute (nous reviendrons dessus)
-E pour la sortie ferm�e
-S pour la sortie ouverte (nous reviendrons aussi dessus)
-D pour le diamants
-T pour le diamants qui tombe (idem)

Ainsi, nous avons mis en place dans le cadre de la phase 2 un systeme permettant � ce que seul un rocher dans un �tat de chute et d'�boulement puisse tuer notre
personnage. Ainsi, le rocher en �tat de chute est mod�lis� par le "F" et nous pouvons plus facilement permettre � l'utilisateur de lui �chapper.
Cette fonctionnalit� marche de la m�me mani�re pour les diamants car nous avons impl�ment� leur chute.

Comme nouvelle fonctionnalit� nous avons aussi permis � l'utilisateur d'entrer le nom d'un fichier niveau en param�tre pour que le programme puisse le lire 
si aucun fichier n'est donn� en param�tre ou alors qu'il est introuvable, le programme cr�e lui m�me et enregistre dans un fichier � part un niveau al�atoire pour
ensuite pouvoir le lire. Pour se faire, nous cr�ons al�atoirement une matrice qui a une certaine taille choisie al�atoirement dans un intervalle afin d'y ajouter tous
les blocs qui peuvent avoir un nombre variable d'occurences pour ensuite y rajouter ceux qui doivent avoir un nombre fixe (comme Rockford par exemple).

De plus, lorsque l'utilisateur quitte le programme en cliquant sur la croix, nous sauvegardons le niveau dans un fichier sous la forme nomniveausave.txt .

Nous avons aussi ins�r� un chronom�tre et un compteur de diamants, et lorsque l'utilisateur a collect� le nombre minimum de diamants stipul� dans le niveau
il peut emprunter la sortie, d'o� l'ajout de 2 types de sorties: sortie ouverte et ferm�e. Et lors de la fin de jeu (soit le joueur est mort soit il a emprunt�
la sortie), nous calculons son score en fonction du temps restant et du nombre de diamants collect�s et lui affichons les 10 meilleurs scores pour ce niveau.

Le probl�me majeur que nous ayons rencontr� est que la biblioth�que upemtk semble avoir plus de mal pour afficher des images. Et comme nous demandons � notre programme
de r�afficher toutes les cases � chaque tour, cela peut engendrer quelques ralentissements. 3 solutions ont alors �t� envisag�es:
- Afficher certains objets avec des formes simple. Un cercle par exemple pour un rocher.
- R�duire la qualit� des images.
- Ne r�afficher seulement les blocs ayant �t� modifi�. Cependant, pour cette solution nous devons utiliser les "tags" li�s aux images et ils semblent avoir
une limite.

****************************************PHASE 3****************************************

Nous avons introduit dans cette phase 3 un menu principal avec s�lection de niveau ainsi que de sauvegardes (derni�re sauvegarde effectu�e en globale ou pour un niveau pr�cis) (Extension 2.a).
L'extension 1.a a �t� introduite en phase 2 (les roches et diamants vont prendre un certains temps pour effectuer un �boulement).
Nous avons aussi rajout� une version basse qualit� qui peut �tre activer avec comme param�tre "-l" (pour "l" pour "Low quality") dans la console.
La derni�re sauvegarde effectu�e peut �tre acc�d� avec le param�tre "-s", si un nom de niveau a �t� sp�cifi� en premier param�tre et "-s" en deuxi�me alors la derni�re sauvegarde de ce niveau sera prise en compte.

Sur le menu, la touche "S" permet de lancer la derni�re sauvegarde globale dans le menu principale sinon la derni�re sauvegarde d'un niveau sp�cifi� dans le menu "Niveaux" (il suffit d'�crire le nom du niveau dans ce menu).
La touche "HD"/"LD" permet de changer la qualit� du jeu ("HD" est la qualit� normale avec des images et "LD" est la basse qualit� avec des formes au lieu d'images � part pour Rockford et la sortie du niveau)

Nous avons cr�er ce mode basse qualit� car comme sp�cifi� � la fin du Readme Phase 2, nous n'avons pas pu mieux g�rer les images.
Il est donc conseill� de jouer en basse qualit� pour moins de "ralentissements".
Sinon vous pouvez profitez de nos textures avec le mode "HD".
