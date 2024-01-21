from google.cloud import contentwarehouse
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
# from google.cloud import documentai_v1beta2 as documentai
# from google.oauth2 import service_account

# # Set Google Cloud credentials
# credentials = service_account.Credentials.from_service_account_file('key.json')

# # Set the input GCS URI of the document to process
# input_uri = 'gs://zaytrics-doc-bucket/53.pdf'

# # Create a Document AI client
# client = documentai.DocumentUnderstandingServiceClient(credentials=credentials)

# # Set the processor name
# processor_name = "projects/"+config['project_id']+"/locations/"+config['location']
# # +"/processors/2e1d3d05ee3b0bcf"
# file=open('32.pdf','rb')
# # Set the request object
# request = {
#     'parent':processor_name,
#     'input_config': {
#         # 'gcs_source': {
#         #     'contents': file.read()
#         # },
#         'contents': file.read(),
#         'mime_type': 'application/pdf'
#     }
# }

# Call the Document AI processor to process the document
# result = client.process_document(request=request)

# Print the text extracted from the document
# document = result.document
# with open('testresult.json','w') as f:
    # json.dump(result.__str__(),f)
# print(result)
# for page in document.pages:
#     print('Page number: {}'.format(page.page_number))
#     print('Page text:\n{}'.format(page.text))

# request = contentwarehouse_v1.CreateDocumentRequest(
#     parent="parent_value",
#     document=document,
# )
# request = contentwarehouse.CreateDocumentRequest({
#         'name':"projects/"+config['project_id']+"/locations/"+config['location']+"/processors/"+processor,
#         'document':}
#     )
# # Make the request
# response = client.create_document(request=request)

# Handle the response
# print(response)



from google.cloud import contentwarehouse

# TODO(developer): Uncomment these variables before running the sample.
# project_number = 'YOUR_PROJECT_NUMBER'
# location = 'YOUR_PROJECT_LOCATION' # Format is 'us' or 'eu'


# Create a Schema Service client
document_schema_client = contentwarehouse.DocumentSchemaServiceClient()

# The full resource name of the location, e.g.:
# projects/{project_number}/locations/{location}
parent = document_schema_client.common_location_path(
    project=config['project_number'], location=config['location']
)

# Define Schema Property of Text Type
property_definition = contentwarehouse.PropertyDefinition(
    name="address",  # Must be unique within a document schema (case insensitive)
    display_name="address",
    is_searchable=True,
    text_type_options=contentwarehouse.TextTypeOptions(),
)

# Define Document Schema Request
document_schema_request =contentwarehouse.DocumentSchema(
        
        name="projects/408508278168/locations/us/documentSchemas/5irfnru9rntgg"
    )
#  contentwarehouse.CreateDocumentSchemaRequest(
#     parent=parent,
#     document_schema=contentwarehouse.DocumentSchema(
#         display_name="5irfnru9rntgg",
#         name="5irfnru9rntgg"
#     ),
# )
# Create a Document schema
# document_schema = document_schema_client.create_document_schema(
#     request=create_document_schema_request
# )
document_schema=document_schema_client.get_document_schema(document_schema_request)


# Create a Document Service client
document_client = contentwarehouse.DocumentServiceClient()

# The full resource name of the location, e.g.:
# projects/{project_number}/locations/{location}
parent = document_client.common_location_path(
    project=config['project_number'], location=config['location']
)


# Define Document Property Value
#document_property = contentwarehouse.Property(
 #   name=document_schema.property_definitions[0].name,
#    text_values=contentwarehouse.TextArray(values=["GOOG"]),
#)

# Define Document
document = contentwarehouse.Document(
    display_name="32.pdf",
    document_schema_name=document_schema.name,
   
)

# Define Request
create_document_request = contentwarehouse.CreateDocumentRequest(
    parent=parent, document=document
)

# Create a Document for the given schema
response = document_client.create_document(request=create_document_request)

# Read the output
# print(f"Rule Engine Output: {response.rule_engine_output}")
# print(f"Document Created: {response.document}")
print(response)
