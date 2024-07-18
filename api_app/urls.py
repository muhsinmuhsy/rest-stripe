from django.urls import path
from . import views
urlpatterns = [
    path('', views.IndexView.as_view()),
    # path('api/create-customer/', views.CreateCustomerView.as_view(), name='create-customer'),
    path('api/create-subscription/', views.CreateSubscriptionView.as_view(), name='create-subscription'),
]


