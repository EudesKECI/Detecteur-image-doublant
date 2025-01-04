import argparse
from pathlib import Path
from PIL import Image
import imagehash
from ProjetASR import main as main_projet_asr


def search_images(path: Path):
    """Cherche des images dans un répertoire."""
    images_tab = []
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
    for elt in path.iterdir():
        if elt.is_file() and elt.suffix.lower() in image_extensions:
            images_tab.append(elt)
    return images_tab

def similar_img_tab(images_tab):
    """Regroupe les images similaires dans des groupes."""
    tol = 15 # tolérance
    tab_doublant = []
    while images_tab:
        current_image = images_tab.pop(0)
        img1 = Image.open(current_image)
        hash1 = imagehash.phash(img1)
        group = [current_image]
        images_to_remove = []
        for img_file in images_tab:
            img2 = Image.open(img_file)
            hash2 = imagehash.phash(img2)
            if (hash1 - hash2) <= tol:
                group.append(img_file)
                images_to_remove.append(img_file)

        for img_file in images_to_remove:
            images_tab.remove(img_file)
        tab_doublant.append(group)
    tab_doublant = [grp for grp in tab_doublant if len(grp) > 1]
    return tab_doublant

def display_similar_img(directory: Path):
    """Affiche les groupes d'images similaires et retourne les groupes."""
    path = Path(directory).resolve()
    if not path.exists() or not path.is_dir():
        print("Le chemin spécifié est introuvable.")
        return []
    image_tab = search_images(path)
    if not image_tab:
        print("Aucune image trouvée dans le répertoire.")
        return []
    images_similair = similar_img_tab(image_tab)
    if not images_similair:
        print("Aucune image similaire détectée.")
        return []
    for i, group in enumerate(images_similair):
        print(f"Groupe {i + 1} :")
        for j, img in enumerate(group, 1):
            print(f"  [{j}] {img.name}")
        print(f"  Taille du groupe : {len(group)}\n")
    return images_similair

def delete_image(images_similair, group_index, img_index):
    """Supprime une image d'un groupe similaire."""
    group = images_similair[group_index]
    image_to_delete = group[img_index]
    image_to_delete.unlink()
    print(f"Image '{image_to_delete.name}' supprimée.")
    group.pop(img_index)
    if not group:
        images_similair.pop(group_index)   

def main():
    
    # initialisation de l'analyseur de commandes
    parser = argparse.ArgumentParser(description="Détecteur et gestionnaire d'images similaires.")
    # création de sous-commandes pour organiser les différentes fonctionnalités
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles") # sous -commande

    # sous-commande pour afficher les images similaires
    parser_display = subparsers.add_parser("display", help="Afficher les groupes d'images similaires.")
    parser_display.add_argument("-d", "--directory", type=str, default=".", help="Répertoire contenant les images (par défaut : répertoire courant).")

    # Commande pour supprimer une image
    parser_delete = subparsers.add_parser("delete", help="Supprimer une image dans un groupe.")
    parser_delete.add_argument("-g", "--group", type=int, required=True, help="Numéro du groupe (commence à 1).")
    parser_delete.add_argument("-i", "--image", type=int, required=True, help="Numéro de l'image dans le groupe (commence à 1).")
    parser_delete.add_argument("-d", "--directory", type=str, default=".", help="Répertoire contenant les images (par défaut : répertoire courant).")

    # sous-commande pour le mode "noob" (exécute directement le main de ProjetASR)
    parser_noob = subparsers.add_parser("noob", help="Mode non développeur, exécute la fonction main de ProjetASR.")
    
    # analyse des arguments passés par l'utilisateur
    args = parser.parse_args()

    # la commande noob, non develeppeur
    if args.command == "noob":
        print("Mode noob activé : exécution de ProjetASR.main()")
        main_projet_asr()
        return
    
    # Commande 'display'
    if args.command == "display":
        directory = Path(args.directory).resolve()
        if not directory.exists() or not directory.is_dir():
            print(f"Erreur : le répertoire '{args.directory}' est invalide.")
            return

        images_similair = display_similar_img(directory)
        if not images_similair:
            return

    # Commande 'delete'
    elif args.command == "delete":
        directory = Path(args.directory).resolve()
        images_tab = search_images(directory)
        images_similair = similar_img_tab(images_tab)  # Affiche les groupes existants avant suppression
        if not images_similair:
            return

        group_index = args.group - 1
        img_index = args.image - 1

        if group_index < 0 or group_index >= len(images_similair):
            print("Numéro de groupe invalide => utiliser d'abord display")
            return
        if img_index < 0 or img_index >= len(images_similair[group_index]):
            print("Numéro d'image invalide => utiliser d'abord display")
            return
        delete_image(images_similair, group_index, img_index)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()