import os
import re
import tempfile
import requests
import shutil
from pdf2image import convert_from_path
import cv2
import numpy as np
from stamp_detection.services import initiate_stamp_detection, document_classifer
from data_extraction.paddleocr import data_extraction_by_paddleocr, extract_shipment_number, extract_delivery_number
from custom_lib.logger import BaseLog
import time
logger = BaseLog()
from data_extraction.apps import gpu_model_pipe, cpu_model_pipe 


number_fields_dict = {
  "shipmentId": ["what is No. Embarque?", "what is Shipment Number?"],
  "deliveryId": ["what is No entrega ?", "what is Delivery Note Number?", "what is No. remission?"]
}

def initialize_number_extraction_model(image, query, device):
    """
    Initializes and utilizes the appropriate number extraction model based on the specified device.

    Parameters:
    - image (Image): The input image.
    - query (str): The query string specifying the information to extract.
    - device (str): The device to use for model execution ("gpu" or "cpu").

    Returns:
    - tuple: A tuple containing:
    - answer (str): The extracted answer from the model.
    - score (float): The confidence score associated with the answer.
    - use_model (str): The name of the model used for extraction.
    """

    if device.lower()=="gpu":
        use_model="ernie"
        response = gpu_model_pipe([{"doc": image, "prompt": query}])
        result = response[0].get('result', [])
        score = result[0].get("prob", 0)
        answer = result[0].get("value", "")

    else:
        use_model="layoutlm"
        result = cpu_model_pipe(image, query)
        score = result[0].get("score", 0)
        answer = result[0].get("answer", "")

    return answer, score, use_model if result else None


def validate_id(key, answer, model):
    """
    Validates extracted IDs based on specific rules for shipment and delivery IDs when using the CPU model.

    Parameters:
    - key (str): The key representing the type of ID (e.g., "shipmentId", "deliveryId").
    - answer (str): The extracted answer from the model.
    - model (str): The name of the model used for extraction.

    Returns:
    - bool: True if the extracted ID is valid, False otherwise.
    """

    if key == "shipmentId" and model.lower()=="cpu":
        return answer == extract_shipment_number(answer)
    elif key == "deliveryId" and model.lower()=="cpu":
        return answer == extract_delivery_number(answer)
    else:
        return True


def is_valid_answer(answer, score, results, key, model):
    """
    Checks the validity of an extracted answer based on various criteria.

    Parameters:
    - answer (str): The extracted answer to validate.
    - score (float): The confidence score associated with the answer.
    - results (dict): A dictionary containing previously extracted results, used for cross-checking IDs.
    - key (str): The key representing the type of ID (e.g., "shipmentId", "deliveryId").
    - model (str): The name of the model used for extraction.

    Returns:
    - bool: True if the answer meets all validity criteria, False otherwise.

    Criteria:
    - Confidence score must be above 0.5.
    - Answer length must be at least 7 characters.
    - Answer must contain only numbers.
    - Answer must pass validation based on specific rules for shipment and delivery IDs (via the validate_id function).
    - Delivery ID must not be identical to the extracted shipment ID (if available).
    """

    return (score > 0.9 and    
            len(answer) >= 7 and
            contains_only_numbers(answer) and
            validate_id(key, answer, model) and 
            not (key=="deliveryId" and answer==results.get("shipmentId", "")))
           

def process_queries(image, queries, key, results, device):
    """
    Processes a set of queries for number extraction from an image.

    Parameters:
    - image (Image): The input image.
    - queries (list): A list of query strings specifying the information to extract.
    - key (str): The key representing the type of ID to extract (e.g., "shipmentId", "deliveryId").
    - results (dict): A dictionary to store the extracted results.
    - device (str): The device to use for model execution ("gpu" or "cpu").

    Returns:
    - bool: True if a valid answer is found for any of the queries, False otherwise.
    """

    for query in queries:
        answer, score, use_model = initialize_number_extraction_model(image, query, device)
        if answer:
            validation_check = is_valid_answer(answer, score, results, key, device)
            logger.print(f"{use_model}: {key} --> {answer}, {validation_check}, {score}")
            if validation_check:
                results[key] = answer
                return True  
    return False


