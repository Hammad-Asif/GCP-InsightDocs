import os
import json
from google.cloud import documentai_v1 as documentai
from google.cloud import storage
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= 'key.json'
config={
'project_id' : 't4-form-sample-project',
'Custom_bucket_name' : 'zaytrics-doc-bucket',
'Expense_bucket_name' : 'expense_bucket',
'invoice_bucket_name' : 'invoice_doc_bucket',
'bucket_file' : '',
'location' : 'us',
'Custom_processor_id' : '2e1d3d05ee3b0bcf',
'Expense_processor_id' : '19f428b10a5af1db',
'invoice_processor_id' : '5ad196c7d2038188',
'local_file' : '',
'type':0}
def SearchFile(config):
    storage_client = storage.Client(config['project_id'])
    if config['type']==0:
        bucket = storage_client.get_bucket(config['Custom_bucket_name'])
    elif config['type']==1:
        bucket = storage_client.get_bucket(config['Expense_bucket_name'])
    else:
        bucket = storage_client.get_bucket(config['invoice_bucket_name'])
    blobs=bucket.list_blobs() #List all objects that satisfy the filter.
    data=[]
    for blob in blobs:
        if '.json' in blob.name:
            data.append(blob.name)
            # data=json.loads(blob.download_as_string())
            # break
        # data=json.loads(blob.download_as_string())
        
    # print('downloaded')
    return {'data':data}

print(SearchFile(config))