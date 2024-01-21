import os
import json
# import uvicorn
from flask import Flask, request, jsonify
from google.cloud import documentai_v1 as documentai
from google.cloud import storage
from flask_cors import CORS
from werkzeug.utils import secure_filename
# from fastapi.middleware.cors import CORSMiddleware
import traceback
# import ray
import asyncio
# from fastapi import FastAPI, Request, HTTPException
# from fastapi.responses import JSONResponse
# from ray import serve
# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=['*'],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
global config
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
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= 'key.json'

def upload_file(config):
    # Initialise a client
    client = storage.Client(config['project_id'])
    if config['type']==0:
        bucket = client.get_bucket(config['Custom_bucket_name'])
    elif config['type']==1:
        bucket = client.get_bucket(config['Expense_bucket_name'])
    else:
        bucket = client.get_bucket(config['invoice_bucket_name'])
    print("Uploading file")
    # Create a blob object from the filepath
    blob = bucket.blob(config['bucket_file'])
    # Upload the file to a destination
    blob.upload_from_filename(config['local_file'])
    print('file uploaded')
def ProcessFile(config):
        
    # Initialize a client
    client = documentai.DocumentProcessorServiceClient()
    print('type',config['type'])
    # Define the name of the input GCS file
    # if config['type']==0:    
    #     gcs_source_uri = 'gs://'+config['Custom_bucket_name']+'/'+config['bucket_file']
    # elif config['type']==1:
    #     gcs_source_uri = 'gs://'+config['Expense_bucket_name']+'/'+config['bucket_file']
    # else:
    #     gcs_source_uri = 'gs://'+config['invoice_bucket_name']+'/'+config['bucket_file']

    # Define the input config
    # input_config = documentai.types.BatchDocumentsInputConfig({
    #     "gcs_documents":{
    #         "documents":[{"gcs_uri":gcs_source_uri,
    #         "mime_type":"application/pdf"}]
    #     }}
    # )
    # Define the name of the output GCS file
    # if config['type']==0:    
    #     gcs_destination_uri = 'gs://'+config['Custom_bucket_name']+'/'+config['bucket_file'][:-4]+'.json'
    # elif config['type']==1:
    #     gcs_destination_uri = 'gs://'+config['Expense_bucket_name']+'/'+config['bucket_file'][:-4]+'.json'
    # else:
    #     gcs_destination_uri = 'gs://'+config['invoice_bucket_name']+'/'+config['bucket_file'][:-4]+'.json'

    # Define the output config
    # output_config = documentai.types.DocumentOutputConfig(
    #     {'gcs_output_config':{'gcs_uri':gcs_destination_uri
    #     }}
    # )
    # Define the request
    if config['type']==0:
        processor=config['Custom_processor_id']
    elif config['type']==1:
        processor=config['Expense_processor_id']
    else:
        processor=config['invoice_processor_id']
    # request = documentai.types.BatchProcessRequest({
    #     'name':"projects/"+config['project_id']+"/locations/"+config['location']+"/processors/"+processor,
    #     'input_documents':input_config,
    #     'document_output_config':output_config}
    # )

    # Process the document
    name = client.processor_path(config['project_id'], config['location'], processor)

    # Read the file into memory
    with open(config['local_file'], "rb") as image:
        image_content = image.read()
    ext=os.path.splitext(config['local_file'])
    # print(ext)
    if ext[1]==".pdf":
        mime_type='application/pdf'
    else:
        mime_type='image/'+ext[1][1:]
    # print(mime_type)
    # Load Binary Data into Document AI RawDocument Object
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name, raw_document=raw_document
    )

    result = client.process_document(request=request)
    return documentai.Document.to_dict(result.document)
    # operation = client.batch_process_documents(request=request)
    # # don't uncomment
    # response = operation.result()