def start_number_field_extraction(image, extraction_dict, device):
    """
    Initiates the extraction of number fields from the given image using a set of predefined queries.

    Parameters:
    - image: The input image from which number fields are to be extracted.
    - extraction_dict: A dictionary containing keys representing field names and values as lists of queries for extraction.
    - device: The device information for image processing.

    Returns:
    - dict: A dictionary containing the extracted number fields, where keys are field names and values are the extracted numbers.

    Notes:
    - Assumes the existence of a function 'process_queries' for executing the extraction queries.
    - Logs the extracted results using the 'logger.print' method.

    Exceptions:
    - Exception: Any exception that may occur during the field extraction process.
    """

    results = {}

    for key, queries in extraction_dict.items():
        found_result = process_queries(image, queries, key, results, device)
        if not found_result:
            results[key] = ""

    logger.print(f"start_number_field_extraction: {results}")

    return results


def pdf_file_operation(file_path, device, is_stamp_details_required="False"):
    """
    Performs operations on a PDF file, extracting relevant data from its images.

    Parameters:
    - file_path (str): The path to the PDF file.
    - device: The device information for image processing.
    - is_stamp_details_required (str, optional): Whether stamp details are required. Default is "False".
    
    Returns:
    - list: A list containing the extracted data for each relevant image in the PDF.

    Notes:
    - Uses 'convert_from_path' function from 'pdf2image' library to convert PDF pages to images.
    - Iterates through the images, classifies them as relevant or not using 'document_classifier'.
    - If classified as relevant, extracts data from the image using 'image_file_operation'.
    - Deletes the original PDF file after processing.

    Exceptions:
    - Exception: Any exception that may occur during PDF conversion, document classification, image processing, or file deletion.
    """

    try:
        res = []

        pdf_images = convert_from_path(file_path)
        for idx, image in enumerate(pdf_images, start=1):

            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_image:
                image_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                cv2.imwrite(temp_image.name, image_cv2)

                relevancy = document_classifer(temp_image.name)
                if relevancy == "Relevant":
                    data = image_file_operation(temp_image.name, device, is_stamp_details_required, idx, False)
                    res.append(data)

        return res

    except Exception as e:
        logger.print(f"Error occurred while extracting data: {str(e)}")
        return []


def ids_extraction(image_path, device):
    """
    Extracts shipment and delivery IDs from an image using a multi-model approach.

    Parameters:
    - image_path (str): The path to the image file.
    - device (str): The device to use for model execution ("gpu" or "cpu").

    Returns:
    - dict: A dictionary containing the extracted IDs, with keys:
        - shipmentId (str): The extracted shipment ID.
        - deliveryId (str): The extracted delivery ID.

    Steps:
    1. Attempts to extract IDs using the primary number field extraction method (assumed to be LayoutLM based on context).
    2. If the primary method fails to extract any IDs, employs a secondary method (PaddleOCR) as a fallback.
    3. Returns a dictionary containing the extracted IDs and any additional information.
    """

    default_data = {
        "shipmentId": "",
        "deliveryId": "",
    }

    extracted_data = start_number_field_extraction(image_path, number_fields_dict, device)
    default_data.update(extracted_data)

    if not check_values_not_empty(extracted_data):
        logger.print(f"{device}-model failed, initiating PaddleOCR method")
        paddleocr_data = data_extraction_by_paddleocr(image_path)
        default_data.update(paddleocr_data)

    return default_data



