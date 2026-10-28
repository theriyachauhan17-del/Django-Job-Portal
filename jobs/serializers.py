from rest_framework import serializers
from .models import Application, Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "company_name",
            "description",
            "location",
            "salary",
            "posted_by",
            "date_posted",
        ]
        read_only_fields = ["id", "posted_by", "date_posted"]


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "company_name",
            "description",
            "location",
            "salary",
            "posted_by",
            "date_posted",
        ]
        read_only_fields = ["id", "posted_by", "date_posted"]


class ApplicationCreateSerializer(serializers.ModelSerializer):
    applicant = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Application
        fields = ["id", "job", "applicant", "date_applied"]
        read_only_fields = ["id", "date_applied"]


