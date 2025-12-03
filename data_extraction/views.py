from data_extraction.services import download_store_docs
from custom_lib.api_view_class import AuthAPIView
from rest_framework.response import Response
from data_extraction.serializer import LoadInvoiceSerializer,ResponseFormatSerializer, AddStampSerializer, StampVerificationSerializer, StampVerificationResponseFormatSerializer, IsStampDetailsRequiredSerializer, AddStampResponseFormatSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from custom_lib.helper import create_swagger_params
from data_extraction.helper import data_extraction, add_stamp, verifying_company, iterate_document_files

class DataExtraction(AuthAPIView):
    parser_classes = (MultiPartParser,)
    @swagger_auto_schema(
            tags=['Data - Extraction'],
            manual_parameters=[create_swagger_params('Authorization',extra={"default":'Bearer XXXX'})],
            request_body=LoadInvoiceSerializer,
            query_serializer=IsStampDetailsRequiredSerializer,
            operation_id="DATA EXTRACTION API",
            security=[],
            responses={200: ResponseFormatSerializer, 401: 'Unauthorized', 400: 'Bad Request'}
        )

    def post(self,request):
            
        serializer = LoadInvoiceSerializer(data=request.data)

        if not serializer.is_valid():
            raise ValueError(50002)
        
        data = serializer.validated_data
        file_or_url = data.get('files') or data.get('url')
        stamp = request.query_params.get('boolStampDetection') or "False"

        doc_path = download_store_docs(file_or_url)
        res = data_extraction(doc_path, is_stamp_details_required=stamp)
        
        return Response(res, status=200)
    

class AddStamp(AuthAPIView):
    parser_classes = (MultiPartParser,)
    @swagger_auto_schema(
            tags=['Add-Stamp'],
            manual_parameters=[create_swagger_params('Authorization',extra={"default":'Bearer XXXX'})],
            request_body=AddStampSerializer,
            operation_id="ADD STAMP API",
            security=[],
            responses={200: AddStampResponseFormatSerializer, 401: 'Unauthorized', 400: 'Bad Request'}
        )

    def post(self,request):
            
        serializer = AddStampSerializer(data=request.data)

        if not serializer.is_valid():
            raise ValueError(50002)
        
        data = serializer.validated_data
        file_or_url = data.get('files') or data.get('url')
        company_id = data.get('companyId')

        doc_path = download_store_docs(file_or_url)

        res = add_stamp(doc_path, company_id)
        
        return Response(res, status=200)
    

class VerificationStamp(AuthAPIView):
    parser_classes = (MultiPartParser,)
    @swagger_auto_schema(
            tags=['Stamp Verification'],
            manual_parameters=[create_swagger_params('Authorization',extra={"default":'Bearer XXXX'})],
            request_body=StampVerificationSerializer,
            operation_id="STAMP VERIFICATION API",
            security=[],
            responses={200: StampVerificationResponseFormatSerializer, 401: 'Unauthorized', 400: 'Bad Request'}
        )

    def post(self,request):
            
        serializer = StampVerificationSerializer(data=request.data)

        if not serializer.is_valid():
            raise ValueError(50002)
        
        data = serializer.validated_data
        file_or_url = data.get('files') or data.get('url')
        company_id = data.get("companyId")

        doc_path = download_store_docs(file_or_url)

        res = verifying_company(doc_path, company_id)

        return Response(res, status=200)


