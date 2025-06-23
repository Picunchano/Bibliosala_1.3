# user.py
import bcrypt #

class Usuario: #
    def __init__(self, id_usuario, username, role): # Renombrado password_hash a role para claridad
        self.id_usuario = id_usuario #
        self.username = username #
        self.role = role # Ahora almacena el rol, no el hash de la contraseña

    @classmethod
    def crear_nuevo_usuario(cls, username, raw_password, role='user'): # Añadido parámetro role
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') #
        # Al crear un nuevo usuario, no se le asigna id_usuario hasta que se guarda en la DB
        # El hash de la contraseña se pasa por separado, no como un atributo del objeto Usuario si este objeto es solo para la sesión.
        # Si este método se usa para preparar un objeto antes de guardar en DB, el hash DEBE ser manejado por data_manager.
        # En este caso, el objeto Usuario en sí no necesita almacenar el password_hash, solo el data_manager lo maneja.
        # Por simplicidad y como el método está en Usuario, lo mantendremos como lo tenías, pero el 'role' es más adecuado.
        return cls(None, username, role) # El id_usuario es None hasta que se guarda en la DB.
                                            # El password_hash NO debe guardarse aquí.

    # Este método ya no es necesario en la clase Usuario si la verificación se hace en data_manager
    # def verificar_password(self, raw_password):
    #     if not self.password_hash:
    #         return False
    #     try:
    #         return bcrypt.checkpw(raw_password.encode('utf-8'), self.password_hash.encode('utf-8'))
    #     except ValueError:
    #         print("Error: El hash almacenado no es un hash bcrypt válido.")
    #         return False

    def to_dict(self): #
        return { #
            "id_usuario": self.id_usuario, #
            "username": self.username, #
            "role": self.role # Ahora se exporta el rol
        }