from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
import os
import hashlib


class MessageEncryptionApp:
    def __init__(self, password):

        self.key = self.derive_key(password)

        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def derive_key(self, password):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,  # Adjust the number of iterations as needed
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        return key

    def private_key_to_10_digits(private_key):
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        sha256 = hashlib.sha256()
        sha256.update(private_key_bytes)

        # Extract the first 10 digits of the hash
        result = int(sha256.hexdigest()[:10], 16)

        return result

    def encrypt_message(self, message):
        msg_bytes = message.encode("utf-8")

        ciphertext = self.public_key.encrypt(
            msg_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        with open("enc", "wb") as file:
            file.write(ciphertext)
        return ciphertext

    def decrypt(self, em=""):
        with open("enc", "rb") as file:
            ct = file.read()
        # Use the derived key for decryption
        decrypted_message = self.private_key.decrypt(
            ct,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_message.decode('utf-8')


if __name__ == "__main__":
    password = "your_password"  # Replace with the actual password
    message_app = MessageEncryptionApp(password)

    original_message = "Hello, this is a secret message!"

    # Encrypt the message
    encrypted_message = message_app.encrypt_message(original_message)
    print(f"Encrypted Message: {encrypted_message.hex()}")

    dm = message_app.decrypt()
    print(f"Decrypted Message: {dm}")
