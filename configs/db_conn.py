from mongoengine import connect


def connect_db(database_name, test=False):
    try:
        if test:
            database_name = f"{database_name}Test"
            print("here")
        URI = f"mongodb+srv://tafarakasparovmhangami:tafara@cluster0.qjovi.mongodb.net/{database_name}?retryWrites=true&w=majority"
        connect(host=URI)

    except Exception as e:
        print(e)
