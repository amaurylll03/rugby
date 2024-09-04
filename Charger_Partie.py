import bibliotheque as bib
def recup_entraineur():
    conn = bib.sqlite3.connect('rugby.db')
    cursor = conn.cursor() 
    cursor.execute("SELECT nom_carriere FROM entraineur") 
    records = cursor.fetchall()
    conn.close()
    return records
def put_carriere_en_cours(text):
    conn=bib.sqlite3.connect("rugby.db")
    cursor=conn.cursor()
    cursor.execute("SELECT ID_Entraineur FROM entraineur WHERE nom_carriere = ?",(text,))
    records = cursor.fetchone()
    cursor.execute("UPDATE carriere_en_cours SET ID_entraineur= ? ",(records[0],))
    conn.commit()
    conn.close()
print(recup_entraineur())
class Charger_une_partie(bib.QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.fenetre_init()
    def fenetre_init(self):
        #Titre de la fenetre et fond de l ecran
        self.setWindowTitle('Choix Entraineur')
        self.setGeometry(0, 0, bib.QApplication.desktop().screenGeometry().width(),
                         bib.QApplication.desktop().screenGeometry().height())  # Mettre la page en pleine écran

        # Fond d'écran couleur unie
        
        self.layout = bib.QVBoxLayout(self)
        
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = bib.QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, bib.QColor(0, 0, 255))  # Bleu
        gradient.setColorAt(0.8, bib.QColor(128, 0, 128))  # Violet
        palette.setBrush(bib.QPalette.Background, gradient)
        self.setPalette(palette)
        for i in range ((len(recup_entraineur()))):
            self.create_button(recup_entraineur()[i][0])
        self.create_button("retour")


    def create_button(self, button_text):
        button = bib.QPushButton(button_text)
        button.setFixedSize(500,100)
        button.setStyleSheet("background-color:#008FFF;")
        # Connecter le bouton à une fonction si nécessaire
        if button_text=="retour":
            button.clicked.connect(self.retour)
        else:
            button.clicked.connect(lambda: self.on_button_click(button_text))
            
        
        # Ajouter le bouton à la disposition
        widget_horizontal=bib.QWidget()
        layout_horizontal=bib.QHBoxLayout(widget_horizontal)
        layout_horizontal.addWidget(button)
        self.layout.addWidget(widget_horizontal)

    def on_button_click(self,button_text):
        put_carriere_en_cours(button_text)
        self.stacked_widget.setCurrentIndex(3)

    def retour(self):
        self.stacked_widget.setCurrentIndex(0)

        

