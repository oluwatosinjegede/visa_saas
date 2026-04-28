from rest_framework import serializers

from .models import ApplicantProfile, SOPSubmission, VisaAssessmentSubmission


class ApplicantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantProfile
        fields = ["age", "country", "education_level", "work_experience"]


class SOPUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class SOPResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOPSubmission
        fields = ["id", "score", "feedback", "result", "created_at"]


class VisaAssessmentQuestionnaireSerializer(serializers.Serializer):
    # Section 1: Identity & demographics
    full_name = serializers.CharField(max_length=255)
    date_of_birth = serializers.DateField()
    age = serializers.IntegerField(min_value=16, max_value=100)
    gender = serializers.CharField(max_length=50, required=False, allow_blank=True)
    nationality = serializers.CharField(max_length=100)
    country_of_residence = serializers.CharField(max_length=100)
    marital_status = serializers.CharField(max_length=50, required=False, allow_blank=True)
    dependents_count = serializers.IntegerField(min_value=0, default=0)
    dependents_reside_with_applicant = serializers.BooleanField(default=False)
    valid_passport = serializers.BooleanField()
    passport_expiry_date = serializers.DateField(required=False, allow_null=True)

    # Section 2: Travel & immigration history
    traveled_outside_home_country = serializers.BooleanField(default=False)
    countries_visited_last_10_years = serializers.ListField(
        child=serializers.CharField(max_length=100), required=False, default=list
    )
    visited_us = serializers.BooleanField(default=False)
    visited_uk = serializers.BooleanField(default=False)
    visited_canada = serializers.BooleanField(default=False)
    visited_schengen = serializers.BooleanField(default=False)
    has_overstay_history = serializers.BooleanField(default=False)
    has_deportation_history = serializers.BooleanField(default=False)
    has_previous_visa_refusal = serializers.BooleanField(default=False)
    previous_refusal_country = serializers.CharField(max_length=100, required=False, allow_blank=True)
    previous_refusal_date = serializers.DateField(required=False, allow_null=True)
    previous_refusal_reason = serializers.CharField(required=False, allow_blank=True)

    # Section 3: Purpose of travel
    visa_type = serializers.ChoiceField(choices=["study", "visit", "work", "business", "pr"])
    destination_country = serializers.CharField(max_length=100)
    intended_duration_days = serializers.IntegerField(min_value=1)
    country_choice_reason = serializers.CharField()
    why_now = serializers.CharField()
    purpose_explanation = serializers.CharField()

    # Section 4: Education and career consistency
    highest_education = serializers.CharField(max_length=120)
    field_of_study = serializers.CharField(max_length=120)
    graduation_year = serializers.IntegerField(min_value=1950, max_value=2100)
    previous_education_summary = serializers.CharField(required=False, allow_blank=True)
    employment_status = serializers.ChoiceField(choices=["employed", "self-employed", "unemployed"])
    job_title = serializers.CharField(max_length=120, required=False, allow_blank=True)
    employer_name = serializers.CharField(max_length=120, required=False, allow_blank=True)
    employment_length_months = serializers.IntegerField(min_value=0, default=0)
    annual_income = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=0)
    trip_aligned_with_career = serializers.BooleanField(default=False)
    career_progression_plan = serializers.CharField()

    # Section 5: Financial capacity
    trip_funding_source = serializers.ChoiceField(choices=["self", "sponsor"])
    sponsor_name = serializers.CharField(max_length=120, required=False, allow_blank=True)
    sponsor_relationship = serializers.CharField(max_length=120, required=False, allow_blank=True)
    sponsor_occupation = serializers.CharField(max_length=120, required=False, allow_blank=True)
    current_bank_balance = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=0)
    average_monthly_inflow = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=0)
    bank_statement_duration_months = serializers.ChoiceField(choices=[6, 9, 12])
    has_large_recent_deposits = serializers.BooleanField(default=False)
    large_deposit_explanation = serializers.CharField(required=False, allow_blank=True)
    assets_property = serializers.BooleanField(default=False)
    assets_investments = serializers.BooleanField(default=False)
    assets_business_ownership = serializers.BooleanField(default=False)
    has_tax_records = serializers.BooleanField(default=False)

    # Section 6: Home country ties
    owns_property_home_country = serializers.BooleanField(default=False)
    has_permanent_job_or_business = serializers.BooleanField(default=False)
    job_or_business_duration_months = serializers.IntegerField(min_value=0, default=0)
    has_approved_leave = serializers.BooleanField(default=False)
    spouse_in_home_country = serializers.BooleanField(default=False)
    children_in_school_home_country = serializers.BooleanField(default=False)
    community_commitments = serializers.CharField(required=False, allow_blank=True)
    return_plan = serializers.CharField()

    # Section 7: Documentation readiness
    has_employment_letter = serializers.BooleanField(default=False)
    has_payslips = serializers.BooleanField(default=False)
    has_admission_letter = serializers.BooleanField(default=False)
    has_invitation_letter = serializers.BooleanField(default=False)
    documents_verifiable = serializers.BooleanField(default=True)
    document_inconsistencies = serializers.BooleanField(default=False)

    # Section 8: Credibility and risk flags
    used_false_documents = serializers.BooleanField(default=False)
    misrepresented_information = serializers.BooleanField(default=False)
    related_to_immigration_violator = serializers.BooleanField(default=False)
    understands_visa_conditions = serializers.BooleanField(default=True)

    # Section 9: Statement of intent
    statement_of_intent = serializers.CharField()

    def validate(self, attrs):
        if attrs.get("trip_funding_source") == "sponsor" and not attrs.get("sponsor_name"):
            raise serializers.ValidationError({"sponsor_name": "Sponsor name is required when funding source is sponsor."})

        if attrs.get("has_previous_visa_refusal") and not attrs.get("previous_refusal_reason"):
            raise serializers.ValidationError({"previous_refusal_reason": "Please provide the previous refusal reason."})

        if attrs.get("has_large_recent_deposits") and not attrs.get("large_deposit_explanation"):
            raise serializers.ValidationError({"large_deposit_explanation": "Please explain the source of large deposits."})

        return attrs


class VisaAssessmentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisaAssessmentSubmission
        fields = [
            "id",
            "score",
            "approval_probability",
            "refusal_risk_level",
            "refusal_risks",
            "recommendations",
            "ai_refusal_prediction",
            "created_at",
        ]