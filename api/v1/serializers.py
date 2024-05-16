from rest_framework import serializers
from api.models import Usuario, Moderador, Tema, Sala, RoomUser
import nltk
import random
from api.backends import EmailAuthBackend
from rest_framework_simplejwt.tokens import RefreshToken

nltk.download("words")

words = nltk.corpus.words.words()


def generate_random_word():
    filtered_words = [word for word in words if len(word) <= 7]
    return random.choice(filtered_words)


def generate_random_username():
    random_word = generate_random_word()
    random_word2 = generate_random_word()
    random_number = random.randint(0, 100)  # Ensure a unique username
    return f"{random_word.capitalize()}{random_word2.capitalize()}{random_number}"


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ("email", "password")
        extra_kwargs = {"password": {"required": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        username = generate_random_username()
        user = Usuario.objects.create_user(
            email=validated_data["email"], username=username
        )
        user.set_password(password)
        user.save()
        return user


class ModeradorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    reason = serializers.CharField()
    email = serializers.EmailField()  # Keep the email field

    class Meta:
        model = Moderador
        fields = ("email", "password", "reason")
        extra_kwargs = {"password": {"required": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        username = generate_random_username()
        user = Usuario.objects.create_user(
            email=validated_data["email"], username=username
        )
        user.set_password(password)
        user.save()

        moderador = Moderador(user=user, reason=validated_data["reason"], active=False)
        moderador.save()
        return moderador


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            auth_backend = EmailAuthBackend()
            user = auth_backend.authenticate(
                request=self.context.get("request"), email=email, password=password
            )
            if not user:
                raise serializers.ValidationError("Invalid email/password.")
            refresh = RefreshToken.for_user(user)

            attrs["token"] = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            attrs["user"] = user
            return attrs
        else:
            raise serializers.ValidationError("Both email and password are required.")


class TemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tema
        fields = (
            "id",
            "name",
        )


class SalasSerializer(serializers.ModelSerializer):
    room_capacity = serializers.SerializerMethodField()
    date_created = serializers.SerializerMethodField()

    def get_room_capacity(self, sala):
        return sala.roomuser_set.count()

    def get_date_created(self, sala):
        return sala.created_at  # Assuming 'created_at' is the field for creation date

    class Meta:
        model = Sala
        fields = ("id", "theme", "room_capacity", "date_created")
        read_only_fields = ('date_created',) 

class RoomUserSerializer(serializers.ModelSerializer):
    sala = serializers.PrimaryKeyRelatedField(queryset=Sala.objects.all())
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())

    class Meta:
        model = RoomUser
        fields = ("sala", "usuario")

    def create(self, validated_data):
        sala = validated_data["sala"]
        usuario = validated_data["usuario"]
        room_user = RoomUser.objects.create(room=sala, user=usuario)
        return room_user
