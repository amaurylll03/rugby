import bibliotheque as bib

class coach_creation(bib.QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.image_button_widget = self.create_image_buttons()  # Initialiser ici
        self.image_selectionne=''
        self.initUI()

    def fenetre_init(self):
        #Titre de la fenetre et fond de l ecran
        self.setWindowTitle('Choix Entraineur')
        self.setGeometry(0, 0, bib.QApplication.desktop().screenGeometry().width(),
                         bib.QApplication.desktop().screenGeometry().height())  # Mettre la page en pleine écran

        # Fond d'écran couleur unie
       
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = bib.QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, bib.QColor(0, 0, 255))  # Bleu
        gradient.setColorAt(0.8, bib.QColor(128, 0, 128))  # Violet
        palette.setBrush(bib.QPalette.Background, gradient)
        self.setPalette(palette)

    def show_selected_option(self):
        if (
        self.nom_carreire_field.text().strip() and
        self.prenom_field.text().strip() and
        self.nom_field.text().strip() and
        self.nationalite_field.text().strip()
        ):
            conn = bib.sqlite3.connect('rugby.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO entraineur (prenom, nom ,nationalite , image ,nom_carriere) VALUES (?,?,?,?,?)",(self.prenom_field.text(),self.nom_field.text(),self.nationalite_field.text(),self.image_selectionne,self.nom_carreire_field.text()))
            conn.commit()
            self.stacked_widget.setCurrentIndex(2)
        

    def form(self):
        form_layout = bib.QFormLayout()
        self.nom_carreire_field = bib.QLineEdit()
        self.nom_carreire_field.setText("Clermont")
        self.prenom_field = bib.QLineEdit()
        self.prenom_field.setText("Amaury")

        self.nom_field = bib.QLineEdit()
        self.nom_field.setText("Lubenec")
        
        self.nationalite_field = bib.QLineEdit()
        self.nationalite_field.setText("France")

        # Ajouter les champs de formulaire avec leur label
        self.add_form_field(form_layout, 'nom de la carriere', self.nom_carreire_field)
        self.add_form_field(form_layout, 'Prénom', self.prenom_field)
        self.add_form_field(form_layout, 'Nom', self.nom_field)
        self.add_form_field(form_layout, 'Nationalité', self.nationalite_field)

        Image_Button = bib.QPushButton("Selection Image", self)
        self.style_button(Image_Button, 25, 620,80)
        Image_Button.clicked.connect(self.afficher_image)

        # Ajouter un QLabel pour afficher l'image sélectionnée
        self.selected_image_label = bib.QLabel(self)
        self.update_selected_image("image/entraineur/unknown.png")

        submit_image_widget = bib.QWidget()
        submit_image_layout = bib.QHBoxLayout(submit_image_widget)
        submit_image_layout.addWidget(Image_Button)
        submit_image_layout.addWidget(self.selected_image_label)  # Ajouter le QLabel à côté du bouton
        submit_image_layout.setAlignment(bib.Qt.AlignCenter)
        submit_image_widget.setMaximumWidth(620)
        form_layout.addRow(submit_image_widget)

        return form_layout

    def add_form_field(self, form_layout, label_text, widget):
        """Ajoute un champ de formulaire avec un label et un widget."""
        label = bib.QLabel(label_text, self)
        label.setStyleSheet("color: white;font:24px;")
        self.style_lineedit(widget)  # Appliquer le style au QLineEdit

        field_widget = bib.QWidget()
        field_layout = bib.QHBoxLayout(field_widget)
        field_layout.addWidget(widget)
        field_layout.setAlignment(bib.Qt.AlignCenter)
        field_widget.setMaximumWidth(500)  # Définir une taille maximale pour le champ de formulaire

        form_layout.addRow(label, field_widget)

    def initUI(self):
        self.fenetre_init()
        main_layout = bib.QHBoxLayout(self)  # Créer un QHBoxLayout principal

        # Ajouter un layout vertical centré dans le QHBoxLayout principal
        center_widget = bib.QWidget()
        center_layout = bib.QVBoxLayout(center_widget)
        center_widget.setMaximumWidth(700)  # Définir une taille maximale pour le conteneur central
        center_widget.setStyleSheet("background-color:#b343b0; border-radius: 10px;")  # Bordure rouge autour du conteneur central

        # Ajouter un label pour indiquer qu'il s'agit de la nouvelle partie
        title_label = bib.QLabel("Entraîneur", self)
        font = bib.QFont()
        font.setPointSize(36)  # Taille de police plus grande
        font.setBold(True)     # Police en gras
        title_label.setFont(font)
        title_label.setStyleSheet("color: white;")  # Couleur du texte en blanc
        center_layout.addWidget(title_label)
        center_layout.setAlignment(title_label, bib.Qt.AlignCenter)

        # Ajouter de l'espace entre le titre et le formulaire

        # Ajouter le formulaire centré
        form_layout = self.form()
        form_widget = bib.QWidget()

        form_widget.setLayout(form_layout)
        center_layout.addWidget(form_widget)

        # Ajouter de l'espace après le formulaire

        # Ajouter un layout horizontal pour les boutons
        button_layout = bib.QHBoxLayout()

        # Ajouter un bouton pour revenir au menu principal
        back_button = bib.QPushButton("Retour au Menu", self)
        self.style_button(back_button, 0, 260,50)
        back_button.clicked.connect(self.go_back_to_menu)

        # Ajouter les boutons au layout horizontal
        button_layout.addWidget(back_button)

        submit_button = bib.QPushButton('Valider')
        self.style_button(submit_button, 0, 260,50)
        submit_button.clicked.connect(self.show_selected_option)
        button_layout.addWidget(submit_button)

        # Ajouter le layout horizontal au layout central
        button_widget = bib.QWidget()
        button_widget.setLayout(button_layout)
        button_widget.setMaximumWidth(800)  # Définir une taille maximale pour le conteneur de boutons
        center_layout.addWidget(button_widget)
        center_layout.setAlignment(button_widget, bib.Qt.AlignCenter)

        # Centrer tout le contenu verticalement
        center_layout.setAlignment(bib.Qt.AlignTop)

        # Layout for image buttons (initially hidden)
        self.image_button_widget.setVisible(False)

        # Main layout adjustment
        main_layout.addWidget(center_widget)
        main_layout.addWidget(self.image_button_widget)
        main_layout.setAlignment(bib.Qt.AlignCenter)  # Centrer horizontalement le layout principal

        self.setLayout(main_layout)

    def afficher_image(self):
        self.image_button_widget.setVisible(not self.image_button_widget.isVisible())

    def create_image_buttons(self):
        image_button_widget = bib.QWidget()
        grid_layout = bib.QGridLayout(image_button_widget)

        # Tableau des images
        images = [f"image/entraineur/entraineur{i+1}.png" for i in range(9)]

        for i in range(3):
            for j in range(3):
                button = bib.QPushButton(self)
                pixmap = bib.QPixmap(images[i*3 + j])
                pixmap = pixmap.scaled(180, 180, bib.Qt.KeepAspectRatio, bib.Qt.SmoothTransformation)
                button.setIcon(bib.QIcon(pixmap))
                button.setIconSize(bib.QSize(160, 160))
                button.setFixedSize(200, 200)
                button.setStyleSheet(self.style_image_button())  # Appliquer le style de bordure
                button.clicked.connect(lambda checked, img=images[i*3 + j]: self.update_selected_image(img))
                grid_layout.addWidget(button, i, j)

        image_button_widget.setMaximumWidth(640)
        image_button_widget.setMaximumHeight(640)
        return image_button_widget

    def update_selected_image(self, image_path):
        pixmap = bib.QPixmap(image_path)
        self.image_selectionne=image_path
        pixmap = pixmap.scaled(90, 90, bib.Qt.KeepAspectRatio, bib.Qt.SmoothTransformation)
        self.selected_image_label.setPixmap(pixmap)
        self.selected_image_label.setFixedSize(100, 100)  # Assurer une taille fixe pour le QLabel
        self.selected_image_label.setStyleSheet(self.style_image_label())
        self.image_button_widget.setVisible(False)  # Masquer le widget des boutons d'image

    def style_image_label(self):
        """Applique un style à la bordure du QLabel d'image sélectionnée."""
        return """
            QLabel {
                border: 2px solid #800080;
                border-radius: 5px;
                padding: 5px;
                background-color: #800080;
            }
        """

    def style_button(self, button, decalage_a_gauche, taille,height):
        """Applique un style avec un dégradé aux boutons."""
        stylesheet = f"""
            QPushButton {{
                background-color: #800080;
                border-width: 10px;
                border-style: solid;
                border-color: #800080;
                font-size: 24px;
                color: #e0e0e0;
                border-radius: 10px;
                height: {height}px;
                width:{taille}px;
                margin-left:{decalage_a_gauche}px;
            }}
            QPushButton:hover {{
                background-color: #0000FF;
                border-color: #0000FF;
                color:#eea6ff;
            }}
        """
        button.setStyleSheet(stylesheet)

    def style_image_button(self):
        """Applique un style à la bordure des boutons d'image."""
        return """
            QPushButton {
                border: 2px solid #800080;
                border-radius: 5px;
                padding: 5px;
                background-color: #800080;
                margin-top:0px;
                margin-bottom:0px;
            }
            QPushButton:hover {
                background-color: #0000FF;
                border-color: #0000FF;
                color: #eea6ff;
            }
        """

    def style_lineedit(self, lineedit):
        """Applique un style avec un dégradé aux champs de texte (QLineEdit)."""
        stylesheet = """
            QLineEdit {
                background-color: #800080;
                border-width: 10px;
                border-style: solid;
                border-color: #800080;
                font-size: 24px;
                color: #e0e0e0;
                border-radius: 10px;
                min-height: 30px;
                max-width:500px;
            }
            QLineEdit:hover {
                background-color: #0000FF;
                border-color: #0000FF;
                color:#eea6ff;
            }
        """
        lineedit.setStyleSheet(stylesheet)

    def clear_widgets(self):
        # Supprimer les widgets et layouts ajoutés dynamiquement
        layout = self.layout()
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    sub_layout = item.layout()
                    if sub_layout:
                        while sub_layout.count():
                            sub_item = sub_layout.takeAt(0)
                            sub_widget = sub_item.widget()
                            if sub_widget:
                                sub_widget.deleteLater()

        # Assurez-vous de vider également le layout principal de GamePage
        main_layout = self.layout()
        if main_layout:
            while main_layout.count():
                item = main_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

    def go_back_to_menu(self):
        self.stacked_widget.setCurrentIndex(0)
