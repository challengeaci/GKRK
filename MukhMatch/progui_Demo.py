from tkinter import *
import sys
from PIL import Image, ImageTk
import fnet
import dsetc
import ssetc
import xlwt
import xlrd

from xlwt import Workbook

wb = Workbook()
sheet1 = wb.add_sheet('Sheet1')

root = Tk()
root.title('SAS V0.690')
root.geometry('256x256')

name = Label(root, text="SMART ATTENDANCE SYSTEM")
name.pack(side=TOP)

init = Button(root, text="Initialize", command= lambda: dsetc.detect() or 1)
init.pack()

scan = Button(root, text="Scan", command= lambda: ssetc.scan() or 1)
scan.pack()

match = Button(root, text="Match", command= lambda: print(fnet.match_db('scan.jpg') or 1))
match.pack()

quit = Button(root, text="Quit", command= sys.exit)
quit.pack()

root.mainloop()