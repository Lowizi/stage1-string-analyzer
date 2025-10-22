from django.urls import path
from .views import (
    StringsCollectionView, GetStringView,
    NaturalLanguageFilterView, DeleteStringView
)

urlpatterns = [
    # Collection endpoint handles GET (list) and POST (create)
    path('strings/', StringsCollectionView.as_view(), name='strings-collection'),
    path('strings/filter-by-natural-language', NaturalLanguageFilterView.as_view(), name='nlp-filter'),

    # Item endpoints
    path('strings/<str:string_value>/', GetStringView.as_view(), name='get-string'),
    path('strings/<str:string_value>', DeleteStringView.as_view(), name='delete-string'),
]
