from passlib.hash import pbkdf2_sha256
from Backend.db_model import User


def check_username(username):
    try:
        user = User.objects(username=username).first()
        if user:
            return user
    except Exception as error:
        print(error)


def hash_password(password):
    try:
        hashed_password = pbkdf2_sha256.hash(password)
        return hashed_password
    except Exception as error:
        print(error)


def verify_password(username, password):
    try:

        if not check_username(username):
            return False

        hashed_password = User.objects(username=username).first()
        if not hashed_password:
            return False
        hashed_password = hashed_password.password
        status = pbkdf2_sha256.verify(password, hashed_password)

        if status:
            return True
    except Exception as error:
        print(error)
