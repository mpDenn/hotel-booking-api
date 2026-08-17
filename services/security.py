from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password):
    hashed_password = pwd_context.hash(password)
    return hashed_password

def verify_password(password, hashed_password):
    verify = pwd_context.verify(password,hashed_password)

    return verify


test_hash = hash_password("test123")

print(test_hash)
print(verify_password("test123", test_hash))
print(verify_password("wrong123", test_hash))