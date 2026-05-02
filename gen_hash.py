import subprocess, sys

try:
    import bcrypt
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "bcrypt"])
    import bcrypt

password = input("Введи пароль: ").strip()
hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))
print("\nВставь это в .env как AUTH_PASSWORD_HASH=")
print(hashed.decode("utf-8"))
