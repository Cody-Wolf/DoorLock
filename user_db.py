import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017")

db = myclient['test1']
collection = db['user1']


class Device:
    id

    def __init__(self, iid):
        self.id = iid


def encode_Device(device):
    return {'type': 'Device', 'id': device.id}


def decode_Device(document):
    return Device(document['id'])


def add_device(id, d):
    ret = find_user(id)
    doc = encode_Device(d)
    if doc in ret['list']:
        return False
    ret['list'].append(doc)
    collection.update_one({'_id': id}, {'$set': ret})
    return True


def del_device(id, d):
    ret = find_user(id)
    doc = encode_Device(d)
    if doc in ret['list']:
        ret['list'].remove(doc)
        collection.update_one({'_id': id}, {'$set': ret})
        return True
    return False


def find_user(id):
    ret = collection.find_one({'_id': id})
    return ret


def creat_user(id, password):
    if find_user(id):
        return False
    ls = []
    collection.insert_one({'_id': id, 'password': password, 'list': ls})
    return True


def password_check(id, password):
    ret = find_user(id)
    if ret and ret['password'] == password:
        return True
    return False


def delete_user(id):
    if find_user(id):
        collection.delete_one({'_id': id})
        return True
    return False


def update_password(id, oldpassword, newpassword):
    ret = find_user(id)
    if ret == None or ret['password'] != oldpassword:
        return False
    ret['password'] = newpassword
    collection.update_one({'_id': id}, {'$set': ret})
    return True
