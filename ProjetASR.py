from pathlib import Path
from PIL import Image
import imagehash
# from ScriptASR import main as main_script_asr
# import sh

def search_images(path: Path):
    """
    Fonction permettant de chercher des images
     dans un repertoire et de les regropées tous dans un tableau
    """
    images_tab = []  # Tableau stockant toutes les images de notre répertoire
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']

    for elt in path.iterdir():
        if elt.is_file() and elt.suffix.lower() in image_extensions:
            images_tab.append(elt)
    return images_tab

def similar_img_tab(images_tab):
    """
    fonction retournant un tableau dans le lequel 
    les images similaires sont regrouper dans un même tableau => [[img1,img2],[img3,img4,img5]]
    """ 
    tol =10
    tab_doublant = [] # tableau stock les tableaux d'image similaire

    while images_tab:
        current_image = images_tab.pop(0)
        img1 = Image.open(current_image)
        hash1 = imagehash.phash(img1)

        # Créer un nouveau groupe pour l'image courante
        group = [current_image]

        # Parcourir le reste des images pour comparer
        images_to_remove = []
        for img_file in images_tab:
            img2 = Image.open(img_file)
            hash2 = imagehash.phash(img2)

            # Si la différence de hash est inférieure ou égale à la tolérance
            if (hash1 - hash2) <= tol:
                group.append(img_file)
                images_to_remove.append(img_file)  # Marquer l'image à retirer

        # Retirer les images similaires de la liste principale
        for img_file in images_to_remove:
            images_tab.remove(img_file)

        # Ajouter le groupe d'images similaires au tableau des doublons
        tab_doublant.append(group)

    # Filtrer les groupes pour enlever ceux avec une seule image (uniques)
    for i in range(len(tab_doublant) - 1, -1, -1):
        if len(tab_doublant[i]) == 1:
            tab_doublant.pop(i)

    return tab_doublant


def display_similar_img():
    """
    Fonction permettant d'afficher des groupes des images similaires
    """
    directory = input(str("Entrer le chemin du répertoire: "))
    path = Path(directory).resolve() # resolve => regle de gerer les liens syboliques "." et ".."
    if not path.exists() or not path.is_dir():
        print("Le chemin introuvable...")
        return
    
    image_tab = search_images(Path(directory))
    if not image_tab:
        print("Répertoire vide...")
        return

    images_similair = similar_img_tab(image_tab)
    if not images_similair:
        print("Il n'existe pas d'image doublant...")
        return


    # Afficher les groupes d'images similaires
    for i, group in enumerate(images_similair):
        print(f"Groupe {i + 1} :")
        for j, img in enumerate(group,1):
            print(f"  [{j}] {img.name}")
        print(f"  Taille: {len(group)}\n")
    return images_similair

def delete_img_group(images_similair):
    """
    Fonction permetant à l'utilisateur de choisir une image 
    dans un groupe d'images similaires et de le supprimer
    """
    try:
        group_index = int(input("Choisissez le numéro du groupe: ")) - 1
        if group_index < 0 or group_index >= len(images_similair):
            print("Numéro de groupe invalide.")
            return

        group = images_similair[group_index]
        for j, img in enumerate(group,1):
            print(f"  [{j}] {img}")

        img_index = int(input("Choisissez le numéro de l'image à supprimer: "))-1
        if img_index < 0 or img_index >= len(group):
            print("Numéro d'image invalide.")
            return

        # Supprimer l'image choisie
        image_to_delete = group[img_index]
      #Demmande de confirmation pour la suppression d'image
        confirmation = input(f"Voulez-vous vraiment supprimer cette image '{image_to_delete}' (oui/non): ").lower()
        if confirmation == "oui":
            # sh.rm(image_to_delete)  # Supprime  l'image selectionner
            image_to_delete.unlink()
            print(f"Image '{image_to_delete}' supprimée avec succès.")
        else:
            print("Aucune image supprimée ")

        # Mettre à jour le groupe
        group.pop(img_index)
        if not group:  # Si le groupe est vide, le retirer
            images_similair.pop(group_index)

    except ValueError:
        print("Veuillez entrer un nombre valide.")

def main():
    images_similair = display_similar_img()       

    while images_similair:
        print("\nOptions:")
        print("1. Supprimer une image")
        print("2. Passer en mode devellopeur")
        print("3. Quitter")

        choice = input("Votre choix: ")

        if choice == "1":
            delete_img_group(images_similair)
        elif choice=="2":
            print("Mode developpeur activer: execution de ScriptASR.main() ")
            break
        elif choice == "3":
            print("Au revoir!")
            break
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main()