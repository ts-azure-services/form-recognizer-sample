"""Sourced from https://learn.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/how-to-guides/use-sdk-rest-api?view=form-recog-3.0.0&preserve-view=true%3Fpivots%3Dprogramming-language-python&tabs=macOS&pivots=programming-language-python"""
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

def load_variables():
    """Load authentication details"""
    env_var=load_dotenv('./variables.env')
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

def analyze_read():
    # Get key, endpoint variables
    auth_dict = load_variables()
    # sample form document
    #formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/read.png"
    formUrl = "https://github.com/ts-azure-services/form-recognizer-sample/blob/main/data/1.png"
    formUrl = formUrl + "?raw=true"
    document_analysis_client = DocumentAnalysisClient(
        endpoint=auth_dict['endpoint'], 
        credential=AzureKeyCredential(auth_dict['key'])
    )

    poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-read", formUrl)
    #poller = document_analysis_client.begin_analyze_document("prebuilt-read", document='./data/1.png', locale='en-US')
    result = poller.result()

    print("Document contains content: ", result.content)

    for idx, style in enumerate(result.styles):
        print(
            "Document contains {} content".format(
                "handwritten" if style.is_handwritten else "no handwritten"
            )
        )

    for page in result.pages:
        print("----Analyzing Read from page #{}----".format(page.page_number))
        print(
            "Page has width: {} and height: {}, measured with unit: {}".format(
                page.width, page.height, page.unit
            )
        )

        for line_idx, line in enumerate(page.lines):
            print(
                "...Line # {} has text content '{}' within bounding box '{}'".format(
                    line_idx,
                    line.content,
                    format_polygon(line.polygon),
                )
            )

        for word in page.words:
            print(
                "...Word '{}' has a confidence of {}".format(
                    word.content, word.confidence
                )
            )

    print("----------------------------------------")

if __name__ == "__main__":
    analyze_read()
