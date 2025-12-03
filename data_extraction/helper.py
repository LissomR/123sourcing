from data_extraction.services import pdf_file_operation, image_file_operation, delete_path
from stamp_detection.pinecone import insert_new_stamp_image_company_name
from stamp_detection.services import file_type_detection, pdf_file_operation_for_stamp_id_verification, image_file_operation_for_stamp_id_verfication
import pandas as pd
import glob
from custom_lib.logger import BaseLog
import os
import time
import paddle
logger = BaseLog()

device ="gpu" if paddle.is_compiled_with_cuda() else "cpu"
logger.print(f"Using device for Data Extraction: {device}")


def data_extraction(doc_path, is_stamp_details_required="False"):
    """
    Orchestrates the data extraction process for different file types.

    Parameters:
    - doc_path (str): The path to the document file.
    - is_stamp_details_required (str, optional): Indicates whether stamp details should be extracted (default: "False").

    Returns:
    - list or dict: The extracted data, structured as either a list (for multi-page documents) or a dictionary. The exact structure depends on the specific file operation functions called.

    Raises:
    - ValueError: If an unsupported file type is encountered.
    - Exception: If an error occurs during document processing.

    Steps:
    1. Determines the file type using `file_type_detection`.
    2. Selects the appropriate file operation function based on the file type.
    3. Calls the selected function to perform data extraction, providing the document path, model, and stamp details requirement.
    4. Returns the extracted data from the function call.
    5. Handles potential errors:
        - Raises a ValueError for unsupported file types.
        - Raises any other exceptions that occur during processing.
    """

    try:

        file_type = file_type_detection(doc_path)
        use_device = device

        file_operations = {"Image": image_file_operation, "PDF": pdf_file_operation}

        if file_type in file_operations:
            res = file_operations[file_type](doc_path, device=use_device, is_stamp_details_required= is_stamp_details_required)
            return res
        else:
            logger.print(f"Unsupported file type: {file_type}")
            raise ValueError(50007)

    except Exception as e:
        logger.print(f"Error processing document: {doc_path}")
        raise e
    
    finally:
        delete_path(doc_path)
    
    


def verifying_company(doc_path, company_id):
    """
    Verifies the company associated with a document by checking for stamp ID matches.

    Parameters:
    - doc_path (str): The path to the document file.
    - company_id (int): The ID of the company to verify.

    Returns:
    - list or dict: The verification results, structured as either a list (for multi-page documents) or a dictionary. The exact structure depends on the specific file operation functions called.

    Raises:
    - ValueError: If an unsupported file type is encountered.
    - Exception: If an error occurs during document processing.

    Steps:
    1. Determines the file type using `file_type_detection`.
    2. Selects the appropriate file operation function for stamp ID verification based on the file type.
    3. Calls the selected function to perform verification, providing the document path and company ID.
    4. Returns the verification results from the function call.
    5. Handles potential errors:
        - Raises a ValueError for unsupported file types.
        - Raises any other exceptions that occur during processing.
    """

    try:
        
        file_type = file_type_detection(doc_path)

        file_operations = {"Image": image_file_operation_for_stamp_id_verfication, "PDF": pdf_file_operation_for_stamp_id_verification}

        if file_type in file_operations:
            res = file_operations[file_type](doc_path, company_id)
            return res
        else:
            logger.print(f"Unsupported file type: {file_type}")
            raise ValueError(50007)

    except Exception as e:
        logger.print(f"Error processing document: {doc_path}")
        raise e
    
    finally:
        delete_path(doc_path)



def add_stamp(doc_path, company_id):
    """
    Adds a stamp to a document based on its file type.

    Parameters:
    - doc_path (str): The path to the document to which the stamp is to be added.
    - company_id: The ID of the company associated with the stamp.

    Returns:
    - dict: A dictionary containing the added stamp ID and associated company ID.

    Notes:
    - Uses 'file_type_detection' to determine the type of the document.
    - If the document type is 'Image', inserts a new stamp image into the database and returns the stamp ID.
    - Raises a ValueError if the document type is unsupported.

    Exceptions:
    - ValueError: Raised if the document type is unsupported or if an error occurs during stamp insertion.
    - Any other exception that may occur during file type detection or stamp insertion.
    """
    try: 

        file_type = file_type_detection(doc_path)

        if file_type == "Image":
            logger.print("Please wait for around 15 seconds")
            stamp_id = insert_new_stamp_image_company_name(doc_path, company_id)
            res = {"stampId": stamp_id, "companyId": company_id}
            return res

        else:
            raise ValueError(50008)
        
    except Exception as e:
        logger.print(f"Error processing document: {doc_path}")
        raise e
    
    finally:
        delete_path(doc_path)



def iterate_document_files(excel_file_name):
    """
    Iterates through PDF files in a specified directory, performs data extraction, and writes results to an Excel file.

    Parameters:
    - excel_file_name (str): The name of the Excel file to which the extracted data will be written.

    Notes:
    - Assumes that the PDF files are located in the "./documents" directory.
    - Uses the 'data_extraction' function for extracting data from each PDF file.
    - Logs information about the current file being processed, duration, and progress.
    - Creates a DataFrame from the extracted data and writes it to the specified Excel file.

    Exceptions:
    - Any exception that may occur during file iteration, data extraction, or Excel writing.
    """

    directory_path = "./documents"
    data = []

    pdf_files = glob.glob(os.path.join(directory_path, "*.pdf"))
    total_files = len(pdf_files)
    files_processed = 0

    for document_path in pdf_files:
        try:
            start_time = time.time() 
            logger.print(f"Current file: {document_path}")
            result = data_extraction(document_path)
            if result:
                end_time = time.time() 
                duration = end_time - start_time  
                logger.print(f"Current file: {document_path}")
                logger.print(f"Duration: {duration}")
                data.append(result)

            files_processed += 1
            logger.print(f"Processed {files_processed} out of {total_files} files.")

        except Exception as e:
            logger.print(f"Error: {str(e)}")

    df = pd.DataFrame(data)

    with pd.ExcelWriter(excel_file_name, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, sheet_name='Results', index=False)


