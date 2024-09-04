import sys
import urllib.request
import sqlite3
import shutil
import os
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,QDesktopWidget, QHBoxLayout, QLabel, QStackedWidget,QTableWidget,QTableWidgetItem, QLineEdit, QComboBox,QSizePolicy, QFrame, QFormLayout,QGridLayout,QMainWindow
from PyQt5.QtGui import QLinearGradient, QColor, QPalette, QFont,QPixmap,QIcon
from PyQt5.QtCore import Qt, QRect,QSize

def recuperer_quinze():
    conn = sqlite3.connect('rugby.db')
    cursor = conn.cursor()

    try:
        # Exécution de la requête SQL pour récupérer l'URL du logo de l'équipe
        cursor.execute("SELECT prenom,nom,poste FROM joueurs WHERE titulaire=1 ORDER BY poste")
        row = cursor.fetchall()
        if row:
            return row
        else:
            return None

    except sqlite3.Error as e:
        print("Erreur lors de l'exécution de la requête SQL :", e)
        return None

    finally:
        # Fermeture de la connexion à la base de données
        conn.close()
def enlever_les_repetitions_dans_bdd():
    conn=sqlite3.connect('rugby.db')
    cursor=conn.cursor()

    cursor.execute('''
    DELETE FROM joueurs
    WHERE id NOT IN (
    SELECT id FROM (
        SELECT MIN(id) as id
        FROM joueurs
        GROUP BY prenom, nom
    )
    )
    ''')

    conn.commit()


    conn.close()
def nom_carriere():
    conn=sqlite3.connect('rugby.db')
    cursor=conn.cursor()

    cursor.execute("SELECT ID_entraineur FROM carriere_en_cours")
    res=cursor.fetchone()
    cursor.execute("SELECT nom_carriere FROM entraineur WHERE ID_Entraineur = ?",(res[0],))
    nomcar=cursor.fetchone()[0]
    return nomcar
def recup_equipe(team_id,nom_carriere):
    conn=sqlite3.connect("sauvegarde/"+nom_carriere+"/rugby.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM equipe WHERE ID_Equipe = ? ",(team_id,))
    res=cursor.fetchone()
    if res == None :
        print("Erreur lors de la recherche de l'equipe , team_id recherche :",team_id)
    return res 
def recup_id_equipe(nom_carriere):
    conn=sqlite3.connect("sauvegarde/"+nom_carriere+"/rugby.db")
    cursor=conn.cursor()
    cursor.execute("SELECT ID_Equipe FROM entraineur WHERE ID_Entraineur = (SELECT MAX(ID_Entraineur) FROM entraineur)")
    res=cursor.fetchone()
    if res == None :
        print("Erreur lors de la recherche de l'id de l'equipe :")
    return res[0] 
def recup_entraineur(nom_carriere):
    conn=sqlite3.connect("sauvegarde/"+nom_carriere+"/rugby.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM entraineur WHERE ID_Entraineur = (SELECT MAX(ID_Entraineur) FROM entraineur)")
    res=cursor.fetchone()
    if res == None :
        print("Erreur lors de la recherche de l'id de l'equipe :")
    return res
def recup_match(id_equipe,nom_carriere):
    conn=sqlite3.connect("sauvegarde/"+nom_carriere+"/rugby.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM match WHERE id_equipe1 = ? OR id_equipe2=?",(id_equipe,id_equipe))
    res=cursor.fetchall()
    if res == None :
        print("Erreur lors de la recherche de l'id de l'equipe :")
    return res





         



