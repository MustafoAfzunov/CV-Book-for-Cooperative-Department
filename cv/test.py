import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from .models import CVSubmission, Education, Certificate, ProfessionalExperience

class CVAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
    def test_cv_submit_success(self):
        """Test successful CV submission"""
        data = {
            "external_id": "TEST123",
            "educations": [
                {
                    "degree_title": "Bachelor of Computer Science",
                    "university": "Test University",
                    "expected_graduation": "2024",
                    "certificates": [
                        {
                            "certificate_title": "AWS Certified",
                            "organization": "Amazon",
                            "year": "2023"
                        }
                    ]
                }
            ],
            "experiences": [
                {
                    "position_title": "Software Developer",
                    "company": "Tech Corp",
                    "dates": "2022-2024",
                    "accomplishments": "Developed web applications using Django"
                }
            ],
            "competencies": [
                {
                    "competency_type": "Leadership",
                    "key_accomplishments": "Led team of 5 developers"
                }
            ],
            "projects": [
                {
                    "project_title": "E-commerce Platform",
                    "year": "2023",
                    "summary": "Built full-stack e-commerce solution"
                }
            ],
            "technical_skills": {
                "programming_languages": "Python, JavaScript, Java",
                "frameworks_databases": "Django, React, PostgreSQL",
                "tools": "Git, Docker, AWS"
            },
            "languages": [
                {"name": "English"},
                {"name": "Spanish"}
            ],
            "community_involvements": [
                {
                    "position_title": "Volunteer Developer",
                    "organization": "Local NGO",
                    "dates": "2023-Present",
                    "achievements": "Built website for charity"
                }
            ],
            "awards": [
                {
                    "award_name": "Best Student Project",
                    "year": "2023",
                    "short_description": "Awarded for innovative AI project"
                }
            ],
            "references": [
                {
                    "reference_name": "John Doe",
                    "position": "Senior Developer",
                    "email": "john@example.com",
                    "phone": "123-456-7890"
                }
            ]
        }
        
        # Mock the PDF generation to avoid file system operations in tests
        with patch('your_app.views.CVSubmitView.generate_pdf') as mock_pdf:
            mock_pdf.return_value = '/media/pdfs/cv_1.pdf'
            
            response = self.client.post('/api/cv/submit/', data, format='json')
            
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('cv_id', response.data)
        self.assertIn('pdf_url', response.data)
        
        # Verify CV was created
        cv = CVSubmission.objects.get(external_id="TEST123")
        self.assertEqual(cv.educations.count(), 1)
        self.assertEqual(cv.experiences.count(), 1)
        self.assertEqual(cv.educations.first().certificates.count(), 1)

    def test_cv_submit_missing_external_id(self):
        """Test CV submission without external_id"""
        data = {"educations": []}
        response = self.client.post('/api/cv/submit/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('external_id is required', response.data['error'])

    def test_cv_submit_duplicate_external_id(self):
        """Test CV submission with duplicate external_id"""
        CVSubmission.objects.create(external_id="DUPLICATE123")
        
        data = {"external_id": "DUPLICATE123"}
        response = self.client.post('/api/cv/submit/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('CV already exists', response.data['error'])

    def test_cv_detail_authenticated(self):
        """Test CV detail retrieval for authenticated user"""
        cv = CVSubmission.objects.create(external_id="DETAIL123")
        Education.objects.create(
            cv=cv,
            degree_title="Test Degree",
            university="Test Uni",
            expected_graduation="2024"
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/cv/{cv.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['external_id'], "DETAIL123")
        self.assertEqual(len(response.data['educations']), 1)

    def test_cv_detail_unauthenticated(self):
        """Test CV detail retrieval without authentication"""
        cv = CVSubmission.objects.create(external_id="UNAUTH123")
        response = self.client.get(f'/api/cv/{cv.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cv_detail_not_found(self):
        """Test CV detail retrieval for non-existent CV"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/cv/99999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('CV not found', response.data['error'])

    def test_cv_submit_empty_sections(self):
        """Test CV submission with empty optional sections"""
        data = {
            "external_id": "EMPTY123",
            "educations": [],
            "experiences": [],
            "languages": []
        }
        
        with patch('your_app.views.CVSubmitView.generate_pdf') as mock_pdf:
            mock_pdf.return_value = '/media/pdfs/cv_1.pdf'
            response = self.client.post('/api/cv/submit/', data, format='json')
            
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        cv = CVSubmission.objects.get(external_id="EMPTY123")
        self.assertEqual(cv.educations.count(), 0)
        self.assertEqual(cv.experiences.count(), 0)

# Manual API Testing Examples (use with Postman, curl, or similar)

# 1. CV Submission Test
POST_DATA_EXAMPLE = {
    "external_id": "USER_12345",
    "educations": [
        {
            "degree_title": "Master of Science in Computer Science",
            "university": "Stanford University",
            "expected_graduation": "May 2024",
            "certificates": [
                {
                    "certificate_title": "Machine Learning Specialization",
                    "organization": "Coursera",
                    "year": "2023"
                },
                {
                    "certificate_title": "AWS Solutions Architect",
                    "organization": "Amazon Web Services",
                    "year": "2023"
                }
            ]
        },
        {
            "degree_title": "Bachelor of Engineering",
            "university": "MIT",
            "expected_graduation": "2022",
            "certificates": []
        }
    ],
    "experiences": [
        {
            "position_title": "Senior Software Engineer",
            "company": "Google",
            "dates": "2022-Present",
            "accomplishments": "Led development of microservices architecture serving millions of users daily"
        },
        {
            "position_title": "Software Engineer Intern",
            "company": "Microsoft",
            "dates": "Summer 2021",
            "accomplishments": "Developed REST APIs and improved system performance by 30%"
        }
    ],
    "competencies": [
        {
            "competency_type": "Technical Leadership",
            "key_accomplishments": "Mentored 3 junior developers and established coding standards"
        }
    ],
    "projects": [
        {
            "project_title": "Real-time Chat Application",
            "year": "2023",
            "summary": "Built scalable chat app using WebSockets, Redis, and Docker"
        }
    ],
    "technical_skills": {
        "programming_languages": "Python, JavaScript, Go, Java, C++",
        "frameworks_databases": "Django, React, Node.js, PostgreSQL, MongoDB",
        "tools": "Docker, Kubernetes, AWS, Git, Jenkins"
    },
    "languages": [
        {"name": "English"},
        {"name": "Mandarin"},
        {"name": "Spanish"}
    ],
    "community_involvements": [
        {
            "position_title": "Technical Mentor",
            "organization": "Girls Who Code",
            "dates": "2022-Present",
            "achievements": "Mentored 15+ students in programming fundamentals"
        }
    ],
    "awards": [
        {
            "award_name": "Dean's List",
            "year": "2021",
            "short_description": "Achieved GPA of 3.9+ for academic excellence"
        }
    ],
    "references": [
        {
            "reference_name": "Dr. Sarah Johnson",
            "position": "Professor of Computer Science",
            "email": "sarah.johnson@stanford.edu",
            "phone": "+1-650-123-4567"
        },
        {
            "reference_name": "Mike Chen",
            "position": "Senior Engineering Manager",
            "email": "mchen@google.com",
            "phone": "+1-415-987-6543"
        }
    ]
}

"""
CURL Commands for Manual Testing:

1. Submit CV:
curl -X POST http://localhost:8000/api/cv/submit/ \
  -H "Content-Type: application/json" \
  -d '{"external_id": "TEST123", "educations": [{"degree_title": "BS Computer Science", "university": "Test Uni", "expected_graduation": "2024", "certificates": []}]}'

2. Get CV Details (replace TOKEN and CV_ID):
curl -X GET http://localhost:8000/api/cv/1/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

3. Test Error Cases:
# Missing external_id
curl -X POST http://localhost:8000/api/cv/submit/ \
  -H "Content-Type: application/json" \
  -d '{}'

# Duplicate external_id (run twice)
curl -X POST http://localhost:8000/api/cv/submit/ \
  -H "Content-Type: application/json" \
  -d '{"external_id": "DUPLICATE123"}'
"""

# Performance Test Example
class CVPerformanceTest(TestCase):
    def test_bulk_cv_creation(self):
        """Test creating multiple CVs to check performance"""
        import time
        start_time = time.time()
        
        # Create 10 CVs with data
        for i in range(10):
            data = {
                "external_id": f"PERF_TEST_{i}",
                "educations": [
                    {
                        "degree_title": f"Degree {i}",
                        "university": f"University {i}",
                        "expected_graduation": "2024"
                    }
                ]
            }
            with patch('your_app.views.CVSubmitView.generate_pdf') as mock_pdf:
                mock_pdf.return_value = f'/media/pdfs/cv_{i}.pdf'
                response = self.client.post('/api/cv/submit/', data, format='json')
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        end_time = time.time()
        print(f"Created 10 CVs in {end_time - start_time:.2f} seconds")
        
        # Verify all were created
        self.assertEqual(CVSubmission.objects.count(), 10)