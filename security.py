from werkzeug.security import safe_str_cmp # just a safe way to compare strings compatiable with older python versions or other caracter formas ACSII, UNICODE etc
from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username) # Same as username_mapping[username] but we can give a default if none is found
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
