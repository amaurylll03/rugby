import bibliotheque as bib
import Calendrier as Cal
# Définir les couleurs
colors = {
    'primary-100': bib.QColor('#0000FF'),
    'primary-200': bib.QColor('#7142FF'),
    'primary-300': bib.QColor('#EEA6FF'),
    'accent-100': bib.QColor('#FFD700'),
    'accent-200': bib.QColor('#917800'),
    'text-100': bib.QColor('#FFFFFF'),
    'text-200': bib.QColor('#E0E0E0'),
    'bg-100': bib.QColor('#800080'),
    'bg-200': bib.QColor('#942293'),
    'bg-300': bib.QColor('#B343B0')
}

def get_starting_xv(team_id):
    conn = bib.sqlite3.connect('rugby.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT Nom, Prenom, image, poste
            FROM joueurs
            WHERE ID_Equipe = ? AND Titulaire = 1
            ORDER BY poste
        """, (team_id,))
        players = cursor.fetchall()
        return players
    except bib.sqlite3.Error as e:
        print("Erreur lors de l'exécution de la requête SQL :", e)
        return []
    finally:
        conn.close()

def recup_stade(id_equipe):
    conn = bib.sqlite3.connect('rugby.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM stade WHERE ID_Equipe = ?", (id_equipe,))
        row = cursor.fetchone()
        if row:
            return row
        else:
            return None
    except bib.sqlite3.Error as e:
        print("Erreur lors de l'exécution de la requête SQL :", e)
        return None
    finally:
        conn.close()

def recup_logo(id_equipe):
    conn = bib.sqlite3.connect('rugby.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM equipe WHERE ID_Equipe = ?", (id_equipe,))
        row = cursor.fetchone()
        if row:
            return row
        else:
            return None
    except bib.sqlite3.Error as e:
        print("Erreur lors de l'exécution de la requête SQL :", e)
        return None
    finally:
        conn.close()
        
import random

def round_robin_schedule(teams):
    if len(teams) % 2 != 0:
        teams.append(None)  # Ajout d'une équipe "fictive" si nombre d'équipes impair

    schedule = []
    n = len(teams)
    for round in range(n - 1):
        matches = []
        for i in range(n // 2):
            home = teams[i]
            away = teams[n - i - 1]
            if home is not None and away is not None:
                if round % 2 == 0:
                    matches.append([home, away])
                else:
                    matches.append([away, home])
        schedule.append(matches)
        teams.insert(1, teams.pop())  # Rotation des équipes
    return schedule

def generate_top14_schedule(equipe, calendrier):
    teams = equipe[0]  # Utiliser les numéros des équipes de 1 à 14
    first_half = round_robin_schedule(teams)
    second_half = [[match[::-1] for match in day] for day in first_half]  # Inverser les matchs pour la phase retour
    full_schedule = first_half + second_half  # 26 journées au total

    # Remplir le calendrier avec les matchs générés
    for i in range(26):
        for j in range(7):
            calendrier[i][j] = full_schedule[i][j]

    return calendrier

def print_schedule(calendrier):
    for day in range(26):
        print(f"Journée {day + 1}:")
        for match in calendrier[day]:
            print(f"  Équipe {match[0]} vs Équipe {match[1]}")
        print("")

# Initialisation
def programmer_saison():
    equipe = [[i + 1 for i in range(14)]]  # Liste des équipes de 1 à 14
    calendrier = [[[0 for k in range(2)] for j in range(7)] for i in range(26)]  # 26 journées, 7 matchs par journée

    # Générer le calendrier
    calendrier = generate_top14_schedule(equipe, calendrier)

    # Imprimer le calendrier
    #print_schedule(calendrier)
    return calendrier
        

class ChooseYourTeam(bib.QWidget):

    def __init__(self,stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.team_id = 1  # Initialiser team_id
        self.init_ui()

    def init_ui(self):
        screen_geometry = bib.QDesktopWidget().screenGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        self.equipe_label = None
        self.budget_label = None
        self.stade_label = None
        self.capacite_label = None
        label_logo_equipe =None


        # Définir les couleurs
        self.colors = {
            'primary-100': bib.QColor('#0000FF'),
            'primary-200': bib.QColor('#7142FF'),
            'primary-300': bib.QColor('#EEA6FF'),
            'primary-400': bib.QColor('#A07F7D'),
            'accent-100': bib.QColor('#FFD700'),
            'accent-200': bib.QColor('#917800'),
            'text-100': bib.QColor('#FFFFFF'),
            'text-200': bib.QColor('#E0E0E0'),
            'bg-100': bib.QColor('#800080'),
            'bg-200': bib.QColor('#942293'),
            'bg-300': bib.QColor('#B343B0')
        }

        # Appliquer la couleur d'arrière-plan de la fenêtre principale
        self.setStyleSheet(f'background-color: {self.colors["bg-100"].name()};')

        # Layout principal
        main_layout = bib.QVBoxLayout()
        main_layout.setSpacing(0)  # Pas d'espacement entre les widgets
        main_layout.setContentsMargins(0, 0, 0, 0)  # Pas de marges autour du layout principal

        # Layout supérieur pour le titre
        title_layout = bib.QHBoxLayout()
        title_label = bib.QLabel('Choix Equipe')
        title_label.setFixedHeight(200)
        title_label.setStyleSheet(f'background-color: {self.colors["bg-300"].name()}; color: {self.colors["text-100"].name()};font-size:30px;')
        title_label.setAlignment(bib.Qt.AlignCenter)  # Centrer le texte
        title_layout.addWidget(title_label)
        title_layout.setContentsMargins(0, 0, 0, 0)  # Pas de marges autour du titre

        # Layout horizontal pour séparer les zones latérales et la zone principale
        main_horizontal_layout = bib.QHBoxLayout()
        main_horizontal_layout.setContentsMargins(0, 0, 0, 0)  # Pas de marges autour du layout horizontal
        main_horizontal_layout.setSpacing(0)  # Pas d'espacement entre les widgets

        # Zone latérale gauche
        self.left_sidebar = bib.QWidget()
        self.left_sidebar.setFixedWidth(int(screen_width * 0.2))  # Largeur fixe pour la zone latérale gauche
        self.left_sidebar.setStyleSheet(f'background-color: {self.colors["bg-200"].name()};')

        # Layout pour les boutons et labels dans la zone latérale gauche
        left_layout = bib.QGridLayout()
        left_layout.setSpacing(0)  # Pas d'espace entre les éléments
        left_layout.setContentsMargins(0, 0, 0, 0)  # Pas de marges internes

        self.update_left_sidebar(left_layout)

        self.left_sidebar.setLayout(left_layout)

        # Zone principale
        self.central_widget = bib.QWidget()
        self.central_widget.setStyleSheet(f'background-color: {self.colors["primary-300"].name()};')

        # Layout pour la zone centrale
        central_layout = bib.QVBoxLayout()
        central_layout.setSpacing(0)  # Pas d'espace entre les éléments
        central_layout.setContentsMargins(0, 0, 0, 0) 
        #self.central_widget.setMaximumSize(2000, 500)  # Limiter la taille maximale de la zone centrale

        # En-tête de la zone centrale
        header_label = bib.QLabel('XV de départ')
        header_label.setFixedHeight(200)
        header_label.setStyleSheet(f'background-color: {self.colors["primary-300"].name()}; color: {self.colors["text-100"].name()};font-size:90px')
        header_label.setAlignment(bib.Qt.AlignCenter)  # Centrer le texte
        central_layout.addWidget(header_label)

        # Grille de labels de 5x7 avec taille maximale de 100x50
        self.grid_layout = bib.QGridLayout()
        self.grid_layout.setSpacing(0)  # Pas d'espace entre les éléments
        self.grid_layout.setContentsMargins(0, 0, 0, 0)  # Pas de marges internes

        self.update_grid_layout()

        central_layout.addLayout(self.grid_layout)

        # Ajouter le layout à la zone principale
        self.central_widget.setLayout(central_layout)

        # Zone latérale droite
        self.right_sidebar = bib.QWidget()
        self.right_sidebar.setFixedWidth(700)  # Largeur fixe pour la zone latérale droite
        self.right_sidebar.setStyleSheet(f'background-color: {self.colors["bg-200"].name()};')

        self.update_right_sidebar()


    

        # Ajouter les widgets au layout horizontal principal
        main_horizontal_layout.addWidget(self.left_sidebar)

        # Espacers pour centrer le widget principal
        #spacer_left = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        #spacer_right = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        #main_horizontal_layout.addItem(spacer_left)  # Espacer à gauche de la zone principale
        main_horizontal_layout.addWidget(self.central_widget)
        #main_horizontal_layout.addItem(spacer_right)  # Espacer à droite de la zone principale
        main_horizontal_layout.addWidget(self.right_sidebar)

        # Ajouter les layouts au layout principal
        main_layout.addLayout(title_layout)
        main_layout.addLayout(main_horizontal_layout)

        # Configurer le layout principal de la fenêtre
        self.setLayout(main_layout)

    def update_left_sidebar(self, layout):
        # Recrée le layout de la zone latérale gauche
        for i in range(7):
            for j in range(2):
                info_equipe = recup_logo(int(i + 7 * j + 1))
                logo_equipe = info_equipe[4]
                Nom_equipe = info_equipe[1]

                button_frame = bib.QFrame()
                button_frame.setFixedSize(100, 130)  # Ajuster la taille fixe du QFrame pour contenir le bouton et le texte
                button_frame.setFrameShape(bib.QFrame.Box)
                button_frame.setFrameShadow(bib.QFrame.Raised)
                button_frame.setLineWidth(1)

                accent_color = self.colors["accent-200"].name()
                primary_color = self.colors["primary-100"].name()
                text_color = self.colors["text-100"].name()
                text200_color = self.colors["text-200"].name()

                #button_frame.setStyleSheet(f'border: 1px solid {accent_color};')  # Couleur de la bordure

                # Création des boutons et labels
                button = bib.QPushButton(f'')
                button.setFixedSize(100, 100)

                if logo_equipe:
                    icon = bib.QIcon(logo_equipe)
                    button.setIcon(icon)
                    button.setIconSize(bib.QSize(60, 60))  # Ajuster la taille de l'image

                stylesheet = f"""
                    QPushButton {{
                        background-color: {primary_color};
                        color: {text_color};
                    }}
                """
                button.setStyleSheet(stylesheet)
                button.setProperty('id_equipe_bouton', int(i + 7 * j + 1))
                button.clicked.connect(self.button_onclick)

                label = bib.QLabel(Nom_equipe)
                label.setStyleSheet(f'color: {text200_color};')
                label.setAlignment(bib.Qt.AlignCenter)  # Centrer le texte

                # Layout pour le bouton et le label dans le QFrame
                button_layout = bib.QVBoxLayout()
                button_layout.addWidget(button)
                button_layout.addWidget(label)
                button_layout.setContentsMargins(0, 0, 0, 0)  # Pas de marges
                button_layout.setSpacing(0)  # Pas d'espace entre le bouton et le texte
                button_frame.setLayout(button_layout)

                # Ajouter le QFrame contenant le bouton et le texte au layout
                layout.addWidget(button_frame, i, j * 2)

    def button_onclick(self):
         button=self.sender()
         team_identifiant = button.property('id_equipe_bouton')
         self.update_team(team_identifiant)
    
    def update_grid_layout(self):
        # Recrée le layout de la grille principale
        texts = [
            ['10', '', '20', '', '30'],
            ['11', '', '21', '', '31'],
            ['', '40', '', '50', ''],
            ['', '41', '', '51', ''],
            ['60', '', '80', '', '70'],
            ['61', '', '81', '', '71'],
            ['', '90', '', '', ''],
            ['', '91', '', '', ''],
            ['', '', '100', '', ''],
            ['', '', '101', '', ''],
            ['110', '120', '', '130', '140'],
            ['111', '121', '', '131', '141'],
            ['', '', '150', '', ''],
            ['', '', '151', '', '']
        ]

        players = get_starting_xv(self.team_id)
        tab = [player[2] for player in players]
        for row in range(14):
            for col in range(5):
                label_text = texts[row][col] if col < len(texts[row]) else ''  # Handle rows of varying length

                if label_text == '':
                    # Empty cell
                    label = bib.QLabel('')
                    label.setStyleSheet(f'background-color: transparent; color: {self.colors["primary-100"].name()};font-size:8px; ')
                    label.setFixedSize(100, 77)
                    label.setAlignment(bib.Qt.AlignCenter)
                    self.grid_layout.addWidget(label, row, col)
                else:
                    match_found = False
                    player_number = int(texts[row][col])
                    for player in players:
                        
                        if player[3] == player_number // 10 and player_number % 10 == 1:
                            # Match found
                            print("Match found for player:", player)
                            label_text = player[1] + " " + player[0]
                            label = bib.QLabel(label_text)
                            label.setStyleSheet(f'background-color: white; color: black;font-size:10px;border-radius:5px;')
                            label.setFixedSize(120, 27)
                            label.setAlignment(bib.Qt.AlignCenter)
                            self.grid_layout.addWidget(label, row, col)
                            match_found = True
                            break
                    
                    if not match_found and len(tab)>1:
                        # No match found, display image
                        # Get a unique image path for each cell
                        if col < len(tab):
                            player_image_path = tab[(int(player_number / 10)-1)]
                        else:
                            player_image_path = tab[0]  # Fallback to the first image if index exceeds

                        label = bib.QLabel()
                        label.setFixedSize(120, 80)
                        label.setAlignment(bib.Qt.AlignCenter)
                        pixmap = bib.QPixmap(player_image_path)  # Load image from player[2]
                        pixmap = pixmap.scaled(120, 80, bib.Qt.KeepAspectRatio, bib.Qt.SmoothTransformation)
                        label.setPixmap(pixmap)
                        label.setStyleSheet(f'background-color: white; color: {self.colors["text-200"].name()};font-size:10px;border-radius:5px;')
                        self.grid_layout.addWidget(label, row, col)


        
                

    def update_right_sidebar(self):
        info_equipe = recup_logo(self.team_id)
        info_stade = recup_stade(self.team_id)

        if self.right_sidebar.layout() is None:
            right_layout = bib.QVBoxLayout()

            if info_equipe:
                self.label_logo_equipe = bib.QLabel()
                self.label_logo_equipe.setFixedSize(150, 150)
                self.label_logo_equipe.setAlignment(bib.Qt.AlignCenter)
                pixmap = bib.QPixmap(info_equipe[4])  # Load image from info_equipe[4]
                pixmap = pixmap.scaled(150, 150, bib.Qt.KeepAspectRatio, bib.Qt.SmoothTransformation)
                self.label_logo_equipe.setPixmap(pixmap)
                self.label_logo_equipe.setStyleSheet(f'background-color: transparent; color: {self.colors["text-200"].name()};font-size:10px;border-radius:5px;')
                right_layout.addWidget(self.label_logo_equipe, alignment=bib.Qt.AlignCenter)


                self.equipe_label = bib.QLabel('Equipe choisie : ' + info_equipe[1])
                self.equipe_label.setStyleSheet(f'color: {self.colors["text-200"].name()};font-size:20px;')
                self.equipe_label.setAlignment(bib.Qt.AlignCenter)
                right_layout.addWidget(self.equipe_label)

                self.budget_label = bib.QLabel(f'Budget : {info_equipe[7]:,}'.replace(',', '  '))
                self.budget_label.setStyleSheet(f'color: {self.colors["text-200"].name()};font-size:20px;')
                self.budget_label.setAlignment(bib.Qt.AlignCenter)
                right_layout.addWidget(self.budget_label)

            if info_stade:
                self.stade_label = bib.QLabel('Nom stade : ' + str(info_stade[1]))
                self.stade_label.setStyleSheet(f'color: {self.colors["text-200"].name()};font-size:20px;')
                self.stade_label.setAlignment(bib.Qt.AlignCenter)
                right_layout.addWidget(self.stade_label)

                self.capacite_label = bib.QLabel(f'Capacité stade : {info_stade[3]:,}'.replace(',', '  '))
                self.capacite_label.setStyleSheet(f'color: {self.colors["text-200"].name()};font-size:20px;')
                self.capacite_label.setAlignment(bib.Qt.AlignCenter)
                right_layout.addWidget(self.capacite_label)

            espace_deuxboutons = bib.QWidget()
            layout_espace_deuxboutons = bib.QHBoxLayout()
            button_valider = bib.QPushButton(f'Valider')
            button_valider.setFixedSize(200, 50)
            button_valider.setStyleSheet(f'background-color: {self.colors["primary-100"].name()}; color: {self.colors["text-100"].name()};')
            button_valider.clicked.connect(self.submit_carierre)

            layout_espace_deuxboutons.addWidget(button_valider)
            button_retour = bib.QPushButton(f'Retour')
            button_retour.setFixedSize(200, 50)
            button_retour.setStyleSheet(f'background-color: {self.colors["primary-100"].name()}; color: {self.colors["text-100"].name()};')
            button_retour.clicked.connect(self.retour_fen_prec)

            
            layout_espace_deuxboutons.addWidget(button_retour)

            espace_deuxboutons.setLayout(layout_espace_deuxboutons)
            right_layout.addWidget(espace_deuxboutons)

            self.right_sidebar.setLayout(right_layout)
        else:
            # Mettre à jour les labels existants
            if info_equipe:
                
                  # Load image from info_equipe[4]
                
                self.label_logo_equipe.setPixmap(bib.QPixmap(info_equipe[4]).scaled(150, 150, bib.Qt.KeepAspectRatio, bib.Qt.SmoothTransformation))
                self.equipe_label.setText('Equipe choisie : ' + info_equipe[1])
                self.budget_label.setText(f'Budget : {info_equipe[7]:,}'.replace(',', '  '))

            if info_stade:
                self.stade_label.setText('Nom stade : ' + str(info_stade[1]))
                self.capacite_label.setText(f'Capacité stade : {info_stade[3]:,}'.replace(',', '  '))
    def submit_carierre(self):
        conn = bib.sqlite3.connect('rugby.db')
        cursor = conn.cursor()
        
        cursor.execute("UPDATE entraineur SET ID_Equipe = ? WHERE ID_Entraineur = (SELECT MAX(ID_Entraineur) FROM entraineur)",(self.team_id,))
        conn.commit()
        cursor.execute("SELECT ID_Entraineur FROM entraineur WHERE ID_Entraineur = (SELECT MAX(ID_Entraineur) FROM entraineur)") 
        res=cursor.fetchone()
        cursor.execute("UPDATE carriere_en_cours SET ID_entraineur = ? ", (res[0], )) 
        conn.commit()
        cursor.execute("SELECT nom_carriere FROM entraineur WHERE ID_Entraineur = (SELECT MAX(ID_Entraineur) FROM entraineur)") 
        res=cursor.fetchone() 
        
        nom_carriere=res[0]
        if not bib.os.path.exists("sauvegarde/"+nom_carriere):
            bib.os.makedirs("sauvegarde/"+nom_carriere)
            print("le dossier a ete cree")
        else:
            a=1
            while bib.os.path.exists("sauvegarde/"+nom_carriere+"("+str(a)+")"):
                a+=1
            nom_carriere+="("+str(a)+")"
            bib.os.makedirs("sauvegarde/"+nom_carriere)
            cursor.execute("UPDATE entraineur SET nom_carriere = ? WHERE ID_Entraineur = (SELECT MAX(ID_Entraineur) FROM entraineur)", (nom_carriere, )) 
            conn.commit()

        conn.close()
        # Copie du fichier 'rugby.db' dans le dossier "bonjour"
        bib.shutil.copy("rugby.db", "sauvegarde/"+nom_carriere+"/rugby.db")
        tableau_saison=programmer_saison()
        conn = bib.sqlite3.connect("sauvegarde/"+nom_carriere+"/rugby.db")
        cursor = conn.cursor()
        day,month,year=1,9,2024
        for k in range (2):
            day,month,year=Cal.prochainsamedi(day,month,year)
        
        for i in range (26):
            if (i+1)%4==0:
                for k in range (2):
                    day,month,year=Cal.prochainsamedi(day,month,year)
            
            for j in range (7):
                cursor.execute("INSERT INTO match (id_equipe1, id_equipe2,id_score1,id_score2,fin,jour,mois,annee) VALUES (?,?,?,?, ?, ?, ?,?)", (tableau_saison[i][j][0], tableau_saison[i][j][1],0,0,0,day,month,year)) 
                conn.commit()
            day,month,year=Cal.prochainsamedi(day,month,year) 
        conn.close()

        self.stacked_widget.setCurrentIndex(3)
    def retour_fen_prec(self):
        conn = bib.sqlite3.connect('rugby.db')
        cursor = conn.cursor()
            
        cursor.execute("DELETE FROM entraineur WHERE ID_Entraineur = (SELECT MAX(ID_Entraineur) FROM entraineur)")
        conn.commit()

        self.stacked_widget.setCurrentIndex(1)

    def update_team(self, team_id):
        self.team_id = team_id
        self.update_grid_layout()
        self.update_right_sidebar()

