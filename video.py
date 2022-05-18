from pytube import YouTube
import os
import youtube_dl

class Video:

    def __init__(self, url="") -> None:
        self.url=url


    def recupVideo(url,user):

        ## AVEC PYTUBE EXTRACTION AU FORMAT MP4 UNIQUEMENT ##

        # video = YouTube(url)
        # lst_audio = video.streams.filter(only_audio=True, file_extension='mp4').order_by('abr')
        # stream = lst_audio[0]		
        # stream.download(os.path.expanduser("~/Desktop/"+user+"_playlist"))

        ## AVEC YOUTUBE_DL EXTRACTION ET CONVERTION AUTO EN MP3 (PLUS LENT) ##

        options = {
            'format':'worstaudio',
            'extractaudio':True,
            'audioformat':'mp3',
            'outtmpl': os.path.expanduser("~/Desktop/"+user+"_playlist/")+'%(title)s.%(ext)s',     
            'noplaylist':True,
            'nocheckcertificate':True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([url])
            info_dict = ydl.extract_info(url, download=False)
            return info_dict.get('title', None)
            
            