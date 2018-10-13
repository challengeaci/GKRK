import pymongo as pm
import pprint as pp
from tkinter import *

client = pm.MongoClient()
db = client['testing']
collection = db['att']

def fetch_one():
    pp.pprint(collection.find_one({"Name": name.get()}))


def fetch_all():
    # print(name.get())
    for c in collection.find({}):
        pp.pprint(c)


root = Tk()
root.title("SAS Prototype DB")
root.geometry('256x256')

name = Entry(root)
name.insert(0, 'Name')
name.pack()
name.focus()
name.bind('<Return>', (lambda event: fetch_one()))
show_one = Button(root, text="Find student", command=fetch_one)
show_one.pack()

show_all = Button(root, text='Show all', command= lambda: fetch_all() or 1)
show_all.pack(side=BOTTOM)

root.mainloop()
