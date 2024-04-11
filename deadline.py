import customtkinter
from mysql.connector import connect

# database named: deadline
# table named: deadlines
mydb = connect(host="localhost", database="deadline", user="joyboy", password="joyboy")
cursor = mydb.cursor()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# General info
root = customtkinter.CTk()
root.geometry("500x500")
root.resizable(False, False)
root.title("deadline")
# icon
root.wm_iconbitmap("icon.ico")


def validEntry(text: str, date: str) -> bool:
    return True


def mysqlAction(action: int, text: str, date: str, tag: str):
    "1- SELECT, 2- INSERT, 3-DELETE"
    if action == 1:
        return "SELECT * FROM deadlines;"
    elif action == 2:
        return f"INSERT INTO deadlines(EVENT, deadline) VALUES('{text}', '{date}', '{tag}');"
    else:
        return ""


def addToDatabase() -> None:
    text = entry.get()
    date = deadline.get()
    if validEntry(text, date):
        cursor = mydb.cursor()
        cursor.execute(mysqlAction(2, text, date, tag))
        mydb.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()

    # print(f"{}: {}")


# frames
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# labels
label = customtkinter.CTkLabel(
    master=frame, text="Deadline Register", font=("Roboto", 24)
)
label.pack(pady=7, padx=10)

# entry
entry = customtkinter.CTkEntry(frame, placeholder_text="add event", width=250)
entry.pack(pady=7, padx=10)
deadline = customtkinter.CTkEntry(frame, placeholder_text="YYYY-MM-DD", width=100)
deadline.pack(anchor="n", side="left", fill="x", pady=5, padx=5)
tag = customtkinter.CTkEntry(frame, placeholder_text="tag: #taghere", width=100)
tag.pack(anchor="n", side="left", fill="x", pady=5, padx=5)

# Buttons
submitBtn = customtkinter.CTkButton(
    master=frame,
    fg_color="green",
    command=addToDatabase,
    text="Submit",
)
submitBtn.pack(anchor="n", side="left", fill="x", pady=5, padx=10)

# treeview
table = customtkinter.CTkTabview(frame)
table.pack(fill="both", pady=20, padx=10)


# label
errMsg = customtkinter.CTkLabel(
    master=frame,
    text='invalid entry, should be "YYYY-MM-DD"',
    font=("Roboto", 12),
    text_color="Red",
)
errMsg.pack(fill="both", pady=20, padx=10)

root.mainloop()
