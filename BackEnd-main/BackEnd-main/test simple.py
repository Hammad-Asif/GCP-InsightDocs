from google.cloud import documentai
from google.cloud import documentai_v1 as documentai
from google.cloud import storage
import os
from google.cloud import contentwarehouse
# TODO(developer): Uncomment these variables before running the sample.
file_path = '4.pdf'
mime_type = 'application/pdf' # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
# field_mask = "text,entities,pages.pageNumber"  # Optional. The fields to return in the Document object.
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

def process_document_sample(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
    field_mask: str = None,
):
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = storage.Client(project_id)
    
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor, e.g.:
    # projects/{project_id}/locations/{location}/processors/{processor_id}
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load Binary Data into Document AI RawDocument Object
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name, raw_document=raw_document, field_mask=field_mask
    )

    result = client.process_document(request=request)
    
    # print(result.__str__)

    # # Create a Schema Service client
    # import json
    # with open('test.json','w') as f:
    #     json.dump(documentai.Document.to_dict(result.document),f)
    # # # documentai.Document.to_dict(result)
    # document_schema_client = contentwarehouse.DocumentSchemaServiceClient()

    # # The full resource name of the location, e.g.:
    # # projects/{project_number}/locations/{location}
    # parent = document_schema_client.common_location_path(
    #     project=config['project_number'], location=config['location']
    # )



    # Create a Document Service client
    document_client = contentwarehouse.DocumentServiceClient()

    # The full resource name of the location, e.g.:
    # projects/{project_number}/locations/{location}
    parent = document_client.common_location_path(
        project=config['project_number'], location=config['location']
    )
    print(type(contentwarehouse.Document))
    # print(help(contentwarehouse.Document))

    # Define Document
    document = contentwarehouse.Document()
    document.name=""
    document.display_name="4.pdf"
    document.document_schema_name="projects/408508278168/locations/us/documentSchemas/5irfnru9rntgg"
        # 'raw_document_path':"gs://zaytrics-doc-bucket/4.pdf",
    document.inline_raw_document=open('4.pdf','rb').read()
    document.cloud_ai_document=documentai.Document.to_dict(result.document).__doc__
    

    # Define Request
    create_document_request = contentwarehouse.CreateDocumentRequest(
        parent=parent, document=document
    )

    # Create a Document for the given schema
    response = document_client.create_document(request=create_document_request)
    # print(response)


res=process_document_sample(config['project_id'],config['location'],config['Custom_processor_id'],file_path,mime_type)