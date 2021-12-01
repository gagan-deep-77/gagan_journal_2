from django.urls import path
from . import views
urlpatterns = [
    path("",views.home,name="home"),
    path("register",views.register,name="register"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("add_post",views.add_post,name="add_post"),
    path("viewPost/<id>",views.viewPost,name="viewPost"),
    path("viewUser/<id>",views.viewUser,name="viewUser"),
    path("deletePost/<id>",views.deletePost,name="deletePost"),
    path("deleteComment/<id>",views.deleteComment,name="deleteComment"),
    path("editPost/<id>",views.editPost,name="editPost"),
]