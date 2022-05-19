from cryptography.fernet import Fernet
import os


def get_password(key_file_path, enc_pass_path):
    try:
        with open(key_file_path, "r") as f:
            key = f.readline().encode()
    except Exception as e:
        raise e

    try:
        with open(enc_pass_path, "r") as f:
            enc_pass = f.readline().encode()
    except Exception as e:
        raise e
    
    fernet = Fernet(key)
    return fernet.decrypt(enc_pass).decode()


def write_key(key_file):
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open(key_file, "wb") as key_file:
        key_file.write(key)


def load_key(key_file):
    """
    Loads the key from the current directory named `key.key`
    """
    return open(key_file, "rb").read()


# Generate key
if __name__ == "__main__":
    key_file = "app/passwords/key.key"
    if not os.path.exists(key_file):
        print(f"Writing Key... to {key_file}")
        write_key(key_file)
    else:
      print(f"Not writing new key because it already exists at {key_file}")
    key = load_key(key_file)
    f = Fernet(key)
    password = "YOUR_PASSWORD"
    encrypted = f.encrypt(password.encode()).decode()
    enc_pass_file = "app/passwords/encrypted_pass.txt"
    if not os.path.exists(enc_pass_file):
        with open(enc_pass_file, "w") as file:
            print(f"Writing encrypted password to {enc_pass_file}")
            file.write(encrypted)
    else:
      print(f"Not writing new encrypted password because it already exists at {enc_pass_file}")

