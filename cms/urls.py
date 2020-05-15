from django.urls import path

from . import views

app_name = 'cms'

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signup/', views.UserCreate.as_view(), name='signup'),
    path('signup_confirm/',views.signup_confirm.as_view(),name='signup_confirm'),
    path('user/<int:pk>/update/', views.UserUpdate.as_view(), name='user_update'),
    path('user_detail/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('user/', views.UserList.as_view(), name='user_list'),
    path('user/<int:pk>/delete/', views.UserDelete.as_view(), name='user_delete'),
    path('password_change/',views.PasswordChange.as_view(),name='password_change'),
    path('password_change/done/',views.PasswordChangeDone.as_view(),name='password_change_done'),
]