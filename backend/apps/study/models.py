from django.conf import settings
from django.db import models


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)


class School(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=120)


class StudyProgram(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    level = models.CharField(max_length=120)


class AdmissionRequirement(models.Model):
    program = models.ForeignKey(StudyProgram, on_delete=models.CASCADE)
    requirement = models.TextField()


class Scholarship(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)


class SchoolApplication(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    program = models.ForeignKey(StudyProgram, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="draft")


class ProgramMatchScore(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    program = models.ForeignKey(StudyProgram, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(default=0)


class TuitionEstimate(models.Model):
    program = models.ForeignKey(StudyProgram, on_delete=models.CASCADE)
    annual_tuition = models.DecimalField(max_digits=12, decimal_places=2)


class StudyPermitReadinessAssessment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    readiness_score = models.PositiveSmallIntegerField(default=0)
