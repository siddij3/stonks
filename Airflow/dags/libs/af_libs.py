from google.oauth2 import service_account


def toBQ(df, project_id, table_id):
    import pandas_gbq
    import os

    path = os.path.expanduser("./dags/libs/.key")

    for filename in os.listdir(path):
        print(filename)
    credentials = service_account.Credentials.from_service_account_file(
    "./dags/libs/.key/gbp_key.json",
    )



    pandas_gbq.to_gbq(df, table_id, project_id=project_id, credentials=credentials, if_exists='append')

    return 1