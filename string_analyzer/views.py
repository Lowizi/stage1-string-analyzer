from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AnalyzedString
from .serializers import AnalyzedStringSerializer
from django.http import Http404
from django.db.models import Q

class StringsAPI(APIView):
    def post(self, request):
        serializer = AnalyzedStringSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        queryset = AnalyzedString.objects.all()
        is_palindrome = request.query_params.get('is_palindrome')
        min_length = request.query_params.get('min_length')
        max_length = request.query_params.get('max_length')
        word_count = request.query_params.get('word_count')
        contains_character = request.query_params.get('contains_character')
        if is_palindrome is not None:
            queryset = queryset.filter(is_palindrome=is_palindrome.lower() == 'true')
        if min_length is not None:
            queryset = queryset.filter(length__gte=int(min_length))
        if max_length is not None:
            queryset = queryset.filter(length__lte=int(max_length))
        if word_count is not None:
            queryset = queryset.filter(word_count=int(word_count))
        if contains_character is not None:
            queryset = queryset.filter(value__icontains=contains_character)
        serializer = AnalyzedStringSerializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'count': queryset.count(),
            'filters_applied': {k: v for k, v in request.query_params.items() if v}
        })

class GetSpecificString(APIView):
    def get(self, request, string_value):
        try:
            string = AnalyzedString.objects.get(value=string_value)
            serializer = AnalyzedStringSerializer(string)
            return Response(serializer.data)
        except AnalyzedString.DoesNotExist:
            raise Http404("String does not exist in the system")

class DeleteString(APIView):
    def delete(self, request, string_value):
        try:
            string = AnalyzedString.objects.get(value=string_value)
            string.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AnalyzedString.DoesNotExist:
            raise Http404("String does not exist in the system")
class NaturalLanguageFilter(APIView):
    def get(self, request):
        print("NaturalLanguageFilter called with query:", request.query_params.get('query'))
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
