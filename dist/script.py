from tkinter import Tk, scrolledtext, Menu, filedialog, END, messagebox
from gtts import gTTS
from pygame import mixer
import speech_recognition as sr
import webbrowser
#
#def openweb()
#
def helpbox(event=None):
    webbrowser.open(url='Help\index.html')

#
def aboutme(event=None):
    webbrowser.open(url='About\index.html')


#
def speechRecognition(area):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        play("start.mp3")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        area.insert(END, text)
    except:
        play("sorry.mp3")

#
def play(music):
    mixer.init()
    mixer.music.load(music)
    mixer.music.play()

#
def fetch(txt):
    voice = gTTS(text=txt,lang="en",slow=False)
    global fileno
    music = "voice"+ str(fileno) +".mp3"
    fileno = fileno+1
    voice.save(music)
    return music

#
def startRecording(event=None):
    speechRecognition(area)


#
def checkData(event=None):
    txt = area.get('1.0', END + '-1c')
    if len(txt) <= 0:
        txt = "Nothing Entered"
    music = fetch(txt)
    play(music)

#
def createNew(event=None):
    if len(area.get('1.0', END + '-1c')) > 0:
        if messagebox.askyesno("Save", "Do you wish to save "):
            saveFile()
        else:
            area.delete('1.0', END)


#
def openFile(event=None):
    filetype = (("Text Files", "*.txt", "TEXT"), ("all files", "*.*"))
    file = filedialog.askopenfile(filetypes=filetype, initialdir="/", title="Open")

    if file != None:
        contents = file.read()
        area.insert('1.0', contents)
        file.close()


#
def saveFile(event=None):
    filetype = (("Text Files", "*.txt", "TEXT"), ("all files", "*.*"))
    file = filedialog.asksaveasfile(filetypes=filetype, initialdir="/", title="Save As")
    
    if file != None:
        data = area.get('1.0', END + '-1c')
        file.write(data)
        file.close()


#
def closeFile(event=None):
    if messagebox.askyesno("Exit", "Are you sure you want to quit"):
        root.destroy()


#
root = Tk(className=" Voise - Text Editor")
root.state('zoomed')
mainmenu = Menu(root)
root.config(menu=mainmenu)
root.bind_all('<Control-Key-n>', createNew)
root.bind_all('<Control-Key-o>', openFile)
root.bind_all('<Control-Key-s>', saveFile)
root.bind_all('<Control-Key-x>', closeFile)
root.bind_all('<Control-Key-r>', startRecording)
root.bind_all('<Control-Key-d>', checkData)

#
area = scrolledtext.ScrolledText(root)
fileno = 0

#
fileMenu = Menu(mainmenu, tearoff=False)
mainmenu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="New", command=createNew, accelerator='Ctrl + N')
fileMenu.add_command(label="Open", command=openFile, accelerator='Ctrl + O')
fileMenu.add_command(label="Save", command=saveFile, accelerator='Ctrl + S')
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=closeFile, accelerator='Ctrl + X')

#
editMenu = Menu(mainmenu, tearoff=False)
mainmenu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Start", command=startRecording, accelerator='Ctrl + R')
editMenu.add_command(label="Check", command=checkData, accelerator='Ctrl + D')

#
helpMenu = Menu(mainmenu, tearoff=False)
mainmenu.add_cascade(label="Help", menu=helpMenu)
helpMenu.add_command(label="Help",command=helpbox)
helpMenu.add_command(label="About",command=aboutme)

#
area.pack(expand=True, fill='both')
root.mainloop()
