from django.urls import path

from auth_app.views import UserDetail, UserEdit, UserEmailExixsts, UserCreate, UserLogin, UserLogout

urlpatterns = [
    path('detail/', UserDetail.as_view()),
    path('edit/', UserEdit.as_view()),
    path('emailCheck/', UserEmailExixsts.as_view()),
    path('register/', UserCreate.as_view()),
    path('login/', UserLogin.as_view(), name="login"),
    path('logout/', UserLogout.as_view()),
]