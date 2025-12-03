import re
from custom_lib.logger import BaseLog
logger = BaseLog()
from data_extraction.apps import ocr_inference 


def data_extraction_by_paddleocr(image):
    """
    Performs data extraction using the PaddleOCR library on the given image.

    Parameters:
    - image: The input image for text extraction using PaddleOCR.

    Returns:
    - dict: A dictionary containing extracted shipment and delivery IDs.

    Notes:
    - Utilizes the 'ocr' function from PaddleOCR to extract text from the image.
    - Processes the OCR result to concatenate the recognized words into text.
    - Calls functions ('extract_shipment_number' and 'extract_delivery_number') to extract shipment and delivery IDs.
    - Logs the extracted data using 'logger.print'.

    Exceptions:
    - Exception: Any exception that may occur during OCR, text processing, or ID extraction.
    """

    try:
        result = ocr_inference.ocr(image)
        text = '\n'.join([word[1][0] for line in result for word in line])
        embarque_number = extract_shipment_number(text)
        entrega_number = extract_delivery_number(text)
        response = {"shipmentId": embarque_number, "deliveryId": entrega_number}
        logger.print(f"regex: {response}")
        return response
    except Exception as e:
        logger.print(f"error in paddleocr: {str(e)}")



def extract_pattern(data, target_pattern, prefix_zeros=0):
    """
    Extracts a pattern with a specified target pattern and optional prefix zeros from the given data.

    Parameters:
    - data (list): The list of potential matches where the pattern is to be extracted.
    - target_pattern (str): The target pattern to be extracted.
    - prefix_zeros (int, optional): The maximum number of prefix zeros allowed in the extracted pattern. Default is 0.

    Returns:
    - str: The extracted pattern.

    Notes:
    - Combines the target pattern with a regular expression for optional prefix zeros.
    - Finds potential matches in the input data and returns the first match with at least 7 characters.
    - If no suitable match is found, returns an empty string.
    """

    combined_pattern = fr'\b0{{0,{prefix_zeros}}}{target_pattern}\d*\b'
    matches = re.findall(combined_pattern, ' '.join(data)) 
    
    for result in matches:
        if len(result) >= 7:
            return result
    
    return ""



def extract_shipment_number(data):
    """
    Extracts a shipment number from a given text string, applying specific rules and validation.

    Parameters:
    - data (str): The text string from which to extract the shipment number.

    Returns:
    - str: The extracted shipment number if found and valid, otherwise an empty string.

    Steps:
    1. Performs a preliminary check using `shipment_number_check` to determine if the text is likely to contain a shipment number. Returns an empty string if not.
    2. Applies a regular expression pattern (`r'\b\d*47\d*\b'`) to match potential shipment numbers containing the digits "47".
    3. Extracts the shipment number using the `extract_pattern` function (details of this function's logic are not provided).
    4. Validates the extracted number:
        - Ensures it has a minimum length of 7 characters.
        - If valid, returns the extracted shipment number.
        - Otherwise, returns an empty string.
    """

    if not shipment_number_check(data):
        return ""

    combined_pattern = r'\b\d*47\d*\b'
    matches = re.findall(combined_pattern, data)
    
    shipment_id = extract_pattern(matches, '47', prefix_zeros=2)

    return shipment_id if len(shipment_id) >= 7 else ""



def extract_delivery_number(data):
    """
    Extracts a delivery number from the given data using a regular expression pattern.

    Parameters:
    - data (str): The input data from which the delivery number is to be extracted.

    Returns:
    - str: The extracted delivery number.

    Notes:
    - Uses a regular expression pattern to find potential matches in the input data.
    - Extracts the delivery number based on the pattern and a specified prefix ('85').
    - If the extracted delivery number has less than 7 characters, falls back to an alternative extraction method ('extract_delivery_number_820_match').

    Exceptions:
    - Assumes the existence of a function 'extract_pattern' for further processing.
    - Any exception that may occur during the pattern matching or alternative extraction.
    """

    pattern = r'\b\d*85\d*\b'
    matches = re.findall(pattern, data)

    delivery_id = extract_pattern(matches, '85', prefix_zeros=1)

    return delivery_id if len(delivery_id) >= 7 else extract_delivery_number_820_match(data)



def extract_delivery_number_820_match(text):
    """
    Fallback method to extract a delivery number using alternative patterns for the '820' prefix.

    Parameters:
    - text (str): The input text from which the delivery number is to be extracted.

    Returns:
    - str: The extracted delivery number based on the alternative patterns.

    Notes:
    - Uses two regular expression patterns to find potential matches in the input text, one for exactly 10 digits and another for any number of digits after '820'.
    - If matches are found, returns the first match with at least 7 characters.
    - If no suitable match is found, returns an empty string.
    """

    pattern_10_digits = r"\b820\d{7}\b"
    pattern_other_digits = r"\b820\d+\b"

    matches = re.findall(pattern_10_digits + "|" + pattern_other_digits, text)

    if matches:
        first_match = matches[0]
        if len(first_match) >= 7:
            return first_match

    return ""



def shipment_number_check(text):
    """
    Checks if the given text is likely a shipment number.

    Args:
        text (str): The text to check.

    Returns:
        bool: True if the text is likely a shipment number, False otherwise.
    """

    first_300_character = text[:300]
    pattern = r'Orde'
    matches = re.findall(pattern, first_300_character)
    if matches:
      return False
    else:
      return True