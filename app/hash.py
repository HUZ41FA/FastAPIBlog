from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'])

class Hash():

    @staticmethod
    def hash_bcrypt(password):
        password = pwd_context.hash(password)
        return password