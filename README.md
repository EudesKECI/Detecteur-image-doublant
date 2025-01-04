# PythonASR

## Groupe : NoName

## Membres du groupe
* KOKPTA Eudes (20220808)
* MOUHAMADOUSSANE Mehdi (20213467)
* SADOUDI Anais (20234661)
* ZAKI Amin (20222058)
### Enseignant
* Franck POMMEREAU 
  * [`Contact`](https://www.ibisc.univ-evry.fr/~fpommereau/)
## Sujet traité
### Rechercher des images en double
* Il s'agit de réaliser un script qui détecte les photos qui sont identiques, ou presque identiques. Pour cela, il faut réduire la résolution de chaque photo (par exemple 16x16 pixels) et comparer ces versions réduites. Le script devra faire une présentation des résultats qui permette la consultation rapide des paquets de doublons, et la suppression des fichiers en trop.


# Rendu #1
## Projet : Recherche des images en doublant
* Recherche tous les images du répertoire choisi par l’utilisateur
* **Traitement des images par l’algorithme pHash (le hachage perceptuel)  dépend de #1**
  * Convertis les images en gris  
  * Réduction de la résolution des images en pixel (par exemple 16x16) 
  * Génère un hachage pour chaque image 
* Comparaison des hachages.   dépend de #2
* Affichage des images identiques ou presque identiques. dépend de #3
* Suppression ou conservation des images doublantes (choix de l’utilisateur) 

## Fonctionnalités supplémentaires : 
* **Mise en place d’une interface utilisateur** 
  * Suppression ou de conservation des images doublant : choix de l’utilisateur 
  * Une corbeille pour stocker les images supprimées avec un délai. 
  * Rendre plus interactive 
  * Plus de facilité 
  * Générer un rapport listant les fichiers en doublon ainsi que les actions effectuées
  * dépend de #1, #2, #3, #4, #5,

* Traitement d’autre format de fichiers qui ne sont pas des images (exemple la musique)
* Ajout des filtres en fonction du format.

# Rendu #2
 **Le hachage perceptuel (pHash) est une méthode qui génère un hachage basé sur l’apparence visuelle de l'image, plutôt que sur ses données binaires. Il permet d’identifier des images similaires même si elles ont été modifiées.**
### Fonctionnement de pHash 
* Réduire la taille: reduire la taille de l'image en une taille fixe, souvent 32x32 pixels. Cela facilite le traitement de l'image.
* Conversion en échelle de gris : l'image est réduite à une échelle de gris juste pour simplifier davantage le nombre de calculs.
* Transformation Discrète du Cosinus (DCT):  L'image redimenssionée subit une DCT: technique utilisée pour transformer des données sous formes de fréquence, ce qui très utile pour catpturer l'essence visuelle de l'image dans son domaine fréquentiel.  Les valeurs de la DCT se concentrent principalement dans les coefficients de basse fréquence (situés dans le coin supérieur gauche de la matrice), qui représentent les aspects globaux de l'image.
* Réduisez le DCT : Bien que le DCT soit de 32x32, conservez simplement le 8x8 en haut à gauche. Ceux-ci représentent les fréquences les plus basses de l'image.
* Calcul de la moyenne: la moyenne des coefficients de la DCT (à l'exclusion du premier, qui correspond à la composante continue ou la moyenne générale de l'image en treme de luminosité ou d'intensité de pixels:Cette valeur correspond à la fréquence zéro (aucune information)) est calculée pour servir de référence pour la génération du hachage.
* Génération du hachage : Un hachage binaire est créé en comparant chaque coefficient DCT retenu avec la moyenne calculée. Si un coefficient est supérieur à la moyenne, un bit de 1 est généré, sinon un bit de 0 est utilisé. Cela forme une séquence binaire unique qui constitue le pHash de l'image.
  
# Rendu final
## Contenu du dépôt
* **Info_Groupe.csv :** Contient les informations relatives au groupe (noms, prénoms, numéros d'étudiant, nom du groupe, et sujet du projet).
* **-ScriptASR.py:** Un script interactif en ligne de commande (CLI), développé avec la bibliothèque argparse. Il est recommandé pour les développeurs familiers avec les lignes de commande.
* **-ProjetASR.py:** Le code principal du projet, conçu pour une interaction simple et intuitive. Il est particulièrement adapté aux débutants ou aux utilisateurs moins à l'aise avec les lignes de commande.
* **-InterfaceASR.py:** Une interface graphique (GUI) interactive développée avec PySide6, pour une utilisation plus visuelle et conviviale.
## Présentation du code
* La structure centrale du projet repose sur le fichier **-ProjetASR.py**.
*  Pour exécuter les fichiers **-InterfaceASR.py** ou **-ScriptASR.py**, il est impératif de placer **-ProjetASR.py** dans le même répertoire
*  Ces fichiers dépendent de **-ProjetASR.py**, car ils appellent des fonctions qui y sont définies. Une mauvaise organisation entraînera des erreurs d'exécution.
## Répartition des rôles
* **Coordinateur du projet :** Eudes KOKPATA
  * Supervise l'avancement global du projet.
  * Assure la communication entre les membres.
  * Rédige les livrables finaux (README, rapport, etc.).
* **Développeurs principaux :** Tous les membres du groupe
  * Responsables du fichier principal **-ProjetASR.py.**
  * Implémentent les fonctionnalités de base du projet.
* **Développeurs CLI :** Eudes KOKPATA, Mehdi MOUHAMADOUSSANE et Anais SADOUDI
  * Conçoivent et implémentent le script en ligne de commande (**-ScriptASR.py**).
  * Configurent l’utilisation de la bibliothèque argparse.
  * Documentent les options et paramètres du script.
* **Développeurs GUI :** Eudes KOKPATA et Amin ZAKI
  * Développent l’interface graphique avec PySide6 (**-InterfaceASR.py**).
  * S'assurent de la convivialité et de l’ergonomie de l’interface utilisateur.
  * Réalisent des tests pour garantir une expérience utilisateur optimale.

## Module utiliser:
* **pillow PIL (Python Learning Library) :** Bibliothèque de traitement d'images permettant diverses opérations sur les fichiers image.
  * *Documentation:* [pillow PIL](https://pypi.org/project/pillow/)
* **ImageHash :** Bibliothèque permettant de générer des hashs à partir d'images en utilisant différents algorithmes tels que `aHash`, `pHash`, `dHash`, etc.
  * *Docummentation:* [ImageHash](https://pypi.org/project/ImageHash)
*  **PySide6 :** Bibliothèque utilisée pour créer des interfaces graphiques (GUI) interactives et modernes. Elle est basée sur Qt pour Python.[PySide6 - Qt for Python](https://doc.qt.io/qtforpython-6/)
* **Path :** Module standard de Python permettant de gérer et d'accéder facilement à l'arborescence des répertoires et fichiers
  *  *Documentaion:* [Pathlib dans la bibliothèque standard](https://docs.python.org/fr/3/library/pathlib.html)
* **Argparse:** Module standard permettant de transformer un script Python en une application en ligne de commande interactive.
  * *Documentaion:* [ Argparse dans la bibliothèque standard](https://docs.python.org/3/library/argparse.html)
* Coool, tous ces modules sont compatibles avec Python et simplifient grandement le développement du projets ! 😃
