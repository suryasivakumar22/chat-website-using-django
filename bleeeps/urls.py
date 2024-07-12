from django.urls import path
from . import views
urlpatterns = [
	path('search/',views.search),
	path('searchresults/',views.searchresult),
	path('welcome/',views.empty),
	path('bleeeps/',views.bleeeps),
]