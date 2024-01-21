import os
import json
from flask import Flask, request, jsonify
from google.cloud import documentai_v1 as documentai
from google.cloud import storage
from flask_cors import CORS
from werkzeug.utils import secure_filename
# from fastapi.middleware.cors import CORSMiddleware
import traceback
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

def ProcessFile(config):
        
    # Initialize a client
    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(config['project_id'], config['location'], '8078b61b2db96401')

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
            pdf = request.files['file']
            fileName = secure_filename(pdf.filename)
            pdf.save('./File/'+fileName)
            frame = run(fileName)
            deleteFiles(fileName)
            return jsonify(frame)
        except Exception as ex:
            traceback.print_exc()
            return ex

@app.route("/OCR", methods=['POST'])
def OCR():
    global config
    print("custom")
    # res = GCPClass.options(name='GCPML').remote()
    # frame = ray.get(res.caller.remote(req))
    obj=GCPClass()
    frame=obj.caller(request)
    return frame

if __name__ == "__main__":
    app.run(debug=True)