import bibliotheque as bib

def recuperation_match_equipe():
    """
    Récupère les données des équipes et des matchs.
    :return: Tuple contenant deux listes : tab_equipe et tab_match
    """
    tab_equipe = [[[] for _ in range(len(bib.recup_equipe(1, bib.nom_carriere())))] for _ in range(14)]
    tab_match = [[[] for _ in range(len(bib.recup_match(1, bib.nom_carriere())))] for _ in range(14)]
    
    for i in range(14):
        tab_equipe[i] = bib.recup_equipe((i + 1), bib.nom_carriere())
        tab_match[i] = bib.recup_match((i + 1), bib.nom_carriere())

    return tab_equipe, tab_match

class ClasseClassement(bib.QWidget):
    def __init__(self, stacked_widget):
        """
        Initialise la fenêtre et ses composants.
        :param stacked_widget: Le widget empilé contenant cette fenêtre
        """
        super().__init__()
        self.stacked_widget = stacked_widget

        # Configuration initiale de la fenêtre
        self.fenetre_init()

        # Layout principal horizontal
        main_layout = bib.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Enlever les marges du layout

        # Création de la table pour afficher les classements
        self.table = bib.QTableWidget()
        self.table.setStyleSheet("background-color:transparent;margin:0;border: 0px solid black;padding:0;")
        self.configurer_table()
        
        # Ajouter la table à un layout centré
        table_layout = bib.QVBoxLayout()
        table_layout.addWidget(self.table)
        table_layout.setAlignment(bib.Qt.AlignCenter)  # Centre la table horizontalement et verticalement

        # Créer un widget pour contenir la table
        table_widget = bib.QWidget()
        table_widget.setLayout(table_layout)
        
        # Création du bouton
        self.bouton_retour = bib.QPushButton("Retour")
        
        # Calculer la hauteur du bouton
        heightone = bib.QApplication.desktop().screenGeometry().height()
        
        # Appliquer le style CSS au bouton avec la hauteur dynamique
        self.bouton_retour.setStyleSheet(f"""
            QPushButton {{
                background-color: #4CAF50;
                color: white;
                font-size: 20px;
                border: none;
                text-align: center;
                padding: 0;
                height: {heightone}px;  /* Hauteur du bouton */
                width: 60px;           /* Largeur du bouton (peut être ajusté si nécessaire) */
                transform: rotate(-90deg);
                transform-origin: center;
            }}
            QPushButton::pressed {{
                background-color: #45a049;  /* Couleur de fond du bouton lors de l'appui */
            }}
        """)

        # Ajouter la table et le bouton au layout principal
        main_layout.addWidget(table_widget)
        main_layout.addWidget(self.bouton_retour)
        
        # Ajouter stretch pour faire en sorte que le bouton prenne toute la hauteur disponible
        #main_layout.addStretch()  # Assure que le bouton occupe la place restante à droite

        self.setLayout(main_layout)

        # Afficher les données du classement
        self.afficher_le_classement()

    def configurer_table(self):
        """
        Configure la structure de la table (colonnes, etc.).
        """
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Logo", "Nom du Club", "Points Marqués", 
            "Points Encaissés", "Points Totals", 
            "Bonus Offensif", "Bonus Défensif"
        ])

        # Définir des largeurs de colonnes fixes (exemple : 200 pixels)
        for i in range(self.table.columnCount()):
            self.table.setColumnWidth(i, 200)

        # Définir une hauteur de ligne fixe (exemple : 80 pixels)
        self.table.verticalHeader().setDefaultSectionSize(80)

        # Redimensionner les colonnes pour s'adapter au contenu
        self.table.resizeColumnsToContents()

    def charger_donnees(self, clubs):
        """
        Remplit la table avec les données des clubs.
        :param clubs: Liste de dictionnaires contenant les informations des clubs
        """
        self.table.setRowCount(len(clubs))

        for i, club in enumerate(clubs):
            # Ajouter le logo
            label_logo = bib.QLabel()
            pixmap = bib.QPixmap(club["logo"])
            label_logo.setPixmap(pixmap.scaled(50, 50, bib.Qt.KeepAspectRatio))
            label_logo.setAlignment(bib.Qt.AlignCenter)
            self.table.setCellWidget(i, 0, label_logo)

            # Fonction pour créer un QTableWidgetItem avec texte centré
            def create_centered_item(text):
                item = bib.QTableWidgetItem(text)
                item.setTextAlignment(bib.Qt.AlignCenter)
                return item

            # Ajouter les informations des clubs
            self.table.setItem(i, 1, create_centered_item(club["nom"]))
            self.table.setItem(i, 2, create_centered_item(str(club["points_marques"])))
            self.table.setItem(i, 3, create_centered_item(str(club["points_encaisse"])))
            self.table.setItem(i, 4, create_centered_item(str(club["points_totals"])))
            self.table.setItem(i, 5, create_centered_item(str(club["bonus_offensif"])))
            self.table.setItem(i, 6, create_centered_item(str(club["bonus_defensif"])))

        # Ajuster la taille des lignes
        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, int((bib.QApplication.desktop().screenGeometry().height()-20)/14))

        # Ajuster les tailles des colonnes
        for col in range(self.table.columnCount()):
            self.table.setColumnWidth(col, int((bib.QApplication.desktop().screenGeometry().width() - 14) / 9))

        #self.table.resizeColumnsToContents()

    def fenetre_init(self):
        """
        Initialise les paramètres de la fenêtre.
        """
        self.setWindowTitle('Classement des Clubs')
        self.setGeometry(0, 0, bib.QApplication.desktop().screenGeometry().width(),
                         bib.QApplication.desktop().screenGeometry().height())  # Mettre la page en plein écran

        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = bib.QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, bib.QColor(0, 0, 255))  # Bleu
        gradient.setColorAt(0.8, bib.QColor(128, 0, 128))  # Violet
        palette.setBrush(bib.QPalette.Background, gradient)
        self.setPalette(palette)

    def afficher_le_classement(self):
        """
        Affiche les données du classement dans la table.
        """
        tableau_equipe, tableau_match = recuperation_match_equipe()
        clubs = []
        print("Le nombre d'équipes trouvées est de : ", len(tableau_equipe))

        # Traitement des données pour remplir les informations des clubs
        for i, equipe in enumerate(tableau_equipe):
            club = {
                "logo": equipe[4],  # Exemple de chemin vers le logo
                "nom": equipe[1],
                "points_marques": 0,  # À calculer en fonction des matchs
                "points_encaisse": 0,  # À calculer en fonction des matchs
                "points_totals": 0,    # À calculer en fonction des matchs et des bonus
                "bonus_offensif": 0,   # À définir selon les règles
                "bonus_defensif": 0    # À définir selon les règles
            }
            clubs.append(club)
        
        self.charger_donnees(clubs)