def image_file_operation(image_path, device, is_stamp_details_required="False", page_index=1, is_image=True):
    """
    Performs operations on an image file, extracting information and optionally detecting stamps.

    Parameters:
    - image_path (str): The path to the image file.
    - device: The device information for image processing.
    - is_stamp_details_required (str, optional): Whether stamp details are required. Default is "False".
    - page_index (int, optional): The index of the page for processing. Default is 1.
    - is_image (bool, optional): Whether is the  image file or pdf file, accodingly return the data. Default is True.

    Returns:
    - list or dict: If 'is_image' is True, returns a list containing the updated data as a dictionary. If 'is_image' is False, returns the updated data as a dictionary.

    Exceptions:
    - Exception: Any exception that may occur during the image processing and operations.
    """

    try:
        start_time = time.time() 

        ids = ids_extraction(image_path, device)
        updated_data = {'page': page_index, **ids}

        if is_stamp_details_required.lower()=="true":

            stamp_data, _ = initiate_stamp_detection(image_path)
            updated_data.update(stamp_data)

        end_time = time.time() 
        duration = end_time - start_time 

        updated_data.update({"duration": duration})

        if is_image:
            return [updated_data]

        return updated_data
    
    except Exception as e:
        logger.print(f"Error occurred: {str(e)}")
        return {}



def download_store_docs(input_file, folder_name="documents"):
    """
    Downloads and stores documents from either an uploaded file or a URL.

    Parameters:
    - input_file: The file to be downloaded, either an uploaded file or a URL.
    - folder_name (str, optional): The name of the folder to store the downloaded documents. Default is "documents".

    Returns:
    - str: The path to the downloaded PDF file.

    Exceptions:
    - ValueError: Raised if the input format is invalid. Provide either an uploaded file or a URL.
    - Exception: Any other exception that may occur during the download and storage process.
    """

    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        if hasattr(input_file, 'read'):
            pdf_path = os.path.join(folder_name, input_file.name)

            with open(pdf_path, 'wb') as pdf_file:
                for chunk in input_file.chunks():
                    pdf_file.write(chunk)

        elif isinstance(input_file, str) and input_file.startswith(('https://')):
            response = requests.get(input_file)
            response.raise_for_status()

            file_name = input_file.split('/')[-1]
            pdf_path = os.path.join(folder_name, file_name)

            with open(pdf_path, 'wb') as pdf_file:
                pdf_file.write(response.content)

        else:
            raise ValueError(50015)

        return pdf_path
    
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 403:
            logger.print(f"Error: Cannot handle URL '{response.status_code}'")
            raise ValueError(50014)
        else:
            raise http_err

    except Exception as e:
        logger.print(f"Download failed: Unable to retrieve document:'{str(e)}'")
        raise ValueError(50016)


def contains_only_numbers(input_string):
    """
    Checks if the input string contains only numerical digits.

    Parameters:
    - input_string (str): The string to be checked.

    Returns:
    - bool: True if the input string contains only numerical digits; False otherwise.
    """

    pattern = re.compile(r'\D')
    return not pattern.search(input_string)



def check_values_not_empty(data):
    """
    Checks if specific keys in the given data dictionary have non-empty values.

    Parameters:
    - data (dict): A dictionary containing key-value pairs.

    Returns:
    - bool: True if all specified keys ('deliveryId', 'shipmentId') have non-empty values; False otherwise.
    """

    keys_to_check = ['deliveryId', "shipmentId"]
    return all(data.get(key) for key in keys_to_check)


def delete_path(path):
    """
    Deletes a file or directory specified by the given path.

    Parameters:
    - path (str): The path to the file or directory to be deleted.

    Notes:
    - If the path points to a file, the file will be removed.
    - If the path points to a directory, the entire directory and its contents will be recursively deleted.
    - If the specified path does not exist or is not a valid file/directory, an error message is logged.

    Exceptions:
    - OSError: If an error occurs during the deletion process, an error message with details will be logged.
    """

    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            logger.print(f"Error: '{path}' does not exist or is not a valid file/directory.")
    except OSError as e:
        logger.print(f"Error: {path} : {e.strerror}")



