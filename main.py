from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip    # Used to copy something.
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


def save():
    website = website_entry.get()
    email = email_entry.get()
    password_1 = password_entry.get()
    new_data = {
        website: {
                    "email": email,
                    "password": password_1
                 }
    }

    if len(website) == 0 or len(password_1) == 0:
        messagebox.showinfo(title="Oops!", message="Please don't leave any field empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)     # Reading the old data.
        except:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)           # Updating the old data.

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)    # Saving the updated data.
        finally:
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()


def find_password():
    website_data = website_entry.get()

    try:
        with open("data.json", "r") as data_file:
            json_data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo("Error", "No Data File Found!")
    else:
        if website_data in json_data:
            email = json_data[website_data]['email']
            password = json_data[website_data]['password']
            messagebox.showinfo(f"{website_data}", f"Email: {email}\nPassword: {password} ")
        else:
            messagebox.showinfo(f"{website_data}", f"No details for {website_data} exists!")


# ---------------------------- UI SETUP ------------------------------- #


# Window Setup.
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Canvas Setup.
canvas = Canvas(width=200, height=200)
key_img = PhotoImage(file="logo.png")
canvas.create_image(115, 100, image=key_img)
canvas.grid(row=0, column=1)

# Labels.
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries.
website_entry = Entry(width=36)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=55)
email_entry.grid(row=2, column=1, columnspan=2)

password_entry = Entry(width=36)
password_entry.grid(row=3, column=1)

# Buttons.

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=2)

add_button = Button(text="Add", width=46, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
