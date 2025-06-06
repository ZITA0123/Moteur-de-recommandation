import hashlib
import json
from pathlib import Path

class UserManager:
    def __init__(self):
        self.users_file = Path("data/users.json")
        self.users_file.parent.mkdir(exist_ok=True)
        if not self.users_file.exists():
            self.users_file.write_text('{}')
        self.users = self.load_users()

    def load_users(self):
        return json.loads(self.users_file.read_text())

    def save_users(self):
        self.users_file.write_text(json.dumps(self.users, indent=2))

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        if username in self.users:
            return False, "Nom d'utilisateur déjà pris"
        
        self.users[username] = {
            "password": self.hash_password(password),
            "preferences": {}
        }
        self.save_users()
        return True, "Inscription réussie"

    def verify_user(self, username, password):
        if username not in self.users:
            return False
        return self.users[username]["password"] == self.hash_password(password)

    def save_user_preferences(self, username, preferences):
        if username in self.users:
            self.users[username]["preferences"] = preferences
            self.save_users()
            return True
        return False 