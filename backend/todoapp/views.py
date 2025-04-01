from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, TodoSerializer
from .models import Todo

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data
            })
        else:
            return Response({'detail: Invalid credentials'})

class DashboardView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)
        return Response({
            'message': 'Welcome to dashboard',
            'user': user_serializer.data
        }, 200)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_todo(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # Save with the logged-in user
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({"error": "Invalid request", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_todos(request):
    todos = Todo.objects.all()
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def update_todo(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
    except Todo.DoesNotExist:
        return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TodoSerializer(todo, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_todo(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
    except Todo.DoesNotExist:
        return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)

    todo.delete()
    return Response({"message": "Todo deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # You could blacklist the refresh token if using blacklist strategy
            refresh_token = request.data.get("refresh_token", None)
            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()  # Blacklist the refresh token
                except Exception as e:
                    return Response({"detail": str(e)}, status=400)

            # Simply return a success response (client will clear the access token)
            return Response({"detail": "Successfully logged out."}, status=200)
        except Exception as e:
            return Response({"detail": "Something went wrong."}, status=500)
