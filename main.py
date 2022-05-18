from string import ascii_letters
from telnetlib import STATUS
from flask import Flask, render_template, request
from pytube import YouTube
from flask_json import FlaskJSON, json_response
import os
from os import listdir
from os.path import isfile, join
from playlist import Playlist
from video import Video
import re
import youtube_dl


app = Flask(__name__)
FlaskJSON(app)


USER="stef"
DERNIER_DL = ""
EXTENSION = ".mp3"

############################################################################

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html",model=USER)

############################################################################

@app.route('/charger', methods=['POST'])
def charger():

    url=request.form.get("video")

    if not url==None and url.startswith('https://www.youtube.com/'):

        try:
            Playlist.creerRepertoire(USER)

            video_name = Video.recupVideo(url,USER) 

            globals()['DERNIER_DL']=video_name+EXTENSION
            
            return render_template("index.html",model=USER)

        except:
            return render_template("index.html",model=USER, error="Problème lors du chargement de la vidéo.")
    else:
        return render_template("index.html",model=USER, error="L'url n'est pas conforme.")

############################################################################

@app.route('/playlist', methods=['GET'])
def playlist():
    try:
        dossier=os.path.expanduser("~/Desktop/"+USER+"_playlist")
        fichiers = [f for f in listdir(dossier) if isfile(join(dossier, f))]
        return json_response(titres=fichiers)
    except FileNotFoundError:
        return json_response(error=f"Le dossier {USER}_playlist n'existe pas.") 

############################################################################

@app.route('/playlist/<lettre>', methods=['GET'])
def playlistWithLetter(lettre):

    try:
        dossier=os.path.expanduser("~/Desktop/"+USER+"_playlist")

        if lettre == "Autres":
            fichiers = [f for f in listdir(dossier) if isfile(join(dossier, f)) and not re.search("^[a-zA-Z]", f)]
        else: 
            fichiers = [f for f in listdir(dossier) if isfile(join(dossier, f)) and f.startswith(lettre)]

        if len(fichiers)==0: raise FileNotFoundError

        return json_response(titres=fichiers, status=200)
    except FileNotFoundError:
        return json_response(error=f'Il n\'y a pas de titres dont l\'artiste commence par un "{lettre}".', status=404)    
    
############################################################################

@app.route('/dernierDl', methods=['GET'])
def dernierDl():

    if DERNIER_DL == "":
        return json_response(error='Il n\'y a pas eu de téléchargement récent.', status=404)
    else:
        dossier=os.path.expanduser("~/Desktop/"+USER+"_playlist")
        fichiers = [f for f in listdir(dossier) if isfile(join(dossier, f)) and f==DERNIER_DL]
        return json_response(titres=fichiers, status=200)
 

############################################################################

@app.route('/selectUser/<user>', methods=['GET'])
def selectUser(user: str):
    
    globals()['USER']=user
    
    return json_response(status=200)

############################################################################

@app.route('/supprimer/<titre>', methods=['GET'])
def suprimerTitre(titre: str):

    dossier=os.path.expanduser("~/Desktop/"+USER+"_playlist")  

    fichier = os.path.join(dossier,titre)

    os.remove(fichier)	
    
    return json_response(status=200)

############################################################################

@app.route('/renameFile/<nom>/<ancienNom>', methods=['GET'])
def renommerTitre(nom: str, ancienNom: str):

    dossier=os.path.expanduser("~/Desktop/"+USER+"_playlist")  

    fichier = os.path.join(dossier,ancienNom)

    newName = os.path.join(dossier,nom)

    os.rename(fichier,newName)	
    
    return json_response(status=200, nom=nom)



################################ MAIN ############################################

if __name__ == "__main__":
    app.run()
