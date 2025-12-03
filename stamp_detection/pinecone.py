from PIL import Image
from io import BytesIO
import requests
import tempfile
from custom_lib.logger import BaseLog
import torch
from pinecone import Pinecone
from api_channel.settings import PINECONE_API_KEY, PINECONE_INDEX_NAME
import datetime
import uuid 
import cv2
import time
import numpy as np
from data_extraction.apps import metaClip_preprocess, metaClip_inference 


logger = BaseLog()


device=torch.device('cuda' if torch.cuda.is_available() else "cpu")

pinecone = Pinecone(api_key=PINECONE_API_KEY)
index = pinecone.Index(PINECONE_INDEX_NAME)


def generate_embedding(image):
    """
    Generates an embedding for the given image using a pre-trained model.

    Parameters:
    - image: The input image for which the embedding will be generated.

    Returns:
    - list: The embedding of the image as a list.

    Notes:
    - Assumes the existence of a pre-trained model ('model') and a device ('device').
    - Uses 'preprocess' function to prepare the image for the model.
    - Extracts image features using the model's 'get_image_features' method.
    - Converts the image features to a list and returns it.
    """

    with torch.no_grad():
        inputs = metaClip_preprocess(images=image, return_tensors="pt").to(device)
        image_features = metaClip_inference.get_image_features(**inputs)
        return image_features.tolist()[0]



def search_similar_image(test_image_path: str, threshold):
    """
    Searches for a similar image to the given test image in a database using embeddings.

    Parameters:
    - test_image_path (str): The file path to the test image.
    - threshold: The similarity threshold below which a match is considered invalid.

    Returns:
    - dict: A dictionary containing information about the most similar image, including certainty score, company ID, and image ID.
    If the certainty score is below the specified threshold, an empty dictionary is returned.

    Notes:
    - Utilizes the 'generate_embedding' function to create an embedding for the test image.
    - Queries the database for the most similar image using the 'query' method.
    - Extracts and returns relevant information from the query results.
    """

    with Image.open(test_image_path) as img:
        embedding = generate_embedding(img)

    results = index.query(namespace="namespace", vector=embedding, top_k=1, include_values=True, include_metadata=True)

    res = {'certainty': results['matches'][0]['score'],
            'company_id': results['matches'][0]['metadata']['company_id'],
            'image_id': results['matches'][0]['id'],
            }

    return (res if results['matches'][0]['score'] >= threshold else {})



def get_top_match_company_ids(image_path, company_id, top_k=10, score_threshold=0.7):
    """
    Gets the top matching company IDs based on the similarity of the provided image with a given company ID.

    Parameters:
    - image_path (str): The file path to the image for which similarity is to be checked.
    - company_id: The company ID for which similarity is being checked.
    - top_k (int, optional): The maximum number of top matches to retrieve. Default is 10.
    - score_threshold (float, optional): The similarity score threshold below which a match is considered invalid. Default is 0.6.

    Returns:
    - tuple: A tuple containing two elements:
    - bool: True if at least one match exists, False otherwise.
    - list: The list of top matching company IDs based on similarity, filtered by the score threshold.

    Exceptions:
    - Exception: Any exception that may occur during the embedding generation, query execution, or result processing.
    """

    try:
        stripped_company_id = company_id.lstrip('0')
        embedding = generate_embedding(Image.open(image_path))
        query_response = index.query(vector=embedding, top_k=top_k, include_metadata=True, filter={"company_id": stripped_company_id}, namespace="namespace")
        matches = query_response.get("matches", [])
        existence = True if len(matches)>0 else False
        filtered_matches = [match["metadata"]["company_id"] for match in matches if match["score"] > score_threshold]
        return existence, filtered_matches[:top_k]
    except Exception as e:
        logger.print(f"error occured when get pincone simalarity: {str(e)}")
        return False, []



