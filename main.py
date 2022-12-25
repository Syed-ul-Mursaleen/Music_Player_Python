import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from mutagen.mp3 import MP3
from pygame import mixer

window = Tk()
window.title("AMR_Music Player")
window.iconbitmap(r'mainicon.ico')
window.resizable(0, 0)
window.geometry("800x400")
mixer.init()  # initializing the mixer
# Create the menubar
MenuBar = Menu(window)
window.config(menu=MenuBar)
window.configure(background="black")
# ----------------------statusbar---------------------------

StatusBar = Label(window, text="welcome", relief=SUNKEN, anchor=W, background="black", fg="white")
StatusBar.pack(side=BOTTOM, fill=X)
# -----------------------------ends--------------------------------

leftframe = Frame(window, background='black')
leftframe.pack(side=LEFT)

Rightframe = Frame(window, background="black")
Rightframe.pack()

TopFrame = Frame(Rightframe, background="black")
TopFrame.pack()

Filelabel = Label(TopFrame, text='AMR MUSIC PLAYER!', background="black", fg="white",font =(None ,20))
Filelabel.pack()

lengthlabel = Label(TopFrame, text='Total Length : --:--', background="black", fg="white",font =(None ,14))
lengthlabel.pack(pady=5)

currenttimelabel = Label(TopFrame, text='Current Time : --:--', relief=GROOVE, background="black", fg="white",font =(None ,14))
currenttimelabel.pack()

playlistlabel = Label(leftframe, text="Playlist", fg="white", background="black",font =14)
playlistlabel.pack(padx=15)

ListLabel = Listbox(leftframe, relief=SUNKEN, fg="white", background="black", width=40, height=15)
ListLabel.pack(padx=10)
playlist = []


def Browse():
    global FileNamePath
    FileNamePath = filedialog.askopenfilename()
    AddToPlaylist(FileNamePath)


def AddToPlaylist(FileName):
    FileName = os.path.basename(FileName)
    index = 0
    ListLabel.insert(index,FileName)
    playlist.insert(index, FileNamePath)
    index += 1


def AboutUs():
    aboutwindow = Tk()
    aboutwindow.title("About us")
    aboutwindow.iconbitmap(r"mainicon.ico")
    aboutwindow.geometry('300x110')
    aboutwindow.configure(background = "black")
    aboutText = Label(aboutwindow,text="Developers",fg = "white",font = (None,20),bg = "black" )
    aboutText.pack()
    member1 = Label(aboutwindow, text="M.SyedulMursaleen  19B-009-SE", fg="white", bg="black")
    member1.pack()
    member2= Label(aboutwindow, text="Abdullah Wasim\t    19b-007-SE", fg="white", bg="black")
    member2.pack()
    member3 = Label(aboutwindow, text="Ramin Shahid\t     19B-020-SE", fg="white", bg="black")
    member3.pack()

def ContactUs():
    contactwindow = Tk()
    contactwindow.title("Contact Us")
    contactwindow.iconbitmap(r"mainicon.ico")
    contactwindow.geometry('300x110')
    contactwindow.configure(background = "black")
    ContactText = Label(contactwindow,text="Developers Contact INFO",fg = "white",font = (None,15),bg = "black" )
    ContactText.pack()
    member1 = Label(contactwindow, text="M.SyedulMursaleen  mmursaleen@students.edu.uit", fg="white", bg="black")
    member1.pack()
    member2= Label(contactwindow, text="Abdullah Wasim\t    awasim@students.uit.edu", fg="white", bg="black")
    member2.pack()
    member3 = Label(contactwindow, text="Ramin Shahid\t    rshahid@students.uit.edu ", fg="white", bg="black")
    member3.pack()


def show_details(PlayingSong):
    Filelabel['text'] = "Playing" + ' - ' + os.path.basename(PlayingSong)
    FileData = os.path.splitext(PlayingSong)

    if FileData[1] == '.mp3':
        audio = MP3(PlayingSong)
        total_length = audio.info.length
    else:
        a = mixer.Sound(PlayingSong)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()

def Del_song():
    SelectedSong = ListLabel.curselection()
    SelectedSong = int(SelectedSong[0])
    ListLabel.delete(SelectedSong)
    playlist.pop(SelectedSong)

