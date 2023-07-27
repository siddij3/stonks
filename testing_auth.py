from google_auth_oauthlib import flow
from google.cloud import bigquery
import google.oauth2.credentials
import google.auth.transport.requests
import google.cloud.bigquery as bq

client = bq.Client.from_service_account_json(".key/gbp_key.json")
print(client)

query_string = """SELECT * FROM `ivory-oarlock-388916.stonks.impliedopen`"""
query_job = client.query(query_string)

results = query_job.result()  

for row in results:
    print("{}: {}".format(row.title, row.unique_words))

