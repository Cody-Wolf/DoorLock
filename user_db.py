import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017")

db = myclient['test']
collection = db['user']


class Device:
    def __init__(self, Name):
        self.name = Name


def encode_Device(device):
    return {'type': 'Device', 'name': device.name}


def decode_Device(document):
    return Device(document['name'])


class User:
    def __init__(self, Name, Pwd, Uid=None, Dls=None, Eml=None, Phe=None):
        self.name = Name
        self.password = Pwd
        if Dls:
            self.device_list = Dls
        else:
            self.device_list = []
        self.email = Eml
        self.phone = Phe
        self.uid = Uid


def encode_User(user):
    return {'_name': user.name, 'password': user.password, 'device_list': list(map(encode_Device, user.device_list)),
            'email': user.email, 'phone': user.phone}


def decode_User(doc):
    return User(doc['_name'], doc['password'], list(map(decode_Device, doc['device_list'])), doc['email'], doc['phone'])


def find_user(name):
    ret = collection.find_one({'_name': name})
    if ret == None:
        return None
    return decode_User(ret)


def count_user(user):
    ret = collection.find_one({'_name': user.name})
    if ret:
        return True
    return False


def creat_user(user):
    if count_user(user):
        return False
    collection.insert_one(encode_User(user))
    return True


def password_check(user):
    ret = find_user(user.name)
    if ret and ret.password == user.password:
        return True
    return False


def delete_user(user):
    if count_user(user):
        collection.delete_one({'_name': user.name})
        return True
    return False


def update_password(user, newpassword):
    if password_check(user):
        user.password = newpassword
        collection.update_one({'_name': user.name}, {'$set': encode_User(user)})
        return True
    return False


def set_email(user, email):
    if password_check(user):
        user.email = email
        collection.update_one({'_name': user.name}, {'$set': encode_User(user)})
        return True
    return False


def set_phone(user, phone):
    if password_check(user):
        user.phone = phone
        collection.update_one({'_name': user.name}, {'$set': encode_User(user)})
        return True
    return False


def add_device(user, device):
    if device in user.device_list:
        return False
    user.device_list.append(device)
    collection.update_one({'_name': user.name}, {'$set': encode_User(user)})
    return True


def del_device(user, device):
    if device in user.device_list:
        user.device_list.remove(device)
        collection.update_one({'_name': user.name}, {'$set': encode_User(user)})
        return True
    return False


def showdb():
    rets = collection.find({})
    for ret in rets:
        print(ret)
    print('^----------------------------------^')
