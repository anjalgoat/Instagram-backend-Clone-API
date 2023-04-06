from rest_framework import generics
from ig.serializers import UserSerializer, UserLoginSerializer, FollowSerializer
from ig.models import User, FollowUser
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

class CreateUser(generics.CreateAPIView):
    def get_queryset(self):
        return User.objects.all()
    serializer_class = UserSerializer

class LoginUserView(APIView):
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = User.objects.get(email = serializer.validated_data['email'])
                if user.password == serializer.validated_data['password']:
                    token = Token.objects.get_or_create(user=user)
                    return Response({"success": True, "token":token[0].key })
                else:
                    return Response({"success": False, "message":"Incorrect Password"})
            except ObjectDoesNotExist:
                return Response({"success": False, "message": "user doesnot exist"})


class RetrieveUser(generics.RetrieveAPIView):
    def get_queryset(self):
        return User.objects.all()
    serializer_class = UserSerializer

# Here in UpdateUser Class APIView is used instead of UpdateAPIView because UpdateUser class has implemented its own put method to handle the update operation. Whereas, UpdateAPIView already provides an implementation for put method that updates a model instance based on the provided pk parameter.

class UpdateUser(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_class = [IsAuthenticated]

    def put(self, request):
        serializer = self.serializer_class(request.user, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True,"message":"user updated"})
        else:
            return Response({"success":False,"message":"error updating user"})
        

        
"""
--------------- ----------Updating using UpdateAPIView-------------------

*Note from put and patch method. Only one is used according to the requirement

class UpdateUser(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "message": "User updated successfully."})

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "message": "User updated successfully."})
"""

class DestroyUser(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_class = [IsAuthenticated]

    def destroy(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            if pk == request.user.id:
                self.perform.destroy(request.user)
                return Response({"success": True,"message":"User deleted"})
            else:
                return Response({"success": False,"message":"User Can't bedeleted"})
        except ObjectDoesNotExist:
            return Response({"success": False,"message":"User doesnot exist"})
        
#------------------------------------Follow/unfollow user---------------------------------

class UserFollow(APIView):
    queryset = FollowUser.objects.all()
    serializer_class = FollowSerializer
    authentication_classes = [TokenAuthentication]
    permission_class = [IsAuthenticated]

    def get(self, request, pk):
        following = FollowUser.objects.filter(user = request.user)
        followers = FollowUser.objects.filter(follows = request.user)
        following_serializer = FollowSerializer(following, many=True)
        follower_serializer = FollowSerializer(followers, many=True)
        return Response({"success":True, "following": follower_serializer.data, "followers": follower_serializer.data})

    def post(self, request, pk):
        try:
            following = User.objects.get(id=pk)
            follow_user = FollowUser.objects.get_or_create(user = request.user, follows = following)
            if not follow_user[1]:
                follow_user[0].delete()
                return Response({"success":True, "message":"User unfollowed"})
            else:
                return Response({"success":True, "message":"User Followed"})


        except ObjectDoesNotExist:
            return Response({"success": False,"message":"User doesnot exist"})

   