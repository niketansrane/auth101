import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hash the plaintext password using a brypt with salt.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password: str, hashed_pwd: bytes) -> bool:
    """
    Validate if the given password's hash matches with given `hashed`.
    """
    return bcrypt.checkpw(password.encode(), hashed_pwd)


if __name__ == "__main__":
    password = "ilovebooks"
    hashed_pwd = hash_password(password)
    print(hashed_pwd) # b'$2b$12$mWaihxsvGxYNwzq4Ueozu.hgvjVC5dIKFXcyeiV8iAiwTqpnOdF9y'
    print(verify_password(password, hashed_pwd)) # True
    print(verify_password("idonotlovebooks", hashed_pwd))