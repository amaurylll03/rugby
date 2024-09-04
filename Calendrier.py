import bibliotheque as bib



def jour_de_la_semaine(jour, mois, annee):
    c = int((14 - mois) / 12)
    a = annee - c
    m = mois + 12 * c - 2
    j = ((jour + a + int(a / 4) - int(a / 100) + int(a / 400) + int((31 * m) / 12)) % 7)
    return j

def programmer_annee(annee):
    if annee % 4 == 0:
        mois_annee = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else:
        mois_annee = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return mois_annee
def prochainsamedi(jour,mois,annee):
    distance_next_saturday=7 if((6-jour_de_la_semaine(jour, mois, annee))==0) else (6-jour_de_la_semaine(jour, mois, annee))
    distance_fin_mois=programmer_annee(annee)[(mois-1)]-jour
    if distance_fin_mois>=distance_next_saturday :
        jour+=distance_next_saturday
    else:
        if mois<12:
            mois+=1  
        else :
            mois=1 
            annee+=1
        jour=distance_next_saturday-distance_fin_mois
    
    return((jour,mois,annee))
    
    

def logo_equipe_match_calendrier(jour,mois,annee):
    con=bib.sqlite3.connect('sauvegarde/'+bib.nom_carriere()+'/rugby.db')
    cursor=con.cursor()
    cursor.execute("SELECT ID_Equipe FROM entraineur WHERE ID_Entraineur = (SELECT MAX(ID_Entraineur) FROM entraineur)")
    res=cursor.fetchone()[0]
    cursor.execute("SELECT id_equipe1,id_equipe2 FROM match WHERE (id_equipe1=? OR id_equipe2=?) AND jour=? AND mois=? AND annee=?",(res,res,jour,mois,annee))
    res_equipes=cursor.fetchone()
    if res_equipes is None:
        return ""
    equipe_adverse=res_equipes[1]+1 if(res_equipes[0]==res) else res_equipes[0]+1
    cursor.execute("SELECT Img_Ecusson FROM equipe WHERE ID_Equipe=?",((equipe_adverse-1),))
    
    nom_equipe_adv=cursor.fetchone()
    return nom_equipe_adv[0]





def init_tableau_pour_calendrier():
    tab = [[0] * 7 for _ in range(6)]
    return tab

def calendrier(mois, annee):
    liste_mois = programmer_annee(annee)
    nombre_jour = liste_mois[mois - 1]
    
    start = (jour_de_la_semaine(1, mois, annee) - 1) if jour_de_la_semaine(1, mois, annee) != 0 else 6
    tab = init_tableau_pour_calendrier()

    for i in range(start, start + nombre_jour):
        tab[int(i / 7)][(i % 7)] = i - start + 1
    
    return tab

