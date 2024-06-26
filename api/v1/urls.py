from django.urls import path

from api.v1.views import (
    UserRegistrationView,
    UserLoginView,
    ModeratorRegistrationView,
    ThemesView,
    RoomsView,
    RoomUserView,
    RemoveUserRoomView,
    UserView,
    BlockUserView,
    GetAllMessagesView,
    UploadAudioView,
    UserDeleteView,
    UserColorView,
    RemoveUserIdRoomView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path(
        "register/moderator/",
        ModeratorRegistrationView.as_view(),
        name="moderator_registration",
    ),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("themes/", ThemesView.as_view(), name="temas"),
    path("rooms/", RoomsView.as_view(), name="salas"),
    path("addUser/", RoomUserView.as_view(), name="sala-usuario"),
    path("removeUser/", RemoveUserRoomView.as_view(), name="sala-usuario-remover"),
    path("user/", UserView.as_view(), name="usuario"),
    path("denounce/", BlockUserView.as_view(), name="usuario-bloquear"),
    path("roomMessages/", GetAllMessagesView.as_view(), name="mensagens"),
    path("upload-audio/", UploadAudioView.as_view(), name="upload-audio"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/delete/", UserDeleteView.as_view(), name="user_delete"),
    path("user/color/", UserColorView.as_view(), name="user_color"),
    path("moderator/removeUser/", RemoveUserIdRoomView.as_view(), name="moderator_remove_user"),
]

# TODO: Adicionar as views para o moderador deletar uma mensagem e bloquear um usuário
