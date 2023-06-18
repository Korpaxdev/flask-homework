import bcrypt


def hash_psw(password):
    password = str(password)
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password, hashed_password):
    password = str(password)
    if isinstance(hashed_password, bytes):
        return bcrypt.checkpw(password.encode(), hashed_password)
    else:
        hashed_password = str(hashed_password).encode()
        return bcrypt.checkpw(password.encode(), hashed_password)
