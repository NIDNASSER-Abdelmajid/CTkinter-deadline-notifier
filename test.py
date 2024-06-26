import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from mysql.connector import connect
import time

mydb = connect(host="localhost", database="deadline", user="joyboy", password="joyboy")
cursor = mydb.cursor()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("500x500")
root.resizable(False, False)
root.title("deadline")
# icon
root.wm_iconbitmap("icon.ico")


# Select records from db
def selectF():
    cursor.execute("SELECT * FROM deadlines ORDER BY deadline LIMIT 10;")
    for event in cursor.fetchall():
        table.insert("", "end", value=(event[1], event[2], event[3]))
    # label.configure(text="10 RECORDS SELECTED!", text_color="green")


# insert record to db
def insertF(text: str, date: str, tag: str):
    cursor.execute(
        f"INSERT INTO deadlines(EVENT, deadline, tags) VALUES('{text}', '{date}', '{tag}');"
    )
    mydb.commit()
    print(cursor.rowcount, "Record inserted successfully into the table")  # delete
    label.configure(
        text=f'"{text}" RECORD INSERTED SUCCESSFULLY INTO THE TABLE.',
        text_color="yellow",
    )


# delete record from db
def deleteF():
    tag = tagDeleteEntry.get()
    cursor.execute(f"DELETE FROM deadlines WHERE tags='{tag}'")
    mydb.commit()
    label.configure(text=f'"{tag}" RECORD IS DELETED.', text_color="red")
    refresh()
    print("deleted")  # delete


# delete outdated records
def verifyValidity():
    cursor.execute(
        """
        DELETE FROM deadlines WHERE deadline <= curdate();"""
    )
    mydb.commit()


# refresh table
def refresh():
    for i in table.get_children():
        table.delete(i)
    selectF()


def addToDatabase():
    # root.update()  # delete
    tag = tagEntry.get()
    if not uTag(tag):
        text = textEntry.get()
        deadline = deadlineEntry.get()

        insertF(text, deadline, tag)
        refresh()
    else:
        print(f"the tag '{tag}' is already used!")


def uTag(tag: str = None):
    cursor.execute("SELECT tags FROM deadlines;")
    tags = cursor.fetchall()
    return tuple([tag]) in tags


# frames
titleFrame = ctk.CTkFrame(root, width=500, height=49)
titleFrame.place(relx=0.5, rely=0, anchor=tk.N)
textboxFrame = ctk.CTkFrame(root, width=500, height=42)
textboxFrame.place(relx=0.5, rely=0, y=49, anchor=tk.N)
threeboxFrame = ctk.CTkFrame(root, width=500, height=49)
threeboxFrame.place(relx=0.5, rely=0, y=91, anchor=tk.N)
tableFrame = ctk.CTkFrame(root, width=500, height=400)
tableFrame.place(relx=0.5, rely=0, y=140, anchor=tk.N)

# Title label
title = ctk.CTkLabel(master=titleFrame, text="Deadline Register", font=("Roboto", 24))
title.place(x=250, y=25, anchor=tk.CENTER)

# Entry textbox
textEntry = ctk.CTkEntry(
    textboxFrame, height=30, width=450, placeholder_text="event name", corner_radius=5
)
textEntry.place(x=250, y=21, anchor=tk.CENTER)

# Two entries + Button
deadlineEntry = ctk.CTkEntry(
    threeboxFrame, width=146, height=30, placeholder_text="YYYY-MM-DD"
)
deadlineEntry.place(x=98, y=25, anchor=tk.CENTER)

tagEntry = ctk.CTkEntry(
    threeboxFrame, width=146, height=30, placeholder_text="tags: #tagname"
)
tagEntry.place(x=250, y=25, anchor=tk.CENTER)

# submit Button
submitButton = ctk.CTkButton(
    threeboxFrame,
    width=146,
    height=30,
    text="Submit",
    fg_color="green",
    command=addToDatabase,
)
submitButton.place(x=402, y=25, anchor=tk.CENTER)

# Treeview ttk
table = ttk.Treeview(tableFrame)
s = ttk.Style(tableFrame)
s.configure("table", rowheight=40)
s.theme_use("clam")
s.configure("Treeview", background="green", foreground="white", font=("Roboto", 12))
table["columns"] = ("events", "deadline", "tag")
table["show"] = "headings"

table.column("events", width=285, minwidth=285, anchor=tk.CENTER)
table.column("deadline", width=95, minwidth=95, anchor=tk.CENTER)
table.column("tag", width=70, minwidth=70, anchor=tk.CENTER)

table.heading("events", text="events", anchor=tk.CENTER)
table.heading("deadline", text="deadline", anchor=tk.CENTER)
table.heading("tag", text="tag", anchor=tk.CENTER)

table.place(x=250, y=114, anchor=tk.CENTER)

# delete button
deleteButton = ctk.CTkButton(
    tableFrame,
    width=146,
    height=30,
    text="delete",
    fg_color="red",
    command=deleteF,
)
deleteButton.place(x=402, y=250, anchor=tk.CENTER)

# tag delete entry
tagDeleteEntry = ctk.CTkEntry(tableFrame, width=146, height=30, placeholder_text="tag")
tagDeleteEntry.place(x=250, y=250, anchor=tk.CENTER)

# query label
label = ctk.CTkLabel(tableFrame, text="", font=("Roboto", 15))
label.place(relx=0.5, y=280, anchor=tk.CENTER)


root.after_idle(verifyValidity)
root.after_idle(selectF)
# root.after_idle(uTag)

root.mainloop()
