import mongoengine


def connect_db(test=False):
    try:
        database_name = "busSystemDSA"
        if test:
            database_name = f"{database_name}Test"

        URI = f"mongodb+srv://tafarakasparovmhangami:tafara@cluster0.qjovi.mongodb.net/{database_name}?retryWrites=true&w=majority"
        mongoengine.register_connection(alias="busSystem", name=database_name, host=URI)
        print("working")
    except Exception as e:
        print(e)


