from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QFileDialog, QMainWindow, QPushButton, QLabel, QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QCheckBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PIL import Image
from ProjetASR import similar_img_tab, search_images 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuration initiale de la fenêtre principale
        self.setGeometry(750, 500, 850, 650)
        self.setWindowTitle("Affichage du répertoire")
        
        # Création du widget central et de sa disposition
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # Label pour afficher le répertoire sélectionné
        self.directory_label = QLabel("Aucun répertoire sélectionné", central_widget)
        self.directory_label.setStyleSheet("font-size: 16px; color: blue; ")
        layout.addWidget(self.directory_label)

        # Bouton pour choisir un répertoire
        self.button_choose_directory = QPushButton("Choisir un répertoire", central_widget)
        self.button_choose_directory.clicked.connect(self.choose_directory)
        self.button_choose_directory.setStyleSheet("background-color: #00ff00")
        layout.addWidget(self.button_choose_directory)
        
        # Label pour afficher un aperçu d'image
        self.image_label = QLabel("Aucune image sélectionnée", central_widget)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black; background-color: #f0f0f0;")
        self.image_label.setFixedHeight(300)
        layout.addWidget(self.image_label)
        
        # Zone de défilement pour afficher les groupes d'images
        self.scroll_area = QScrollArea(central_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)
        
        # Définir le widget central
        self.setCentralWidget(central_widget)
    
    # Méthode pour choisir un répertoire
    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Choisir un répertoire")
        if directory:
            self.directory_label.setText(f"Répertoire sélectionné : {directory}")
            self.display_images(directory)
        else:
            self.directory_label.setText("Aucun répertoire sélectionné")
    
    # Méthode pour afficher les images du répertoire
    def display_images(self, directory):
        try:
            # Recherche des images et regroupement par similarité
            images_tab = search_images(Path(directory))
            grouped_images = similar_img_tab(images_tab)
            
            # Supprimer les anciens widgets pour actualiser l'affichage
            for i in reversed(range(self.scroll_layout.count())):
                widget = self.scroll_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            # Parcours des groupes d'images similaires pour les afficher
            for group in grouped_images:
                if group:  # Si le groupe contient des images
                    group_container = QWidget()
                    group_layout = QVBoxLayout(group_container)
                    group_title = QLabel(f"Groupe d'images similaires ({len(group)} images)")
                    group_title.setStyleSheet("font-weight: bold;")
                    group_layout.addWidget(group_title)

                    # Checkbox et bouton alignés pour chaque image
                    checkboxes = []
                    for image_name in group:
                        file_path = Path(directory) / image_name

                        # Layout horizontal pour aligner le bouton et la checkbox
                        item_layout = QHBoxLayout()
                        
                        # Bouton pour afficher l'aperçu de l'image
                        button = QPushButton(str(image_name.name))
                        button.clicked.connect(lambda checked, f=file_path: self.show_image(f))
                        item_layout.addWidget(button)

                        # Checkbox sans texte, alignée à droite du bouton
                        checkbox = QCheckBox()
                        checkbox.setObjectName(str(image_name.name))
                        checkboxes.append(checkbox)
                        item_layout.addWidget(checkbox)

                        group_layout.addLayout(item_layout)

                    # Ajouter un bouton de suppression
                    delete_button = QPushButton("Supprimer")
                    delete_button.setFixedSize(200, 30)
                    delete_button.clicked.connect(lambda: self.delete_selected_files(directory, checkboxes))
                    delete_button.setStyleSheet('background-color: #ff0000')
                    group_layout.addWidget(delete_button)
                    
                    # Ajouter le groupe au layout principal
                    self.scroll_layout.addWidget(group_container)

        except Exception as e:
            self.directory_label.setText(f"Erreur : {e}")
    
    # Méthode pour afficher une image dans le label d'aperçu
    def show_image(self, file_path):
        try:
            pixmap = QPixmap(str(file_path))
            if not pixmap.isNull():
                self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
            else:
                self.image_label.setText("Impossible d'afficher l'image")
        except Exception as e:
            self.image_label.setText(f"Erreur : {e}")
            print(e)

    # Méthode pour supprimer les fichiers sélectionnés
    def delete_selected_files(self, directory, checkboxes):
        try:
            # Parcourir les fichiers sélectionnés à supprimer
            for checkbox in checkboxes:
                if checkbox.isChecked():
                    file_path = Path(directory) / checkbox.objectName()
                    print(f"Tentative de suppression : {file_path}")  # Debug
                    if file_path.exists():
                        file_path.unlink()  # Supprime le fichier
                        print(f"Fichier supprimé : {file_path}")
                    else:
                        print(f"Fichier introuvable : {file_path}")

            # Rafraîchir l'affichage après suppression
            self.display_images(directory)

        except Exception as e:
            print(f"Erreur lors de la suppression des fichiers : {e}")

        # Rafraîchir l'affichage
        self.display_images(directory)
        # self.delete_selected_files(directory, checkboxes)

if __name__ == "__main__":
    # Création et lancement de l'application
    app = QApplication([]) # Initialisation de l'application Qt
    window = MainWindow() # Création de la fenêtre principale
    window.show() # Affichage de la fenêtre principale
    app.exec() # Exécution de la boucle événementielle de l'application

    