def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    currenttime = 0
    while currenttime <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(currenttime, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            currenttime += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        StatusBar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            SelectedSong = ListLabel.curselection()
            SelectedSong = int(SelectedSong[0])
            playsong = playlist[SelectedSong]
            mixer.music.load(playsong)
            mixer.music.play()
            StatusBar['text'] = "Playing : " + os.path.basename(FileNamePath)
            show_details(playsong)
        except:
            tkinter.messagebox.showerror('File not found', 'AMR could not find the file. Please check again.')


def stop_music():
    mixer.music.stop()
    StatusBar['text'] = "Music Stopped"


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    StatusBar['text'] = "Music Paused"



def nextsong():
    try:
        stop_music()
        time.sleep(1)
        SelectedSong = ListLabel.curselection()
        SelectedSong = int(SelectedSong[0])
        SelectedSong += 1
        playsong = playlist[SelectedSong]
        mixer.music.load(playsong)
        mixer.music.play()
        StatusBar['text'] = "Playing : " + os.path.basename(playsong)
        show_details(playsong)
    except:
        tkinter.messagebox.showinfo("info","Playlist ends")

def previoussong():
    global SelectedSong
    try:
        stop_music()
        time.sleep(1)
        SelectedSong = ListLabel.curselection()
        SelectedSong = int(SelectedSong[0])
        SelectedSong -= 1
        playsong = playlist[SelectedSong]
        mixer.music.load(playsong)
        mixer.music.play()
        StatusBar['text'] = "Playing : " + os.path.basename(playsong)
        show_details(playsong)
    except:
        tkinter.messagebox.showinfo("info", "Playlist ends")
    return



def set_vol(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1


muted = FALSE


def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


def tabclosing():
    stop_music()
    window.destroy()


# -----------------------------Sub Menu--------------------------------------

SubMenu = Menu(MenuBar, tearoff=0, background="black", fg="white")

MenuBar.add_cascade(label="File", menu=SubMenu)
SubMenu.add_command(label="Open", command=Browse)
SubMenu.add_command(label="Exit", command=window.destroy)

SubMenu = Menu(MenuBar, tearoff=0, background="black", fg="white")
MenuBar.add_cascade(label="Help", menu=SubMenu)
SubMenu.add_command(label="Contact Us", command=ContactUs)
SubMenu.add_command(label="About Us", command=AboutUs)
# ---------------------------------Ends----------------------------------------

middleframe = Frame(Rightframe, background="black")
middleframe.pack(pady=50, padx=30)

AddBtn = Button(leftframe, text="Add", command=Browse ,background = "#0c50c7",fg  ="white")
AddBtn.pack(side=LEFT, padx=40, ipadx=10)

DeleteBtn = Button(leftframe, text="Delete",command = Del_song,background = "#0c50c7",fg  ="white")
DeleteBtn.pack(ipadx=10)

previousphoto = PhotoImage(file="previous.png")
previousbtn = Button(middleframe, image=previousphoto, command=previoussong,bd = 0)
previousbtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='stop.png')
stopBtn = Button(middleframe, image=stopPhoto, command=stop_music,bd = 0)
stopBtn.grid(row=0, column=1, padx=10)

playPhoto = PhotoImage(file='play.png')
playBtn = Button(middleframe, image=playPhoto, command=play_music,bd = 0)
playBtn.grid(row=0, column=2, padx=10)

pausePhoto = PhotoImage(file='pause.png')
pauseBtn = Button(middleframe, image=pausePhoto, command=pause_music,bd = 0)
pauseBtn.grid(row=0, column=3, padx=10)

nextphoto = PhotoImage(file="next.png")
nextbtn = Button(middleframe, image=nextphoto, command=nextsong,bd = 0)
nextbtn.grid(row=0, column=4, padx=10)
# Bottom Frame for volume, rewind, mute etc.

bottomframe = Frame(Rightframe, background="black")
bottomframe.pack()

mutePhoto = PhotoImage(file='mute.png')
volumePhoto = PhotoImage(file='vol.png')
volumeBtn = Button(bottomframe, image=volumePhoto, command=mute_music,bd = 0)
volumeBtn.grid(row=0, column=1)

scale = Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol,bd = 0)
scale.set(70)
scale.configure(background="black", fg="white")
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)

window.protocol("WM_DELETE_WINDOW", tabclosing)
window.mainloop()
