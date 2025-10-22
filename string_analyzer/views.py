
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.shortcuts import get_object_or_404

from .models import StringEntry
from .serializers import StringEntrySerializer, CreateStringSerializer
from .filters import apply_filters, validate_filter_params
from .nlp_paser import parse_natural_language, NaturalLanguageParseError
from rest_framework import generics
from .utils import analyze_string

class StringsCollectionView(generics.ListCreateAPIView):
    """Handles GET (list with filters) and POST (create new string).

    GET: uses `StringEntrySerializer` and supports filtering via query params
    POST: uses `CreateStringSerializer`, validates and returns 409 on duplicate
    """
    queryset = StringEntry.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateStringSerializer
        return StringEntrySerializer

    def get(self, request, *args, **kwargs):
        # validate query params and apply filters
        try:
            validated_params = validate_filter_params(request.query_params)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        qs = apply_filters(self.get_queryset(), validated_params)
        serializer = StringEntrySerializer(qs, many=True)
        return Response({
            "data": serializer.data,
            "count": qs.count(),
            "filters_applied": validated_params
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except DRFValidationError as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        value = serializer.validated_data.get('value')
        props = analyze_string(value)
        if StringEntry.objects.filter(id=props['sha256_hash']).exists():
            return Response({'detail': 'String already exists.'}, status=status.HTTP_409_CONFLICT)

        entry = serializer.save()
        return Response(StringEntrySerializer(entry).data, status=status.HTTP_201_CREATED)

class GetStringView(APIView):
    def get(self, request, string_value):
        entry = get_object_or_404(StringEntry, value=string_value)
        return Response(StringEntrySerializer(entry).data, status=status.HTTP_200_OK)

class ListStringsView(APIView):
    def get(self, request):
        qs = StringEntry.objects.all()
        # Validate query params before applying
        try:
            validated_params = validate_filter_params(request.query_params)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        qs = apply_filters(qs, validated_params)
        serializer = StringEntrySerializer(qs, many=True)
        return Response({
            "data": serializer.data,
            "count": qs.count(),
            "filters_applied": validated_params
        })

class NaturalLanguageFilterView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response({"detail": "Query is required."}, status=400)
        try:
            filters = parse_natural_language(query)
        except NaturalLanguageParseError as e:
            return Response({"detail": str(e)}, status=400)
        except ValueError as e:
            return Response({"detail": str(e)}, status=422)

        qs = apply_filters(StringEntry.objects.all(), filters)
        serializer = StringEntrySerializer(qs, many=True)
        return Response({
            "data": serializer.data,
            "count": qs.count(),
            "interpreted_query": {
                "original": query,
                "parsed_filters": filters
            }
        })

class DeleteStringView(APIView):
    def delete(self, request, string_value):
        entry = get_object_or_404(StringEntry, value=string_value)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

