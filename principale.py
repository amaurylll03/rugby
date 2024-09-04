import bibliotheque as bib
import entraineur as coach
import choixequipenextgen as teamchoice 
import pageJouer as Pj
import Calendrier as Cl
import Charger_Partie as Cp
import classement as Cla
"""
primary-100:#0000FF
primary-200:#7142ff
primary-300:#eea6ff
accent-100:#FFD700
accent-200:#917800
text-100:#FFFFFF
text-200:#e0e0e0
bg-100:#800080
bg-200:#942293
bg-300:#b343b0
"""





class Menu(bib.QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()
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

        # Réinitialiser le layout principal
        self.setLayout(bib.QVBoxLayout(self))

    def initUI(self):

        #titre et taille de fenetre
        self.setWindowTitle('Menu Principal')
        self.setGeometry(0, 0, bib.QApplication.desktop().screenGeometry().width(),
                         bib.QApplication.desktop().screenGeometry().height())

        # Dégradé bleu-violet en fond
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = bib.QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, bib.QColor(0, 0, 255))  # Bleu
        gradient.setColorAt(0.8, bib.QColor(128, 0, 128))  # Violet
        palette.setBrush(bib.QPalette.Background, gradient)
        self.setPalette(palette)

        # Layout vertical pour les éléments
        layout = bib.QVBoxLayout(self)

        # Ajouter de l'espace en haut pour le titre
        
        # Ajouter le titre en gros caractères
        label_title = bib.QLabel("RUGBY MANAGER", self)
        font = bib.QFont()
        font.setPointSize(36)  # Taille de police plus grande
        font.setBold(True)     # Police en gras
        label_title.setFont(font)
        label_title.setStyleSheet("""
            color: #eea6ff;
            border: solid 10px black;
            background-color: transparent;
        """)

        layout_title=bib.QHBoxLayout(self)

        layout_title.addWidget(label_title)
        label_title.setAlignment(bib.Qt.AlignCenter) 
        
         # Couleur du texte en blanc
        layout.addLayout(layout_title)
         # Alignement au centre
       
        

        # Ajouter de l'espace entre le titre et les boutons
        layout.addSpacing(100)  # Ajoute 50 pixels d'espace entre le titre et les boutons

        # Création des boutons avec différents dégradés et actions
        self.create_button(layout, "Nouvelle Partie", "#1E90FF", "#1050A0", self.start_new_game)
        self.create_button(layout, "Charger Partie", "#1E90FF", "#1050A0", self.load_game)
        self.create_quit_button(layout, "Quitter", "#8B0000", "#600000")

        # Centrer les éléments dans le layout
        layout.setAlignment(bib.Qt.AlignCenter)

        self.setLayout(layout)

    def create_button(self, layout, button_text, color1, color2, action_function):
        button = bib.QPushButton(button_text, self)
        self.style_button(button)
        button.clicked.connect(action_function)
        layout.addWidget(button)

    def style_button(self, button, ):
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
                min-width: 200px;
                min-height: 50px;
                max-width:400px;
                padding 0;
                
                

            }}
            QPushButton:hover {{
                background-color: #0000FF;
                border-color: #0000FF;
                color:#eea6ff;
                
                
            }}
        """
        button.setStyleSheet(stylesheet)

    def create_quit_button(self, layout, button_text, color1, color2):
        button = bib.QPushButton(button_text, self)
        self.style_button(button)
        button.clicked.connect(self.quit)
        layout.addWidget(button)

    def start_new_game(self):
        self.stacked_widget.setCurrentIndex(1)

    def load_game(self):
        self.stacked_widget.setCurrentIndex(5)

    def quit(self):
        print("Quitting the program")
        bib.QApplication.instance().quit()


if __name__ == "__main__":
    app = bib.QApplication(bib.sys.argv)

    stacked_widget = bib.QStackedWidget()
    
    menu_page = Menu(stacked_widget)
    game_page = coach.coach_creation(stacked_widget)
    choix_equipe=teamchoice.ChooseYourTeam(stacked_widget)
    menu_jouer=Pj.page_jouer(stacked_widget)
    caldendrier=Cl.page_calendrier(stacked_widget)
    page_charger_parite=Cp.Charger_une_partie(stacked_widget)
    page_classement=Cla.ClasseClassement(stacked_widget)

    stacked_widget.addWidget(menu_page)
    stacked_widget.addWidget(game_page)
    stacked_widget.addWidget(choix_equipe)
    stacked_widget.addWidget(menu_jouer)
    stacked_widget.addWidget(caldendrier)
    stacked_widget.addWidget(page_charger_parite)
    stacked_widget.addWidget(page_classement)
    stacked_widget.showFullScreen()  # Afficher en plein écran

    bib.sys.exit(app.exec_())