def get_company_id_similarity(image, bbox, for_company_id_verification=False, company_id="", threshold = 0.7):
    """
    Retrieves similarity information for a company ID within a cropped image region.

    Parameters:
    - image (Image): The input image.
    - bbox (list): A list containing bounding box coordinates (x1, y1, x2, y2, rotation, confidence).
    - for_company_id_verification (bool, optional): If True, performs company ID verification. Defaults to False.
    - company_id (str, optional): The ID of the company to verify against, used only when for_company_id_verification is True. Defaults to "".
    - threshold (float, optional): Similarity threshold for image search. Defaults to 0.7.

    Returns:
    - tuple: A tuple containing:
    - existence (bool): Indicates whether a company ID was detected.
    - filter_res (dict): A dictionary containing similarity results, either company ID matches or image search results.

    Raises:
    - Exception: If an error occurs during image processing or similarity retrieval.
    """

    try:
        image_path = get_bounding_box_image(image, bbox)

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_file_path = temp_file.name
            image_path.save(temp_file_path, format='PNG')

            if for_company_id_verification:
                existence, filter_res = get_top_match_company_ids(temp_file_path, company_id)
                return existence, filter_res

            filter_res = search_similar_image(temp_file_path, threshold = threshold)

        return False, filter_res
    except Exception as e:
        logger.print(f"Error while recognizing stamp: {str(e)}")
        return {}



def get_bounding_box_image(image_input, bbox):
    """
    Gets a cropped image using the specified bounding box from the given image input.

    Parameters:
    - image_input: The input data representing the image, which can be a file path, URL, or PIL Image.
    - bbox (list): The bounding box coordinates in the format [x_min, y_min, x_max, y_max].

    Returns:
    - PIL Image: The cropped image based on the specified bounding box.
    """

    image = get_image_from_input(image_input)
    x_min, y_min, x_max, y_max = map(int, bbox[:4])
    cropped_image = image.crop((x_min, y_min, x_max, y_max))
    return cropped_image



def get_image_from_input(input_data):
    """
    Gets an image from the given input data, which can be a file path, URL, or PIL Image.

    Parameters:
    - input_data: The input data representing the image, which can be a file path, URL, or PIL Image.

    Returns:
    - PIL Image: The image extracted from the input data.

    Notes:
    - If the input data is a string and starts with "http," it is treated as a URL, and the image is fetched using requests.
    - If the input data is a string representing a file path or a PIL Image, it is opened using the corresponding method.
    - If the input data is already a PIL Image, it is returned as is.
    """

    if isinstance(input_data, str):
        if input_data.startswith("http"):
            response = requests.get(input_data)
            image = Image.open(BytesIO(response.content))
        else:
            image = Image.open(input_data)
    else:
        image = input_data

    return image



def insert_new_stamp_image_company_name(stamp_image, company_id):
    """
    Inserts a new stamp image into a database along with the associated company ID.

    Parameters:
    - stamp_image: The image of the stamp to be inserted.
    - company_id: The ID of the company associated with the stamp.

    Returns:
    - str: The encoded ID of the inserted stamp.

    Notes:
    - The function converts the stamp image to an OpenCV format.
    - Generates a unique stamp ID using the current timestamp and the provided company ID.
    - Encodes the stamp ID using a UUID algorithm.
    - Inserts the stamp image, its embedding, and the associated company ID into the database.
    - Pauses for 15 seconds to allow time for the database operation to complete.
    - Deletes the original stamp image file.

    Exceptions:
    - Exception: Any exception that may occur during the image conversion, ID generation, database insertion, or file deletion.
    """

    img = cv2.cvtColor(np.array(Image.open(stamp_image)), cv2.COLOR_RGB2BGR)
    stamp_id = f"{company_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]}"
    encoded_stamp_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, stamp_id))
    upsert_data = [(encoded_stamp_id, generate_embedding(img), {'company_id' : str(company_id)})]
    index.upsert(vectors=upsert_data, namespace="namespace")
    time.sleep(15)
    
    return encoded_stamp_id