def downloadFile(config,search):
    storage_client = storage.Client(config['project_id'])
    if config['type']==0:
        bucket = storage_client.get_bucket(config['Custom_bucket_name'])
    elif config['type']==1:
        bucket = storage_client.get_bucket(config['Expense_bucket_name'])
    else:
        bucket = storage_client.get_bucket(config['invoice_bucket_name'])
    if search:
        blobs=bucket.list_blobs(prefix=config['bucket_file'], delimiter='')
    else:
        blobs=bucket.list_blobs(prefix=config['bucket_file'][:-4]+'.json', delimiter='') #List all objects that satisfy the filter.
    data=''
    for blob in blobs:
        print(blob)
        data=json.loads(blob.download_as_string())
        break
    print('downloaded')
    return {'data':data}


def run(fileName):
    try:
        global config
        config['bucket_file']=fileName
        config['local_file']="./File/"+fileName
        # upload_file(config)
        data=ProcessFile(config)
        # data=downloadFile(config,False)
        return data
    except Exception as e:
        return traceback.format_exc()

def deleteFiles(fileName):
    if os.path.exists("./File/"+fileName):
        os.remove("./File/"+fileName)
# @ray.remote(num_cpus=0.3)
class GCPClass:
    def caller(self, request):
        try:
            # if not os.path.isdir("File/"):
            #     os.makedirs("File/")
            # body = asyncio.run(request.form())
            # content = asyncio.run(body['file'].read())
            # with open('File/'+body['file'].filename, 'wb') as f:
            #     f.write(content)
            # with open('PdfFile/'+body['file'].filename, 'wb') as f:
            #     f.write(content)
            pdf = request.files['file']
            fileName = secure_filename(pdf.filename)
            pdf.save('./File/'+fileName)
            frame = run(fileName)
            deleteFiles(fileName)
            return jsonify(frame)
        except Exception as ex:
            traceback.print_exc()
            return ex

@app.route("/Custom", methods=['POST'])
def Custom():
    global config
    config['type']=0
    print("custom")
    # res = GCPClass.options(name='GCPML').remote()
    # frame = ray.get(res.caller.remote(req))
    obj=GCPClass()
    frame=obj.caller(request)
    return frame

@app.route("/Expense", methods=['POST'])
def Expense():
    global config
    config['type']=1
    print("expense")
    # res = GCPClass.options(name='GCPML').remote()
    # frame = ray.get(res.caller.remote(req))
    obj=GCPClass()
    frame=obj.caller(request)
    return frame

@app.route("/invoice", methods=['POST'])
def invoice():
    global config
    config['type']=2
    print("invoice")
    # res = GCPClass.options(name='GCPML').remote()
    # frame = ray.get(res.caller.remote(req))
    obj=GCPClass()
    frame=obj.caller(request)
    return frame
@app.route("/test",methods=['GET'])
def Testing():
    return "Hello World"

@app.route("/searchInCustom",methods=['POST'])
def SearchInCsutom():
    try:
        global config
        config['type']=0
        return SearchFile(config)
    except Exception as e:
        return traceback.format_exc()

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
            data.append({"ID":blob.id,
            "Name":blob.name})
            # data=json.loads(blob.download_as_string())
            # break
        # data=json.loads(blob.download_as_string())
        
    # print('downloaded')
    return {'data':data}
@app.route("/downloadCustomFile", methods=['POST'])
def downloadCustomFile():
    try:
        global config
        config['bucket_file']=request.args.get('fileName')
        config['type']=0
        data=downloadFile(config,True)
        return data
    except Exception as e:
        return traceback.format_exc()
# app.add_api_route('/Custom', methods=["POST"], endpoint=Custom)
# app.add_api_route('/Expense', methods=["POST"], endpoint=Expense)
# app.add_api_route('/invoice', methods=["POST"], endpoint=invoice)


# @serve.deployment(route_prefix="/")
# @serve.ingress(app)
# class GCPMLWrapper:
#     pass


# try:
    # serve.run(GCPMLWrapper.bind(), host="0.0.0.0", port="8080")
    # while True:
    #     a = 0
# except Exception as e:
#     print(traceback.format_exc())
if __name__ == "__main__":
    app.run(debug=True)