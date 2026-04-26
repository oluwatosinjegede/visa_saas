from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    PLATFORM_ADMIN = "PLATFORM_ADMIN", "Platform Admin"
    APPLICANT = "APPLICANT", "Applicant"
    IMMIGRATION_CONSULTANT = "IMMIGRATION_CONSULTANT", "Immigration Consultant"
    RECRUITER = "RECRUITER", "Recruiter"
    EMPLOYER = "EMPLOYER", "Employer"
    SCHOOL_ADMIN = "SCHOOL_ADMIN", "School Admin"
    AGENT = "AGENT", "Agent"
    SUPPORT_STAFF = "SUPPORT_STAFF", "Support Staff"


class OrganizationType(models.TextChoices):
    CONSULTANCY = "CONSULTANCY", "Consultancy"
    SCHOOL = "SCHOOL", "School"
    EMPLOYER = "EMPLOYER", "Employer"
    RECRUITMENT_AGENCY = "RECRUITMENT_AGENCY", "Recruitment Agency"
    INTERNAL_TEAM = "INTERNAL_TEAM", "Internal Team"


class User(AbstractUser):
    role = models.CharField(max_length=40, choices=Role.choices, default=Role.APPLICANT)


class Organization(models.Model):
    name = models.CharField(max_length=255)
    organization_type = models.CharField(max_length=40, choices=OrganizationType.choices)


class OrganizationMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=40, choices=Role.choices)


class Permission(models.Model):
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    country_of_residence = models.CharField(max_length=120, blank=True)
    nationality = models.CharField(max_length=120, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    education_level = models.CharField(max_length=120, blank=True)
    work_experience_years = models.PositiveSmallIntegerField(default=0)
    preferred_destination_country = models.CharField(max_length=120, blank=True)
    preferred_pathway = models.CharField(max_length=120, blank=True)
