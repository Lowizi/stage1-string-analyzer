from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import AnalyzedString
from .serializers import AnalyzedStringSerializer
import hashlib
from django.http import HttpResponse

class StringsAPI(APIView):
    def post(self, request):
        print("StringsAPI POST called with data:", request.data)  # Debug print
        serializer = AnalyzedStringSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                print("POST successful, returning 201")  # Debug print
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(f"POST exception: {str(e)}")  # Debug print
                return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if "value" in serializer.errors and "already exists" in str(serializer.errors["value"]):
            print("POST duplicate detected, returning 409")  # Debug print
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
        print("POST validation failed, returning 422")  # Debug print
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class StringViewSet(viewsets.ViewSet):
    lookup_field = 'string_value'  # Custom lookup field instead of pk

    def retrieve(self, request, string_value=None):
        print(f"Retrieve called with string_value: {string_value}")  # Debug print
        if not string_value:
            return Response({"detail": "String value required"}, status=status.HTTP_400_BAD_REQUEST)
        sha256_hash = hashlib.sha256(string_value.encode()).hexdigest()
        analyzed_string = AnalyzedString.objects.filter(sha256_hash=sha256_hash).first()
        if not analyzed_string:
            print("No string found, returning 404")  # Debug print
            return Response({"detail": "String does not exist in the system"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AnalyzedStringSerializer(analyzed_string)
        print("String found, returning 200")  # Debug print
        return Response(serializer.data)

    def destroy(self, request, string_value=None):
        print(f"Destroy called with string_value: {string_value}")  # Debug print
        print(f"Request method: {request.method}")  # Check the method
        if not string_value:
            return Response({"detail": "String value required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            sha256_hash = hashlib.sha256(string_value.encode()).hexdigest()
            print(f"Calculated sha256_hash: {sha256_hash}")  # Debug print
            analyzed_string = AnalyzedString.objects.filter(sha256_hash=sha256_hash).first()
            print(f"Queried analyzed_string: {analyzed_string}")  # Debug print
            if not analyzed_string:
                print("No matching string found, returning 404")  # Debug print
                return Response({"detail": "String does not exist"}, status=status.HTTP_404_NOT_FOUND)
            analyzed_string.delete()
            print("String deleted successfully")  # Debug print
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(f"Exception occurred: {str(e)}")  # Debug print
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NaturalLanguageFilter(APIView):
    def get(self, request):
        print("NaturalLanguageFilter called with query:", request.query_params.get('query'))  # Debug print
        query = request.query_params.get('query', '').lower()
        queryset = AnalyzedString.objects.all()
        parsed_filters = {}
        if 'palindromic' in query:
            queryset = queryset.filter(is_palindrome=True)
            parsed_filters['is_palindrome'] = True
        if 'single word' in query:
            queryset = queryset.filter(word_count=1)
            parsed_filters['word_count'] = 1
        serializer = AnalyzedStringSerializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'count': queryset.count(),
            'interpreted_query': {'original': query, 'parsed_filters': parsed_filters}
        })

def home(request):
    return HttpResponse("String Analyzer API")
