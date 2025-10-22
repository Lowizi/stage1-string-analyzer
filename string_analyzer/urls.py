from django.urls import path
from .views import (
    StringsCollectionView, ItemDetailView,
    NaturalLanguageFilterView
)

urlpatterns = [
    # Collection endpoint handles GET (list) and POST (create)
    # Collection: accept both '/strings' and '/strings/'
    path('strings/', StringsCollectionView.as_view(), name='list-strings'),
    path('strings', StringsCollectionView.as_view(), name='create-string'),
    path('strings/filter-by-natural-language', NaturalLanguageFilterView.as_view(), name='nlp-filter'),

    # Item endpoints
    # Item endpoints: accept both trailing slash and no-slash variants
    path('strings/<str:string_value>/', ItemDetailView.as_view(), name='get-string'),
    path('strings/<str:string_value>', ItemDetailView.as_view(), name='delete-string'),
]
