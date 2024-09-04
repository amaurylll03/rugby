import bibliotheque as bib
def recherche_carriere_en_cours ():
    conn = bib.sqlite3.connect('rugby.db')
    cursor = conn.cursor()
   
    cursor.execute("SELECT * FROM carriere_en_cours ")
    record = cursor.fetchone()
    conn.close()
    
    return record[0]
def recherche_entraineur(id_entraineur):
    conn = bib.sqlite3.connect('rugby.db')
    cursor = conn.cursor()
   
    cursor.execute("SELECT prenom,nom,image,ID_Equipe,nationalite FROM entraineur WHERE ID_Entraineur=? ",(id_entraineur,))
    record = cursor.fetchone()
    conn.close()
    return record
def recherche_equipe(id_equipe):
    conn = bib.sqlite3.connect('rugby.db')
    cursor = conn.cursor()
   
    cursor.execute("SELECT Nom,Img_Ecusson FROM equipe WHERE ID_Equipe=? ",(id_equipe,))
    record = cursor.fetchone()
    conn.close()
    return record

class page_jouer(bib.QWidget):
    def __init__(self,stacked_widget ):
        super().__init__()
        self.image_entraineur=None
        self.prenom_nom_entraineur_layout=None
        self.image_club=None
        self.prenom_nom_entraineur_layout=None
        self.fenetre_init()
        self.partage_de_la_page()
        



        self.stacked_widget = stacked_widget

        
    def fenetre_init(self):
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
    def showEvent(self, event):
        # Cette méthode est appelée chaque fois que la page est affichée
        info_entraineur_sortie_bdd=recherche_entraineur(recherche_carriere_en_cours())
     


        pixmap = bib.QPixmap(info_entraineur_sortie_bdd[2])

        # Ajuster le QLabel pour qu'il ait une taille définie (facultatif, en fonction de votre layout)
        self.image_entraineur.setStyleSheet("background-color: transparent;border:2px;border-color:transparent;border-radius:10px;")

        # Redimensionner le pixmap pour qu'il s'adapte à la taille du QLabel, en conservant les proportions
        scaled_pixmap = pixmap.scaledToHeight(
            int(bib.QApplication.desktop().screenGeometry().height()*6/45),  
            bib.Qt.SmoothTransformation
        )
        self.image_entraineur.setAlignment(bib.Qt.AlignTop | bib.Qt.AlignLeft)
        font = bib.QFont()
        font.setPointSize(20)

        # Appliquer le pixmap redimensionné au QLabel
        self.image_entraineur.setPixmap(scaled_pixmap)
        while self.prenom_nom_entraineur_layout.count():
                item = self.prenom_nom_entraineur_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
        if(self.prenom_nom_entraineur_layout.count() ==0):
            info1=bib.QLabel(info_entraineur_sortie_bdd[4],self)
            info1.setFont(font)
            info1.setStyleSheet("background-color: transparent;border:none;")
            info1.setFixedSize(int(bib.QApplication.desktop().screenGeometry().width()* 1 / 10 ), int(bib.QApplication.desktop().screenGeometry().height()*5/27))
            info1.setAlignment(bib.Qt.AlignTop| bib.Qt.AlignLeft)
            


            prenom_entraineur=bib.QLabel(info_entraineur_sortie_bdd[0],self)
            prenom_entraineur.setFont(font)
            prenom_entraineur.setStyleSheet("background-color: transparent;border:none;")
            prenom_entraineur.setAlignment(bib.Qt.AlignTop| bib.Qt.AlignLeft)
            prenom_entraineur.setFixedSize(int(bib.QApplication.desktop().screenGeometry().width()* 1 / 10 ), int(bib.QApplication.desktop().screenGeometry().height()/27))

            self.prenom_nom_entraineur_layout.addWidget(prenom_entraineur)
            nom_entraineur=bib.QLabel(info_entraineur_sortie_bdd[1],self)
            nom_entraineur.setStyleSheet("background-color: transparent;border:none;")
            nom_entraineur.setFont(font)
            nom_entraineur.setAlignment(bib.Qt.AlignTop| bib.Qt.AlignLeft)
            nom_entraineur.setFixedSize(int(bib.QApplication.desktop().screenGeometry().width()* 1 / 10 ), int(bib.QApplication.desktop().screenGeometry().height()/27))
            
            self.prenom_nom_entraineur_layout.addWidget(nom_entraineur)
            self.prenom_nom_entraineur_layout.addWidget(info1)
        
            
        # Charger l'image depuis la base de données
        pixmap = bib.QPixmap(recherche_equipe(info_entraineur_sortie_bdd[3])[1])

        # Ajuster le QLabel pour qu'il ait une taille définie (facultatif, en fonction de votre layout)
        self.image_club.setStyleSheet("background-color: transparent;border:2px;border-color:transparent;border-radius:10px;")

        # Redimensionner le pixmap pour qu'il s'adapte à la taille du QLabel, en conservant les proportions
        scaled_pixmap = pixmap.scaledToHeight(
            int(bib.QApplication.desktop().screenGeometry().height()*4/45),  
            bib.Qt.SmoothTransformation
        )
        self.image_club.setAlignment(bib.Qt.AlignTop | bib.Qt.AlignRight)
        self.image_club.setPixmap(scaled_pixmap)
        

        super().showEvent(event)
    def partage_de_la_page(self):
        
        

        font = bib.QFont()
        font.setPointSize(20)
        main_layout = bib.QVBoxLayout()
        main_layout.setSpacing(0)  # Pas d'espacement entre les widgets
        main_layout.setContentsMargins(0, 0, 0, 0)  # Pas de marges autour du layout principal

        entete=bib.QWidget()
        entetelayout=bib.QHBoxLayout(entete)
        entete.setStyleSheet("background-color:#0000FF;")
        entetelayout.setSpacing(0)  # Pas d'espacement entre les widgets
        entetelayout.setContentsMargins(0, 0, 0, 0)

        info_entraineur=bib.QWidget()
        info_entraineur_layout=bib.QHBoxLayout(info_entraineur)
        info_entraineur_layout.setSpacing(0)
        info_entraineur_layout.setContentsMargins(0, 0, 0, 0)
        self.image_entraineur = bib.QLabel("", self)

        # Charger l'image depuis la base de données
        
        
        prenom_nom_entraineur=bib.QWidget()
        prenom_nom_entraineur.setStyleSheet("background-color:transparent;")
        prenom_nom_entraineur.setFixedSize(int(bib.QApplication.desktop().screenGeometry().width()* 1 / 10 ), 
                            int(bib.QApplication.desktop().screenGeometry().height()*2/9 ))
        
     
        prenom_nom_entraineur.setStyleSheet("background-color: transparent;")
        self.prenom_nom_entraineur_layout=bib.QVBoxLayout(prenom_nom_entraineur)
        self.prenom_nom_entraineur_layout.setAlignment(bib.Qt.AlignTop)
        self.prenom_nom_entraineur_layout.setSpacing(0)
        self.prenom_nom_entraineur_layout.setContentsMargins(0, 0, 0, 0)
        

        

        
        
        """
        info2=bib.QLabel("",self)
        info2.setStyleSheet("background-color: transparent;border:none;")
        self.prenom_nom_entraineur_layout.addWidget(info2)
        info3=bib.QLabel("",self)
        info3.setStyleSheet("background-color: transparent;border:none;")
        self.prenom_nom_entraineur_layout.addWidget(info3)"""
    
        info_entraineur_layout.addWidget(prenom_nom_entraineur)
        info_entraineur_layout.addWidget(self.image_entraineur)
        entetelayout.addWidget(info_entraineur)



        font.setPointSize(36)
        
        label_title = bib.QLabel("Menu Jouer", self)
        label_title.setFont(font)
        entete.setFixedSize(int(bib.QApplication.desktop().screenGeometry().width() ), 
                            int(bib.QApplication.desktop().screenGeometry().height() * 2 / 9))
        label_title.setStyleSheet("background-color: transparent;")
        label_title.setAlignment(bib.Qt.AlignHCenter | bib.Qt.AlignTop )
        entetelayout.addWidget(label_title)
        


        self.image_club = bib.QLabel("", self)

        


        # Appliquer le pixmap redimensionné au QLabel
        

        self.image_club.setStyleSheet("background-color: transparent;border:none;")
        entetelayout.addWidget(self.image_club)
        
        main_layout.addWidget(entete)


        choix_menu=bib.QWidget()
        bouton_choix_menu_transversale=bib.QHBoxLayout(choix_menu)
        bouton_choix_menu_transversale.setSpacing(0)  # Pas d'espacement entre les widgets
        bouton_choix_menu_transversale.setContentsMargins(0, 0, 0, 0)
        nom_menu=['jouer',"gestion d'équipe","mercato","quittez"]
        for j in range (4):

                buttona = bib.QPushButton(nom_menu[j])
                
                buttona.clicked.connect(lambda checked,nom_menub=nom_menu[j]: self.bouton_choix_onglet(nom_menub))

                buttona.setFixedSize(int(bib.QApplication.desktop().screenGeometry().width() / 4), 
                            int(bib.QApplication.desktop().screenGeometry().height()  / 9))
                self.style_button(buttona)
                bouton_choix_menu_transversale.addWidget(buttona)

        main_layout.addWidget(choix_menu)



        quatre_boutons = bib.QWidget()
        quatre_boutons.setSizePolicy(bib.QSizePolicy.Expanding, bib.QSizePolicy.Expanding)
        grid_layout = bib.QGridLayout(quatre_boutons)
        grid_layout.setSpacing(0)  # Pas d'espacement entre les widgets
        grid_layout.setContentsMargins(0, 0, 0, 0)
        nom_menu2=["simuler","calendrier","classement","entrainement"]
        for i in range (2):
            for j in range (2):

                button = bib.QPushButton()
                button.setText(nom_menu2[(i*2+j)])
                button.clicked.connect(getattr(self, nom_menu2[(i*2+j)]))
                button.setFixedSize(int(bib.QApplication.desktop().screenGeometry().width() / 2), 
                            int(bib.QApplication.desktop().screenGeometry().height() / 3))
                self.style_button(button)
                grid_layout.addWidget(button,i,j)

        main_layout.addWidget(quatre_boutons)
        self.setLayout(main_layout)
    def calendrier(self):
        self.stacked_widget.setCurrentIndex(4)
    def simuler(self):
        self.stacked_widget.setCurrentIndex(4)
    def entrainement(self):
        self.stacked_widget.setCurrentIndex(4)
    def classement(self):
        self.stacked_widget.setCurrentIndex(6)
    def style_button(self, button ):
        """Applique un style avec un dégradé aux boutons."""
        stylesheet = f"""
            QPushButton {{
                margin: 0px;
                padding: 0px;
                background-color: transparent;
                border-style: solid;
                border-color: #800080;
                font-size: 24px;
                color: #e0e0e0;
            }}
            QPushButton:hover {{
                background-color: #0000FF;
                border-color: #0000FF;
                color:#eea6ff;
            }}
        """
        button.setStyleSheet(stylesheet)
    def bouton_choix_onglet(self,texte):
        if texte =="quittez":

            self.stacked_widget.setCurrentIndex(0)


"""if __name__ == "__main__":

    app = bib.QApplication(bib.sys.argv)
    page = page_jouer()  # Créer une instance de la classe PageJouer
    page.showFullScreen()  # Afficher en plein écran
    bib.sys.exit(app.exec_())"""
