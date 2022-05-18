
import os
import collections


class Playlist:
    
    def __init__(self, lst_videos: collections) -> None:
        self.lst_videos=lst_videos


    def creerRepertoire(user):
        if not os.path.exists(os.path.expanduser("~/Desktop/"+user+"_playlist")):
            
            os.mkdir(os.path.expanduser("~/Desktop/"+user+"_playlist"))