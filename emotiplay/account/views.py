from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    AdminCreateSerializer,
    UserUpdateSerializer,
)
from django.http import JsonResponse


# Signup View
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


# Create Admin View
class AdminCreateView(generics.CreateAPIView):
    serializer_class = AdminCreateSerializer
    permission_classes = [permissions.IsAdminUser]


# User Login can be managed with djoser or JWT views


# Retrieve a single user by ID
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# Retrieve all users
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAdminUser]


def user_list(request):
    users = User.objects.values(
        "id", "email", "first_name", "last_name"
    )  # Adjust fields as needed
    return JsonResponse(list(users), safe=False)


# Update user data
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user  # Allow users to update their own data


class UpdateUserPreferences(APIView):
    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
