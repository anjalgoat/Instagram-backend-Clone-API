from rest_framework.views import APIView
from rest_framework import generics
from ig.serializers import PostSerializer, CommentSerializer
from ig.models import Post, PostLike, PostComment
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

class CreatePost(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_class = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class RetrievePost(generics.RetrieveAPIView):
    def get_queryset(self):
        return Post.objects.all()
    serializer_class = PostSerializer

class UpdatePost(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_class = [IsAuthenticated]

    def put(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"success":True,"message":"Post Updated"})
        else:
            print(serializer.errors)
            return Response({"success":False,"message":"Error Updating"})

class DestroyPost(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_class = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            post = Post.objects.get(id=pk)
            if post.user.id == request.user.id:
                self.perform_destroy(post)
                return Response({"success":True,"message":"Post Deleted"})
            else:
                return Response({"success":False,"message":"Error Deleting"})
        except ObjectDoesNotExist:
            return Response({"success":False,"message":"Post doesnot exist"})
        
class RetriveUserPosts(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_class = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user_posts = Post.objects.filter(user=request.user.id)
        serializer = self.serializer_class(user_posts,many=True)
        return Response({"success":True,"message": serializer.data})
    
#----------------------------Post Like--------------

class LikePost(APIView):
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_class = [IsAuthenticated]

    def get(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            post_likes = PostLike.objects.filter(post=post)

            # Get the count of likes for the post
            like_count = post_likes.count()

            # Check if the authenticated user has already liked the post
            user_like = post_likes.filter(user=request.user).exists()

            return Response({"success": True, "message": {
                "like_count": like_count,
                "user_like": user_like
            }})
            
        except ObjectDoesNotExist:
            return Response({"success": False, "message": "Post does not exist"})
    
    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)

            # Check if the authenticated user has already liked the post
            existing_like = PostLike.objects.filter(post=post, user=request.user)
            if existing_like.exists():
                return Response({"success": False, "message": "You have already liked this post"})

            # Create a new post like object and save it to the database
            new_like = PostLike(post=post, user=request.user)
            new_like.save()

            return Response({"success": True, "message": "Post liked successfully"})
            
        except ObjectDoesNotExist:
            return Response({"success": False, "message": "Post does not exist"})
    
    def delete(self, request, pk):
        try:
            post = Post.objects.get(id=pk)

            # Check if the authenticated user has already liked the post
            existing_like = PostLike.objects.filter(post=post, user=request.user)
            if not existing_like.exists():
                return Response({"success": False, "message": "You have not liked this post yet"})

            # Delete the post like object from the database
            existing_like.delete()

            return Response({"success": True, "message": "Post unliked successfully"})
            
        except ObjectDoesNotExist:
            return Response({"success": False, "message": "Post does not exist"})


#-------------------POST comments------------------

class CommentPost(APIView):
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_class = [IsAuthenticated]

    def get(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            comments = PostComment.objects.filter(post=post)
            serializer = self.serializer_class(comments, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"success": False, "message": "Post does not exist"})

    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            serializer = self.serializer_class(data=request.data,context={'request': request})
            if serializer.is_valid():
                serializer.save(post=post)
                return Response({"success": True, "message": "Comment added successfully"})
            else:
                return Response({"success": False, "message": serializer.errors})
        except ObjectDoesNotExist:
            return Response({"success": False, "message": "Post does not exist"})

class CommentDetail(APIView):
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  

    def put(self, request, comment_id, format=None):
        try:
            comment = self.objects.get(id=comment_id)
            serializer = self.serializer_class(instance=comment, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"success": True, "message": "Comment updated successfully"})
            else:
                return Response({"success": False, "message": serializer.errors})
        except ObjectDoesNotExist:
            return Response({"success": False, "message": "Comment does not exist"})

    def delete(self, request, comment_id):
        try:
            comment = self.objects.get(id=comment_id)
            comment.delete()
            return Response({"success": True, "message": "Comment deleted successfully"})
        except ObjectDoesNotExist:
            return Response({"success": False, "message": "Comment does not exist"})