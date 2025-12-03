import os
import cv2
import numpy as np
from PIL import Image
from stamp_detection.pinecone import get_company_id_similarity
from pdf2image import convert_from_path
import tempfile
from custom_lib.logger import BaseLog
from data_extraction.apps import stamp_detection_model, document_classifier_model 
logger = BaseLog()


 
def initiate_stamp_detection(image_path):
    """
    Initiates stamp detection on the given image and extracts relevant stamp details.

    Parameters:
    - image_path (str): The path to the image for stamp detection.

    Returns:
    - tuple: A tuple containing two elements:
    - dict: Combined data including the count of detected stamps and details of each stamp.
    - list: List of bounding boxes for detected stamps.

    Exceptions:
    - Exception: Any exception that may occur during stamp detection, company ID similarity check, or data extraction.
    """

    new_result = stamp_detection_model(image_path)
    
    bounding_boxes = new_result[0].boxes.data.tolist()

    filtered_bounding_boxes = [item for item in bounding_boxes if item[4] > 0.35]

    stamp_details_list = []
    for box in filtered_bounding_boxes:

        _, stamp_data = get_company_id_similarity(image_path, box[:6])

        if not stamp_data: 
            logger.print(f"Empty stamp_data for box: {box[:6]}")
            continue

        stamp_details = {
            'companyId': stamp_data.get("company_id", ""),  
            'boundingBoxCoordinates': box[:4]
        }
        stamp_details_list.append(stamp_details)
    combined_data = {
        'stampCount': len(bounding_boxes),
        'stampDetails': stamp_details_list
    }
    return combined_data, bounding_boxes


def verifying_company_id_function(image_path, company_id):
    """
    Verifies the presence and match of a company ID within an image using a stamp detection model and a company ID similarity function.

    Parameters:
    - image_path (str): The path to the image file.
    - company_id (int): The ID of the company to be verified.

    Returns:
    - dict: A dictionary containing verification results, including:
    - companyExist (bool): Indicates whether any company ID was detected in the image.
    - companyMatch (bool): Indicates whether the detected company ID matches the provided company_id.
    - boundingBoxCoordinates (list): A list of bounding box coordinates (x1, y1, x2, y2) for detected company IDs.
    """
    try: 
        new_result = stamp_detection_model(image_path)
        
        bounding_boxes = new_result[0].boxes.data.tolist()

        filtered_bounding_boxes = [item for item in bounding_boxes if item[4] > 0.35]

        company_ids = []
        bounding_boxes = []
        for box in filtered_bounding_boxes:

            existence, company_id = get_company_id_similarity(image_path, box[:6], for_company_id_verification=True, company_id=company_id)

            if company_id:

                company_ids.extend(company_id)
                bounding_boxes.append(box[:4])

        combined_data = {
            'companyExist': existence,
            'comapanyMatch': True if len(company_ids)> 0 else False,
            'boundingBoxCoordinates': bounding_boxes
        }
        return combined_data
    
    except Exception as e:
        
        logger.print("error while processing single image file", str(e))
        return {
            'companyExist': False,
            'comapanyMatch': False,
            'boundingBoxCoordinates': []
        }



def image_file_operation_for_stamp_id_verfication(image_path, company_id, page_index=1, is_image = True):
    """
    Processes an image file for stamp ID verification, extracting relevant information.

    Parameters:
    - image_path (str): The path to the image file.
    - company_id (int): The ID of the company associated with the document.
    - page_index (int, optional): The page number of the image within a multi-page document. Defaults to 1.
    - is_image (bool, optional): Flag indicating whether the input file is a standalone image or part of a larger document. Defaults to True.

    Returns:
    - list or dict: If is_image is True, returns a list containing a single dictionary with the extracted information. Otherwise, returns a dictionary directly. The structure of the dictionary is:
    - company_id (int): The ID of the company associated with the document.
    - page (int): The page number of the extracted information.
    - stamp_id (str): The extracted stamp ID (if found).
    - other_extracted_data (dict): Any other extracted information from the image.

    Raises:
    - Exception: If an error occurs while processing the image file.
    """

    try:
        res = verifying_company_id_function(image_path, company_id)

        data_dict = {"page": page_index, **res}

        if is_image:
            return [data_dict]

        return data_dict
    except Exception as e:
        logger.print("error while processing single image file", str(e))


def pdf_file_operation_for_stamp_id_verification(file_path, company_id):
    """
    Processes a PDF file for stamp ID verification, extracting relevant information from relevant pages.

    Parameters:
    file_path (str): The path to the PDF file.
    company_id (int): The ID of the company associated with the document.

    Returns:
    list: A list of dictionaries, where each dictionary contains the extracted information from a relevant page. Each dictionary contains:
    company_id (int): The ID of the company associated with the document.
    page_number (int): The page number of the extracted information.
    stamp_id (str): The extracted stamp ID (if found).
    other_extracted_data (dict): Any other extracted information from the page.

    Raises:
    ValueError: If an error occurs while processing the PDF file. 
    
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
                    res_dict = image_file_operation_for_stamp_id_verfication(temp_image.name, company_id, idx, False)  
                    res.append(res_dict) 

        return res

    except Exception as e:
        logger.print(f"Error occurred while get ids: {str(e)}")
        return []


def document_classifer(image_path):
    """
    Classifies a document based on the given image using a pre-trained document classifier model.

    Parameters:
    - image_path (str): The path to the image of the document.

    Returns:
    - str: The predicted label for the document.

    Exceptions:
    - Exception: Any exception that may occur during the document classification process.
    """

    try:
        res = document_classifier_model(image_path)
        probs = res[0].probs.data.tolist()
        label = res[0].names[np.argmax(probs)]
        return label
    
    except Exception as e:
        logger.print(f"Error occurred in document_classifer: {str(e)}")
        return ""


def binary_object_with_boxes(image, bounding_boxes):
    """
    Creates a binary object representing an image with bounding boxes drawn on it.

    Parameters:
    - image: The input image, either a file path or a PIL Image.
    - bounding_boxes (list): A list of bounding boxes to be drawn on the image.

    Returns:
    - bytes or None: If successful, returns the binary representation of the image with bounding boxes. Returns None in case of an error.

    Exceptions:
    - ValueError: Raised if the input is not a valid PIL Image or image path.
    - Exception: Any other exception that may occur during the image processing and box drawing.
    """

    try:
        if isinstance(image, str):
            original_image = cv2.imread(image)
        elif isinstance(image, Image.Image):
            original_image = np.array(image)
        else:
            raise ValueError("Input should be a PIL Image or an image path.")

        image_with_boxes = original_image.copy()
        for box in bounding_boxes:
            x_min, y_min, x_max, y_max = map(int, box[:4])
            cv2.rectangle(image_with_boxes, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2) 

        _, encoded_image = cv2.imencode('.png', image_with_boxes)
        return encoded_image.tobytes()
    
    except Exception as e:
        logger.print(f"An error occurred while creating an image with boxes: {str(e)}")
        return None


def file_type_detection(file_path):
    """
    Detects the type of file based on its extension.

    Parameters:
    - file_path (str): The path to the file.

    Returns:
    - str: The type of file ('Image', 'PDF', or 'Unknown') based on its extension.
    """

    image_extensions = ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp']
    pdf_extension = '.pdf'

    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension in image_extensions:
        return 'Image'
    elif file_extension == pdf_extension:
        return 'PDF'
    else:
        logger.print("Invalid file selection. Please choose files in supported formats, such as images or PDFs.")
        raise ValueError(50007)
    