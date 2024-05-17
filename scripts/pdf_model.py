"""Goal is to use the pre-built read model to get text from a PDF document"""
import os
import time
import argparse
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

def analyze_read(data_file=None, output_path=None):
    # Get key, endpoint variables
    auth_dict = load_variables()
    # sample form document
    document_analysis_client = DocumentAnalysisClient(endpoint=auth_dict['endpoint'], credential=AzureKeyCredential(auth_dict['key']))

    # Read sample data from PDF
    with open(data_file, 'rb') as f:
        data = f.read()

    poller = document_analysis_client.begin_analyze_document("prebuilt-read", document=data, locale='en-US')
    result = poller.result()

    # Write full text out to text file
    with open(output_path, 'w') as f:
        f.write(result.content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data_input_file", help="PDF document to input")
    parser.add_argument("-o", "--output_path", help="Path to store OCR results")
    args = parser.parse_args()

    start = time.time()
    analyze_read(data_file=args.data_input_file, output_path=args.output_path)
    end = time.time()
    print(f"Script took {end-start} seconds.")
