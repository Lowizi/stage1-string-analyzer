
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import StringEntry
from .serializers import StringEntrySerializer, CreateStringSerializer
from .filters import apply_filters
from .nlp_paser import parse_natural_language

class CreateStringView(generics.CreateAPIView):
    serializer_class = CreateStringSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        entry = serializer.save()
        return Response(StringEntrySerializer(entry).data, status=status.HTTP_201_CREATED)

class GetStringView(APIView):
    def get(self, request, string_value):
        entry = get_object_or_404(StringEntry, value=string_value)
        return Response(StringEntrySerializer(entry).data, status=status.HTTP_200_OK)

class ListStringsView(APIView):
    def get(self, request):
        qs = StringEntry.objects.all()
        qs = apply_filters(qs, request.query_params)
        serializer = StringEntrySerializer(qs, many=True)
        return Response({
            "data": serializer.data,
            "count": qs.count(),
            "filters_applied": dict(request.query_params)
        })

class NaturalLanguageFilterView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response({"detail": "Query is required."}, status=400)
        try:
            filters = parse_natural_language(query)
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)

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

