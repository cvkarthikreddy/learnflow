import os
import json
import base64
import random
import string
from cryptography.fernet import Fernet
from getpass import getpass

def generate_key():
    return Fernet.generate_key()

def load_or_create_key():
    key_file = 'secret.key'
    if os.path.exists(key_file):
        with open(key_file, 'rb') as file:
            return file.read()
    else:
        key = generate_key()
        with open(key_file, 'wb') as file:
            file.write(key)
        return key
key = load_or_create_key()
cipher = Fernet(key)
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))
def store_password(category, name, password):
    encrypted_password = cipher.encrypt(password.encode())
    if os.path.exists('passwords.json'):
        with open('passwords.json', 'r') as file:
            data = json.load(file)
    else:
        data = {}

    if category not in data:
        data[category] = {}
    data[category][name] = base64.urlsafe_b64encode(encrypted_password).decode()

    with open('passwords.json', 'w') as file:
        json.dump(data, file, indent=4)
def retrieve_password(category, name):
    if not os.path.exists('passwords.json'):
        print("No passwords stored.")
        return None

    with open('passwords.json', 'r') as file:
        data = json.load(file)

    try:
        encrypted_password = base64.urlsafe_b64decode(data[category][name])
        return cipher.decrypt(encrypted_password).decode()
    except KeyError:
        print("Password not found.")
        return None

def main():
    while True:
        print("\nPassword Manager")
        print("1. Generate a Password")
        print("2. Store a Password")
        print("3. Retrieve a Password")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            length = int(input("Enter the length of the password: "))
            print("Generated Password:", generate_password(length))
        elif choice == '2':
            category = input("Enter the category (e.g., Social Media, Email): ")
            name = input("Enter the name or service (e.g., Facebook, Gmail): ")
            password = getpass("{don't worry your password won't visiable when your entering your pass just click enter }Enter the password: ")
            store_password(category, name, password)
            print("Password stored successfully.")
        elif choice == '3':
            category = input("Enter the category: ")
            name = input("Enter the name or service: ")
            password = retrieve_password(category, name)
            if password:
                print("Retrieved Password:", password)
        elif choice == '4':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
