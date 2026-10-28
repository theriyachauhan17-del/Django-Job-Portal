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


class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(
        source="job.title",
        read_only=True,
    )
    company_name = serializers.CharField(
        source="job.company_name",
        read_only=True,
    )
    applicant_username = serializers.CharField(
        source="applicant.username",
        read_only=True,
    )

    class Meta:
        model = Application
        fields = [
            "id",
            "job",
            "job_title",
            "company_name",
            "applicant",
            "applicant_username",
            "date_applied",
        ]
        read_only_fields = fields



