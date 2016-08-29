from Tkinter import *
from os import path
from libs import process
import subprocess
import tkMessageBox
import tkFileDialog
import ttk
import Image, ImageTk


class MainFrame:
    def __init__(self, master):
        master.title("Image Processing")

        frame = Frame(master)
        frame.pack()

        src = Frame(frame)
        src.pack(side=LEFT)

        res = Frame(frame)
        res.pack(side=LEFT)

        src_label = Label(src)
        src_label.pack(side=TOP)

        res_label = Label(res)
        res_label.pack(side=TOP)

        open_button = Button(src, text="Browse", command=lambda: self.open_image(res, res_label, src_label))
        open_button.pack(side=BOTTOM)

    def good(self):
        tkMessageBox.showinfo("Success", "Recognition is good")

    def bad(self):
        tkMessageBox.showinfo("Failure", "Recognition is bad")

    def editor(self, filename):
        baseName = path.basename(filename)
        smipath = path.relpath(path.join(path.splitext(filename)[0], baseName, '.smi'))
        print smipath
        subprocess.call(['msketch', smipath])

    def open_image(self, res, res_label, src_label):
        fileName = tkFileDialog.askopenfilename()
        folder = path.split(fileName)[0]
        baseName = path.basename(fileName)
        name = path.splitext(baseName)[0]
        pngBaseName = name + '.final.png'

        srcImage = Image.open(fileName)
        tksrc = ImageTk.PhotoImage(srcImage)
        src_label.config(compound=BOTTOM, image=tksrc, text=baseName)
        src_label.image = tksrc
        top.update()
    
        size = 'png:w' + str(srcImage.size[0]) + ',h' + str(srcImage.size[1])
        process.launch_correct(fileName, size)
        pngName = path.join(folder, name, pngBaseName)
        resImage = Image.open(pngName)
        tkres = ImageTk.PhotoImage(resImage)
        res_label.config(compound=BOTTOM, image=tkres, text=pngBaseName)
        res_label.image = tkres
        top.update()

        buttonFrame = Frame(res)
        buttonFrame.pack(side=BOTTOM)

        goodButton = Button(buttonFrame, text="Good", command=self.good)
        goodButton.pack(side=LEFT)

        badButton = Button(buttonFrame, text="Bad", command=self.bad)
        badButton.pack(side=LEFT)

        editorButton = Button(buttonFrame, text="Open editor", command=lambda: self.editor(fileName))
        editorButton.pack(side=LEFT)


top = Tk()
main = MainFrame(top)
top.mainloop()
