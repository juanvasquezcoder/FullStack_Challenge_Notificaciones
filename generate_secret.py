# generate_secret.py
import secrets

with open(".env", "a") as f:
    f.write(f"\nSECRET_KEY={secrets.token_hex(32)}\n")

print("SECRET_KEY generada y agregada a .env")