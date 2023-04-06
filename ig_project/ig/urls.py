from django.contrib import admin
from django.urls import path
from ig.apiviews.user import CreateUser, LoginUserView, RetrieveUser, UpdateUser, DestroyUser, UserFollow
from ig.apiviews.post import CreatePost, RetrievePost, UpdatePost, DestroyPost, RetriveUserPosts, LikePost, CommentPost, CommentDetail

urlpatterns = [

    #------------------------User view url-----------------
    path('user/create',CreateUser.as_view(), name='create_user'),
    path('user/login',LoginUserView.as_view(), name='login_user'),
    path('user/<int:pk>',RetrieveUser.as_view(), name='retreive_user'),
    path('user/update',UpdateUser.as_view(), name='update_user'),
    path('user/delete/<int:pk>',DestroyUser.as_view(), name="destroy_user"),

    #-------------------------POST view url------------
    path("post/create", CreatePost.as_view(), name = 'create_post'),
    path('post/<int:pk>',RetrievePost.as_view(), name='retreive_post'),
    path('post/update/<int:pk>',UpdatePost.as_view(), name='Update Post'),
    path('post/delete/<int:pk>',DestroyPost.as_view(), name="destroy_post"),
    path("posts", RetriveUserPosts.as_view(), name = 'user_post'),

    #-------------------------postlike--------------------
    path('post/like/<int:pk>',LikePost.as_view(), name="post_like"),

    #----------------------------Post comment-----------------
    path('post/comment/<int:pk>',CommentPost.as_view(), name="post_comment"),
    path('post/comment/<int:comment_id>/', CommentDetail.as_view(), name='comment-detail'),

    #--------------------------------Follow/Unfollow User--------------------------
    path('user/follow/<int:pk>',UserFollow.as_view(), name="follow_user")


]