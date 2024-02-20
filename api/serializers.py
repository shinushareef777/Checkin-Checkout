from rest_framework import serializers
from .models import CheckIn, Instructor, CheckOut


class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = "__all__"


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = "__all__"


class CheckOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckOut
        fields = "__all__"


class MonthlySummarySerializer(serializers.Serializer):
    name = serializers.CharField()
    month = serializers.CharField()
    total_hours = serializers.FloatField()
