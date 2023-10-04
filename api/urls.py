from django.urls import path
from .views import (
    UserPosts, UserPostView, delete_attachment,
    PostsListView, UserPostsCategoryListView, PostCommentsListView,
    PostCommentView, EditDeleteCommentView, UsersListView, UserView, ProfileView,
    like_or_dislike_post, get_post, PostsCategoryListView, MyRecentPostsListView,
    UserRecentPostViewList, UploadAttachment, MyConstituencyPostView, ClarifiedToogleView,
    MyDistrictPostView, MyNewsFeed, UploadToFirebaseStorage, UserTaggedPosts, MyTaggedPosts,
    SavePost, SavedPosts
    )

urlpatterns = [
    path('user_post_create/', UserPosts.as_view()),
    path('user_post/<int:pk>/', UserPostView.as_view()),
    path('delete_users_attachment/<int:pk>/', delete_attachment),
    path('posts/', PostsListView.as_view()),
    path('category_posts/<int:category>/', PostsCategoryListView.as_view()),
    path('post/<int:pk>/', get_post),
    path('user_category_posts/<int:category>/', UserPostsCategoryListView.as_view()),
    path('post_comments/<int:post_id>/', PostCommentsListView.as_view()),
    path('create_comment/<int:pk>/', PostCommentView.as_view()),
    path('comment_update_delete/<int:pk>/', EditDeleteCommentView.as_view()),
    path('user_list/', UsersListView.as_view()),
    path('user/<int:pk>/', UserView.as_view()),
    path('myprofile/', ProfileView.as_view()),
    path('generate_like_dislike/<int:pk>/', like_or_dislike_post),
    path('my_recent_posts/', MyRecentPostsListView.as_view()),
    path('user_recent_posts/<int:user_id>/', UserRecentPostViewList.as_view()),
    path('upload_attachment/', UploadAttachment.as_view()),
    path('my_constituency_posts/', MyConstituencyPostView.as_view()),
    path('toggle_post_clarified/<int:pk>/', ClarifiedToogleView.as_view()),
    path('my_district_posts/', MyDistrictPostView.as_view()),
    path('my_news_feed/', MyNewsFeed.as_view()),
    path('upload_firebase/', UploadToFirebaseStorage.as_view()),
    path('tagged_posts/<int:pk>/', UserTaggedPosts.as_view()),
    path('my_tagged_posts/', MyTaggedPosts.as_view()),
    path('save_post/<int:pk>/', SavePost.as_view()),
    path('saved_posts/',SavedPosts.as_view())
]