def recup_date():
    
    conn = bib.sqlite3.connect('sauvegarde/'+bib.nom_carriere()+'/rugby.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM date_du_jour")
    record = cursor.fetchone()
    conn.close()
    return record  # retourne un tuple composé de jour, mois, année
def moi_annee(tab):
    moi=["janvier","fevrier","mars","avril","mai","juin","juillet","aout","septembre","octobre","novembre","decembre"]
    text=moi[((tab[2])-1)]+" "+str(tab[3])
    return text
class page_calendrier(bib.QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.label_dict = {} 
        self.label_moi_annee=None
        self.date_tuple = [0, 0, 0, 0]
        (self.date_tuple[0], self.date_tuple[1], self.date_tuple[2], self.date_tuple[3]) = recup_date()
        self.fenetre_init()
        self.afficher_calendrier()

    def fenetre_init(self):
        self.setWindowTitle('Choix Entraineur')
        self.setGeometry(0, 0, bib.QApplication.desktop().screenGeometry().width(),
                         bib.QApplication.desktop().screenGeometry().height())  # Mettre la page en pleine écran

        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = bib.QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, bib.QColor(0, 0, 255))  # Bleu
        gradient.setColorAt(0.8, bib.QColor(128, 0, 128))  # Violet
        palette.setBrush(bib.QPalette.Background, gradient)
        self.setPalette(palette)

    def afficher_calendrier(self):
        tableau_affichage_date = calendrier(self.date_tuple[2], self.date_tuple[3])
        
        
        
    
        box_calendrier = bib.QWidget()
        box_calendrier_layout = bib.QGridLayout(box_calendrier)
        box_calendrier_layout.setSpacing(0)
        box_calendrier_layout.setContentsMargins(0, 0, 0, 0)
   
        # Ajouter les cases au layout
        for i in range(6):
            for j in range(7):
                
                one_box = bib.QLabel(str(tableau_affichage_date[i][j])) if tableau_affichage_date[i][j] != 0 else bib.QLabel("")
                one_box.setFixedSize(150, 150)
                one_box.setAlignment(bib.Qt.AlignHCenter | bib.Qt.AlignVCenter)
                one_box.setStyleSheet("background-color: #0000FF; margin: 5px; font-size: 30px; border: none;")
                one_box.setStyleSheet("background-color:red;margin:5px;font-size:30px;border:none")if(self.date_tuple[1]==tableau_affichage_date[i][j]) else one_box.setStyleSheet("background-color:#0000FF;margin:5px;font-size:30px;border: none;")
                
                if logo_equipe_match_calendrier(tableau_affichage_date[i][j],self.date_tuple[2],self.date_tuple[3])!="":
                    one_box.setPixmap(bib.QPixmap(logo_equipe_match_calendrier(tableau_affichage_date[i][j],self.date_tuple[2],self.date_tuple[3])).scaled(100, 100, bib.Qt.KeepAspectRatio, bib.Qt.SmoothTransformation)) 
                
                box_calendrier_layout.addWidget(one_box, i, j)
                self.label_dict[(i, j)] = one_box
                
        # Appliquer une bordure au widget contenant la grille
        box_calendrier.setStyleSheet("border: 2px solid #800080;background-color:#800080;")
        box_calendrier.setFixedSize(1100, 960)
        
        # Créer un layout central et y ajouter box_calendrier avec alignement centré
        central_widget = bib.QWidget()
        central_layout = bib.QHBoxLayout(central_widget)
        central_layout.addWidget(box_calendrier, alignment=bib.Qt.AlignCenter)
        
        # Ajouter les boutons
        right_widget = bib.QWidget()
        right_layout = bib.QVBoxLayout(right_widget)
        text_moi_annee=moi_annee(self.date_tuple)
        self.label_moi_annee = bib.QLabel(text_moi_annee)
        font = self.label_moi_annee.font()
        font.setPointSize(24)
        self.label_moi_annee.setFont(font)

        self.label_moi_annee.setFixedSize(300, 100)
        self.label_moi_annee.setFont(font)
        right_layout.addWidget(self.label_moi_annee)

        button_mois_suivant = bib.QPushButton("Mois Suivant", self) 
        button_mois_suivant.clicked.connect(self.mois_suivant) 
        button_mois_suivant.setStyleSheet("background-color: blue;font-size:24px;") 
        button_mois_suivant.setFixedSize(200, 100)
        right_layout.addWidget(button_mois_suivant)

        button_mois_precedent = bib.QPushButton("Mois Precedent", self) 
        button_mois_precedent.clicked.connect(self.mois_precedent) 
        button_mois_precedent.setStyleSheet("background-color: blue;font-size:24px;") 
        button_mois_precedent.setFixedSize(200, 100)
        right_layout.addWidget(button_mois_precedent)

        button_retour = bib.QPushButton("Retour", self) 
        button_retour.clicked.connect(self.button_retour) 
        button_retour.setStyleSheet("background-color: blue;font-size:24px;") 
        button_retour.setFixedSize(200, 100)

        right_layout.addWidget(button_retour)

        central_layout.addWidget(right_widget)
        
        # Ajouter le widget central au layout principal
        main_layout = bib.QVBoxLayout(self)  # Utiliser le layout principal existant
        main_layout.addWidget(central_widget)
        self.setLayout(main_layout)
        
    def button_retour(self):
        self.stacked_widget.setCurrentIndex(3)
    def update_label(self, i, j, new_text):
        # Récupérer le QLabel correspondant à la position (i, j)
        label = self.label_dict.get((i, j))
        
        label.setText(new_text)
        label.setStyleSheet("background-color: #0000FF; margin: 5px; font-size: 30px; border: none;")
        datetemp=[0,0,0,0]
        datetemp=recup_date()
        if new_text != "" :
            if (int(new_text)==datetemp[1] and self.date_tuple[2]==datetemp[2] and self.date_tuple[3]==datetemp[3]):
                label.setStyleSheet("background-color: red; margin: 5px; font-size: 30px; border: none;")
    
    def update_label_photo(self,image_nom,i,j):
        pixmap = bib.QPixmap(image_nom)
        
        pixmap = pixmap.scaled(100, 100, bib.Qt.KeepAspectRatio, bib.Qt.SmoothTransformation)

        # Assigner l'image redimensionnée à l'étiquette
        label = self.label_dict.get((i, j))
        label.setPixmap(pixmap)
        label.setAlignment(bib.Qt.AlignCenter)    
    def mois_precedent(self):
        if self.date_tuple[2] > 1:
            self.date_tuple[2] -= 1
        else:
            self.date_tuple[2] = 12
            self.date_tuple[3] -= 1
        tableau_affichage_date = calendrier(self.date_tuple[2], self.date_tuple[3])
        self.label_moi_annee.setText(moi_annee(self.date_tuple))

        for i in range (6):
            for j in range (7):
                label = self.label_dict.get((i, j))
        
                label.setText("1")
                if(logo_equipe_match_calendrier(tableau_affichage_date[i][j],self.date_tuple[2],self.date_tuple[3])==""):
                    self.update_label( i, j, str(tableau_affichage_date[i][j])) if tableau_affichage_date[i][j] != 0 else self.update_label( i, j, "")
                else:
                    self.update_label_photo(logo_equipe_match_calendrier(tableau_affichage_date[i][j],self.date_tuple[2],self.date_tuple[3]),i,j)   


    def mois_suivant(self):
        if self.date_tuple[2] < 12:
            self.date_tuple[2] += 1
        else:
            self.date_tuple[2] = 1
            self.date_tuple[3] += 1
        tableau_affichage_date = calendrier(self.date_tuple[2], self.date_tuple[3])
        self.label_moi_annee.setText(moi_annee(self.date_tuple))
        for i in range (6):
            for j in range (7):
                label = self.label_dict.get((i, j))
        
                label.setText("1")
                if(logo_equipe_match_calendrier(tableau_affichage_date[i][j],self.date_tuple[2],self.date_tuple[3])==""):
                    self.update_label( i, j, str(tableau_affichage_date[i][j])) if tableau_affichage_date[i][j] != 0 else self.update_label( i, j, "")
                else:
                    self.update_label_photo(logo_equipe_match_calendrier(tableau_affichage_date[i][j],self.date_tuple[2],self.date_tuple[3]),i,j)
                #self.update_label( i, j, str(tableau_affichage_date[i][j])) if tableau_affichage_date[i][j] != 0 else self.update_label( i, j, "")
                

