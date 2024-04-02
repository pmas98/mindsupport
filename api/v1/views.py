from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api.v1.serializers import (
    UserRegistrationSerializer,
    LoginSerializer,
    ModeradorRegistrationSerializer,
    TemaSerializer,
    RoomUserSerializer,
)
from api.models import Sala, Usuario, RoomUser, Tema, Moderador
from api.v1.serializers import SalasSerializer
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from firebase_admin import firestore, storage
import tempfile
from datetime import timedelta
from channels.generic.websocket import WebsocketConsumer


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {"message": "User registration successful!"}
        return Response(response_data, status=status.HTTP_201_CREATED)


class ModeratorRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ModeradorRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {"message": "User registration successful!"}
        return Response(response_data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data.get("token")
            return Response({"token": token}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThemesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        themes = Tema.objects.all()
        serializer = TemaSerializer(themes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TemaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {"message": "Theme created successfully!"}
        return Response(response_data, status=status.HTTP_201_CREATED)


class RoomsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        theme_id = request.query_params.get("theme")
        if theme_id:
            rooms = Sala.objects.filter(theme_id=theme_id)
        else:
            rooms = Sala.objects.all()
        serializer = SalasSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SalasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {"message": "Room created successfully!"}
        return Response(response_data, status=status.HTTP_201_CREATED)


class RoomUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        usuario_id = Usuario.objects.get(username=user).id
        request.data["usuario"] = usuario_id
        serializer = RoomUserSerializer(
            data=request.data, context={"usuario": usuario_id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {"message": "RoomUser created successfully!"}
        return Response(response_data, status=status.HTTP_201_CREATED)


class RemoveUserRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        room_id = request.data.get("sala")
        user = request.user
        usuario = Usuario.objects.get(username=user).id
        sala = Sala.objects.get(id=room_id)
        room_user = RoomUser.objects.filter(room=sala, user=usuario).first()
        if room_user:
            room_user.delete()
            response_data = {"message": "RoomUser deleted successfully!"}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {"message": "RoomUser not found!"}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        usuario = Usuario.objects.get(username=user)
        moderador = Moderador.objects.filter(user=usuario).first()
        data = {
            "id": usuario.id,
            "username": usuario.username,
            "is_moderator": True if (moderador and moderador.active) else False,
            "created_at": datetime.strftime(usuario.date_joined, "%b %d"),
        }
        return Response(data, status=status.HTTP_200_OK)


class BlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.data.get("user")
        user = Usuario.objects.get(id=user)
        block_reason = request.data.get("block_reason")
        user.block_reason = block_reason
        user.save()
        response_data = {"message": "User blocked successfully!"}
        return Response(response_data, status=status.HTTP_200_OK)


class UploadAudioView(APIView, WebsocketConsumer):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        audio = request.data.get("audio")
        room = request.data.get("room")
        user = request.user
        username = request.data.get("username")

        db = firestore.client()
        bucket_name = "mindsupport-5da6e.appspot.com"
        bucket = storage.bucket(bucket_name)
        blob = None
        if audio:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(audio.read())
                tmp_file_path = tmp.name
                name = f"{user}-{room}-{datetime.now()}.mp3"
                blob = bucket.blob(name)
                with open(tmp_file_path, "rb") as tmp_file:
                    blob.upload_from_file(tmp_file)
                try:
                    audio_url = blob.generate_signed_url(
                        expiration=timedelta(days=365), method="GET"
                    )
                    db.collection("roomChat").add(
                        {
                            "userid": user.id,
                            "username": username,
                            "room": room,
                            "message": "",
                            "timestamp": datetime.now(),
                            "audio": audio_url if blob else "",
                        }
                    )
                    print("Message added successfully.")
                    return Response(
                        {"audio": audio_url if blob else ""}, status=status.HTTP_200_OK
                    )

                except Exception as e:
                    print(f"Error adding message: {e}")
                return Response({"audio": blob.public_url}, status=status.HTTP_200_OK)


def SaveMessageView(userid, username, room, message, audio):
    db = firestore.client()
    bucket_name = "mindsupport-5da6e.appspot.com"
    bucket = storage.bucket(bucket_name)
    blob = None
    if audio:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(audio)
            tmp_file_path = tmp.name
            name = f"{username}-{room}-{datetime.now()}.mp3"
            blob = bucket.blob(name)
            blob = bucket.blob(name)
            with open(tmp_file_path, "rb") as tmp_file:
                blob.upload_from_file(tmp_file)
            try:
                audio_url = blob.generate_signed_url(
                    expiration=timedelta(days=365), method="GET"
                )
                db.collection("roomChat").add(
                    {
                        "userid": userid,
                        "username": username,
                        "room": room,
                        "message": message,
                        "timestamp": datetime.now(),
                        "audio": audio_url if blob else "",
                    }
                )
                print("Message added successfully.")
                return audio_url if blob else ""

            except Exception as e:
                print(f"Error adding message: {e}")
            return blob.public_url
    else:
        try:
            db.collection("roomChat").add(
                {
                    "userid": userid,
                    "username": username,
                    "room": room,
                    "message": message,
                    "timestamp": datetime.now(),
                    "audio": blob.public_url if blob else "",
                }
            )
            print("Message added successfully.")

        except Exception as e:
            print(f"Error adding message: {e}")


class GetAllMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        room = request.data.get("room")
        limit = request.data.get("limit")
        db = firestore.client()
        messages = (
            db.collection("roomChat")
            .where("room", "==", int(room))
            .order_by("timestamp", direction=firestore.Query.DESCENDING)
            .limit(limit)
            .stream()
        )
        data = []
        for message in messages:
            message_data = message.to_dict()
            message_data["hour"] = message_data["timestamp"].strftime("%H:%M:%S")
            message_data["timestamp"] = message_data["timestamp"].strftime("%b %d")
            data.append(message_data)
        return Response(data, status=status.HTTP_200_OK)
