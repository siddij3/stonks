
# import google.auth.transport.requests
# import google.cloud.bigquery as bq

# client = bq.Client.from_service_account_json(".key/gbp_key.json")
# print(client)

# query_string = """SELECT * FROM `ivory-oarlock-388916.stonks.impliedopen`"""
# query_job = client.query(query_string)

# results = query_job.result()  




from google.oauth2 import service_account
import pandas_gbq


credentials = service_account.Credentials.from_service_account_file(
   ".key/gbp_key.json",
)
sql = """SELECT * FROM `ivory-oarlock-388916.stonks.impliedopen`"""

df = pandas_gbq.read_gbq(sql, project_id="ivory-oarlock-388916", credentials=credentials)

for row in df:
    print(row)