import customtkinter
from mysql.connector import connect

# database named: deadline
mydb = connect(host="localhost", user="joyboy", password="joyboy")

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# General info
root = customtkinter.CTk()
root.geometry("500x500")
root.resizable(False, False)
root.title("deadline")


def notValidEntry():
    errMsg = customtkinter.CTkLabel(
        master=frame,
        text='invalid entry, should be "YYYY-MM-DD"',
        font=("Roboto", 12),
        text_color="Red",
    )
    errMsg.pack(before=deadline)


def addToDatabase():
    # if
    #     print("00000")
    #     label.destroy()

    notValidEntry()
    print(f"{entry.get()}: {deadline.get()}")


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
deadline.pack(pady=5, padx=10)

# Buttons
submitBtn = customtkinter.CTkButton(
    master=frame,
    fg_color="green",
    command=addToDatabase,
    text="Submit",
)
submitBtn.pack(pady=10, padx=60)

root.mainloop()
