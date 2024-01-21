from google.cloud import contentwarehouse
from google.cloud import documentai_v1 as documentai
import os,json
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
'type':0,
'project_number':408508278168}
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= 'key.json'

# Import required libraries
from google.cloud import documentai_v1beta2 as documentai
from google.oauth2 import service_account

# Set Google Cloud credentials
credentials = service_account.Credentials.from_service_account_file('key.json')

# Set the input GCS URI of the document to process
input_uri = 'gs://zaytrics-doc-bucket/53.pdf'

# Create a Document AI client
client = documentai.DocumentUnderstandingServiceClient(credentials=credentials)

# Set the processor name
processor_name = "projects/"+config['project_id']+"/locations/"+config['location']
# +"/processors/2e1d3d05ee3b0bcf"
file=open('32.pdf','rb')
# Set the request object
request = {
    'parent':processor_name,
    'input_config': {
        # 'gcs_source': {
        #     'contents': file.read()
        # },
        'contents': file.read(),
        'mime_type': 'application/pdf'
    }
}

# Call the Document AI processor to process the document
result = client.process_document(request=request)


document_client = contentwarehouse.DocumentServiceClient()

# The full resource name of the location, e.g.:
# projects/{project_number}/locations/{location}
parent = document_client.common_location_path(
    project=config['project_number'], location=config['location']
)
print(documentai.Document.to_dict(result).keys())

# Define Document
document = contentwarehouse.Document(
    raw_document_file_type=1,
    display_name="60.pdf",
    document_schema_name="projects/408508278168/locations/us/documentSchemas/5irfnru9rntgg",
     cloud_ai_document=documentai.Document.to_dict(result)
   
)
print(document)

# Define Request
create_document_request = contentwarehouse.CreateDocumentRequest(
    parent=parent, document=document
)

# Create a Document for the given schema
response = document_client.create_document(request=create_document_request)



# import requests
# url='https://contentwarehouse.googleapis.com/v1/projects/408508278168/locations/US/documents'
# header={'Content-Type': 'application/json; charset=UTF-8'}
# data={'document': {'name':"",
#   'display_name': '32.pdf',
#   'document_schema_name': 'projects/408508278168/locations/US/documentSchemas/5irfnru9rntgg',
#   'cloud_ai_document': result,
#   }}
# response=requests.post(url,data=data,headers=header)
# print(response.json())
# # Print the text extracted from the document
# # document = result.document
# # with open('testresult.json','w') as f:
#     # json.dump(result.__str__(),f)

# # for page in document.pages:
# #     print('Page number: {}'.format(page.page_number))
# #     print('Page text:\n{}'.format(page.text))

# # request = contentwarehouse_v1.CreateDocumentRequest(
# #     parent="parent_value",
# #     document=document,
# # )
# # request = contentwarehouse.CreateDocumentRequest({
# #         'name':"projects/"+config['project_id']+"/locations/"+config['location']+"/processors/"+processor,
# #         'document':}
# #     )
# # # Make the request
# # response = client.create_document(request=request)

# # Handle the response
# # print(response)