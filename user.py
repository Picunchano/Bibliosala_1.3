# user.py
import bcrypt

class Usuario:
    def __init__(self, id_usuario, username, password_hash):
        self.id_usuario = id_usuario
        self.username = username
        self.password_hash = password_hash

    @classmethod
    def crear_nuevo_usuario(cls, username, raw_password):
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return cls(None, username, hashed_password)

    def verificar_password(self, raw_password):
        if not self.password_hash:
            return False
        try:
            # Asegurarse de que ambos, el hash almacenado y la contraseña de entrada, estén codificados en bytes
            return bcrypt.checkpw(raw_password.encode('utf-8'), self.password_hash.encode('utf-8'))
        except ValueError:
            print("Error: El hash almacenado no es un hash bcrypt válido.")
            return False

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "username": self.username,
            "password_hash": self.password_hash
        }

    @staticmethod
    def hash_password(raw_password):
        return bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')