from rest_framework import serializers


class IsStampDetailsRequiredSerializer(serializers.Serializer):
    boolStampDetection =  serializers.BooleanField(required=False, default=False)


class LoadInvoiceSerializer(serializers.Serializer):
    files = serializers.FileField(required=False)
    url = serializers.CharField(required=False)

    def validate(self, attrs):
        files = attrs.get('files')
        url = attrs.get('url')

        if not files and not url:
            raise ValueError(50007)

        if files and url:
            raise ValueError(50001)
        
        return attrs
    

class AddStampSerializer(serializers.Serializer):
    files = serializers.FileField(required=False)
    url = serializers.CharField(required=False)
    companyId = serializers.CharField(required=True)


    def validate(self, attrs):
        files = attrs.get('files')
        url = attrs.get('url')

        if not files and not url:
            raise ValueError(50007)

        if files and url:
            raise ValueError(50001)

        return attrs
    

class AddStampDataSerializer(serializers.Serializer):
    stampId = serializers.CharField()
    comapanyId = serializers.CharField()


class AddStampResponseFormatSerializer(serializers.Serializer):
    errorCode = serializers.IntegerField()
    errorMessage = serializers.CharField()
    data = AddStampDataSerializer()



class StampVerificationSerializer(serializers.Serializer):
    files = serializers.FileField(required=False)
    url = serializers.CharField(required=False)
    companyId = serializers.CharField(required=False)

    def validate(self, attrs):
        files = attrs.get('files')
        url = attrs.get('url')

        if not files and not url:
            raise ValueError(50007)

        if files and url:
            raise ValueError(50001)

        return attrs





class StampDetailSerializer(serializers.Serializer):
    companyId = serializers.CharField()
    boundingBoxCoordinates = serializers.ListField(child=serializers.FloatField())

class DataSerializer(serializers.Serializer):
    page = serializers.IntegerField()
    shipmentId = serializers.CharField()
    deliveryId = serializers.CharField()
    stampCount = serializers.IntegerField()
    stampDetails = StampDetailSerializer(many=True)

class ResponseFormatSerializer(serializers.Serializer):
    errorCode = serializers.IntegerField()
    errorMessage = serializers.CharField()
    data = DataSerializer(many=True)



class StampVerificationDataSerializer(serializers.Serializer):
    page = serializers.IntegerField()
    comapanyMatch = serializers.BooleanField()
    boundingBoxCoordinates = serializers.ListField(child=serializers.FloatField())


class StampVerificationResponseFormatSerializer(serializers.Serializer):
    errorCode = serializers.IntegerField()
    errorMessage = serializers.CharField()
    data = StampVerificationDataSerializer()




