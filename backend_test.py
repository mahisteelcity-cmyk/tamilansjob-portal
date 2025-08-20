#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for TamilansJob.com Job Portal
Tests all backend endpoints including seed data, districts, qualifications, categories, and jobs APIs
"""

import requests
import json
import time
import os
from datetime import datetime, timedelta

# Get base URL from environment - using local URL due to external ingress issue
BASE_URL = "http://localhost:3000/api"

class TamilansJobAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.test_results = []
        
    def log_test(self, test_name, success, message, response_data=None):
        """Log test results"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'response_data': response_data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if response_data and not success:
            print(f"   Response: {response_data}")
    
    def test_root_endpoint(self):
        """Test GET /api - Basic health check"""
        try:
            response = self.session.get(f"{self.base_url}")
            if response.status_code == 200:
                data = response.json()
                if data.get('message') == "TamilansJob.com API":
                    self.log_test("Root API Health Check", True, "API is responding correctly")
                    return True
                else:
                    self.log_test("Root API Health Check", False, f"Unexpected response: {data}")
                    return False
            else:
                self.log_test("Root API Health Check", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Root API Health Check", False, f"Exception: {str(e)}")
            return False
    
    def test_seed_data(self):
        """Test POST /api/seed - Initialize seed data"""
        try:
            response = self.session.post(f"{self.base_url}/seed")
            if response.status_code == 200:
                data = response.json()
                expected_counts = {
                    'districts': 6,
                    'qualifications': 7,
                    'categories': 6,
                    'jobs': 2
                }
                
                if data.get('message') == 'Seed data created successfully':
                    counts = data.get('counts', {})
                    all_correct = True
                    for key, expected in expected_counts.items():
                        if counts.get(key) != expected:
                            all_correct = False
                            break
                    
                    if all_correct:
                        self.log_test("Seed Data Creation", True, f"All seed data created successfully: {counts}")
                        return True
                    else:
                        self.log_test("Seed Data Creation", False, f"Incorrect counts: expected {expected_counts}, got {counts}")
                        return False
                else:
                    self.log_test("Seed Data Creation", False, f"Unexpected response: {data}")
                    return False
            else:
                self.log_test("Seed Data Creation", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Seed Data Creation", False, f"Exception: {str(e)}")
            return False
    
    def test_districts_get(self):
        """Test GET /api/districts - Fetch all districts"""
        try:
            response = self.session.get(f"{self.base_url}/districts")
            if response.status_code == 200:
                districts = response.json()
                if isinstance(districts, list) and len(districts) >= 6:
                    # Check if districts have required fields
                    required_fields = ['id', 'name_en', 'name_ta', 'slug']
                    first_district = districts[0]
                    has_all_fields = all(field in first_district for field in required_fields)
                    
                    if has_all_fields:
                        # Check for specific districts
                        district_names = [d['name_en'] for d in districts]
                        expected_districts = ['Chennai', 'Coimbatore', 'Madurai']
                        has_expected = all(name in district_names for name in expected_districts)
                        
                        if has_expected:
                            self.log_test("Districts GET", True, f"Retrieved {len(districts)} districts with all required fields")
                            return districts
                        else:
                            self.log_test("Districts GET", False, f"Missing expected districts. Got: {district_names}")
                            return False
                    else:
                        self.log_test("Districts GET", False, f"Districts missing required fields: {first_district}")
                        return False
                else:
                    self.log_test("Districts GET", False, f"Expected list with >=6 districts, got: {type(districts)} with {len(districts) if isinstance(districts, list) else 'N/A'} items")
                    return False
            else:
                self.log_test("Districts GET", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Districts GET", False, f"Exception: {str(e)}")
            return False
    
    def test_districts_post(self):
        """Test POST /api/districts - Create new district"""
        try:
            new_district = {
                "name_en": "Kanyakumari",
                "name_ta": "கன்னியாகுமரி",
                "slug": "kanyakumari"
            }
            
            response = self.session.post(f"{self.base_url}/districts", json=new_district)
            if response.status_code == 200:
                district = response.json()
                required_fields = ['id', 'name_en', 'name_ta', 'slug', 'createdAt']
                has_all_fields = all(field in district for field in required_fields)
                
                if has_all_fields and district['name_en'] == new_district['name_en']:
                    self.log_test("Districts POST", True, f"Successfully created district: {district['name_en']}")
                    return district
                else:
                    self.log_test("Districts POST", False, f"Created district missing fields or incorrect data: {district}")
                    return False
            else:
                self.log_test("Districts POST", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Districts POST", False, f"Exception: {str(e)}")
            return False
    
    def test_qualifications_get(self):
        """Test GET /api/qualifications - Fetch all qualifications"""
        try:
            response = self.session.get(f"{self.base_url}/qualifications")
            if response.status_code == 200:
                qualifications = response.json()
                if isinstance(qualifications, list) and len(qualifications) >= 7:
                    required_fields = ['id', 'name_en', 'name_ta', 'slug', 'order']
                    first_qual = qualifications[0]
                    has_all_fields = all(field in first_qual for field in required_fields)
                    
                    if has_all_fields:
                        # Check for specific qualifications
                        qual_names = [q['name_en'] for q in qualifications]
                        expected_quals = ['10th', '12th/HSC', 'B.E/B.Tech', 'Any Degree']
                        has_expected = all(name in qual_names for name in expected_quals)
                        
                        if has_expected:
                            self.log_test("Qualifications GET", True, f"Retrieved {len(qualifications)} qualifications with all required fields")
                            return qualifications
                        else:
                            self.log_test("Qualifications GET", False, f"Missing expected qualifications. Got: {qual_names}")
                            return False
                    else:
                        self.log_test("Qualifications GET", False, f"Qualifications missing required fields: {first_qual}")
                        return False
                else:
                    self.log_test("Qualifications GET", False, f"Expected list with >=7 qualifications, got: {len(qualifications) if isinstance(qualifications, list) else 'N/A'}")
                    return False
            else:
                self.log_test("Qualifications GET", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Qualifications GET", False, f"Exception: {str(e)}")
            return False
    
    def test_qualifications_post(self):
        """Test POST /api/qualifications - Create new qualification"""
        try:
            new_qualification = {
                "name_en": "M.Tech",
                "name_ta": "எம்.டெக்",
                "slug": "mtech",
                "order": 8
            }
            
            response = self.session.post(f"{self.base_url}/qualifications", json=new_qualification)
            if response.status_code == 200:
                qualification = response.json()
                required_fields = ['id', 'name_en', 'name_ta', 'slug', 'order', 'createdAt']
                has_all_fields = all(field in qualification for field in required_fields)
                
                if has_all_fields and qualification['name_en'] == new_qualification['name_en']:
                    self.log_test("Qualifications POST", True, f"Successfully created qualification: {qualification['name_en']}")
                    return qualification
                else:
                    self.log_test("Qualifications POST", False, f"Created qualification missing fields or incorrect data: {qualification}")
                    return False
            else:
                self.log_test("Qualifications POST", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Qualifications POST", False, f"Exception: {str(e)}")
            return False
    
    def test_categories_get(self):
        """Test GET /api/categories - Fetch all categories"""
        try:
            response = self.session.get(f"{self.base_url}/categories")
            if response.status_code == 200:
                categories = response.json()
                if isinstance(categories, list) and len(categories) >= 6:
                    required_fields = ['id', 'name_en', 'name_ta', 'slug', 'sector']
                    first_cat = categories[0]
                    has_all_fields = all(field in first_cat for field in required_fields)
                    
                    if has_all_fields:
                        # Check for specific categories
                        cat_names = [c['name_en'] for c in categories]
                        expected_cats = ['TNPSC', 'TRB', 'Police', 'Banking']
                        has_expected = all(name in cat_names for name in expected_cats)
                        
                        if has_expected:
                            self.log_test("Categories GET", True, f"Retrieved {len(categories)} categories with all required fields")
                            return categories
                        else:
                            self.log_test("Categories GET", False, f"Missing expected categories. Got: {cat_names}")
                            return False
                    else:
                        self.log_test("Categories GET", False, f"Categories missing required fields: {first_cat}")
                        return False
                else:
                    self.log_test("Categories GET", False, f"Expected list with >=6 categories, got: {len(categories) if isinstance(categories, list) else 'N/A'}")
                    return False
            else:
                self.log_test("Categories GET", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Categories GET", False, f"Exception: {str(e)}")
            return False
    
    def test_categories_post(self):
        """Test POST /api/categories - Create new category"""
        try:
            new_category = {
                "name_en": "Railway",
                "name_ta": "ரயில்வே",
                "slug": "railway",
                "sector": "central"
            }
            
            response = self.session.post(f"{self.base_url}/categories", json=new_category)
            if response.status_code == 200:
                category = response.json()
                required_fields = ['id', 'name_en', 'name_ta', 'slug', 'sector', 'createdAt']
                has_all_fields = all(field in category for field in required_fields)
                
                if has_all_fields and category['name_en'] == new_category['name_en']:
                    self.log_test("Categories POST", True, f"Successfully created category: {category['name_en']}")
                    return category
                else:
                    self.log_test("Categories POST", False, f"Created category missing fields or incorrect data: {category}")
                    return False
            else:
                self.log_test("Categories POST", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Categories POST", False, f"Exception: {str(e)}")
            return False
    
    def test_jobs_get_all(self):
        """Test GET /api/jobs - Fetch all jobs"""
        try:
            response = self.session.get(f"{self.base_url}/jobs")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and 'jobs' in data:
                    jobs = data['jobs']
                    if len(jobs) >= 2:
                        # Check job structure
                        required_fields = ['id', 'title', 'summary', 'vacancies', 'dept', 'sector', 'status']
                        first_job = jobs[0]
                        has_all_fields = all(field in first_job for field in required_fields)
                        
                        if has_all_fields:
                            # Check pagination info
                            has_pagination = all(key in data for key in ['total', 'page', 'totalPages'])
                            if has_pagination:
                                self.log_test("Jobs GET All", True, f"Retrieved {len(jobs)} jobs with pagination info. Total: {data['total']}")
                                return data
                            else:
                                self.log_test("Jobs GET All", False, f"Missing pagination info: {data.keys()}")
                                return False
                        else:
                            self.log_test("Jobs GET All", False, f"Jobs missing required fields: {first_job}")
                            return False
                    else:
                        self.log_test("Jobs GET All", False, f"Expected >=2 jobs, got: {len(jobs)}")
                        return False
                else:
                    self.log_test("Jobs GET All", False, f"Expected dict with 'jobs' key, got: {type(data)}")
                    return False
            else:
                self.log_test("Jobs GET All", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Jobs GET All", False, f"Exception: {str(e)}")
            return False
    
    def test_jobs_filtering(self, districts, qualifications, categories):
        """Test job filtering with various parameters"""
        if not districts or not qualifications or not categories:
            self.log_test("Jobs Filtering", False, "Missing reference data for filtering tests")
            return False
        
        try:
            # Test district filtering
            district_id = districts[0]['id']
            response = self.session.get(f"{self.base_url}/jobs?district={district_id}")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Jobs Filter by District", True, f"District filter returned {len(data.get('jobs', []))} jobs")
            else:
                self.log_test("Jobs Filter by District", False, f"HTTP {response.status_code}")
                return False
            
            # Test qualification filtering
            qual_id = qualifications[1]['id']  # 12th/HSC
            response = self.session.get(f"{self.base_url}/jobs?qualification={qual_id}")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Jobs Filter by Qualification", True, f"Qualification filter returned {len(data.get('jobs', []))} jobs")
            else:
                self.log_test("Jobs Filter by Qualification", False, f"HTTP {response.status_code}")
                return False
            
            # Test category filtering
            cat_id = categories[1]['id']  # TNPSC
            response = self.session.get(f"{self.base_url}/jobs?category={cat_id}")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Jobs Filter by Category", True, f"Category filter returned {len(data.get('jobs', []))} jobs")
            else:
                self.log_test("Jobs Filter by Category", False, f"HTTP {response.status_code}")
                return False
            
            # Test search functionality
            response = self.session.get(f"{self.base_url}/jobs?search=TNPSC")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Jobs Search", True, f"Search returned {len(data.get('jobs', []))} jobs")
            else:
                self.log_test("Jobs Search", False, f"HTTP {response.status_code}")
                return False
            
            # Test pagination
            response = self.session.get(f"{self.base_url}/jobs?page=1&limit=1")
            if response.status_code == 200:
                data = response.json()
                if len(data.get('jobs', [])) <= 1 and data.get('page') == 1:
                    self.log_test("Jobs Pagination", True, f"Pagination working correctly")
                else:
                    self.log_test("Jobs Pagination", False, f"Pagination not working as expected: {data}")
                    return False
            else:
                self.log_test("Jobs Pagination", False, f"HTTP {response.status_code}")
                return False
            
            # Test combined filters
            response = self.session.get(f"{self.base_url}/jobs?district={district_id}&qualification={qual_id}&search=Group")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Jobs Combined Filters", True, f"Combined filters returned {len(data.get('jobs', []))} jobs")
                return True
            else:
                self.log_test("Jobs Combined Filters", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Jobs Filtering", False, f"Exception: {str(e)}")
            return False
    
    def test_jobs_post(self, districts, qualifications, categories):
        """Test POST /api/jobs - Create new job"""
        if not districts or not qualifications or not categories:
            self.log_test("Jobs POST", False, "Missing reference data for job creation")
            return False
        
        try:
            future_date = (datetime.now() + timedelta(days=30)).isoformat()
            new_job = {
                "title": "Test Police Constable Recruitment 2025",
                "summary": "Test recruitment for police constable positions",
                "content": "Detailed job description for police constable recruitment",
                "vacancies": 500,
                "dept": "Tamil Nadu Police",
                "sector": "police",
                "board": "TNUSRB",
                "jobType": "permanent",
                "payScale": "₹21,700 - ₹69,100",
                "salaryFrom": 21700,
                "salaryTo": 69100,
                "ageMin": 18,
                "ageMax": 28,
                "fees": 500,
                "selectionProcess": "Physical Test + Written Exam",
                "mode": "offline",
                "lastDate": future_date,
                "districtId": districts[0]['id'],
                "qualificationIds": [qualifications[0]['id']],  # 10th
                "categoryIds": [categories[3]['id']],  # Police
                "tags": ["police", "constable", "government"],
                "status": "published"
            }
            
            response = self.session.post(f"{self.base_url}/jobs", json=new_job)
            if response.status_code == 200:
                job = response.json()
                required_fields = ['id', 'title', 'summary', 'vacancies', 'dept', 'sector', 'status']
                has_all_fields = all(field in job for field in required_fields)
                
                if has_all_fields and job['title'] == new_job['title']:
                    self.log_test("Jobs POST", True, f"Successfully created job: {job['title']}")
                    return job
                else:
                    self.log_test("Jobs POST", False, f"Created job missing fields or incorrect data: {job}")
                    return False
            else:
                self.log_test("Jobs POST", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Jobs POST", False, f"Exception: {str(e)}")
            return False
    
    def test_jobs_get_single(self, job_id):
        """Test GET /api/jobs/{id} - Get single job details"""
        if not job_id:
            self.log_test("Jobs GET Single", False, "No job ID provided")
            return False
        
        try:
            response = self.session.get(f"{self.base_url}/jobs/{job_id}")
            if response.status_code == 200:
                job = response.json()
                required_fields = ['id', 'title', 'summary', 'content', 'vacancies', 'dept']
                has_all_fields = all(field in job for field in required_fields)
                
                if has_all_fields and job['id'] == job_id:
                    self.log_test("Jobs GET Single", True, f"Successfully retrieved job: {job['title']}")
                    return job
                else:
                    self.log_test("Jobs GET Single", False, f"Job missing fields or incorrect ID: {job}")
                    return False
            elif response.status_code == 404:
                self.log_test("Jobs GET Single", False, f"Job not found (404) - this might be expected if job doesn't exist")
                return False
            else:
                self.log_test("Jobs GET Single", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Jobs GET Single", False, f"Exception: {str(e)}")
            return False
    
    def test_error_handling(self):
        """Test error handling for invalid routes and data"""
        try:
            # Test invalid route
            response = self.session.get(f"{self.base_url}/invalid-route")
            if response.status_code == 404:
                self.log_test("Error Handling - Invalid Route", True, "Correctly returned 404 for invalid route")
            else:
                self.log_test("Error Handling - Invalid Route", False, f"Expected 404, got {response.status_code}")
            
            # Test invalid job ID
            response = self.session.get(f"{self.base_url}/jobs/invalid-id")
            if response.status_code == 404:
                self.log_test("Error Handling - Invalid Job ID", True, "Correctly returned 404 for invalid job ID")
            else:
                self.log_test("Error Handling - Invalid Job ID", False, f"Expected 404, got {response.status_code}")
            
            return True
        except Exception as e:
            self.log_test("Error Handling", False, f"Exception: {str(e)}")
            return False
    
    def test_cors_headers(self):
        """Test CORS headers are properly set"""
        try:
            response = self.session.options(f"{self.base_url}")
            if response.status_code == 200:
                headers = response.headers
                cors_headers = [
                    'Access-Control-Allow-Origin',
                    'Access-Control-Allow-Methods',
                    'Access-Control-Allow-Headers'
                ]
                has_cors = all(header in headers for header in cors_headers)
                
                if has_cors:
                    self.log_test("CORS Headers", True, "All required CORS headers present")
                    return True
                else:
                    self.log_test("CORS Headers", False, f"Missing CORS headers. Present: {list(headers.keys())}")
                    return False
            else:
                self.log_test("CORS Headers", False, f"OPTIONS request failed: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("CORS Headers", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all backend API tests"""
        print(f"🚀 Starting TamilansJob.com Backend API Tests")
        print(f"📍 Base URL: {self.base_url}")
        print("=" * 80)
        
        # Test 1: Root endpoint
        self.test_root_endpoint()
        
        # Test 2: Initialize seed data
        seed_success = self.test_seed_data()
        
        # Test 3: Districts API
        districts = self.test_districts_get()
        self.test_districts_post()
        
        # Test 4: Qualifications API
        qualifications = self.test_qualifications_get()
        self.test_qualifications_post()
        
        # Test 5: Categories API
        categories = self.test_categories_get()
        self.test_categories_post()
        
        # Test 6: Jobs API
        jobs_data = self.test_jobs_get_all()
        
        # Test 7: Job filtering (only if we have reference data)
        if districts and qualifications and categories:
            self.test_jobs_filtering(districts, qualifications, categories)
        
        # Test 8: Create new job
        new_job = None
        if districts and qualifications and categories:
            new_job = self.test_jobs_post(districts, qualifications, categories)
        
        # Test 9: Get single job (use created job or first from seed data)
        job_id = None
        if new_job:
            job_id = new_job['id']
        elif jobs_data and jobs_data.get('jobs'):
            job_id = jobs_data['jobs'][0]['id']
        
        if job_id:
            self.test_jobs_get_single(job_id)
        
        # Test 10: Error handling
        self.test_error_handling()
        
        # Test 11: CORS headers
        self.test_cors_headers()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if total - passed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  • {result['test']}: {result['message']}")
        
        print("\n✅ PASSED TESTS:")
        for result in self.test_results:
            if result['success']:
                print(f"  • {result['test']}")
        
        return self.test_results

if __name__ == "__main__":
    tester = TamilansJobAPITester()
    results = tester.run_all_tests()