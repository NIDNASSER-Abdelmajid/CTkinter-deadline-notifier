import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from mysql.connector import connect

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


def mysqlAction(action: int, text: str = None, date: str = None, tag: str = None):
    "1- SELECT, 2- INSERT, 3-DELETE"
    if action == 1:
        return "SELECT * FROM deadlines;"
    elif action == 2:
        return f"INSERT INTO deadlines(EVENT, deadline, tags) VALUES('{text}', '{date}', '{tag}');"
    else:
        return ""


def addToDatabase():
    text = textEntry.get()
    deadline = deadlineEntry.get()
    tag = tagEntry.get()
    cursor = mydb.cursor()
    cursor.execute(mysqlAction(2, text, deadline, tag))
    mydb.commit()
    print(cursor.rowcount, "Record inserted successfully into Laptop table")
    cursor.execute("SELECT * FROM deadlines LIMIT 10 ORDER BY deadline;")
    for event in cursor.fetchall():
        print("done")
        table.insert("", "end", value=(event[1], event[2], event[3]))
        print("done 2")
    # cursor.close()


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

# Button
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
s.theme_use("clam")
s.configure("Treeview", background="green", foreground="white", font=("Roboto", 12))
table["columns"] = ("events", "deadline", "tag")
table["show"] = "headings"

table.column("events", width=325, minwidth=325, anchor=tk.CENTER)
table.column("deadline", width=75, minwidth=75, anchor=tk.CENTER)
table.column("tag", width=50, minwidth=50, anchor=tk.CENTER)

table.heading("events", text="events", anchor=tk.CENTER)
table.heading("deadline", text="deadline", anchor=tk.CENTER)
table.heading("tag", text="tag", anchor=tk.CENTER)

table.place(x=250, y=114, anchor=tk.CENTER)

root.mainloop()
