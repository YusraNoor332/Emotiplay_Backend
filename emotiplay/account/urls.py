from django.urls import path
from .views import (
    UserCreateView,
    AdminCreateView,
    UserDetailView,
    UserListView,
    UserUpdateView,
    UpdateUserPreferences,
    user_list,
)

urlpatterns = [
    # User endpoints
    path("signup/", UserCreateView.as_view(), name="user-signup"),
    path("admin/signup/", AdminCreateView.as_view(), name="admin-signup"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users-all/", user_list, name="user-list-all"),
    path("user/update/", UserUpdateView.as_view(), name="user-update"),
    path(
        "update-preferences/<int:user_id>/",
        UpdateUserPreferences.as_view(),
        name="update-user-preferences",
    ),
]
