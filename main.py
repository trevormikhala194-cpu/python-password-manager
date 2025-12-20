import json
import os
from cryptography.fernet import Fernet

# -----------------------------
# FILE NAMES
# -----------------------------
DATA_FILE = "passwords.json"
KEY_FILE = "secret.key"

# -----------------------------
# GENERATE ENCRYPTION KEY
# -----------------------------
def generate_key():
    key = Fernet.generate_key()

    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

# -----------------------------
# LOAD ENCRYPTION KEY
# -----------------------------
def load_key():
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

# Create key if it doesn't exist
if not os.path.exists(KEY_FILE):
    generate_key()

key = load_key()
cipher = Fernet(key)

# -----------------------------
# LOAD PASSWORDS
# -----------------------------
def load_passwords():

    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}

# -----------------------------
# SAVE PASSWORDS
# -----------------------------
def save_passwords(passwords):

    with open(DATA_FILE, "w") as file:
        json.dump(passwords, file, indent=4)

# -----------------------------
# ADD PASSWORD
# -----------------------------
def add_password():

    website = input("Enter website/app name: ")
    username = input("Enter username/email: ")
    password = input("Enter password: ")

    encrypted_password = cipher.encrypt(
        password.encode()
    ).decode()

    passwords = load_passwords()

    passwords[website] = {
        "username": username,
        "password": encrypted_password
    }

    save_passwords(passwords)

    print("\nPassword saved successfully!")

# -----------------------------
# VIEW PASSWORDS
# -----------------------------
def view_passwords():

    passwords = load_passwords()

    if not passwords:
        print("\nNo saved passwords.")
        return

    print("\n===== SAVED PASSWORDS =====")

    for website, details in passwords.items():

        decrypted_password = cipher.decrypt(
            details["password"].encode()
        ).decode()

        print("\n---------------------------")
        print(f"Website : {website}")
        print(f"Username: {details['username']}")
        print(f"Password: {decrypted_password}")

# -----------------------------
# SEARCH PASSWORD
# -----------------------------
def search_password():

    website = input("Enter website to search: ")

    passwords = load_passwords()

    if website in passwords:

        details = passwords[website]

        decrypted_password = cipher.decrypt(
            details["password"].encode()
        ).decode()

        print("\nPassword Found")
        print("-------------------")
        print(f"Username: {details['username']}")
        print(f"Password: {decrypted_password}")

    else:
        print("\nNo password found for that website.")

# -----------------------------
# DELETE PASSWORD
# -----------------------------
def delete_password():

    website = input("Enter website to delete: ")

    passwords = load_passwords()

    if website in passwords:

        del passwords[website]

        save_passwords(passwords)

        print("\nPassword deleted successfully!")

    else:
        print("\nWebsite not found.")

# -----------------------------
# PASSWORD GENERATOR
# -----------------------------
def generate_password():

    import random
    import string

    length = int(input("Enter password length: "))

    characters = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    password = ''.join(
        random.choice(characters)
        for _ in range(length)
    )

    print(f"\nGenerated Password: {password}")

# -----------------------------
# MAIN MENU
# -----------------------------
def main():

    while True:

        print("\n==============================")
        print("     PYTHON PASSWORD MANAGER")
        print("==============================")
        print("1. Add Password")
        print("2. View Passwords")
        print("3. Search Password")
        print("4. Delete Password")
        print("5. Generate Password")
        print("6. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            add_password()

        elif choice == "2":
            view_passwords()

        elif choice == "3":
            search_password()

        elif choice == "4":
            delete_password()

        elif choice == "5":
            generate_password()

        elif choice == "6":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid option. Try again.")

# -----------------------------
# START PROGRAM
# -----------------------------
if __name__ == "__main__":
    main()