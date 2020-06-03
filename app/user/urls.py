from django.urls import path
from user import views


app_name = 'user'

urlpatterns = [
    # If it matches the 1st argument it will then get passed to
    # the views which will then render the API
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me')
]
