from django.urls import path
from .views import Login, Register, OnlineUsers, Logout, CustomTokenRefreshView, SuggestedFriendsView


urlpatterns = [
    path('login/', Login.as_view(), name="login"),
    path('login/refresh/', CustomTokenRefreshView.as_view(), name="refresh_token"),
    path('register/', Register.as_view(), name="register"),
    path('online-users/', OnlineUsers.as_view(), name="online_users"),
    path('logout/', Logout.as_view(), name="logout"),
    path('suggested-friends/<int:user_id>/', SuggestedFriendsView.as_view(), name="suggested_friends"),
]