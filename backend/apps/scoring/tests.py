from django.test import SimpleTestCase

from .services import assess_questionnaire


class VisaAssessmentServiceTests(SimpleTestCase):
    def test_high_quality_questionnaire_scores_well(self):
        payload = {
            "full_name": "Jane Doe",
            "date_of_birth": "1994-08-01",
            "age": 31,
            "gender": "Female",
            "nationality": "Kenyan",
            "country_of_residence": "Kenya",
            "marital_status": "Married",
            "dependents_count": 1,
            "dependents_reside_with_applicant": True,
            "valid_passport": True,
            "passport_expiry_date": "2031-01-01",
            "traveled_outside_home_country": True,
            "countries_visited_last_10_years": ["UAE", "UK"],
            "visited_us": False,
            "visited_uk": True,
            "visited_canada": False,
            "visited_schengen": False,
            "has_overstay_history": False,
            "has_deportation_history": False,
            "has_previous_visa_refusal": False,
            "previous_refusal_country": "",
            "previous_refusal_date": None,
            "previous_refusal_reason": "",
            "visa_type": "study",
            "destination_country": "Canada",
            "intended_duration_days": 365,
            "country_choice_reason": "Program quality and innovation ecosystem",
            "why_now": "Career upskilling for data science leadership roles",
            "purpose_explanation": "I am pursuing this specialized program to bridge my software engineering background with advanced AI product strategy and return to lead digital transformation initiatives in my home market.",
            "highest_education": "BSc Computer Science",
            "field_of_study": "Computer Science",
            "graduation_year": 2018,
            "previous_education_summary": "BSc in CS after a STEM-focused high school track.",
            "employment_status": "employed",
            "job_title": "Senior Software Engineer",
            "employer_name": "TechCo",
            "employment_length_months": 60,
            "annual_income": "38000",
            "trip_aligned_with_career": True,
            "career_progression_plan": "Return to transition into AI product leadership and eventually launch a local education technology startup.",
            "trip_funding_source": "self",
            "sponsor_name": "",
            "sponsor_relationship": "",
            "sponsor_occupation": "",
            "current_bank_balance": "12000",
            "average_monthly_inflow": "2400",
            "bank_statement_duration_months": 12,
            "has_large_recent_deposits": False,
            "large_deposit_explanation": "",
            "assets_property": True,
            "assets_investments": True,
            "assets_business_ownership": False,
            "has_tax_records": True,
            "owns_property_home_country": True,
            "has_permanent_job_or_business": True,
            "job_or_business_duration_months": 60,
            "has_approved_leave": True,
            "spouse_in_home_country": True,
            "children_in_school_home_country": False,
            "community_commitments": "Active mentor in local coding bootcamp.",
            "return_plan": "Resume role with promotion track and continue mentoring commitments.",
            "has_employment_letter": True,
            "has_payslips": True,
            "has_admission_letter": True,
            "has_invitation_letter": False,
            "documents_verifiable": True,
            "document_inconsistencies": False,
            "used_false_documents": False,
            "misrepresented_information": False,
            "related_to_immigration_violator": False,
            "understands_visa_conditions": True,
            "statement_of_intent": "My visa should be approved because my purpose is academically clear, financed transparently, and aligned with my long-term career path in my home country where I already have stable employment, family responsibilities, and property ties.",
        }

        result = assess_questionnaire(payload)

        self.assertGreaterEqual(result["score"], 80)
        self.assertEqual(result["approval_probability"], "High")

    def test_critical_red_flags_generate_high_risk(self):
        payload = {
            "valid_passport": False,
            "has_overstay_history": True,
            "has_deportation_history": True,
            "has_previous_visa_refusal": True,
            "used_false_documents": True,
            "misrepresented_information": True,
            "trip_aligned_with_career": False,
            "current_bank_balance": 100,
            "average_monthly_inflow": 10,
            "has_large_recent_deposits": True,
            "large_deposit_explanation": "",
            "has_tax_records": False,
            "owns_property_home_country": False,
            "has_permanent_job_or_business": False,
            "has_approved_leave": False,
            "spouse_in_home_country": False,
            "children_in_school_home_country": False,
            "documents_verifiable": False,
            "document_inconsistencies": True,
            "purpose_explanation": "Short reason.",
            "statement_of_intent": "Short.",
        }

        result = assess_questionnaire(payload)

        self.assertLessEqual(result["score"], 20)
        self.assertEqual(result["refusal_risk_level"], "High")
        self.assertTrue(result["refusal_risks"])