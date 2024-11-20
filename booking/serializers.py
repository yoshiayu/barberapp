from rest_framework import serializers
from .models import User, Service, Appointment, Schedule, Reservation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)  # フロントエンドから受け取る用
    email = serializers.EmailField(write_only=True)  # フロントエンドから受け取る用

    class Meta:
        model = Appointment
        fields = ["user", "service", "date", "time", "status"]

    def validate(self, data):
        # 同じ日時・時間・サービスで予約が存在する場合エラー
        if Appointment.objects.filter(
            date=data["date"], time=data["time"], service=data["service"]
        ).exists():
            raise serializers.ValidationError(
                "この日時とコースは既に予約されています。"
            )
        return data

    def create(self, validated_data):
        # nameとemailを使用してUserを作成または取得
        name = validated_data.pop("name")
        email = validated_data.pop("email")
        user, created = User.objects.get_or_create(email=email, defaults={"name": name})

        # 残りのデータでAppointmentを作成
        validated_data["user"] = user
        return super().create(validated_data)


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
