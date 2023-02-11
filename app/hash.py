from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'])

class Hash():

    @staticmethod
    def hash_bcrypt(password) -> str:
        password = pwd_context.hash(password)
        return password

    # @staticmethod
    # def verify(password,hash_password) -> bool:
    #     return pwd_context.verify(password, hash_password)