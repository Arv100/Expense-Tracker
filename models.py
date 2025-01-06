from pymongo.mongo_client import MongoClient
from config import URI

def add_to_collection(date,description,amount,type,user):
    with MongoClient(URI, tls=True, tlsAllowInvalidCertificates=True) as client:
        db = client['Expense_tracker']
        collection = db['tracker_collection']
        collection.insert_one(
            {
                'transaction_date' : date,
                'transaction_description' : description,
                'amount' : int(amount),
                'type' : type,
                'user' : user
             }
        )

def fetch_data(**params):
    user = params.get('user',None)
    with MongoClient(URI, tls=True, tlsAllowInvalidCertificates=True) as client:
        db = client['Expense_tracker']
        collection = db['tracker_collection']
        user_filter = collection.find({"user" : user})
        data = {}
        for i,col in enumerate(user_filter):
            data[i + 1] = {
                'transaction_date' : col['transaction_date'],
                'transaction_desctiption' : col['transaction_description'],
                'amount' : int(col['amount']),
                'type' : col['type'],
            }
        return data

def register(**params):
    username = params['user']
    email = params['email']
    password = params['password']
    date = params['date']
    with MongoClient(URI, tls=True, tlsAllowInvalidCertificates=True) as client:
        db = client['Expense_tracker']
        collection = db['Credentials']
        if collection.find_one({'email' : email}):
            return False
        collection.insert_one(
            {
                'username' : username,
                'email' : email,
                'password' : password,
                'date' : date
            }
        )
        return True

def login_(**params):
    email = params['email']
    with MongoClient(URI, tls=True, tlsAllowInvalidCertificates=True) as client:
        db = client['Expense_tracker']
        collection = db['Credentials']
        user = collection.find_one({'email' : email})
        if user:
            return user
        return False


if __name__ == "__main__":
    fetch_data(user='Arvi')

