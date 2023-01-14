"""Sourced from https://learn.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/how-to-guides/use-sdk-rest-api?view=form-recog-3.0.0&preserve-view=true%3Fpivots%3Dprogramming-language-python&tabs=macOS&pivots=programming-language-python"""
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

def load_variables():
    """Load authentication details"""
    load_dotenv('./variables.env')
    auth_dict = {"resource":os.environ['COG_RESOURCE'],
                 "key":os.environ['COG_KEY'],
                 "endpoint":os.environ['ENDPOINT'],
                 "location":os.environ['LOCATION'],
                 }
    return auth_dict

# formatting function
def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in polygon])

def analyze_read(page_number=None):
    # Get key, endpoint variables
    auth_dict = load_variables()
    # sample form document
    #formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/read.png"
    formUrl = f"https://github.com/ts-azure-services/form-recognizer-sample/blob/main/data/{page_number}.png"
    formUrl = formUrl + "?raw=true"
    document_analysis_client = DocumentAnalysisClient(
        endpoint=auth_dict['endpoint'], 
        credential=AzureKeyCredential(auth_dict['key'])
    )

    poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-read", formUrl)
    result = poller.result()
    return result.content
    #print("Document contains content: ", result.content)

if __name__ == "__main__":
    page_numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    #page_numbers = [1, 2]#test
    complete_memo = ""
    for page in page_numbers:
        text = analyze_read(page)
        complete_memo += text

    # Write out full memo
    with open('./outputs/complete_memo.txt', 'w') as f:
        f.write(complete_memo)
