from tkinter import *
import sys
from PIL import Image, ImageTk
# import fnet1
import dsetc
import ssetc
import pymongo as pm

client = pm.MongoClient()
db = client['testing']
att = db['att']

def add_r(record):
    if record != -1:
        att.insert_one(record)

from Mukh.facematch import fnet

root = Tk()
root.title('SAS V0.690')
root.geometry('256x256')

name = Label(root, text="SMART ATTENDANCE SYSTEM")
name.pack(side=TOP)

init = Button(root, text="Initialize", command= lambda: dsetc.detect() or 1)
init.pack()

scan = Button(root, text="Scan", command= lambda: ssetc.scan() or 1)
scan.pack()

match = Button(root, text="Match", command= lambda: add_r(fnet.match_db('scan.jpg')) or 1)
match.pack()

quit = Button(root, text="Quit", command= sys.exit)
quit.pack()

root.mainloop()