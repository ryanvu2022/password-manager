from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


def save_password():
    website = website_entry.get().capitalize()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as file:
                # Reading old data
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as file:
                # Saving updated data
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            email_entry.insert(0, "ryanvu2022@gmail.com")
            password_entry.delete(0, END)
            website_entry.focus()


def find_password():
    website = website_entry.get().capitalize()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            messagebox.showinfo(title=website, message=f"Email:          {data[website]['email']}"
                                                       f"\nPassword:   {data[website]['password']}"
                                                       f"\n"
                                                       f"\nPassword has been copied to the clipboard.")
            pyperclip.copy(data[website]['password'])
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists")
    finally:
        website_entry.delete(0, END)


def clear_entries():
    website_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=160, height=150)
locker_img = PhotoImage(file="lock.png")
canvas.create_image(96, 66, image=locker_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.config(pady=5)
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.config(pady=5)
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.config(pady=5)
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry()
website_entry.focus()
website_entry.grid(row=1, column=1, sticky="EW")

email_entry = Entry()
email_entry.insert(0, "ryanvu2022@gmail.com")
email_entry.grid(row=2, column=1, sticky="EW")

password_entry = Entry()
password_entry.grid(row=3, column=1, columnspan=2, sticky="EW")

# Buttons
search_button = Button(text="Search", command=find_password)
search_button.grid(row=1, column=2, sticky="EW")

clear_button = Button(text="Clear All", command=clear_entries)
clear_button.grid(row=2, column=2, sticky="EW")

password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(row=3, column=2, sticky="EW")

add_button = Button(text="Add", width=35, command=save_password)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

window.mainloop()
