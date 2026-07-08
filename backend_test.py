#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for E-commerce with Wasay Inquiry System
Tests all 3 API endpoints with various scenarios
"""

import requests
import json
from datetime import datetime

# Backend URL from frontend/.env
BASE_URL = "https://commerce-3d-wasay.preview.emergentagent.com/api"

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Test results tracking
test_results = {
    "passed": 0,
    "failed": 0,
    "total": 0
}

def print_test_header(test_name):
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}TEST: {test_name}{RESET}")
    print(f"{BLUE}{'='*80}{RESET}")

def print_result(passed, message, details=None):
    test_results["total"] += 1
    if passed:
        test_results["passed"] += 1
        print(f"{GREEN}✓ PASS:{RESET} {message}")
    else:
        test_results["failed"] += 1
        print(f"{RED}✗ FAIL:{RESET} {message}")
    
    if details:
        print(f"  Details: {details}")

def print_summary():
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}TEST SUMMARY{RESET}")
    print(f"{BLUE}{'='*80}{RESET}")
    print(f"Total Tests: {test_results['total']}")
    print(f"{GREEN}Passed: {test_results['passed']}{RESET}")
    print(f"{RED}Failed: {test_results['failed']}{RESET}")
    
    if test_results['failed'] == 0:
        print(f"\n{GREEN}ALL TESTS PASSED!{RESET}")
    else:
        print(f"\n{RED}SOME TESTS FAILED!{RESET}")

# ============================================================================
# TEST 1: POST /api/inquiries/contact
# ============================================================================

def test_contact_inquiry_valid_all_fields():
    """Test contact inquiry with all fields including optional phone"""
    print_test_header("Contact Inquiry - Valid Data (All Fields)")
    
    payload = {
        "name": "John Smith",
        "email": "john.smith@example.com",
        "phone": "+1-555-0123",
        "message": "I'm interested in your Amazon FBA services. Can you provide more details?"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/inquiries/contact", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check response structure
            has_success = "success" in data and data["success"] == True
            has_message = "message" in data and isinstance(data["message"], str)
            has_inquiry_id = "inquiry_id" in data and isinstance(data["inquiry_id"], str)
            
            if has_success and has_message and has_inquiry_id:
                print_result(True, "Valid contact inquiry with all fields accepted", 
                           f"inquiry_id: {data['inquiry_id']}")
                return data["inquiry_id"]
            else:
                print_result(False, "Response structure incorrect", 
                           f"Response: {json.dumps(data, indent=2)}")
                return None
        else:
            print_result(False, f"Expected status 200, got {response.status_code}", 
                       f"Response: {response.text}")
            return None
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")
        return None

def test_contact_inquiry_valid_without_phone():
    """Test contact inquiry without optional phone field"""
    print_test_header("Contact Inquiry - Valid Data (Without Optional Phone)")
    
    payload = {
        "name": "Sarah Johnson",
        "email": "sarah.j@example.com",
        "message": "I would like to know more about your eBay listing services and pricing."
    }
    
    try:
        response = requests.post(f"{BASE_URL}/inquiries/contact", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and "inquiry_id" in data:
                print_result(True, "Valid contact inquiry without phone accepted", 
                           f"inquiry_id: {data['inquiry_id']}")
                return data["inquiry_id"]
            else:
                print_result(False, "Response structure incorrect", 
                           f"Response: {json.dumps(data, indent=2)}")
                return None
        else:
            print_result(False, f"Expected status 200, got {response.status_code}", 
                       f"Response: {response.text}")
            return None
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")
        return None

def test_contact_inquiry_missing_name():
    """Test contact inquiry with missing required name field"""
    print_test_header("Contact Inquiry - Missing Required Field (name)")
    
    payload = {
        "email": "test@example.com",
        "message": "This is a test message with at least 10 characters."
    }
    
    try:
        response = requests.post(f"{BASE_URL}/inquiries/contact", json=payload, timeout=10)
        
        if response.status_code == 422:  # Pydantic validation error
            print_result(True, "Missing name field correctly rejected with 422")
        else:
            print_result(False, f"Expected status 422, got {response.status_code}", 
                       f"Response: {response.text}")
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")

def test_contact_inquiry_missing_email():
    """Test contact inquiry with missing required email field"""
    print_test_header("Contact Inquiry - Missing Required Field (email)")
    
    payload = {
        "name": "Test User",
        "message": "This is a test message with at least 10 characters."
    }
    
    try:
        response = requests.post(f"{BASE_URL}/inquiries/contact", json=payload, timeout=10)
        
        if response.status_code == 422:
            print_result(True, "Missing email field correctly rejected with 422")
        else:
            print_result(False, f"Expected status 422, got {response.status_code}", 
                       f"Response: {response.text}")
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")

def test_contact_inquiry_missing_message():
    """Test contact inquiry with missing required message field"""
    print_test_header("Contact Inquiry - Missing Required Field (message)")
    
    payload = {
        "name": "Test User",
        "email": "test@example.com"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/inquiries/contact", json=payload, timeout=10)
        
        if response.status_code == 422:
            print_result(True, "Missing message field correctly rejected with 422")
        else:
            print_result(False, f"Expected status 422, got {response.status_code}", 
                       f"Response: {response.text}")
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")

def test_contact_inquiry_invalid_email():
    """Test contact inquiry with invalid email format"""
    print_test_header("Contact Inquiry - Invalid Email Format")
    
    payload = {
        "name": "Test User",
        "email": "invalid-email-format",
        "message": "This is a test message with at least 10 characters."
    }
    
    try:
        response = requests.post(f"{BASE_URL}/inquiries/contact", json=payload, timeout=10)
        
        if response.status_code == 422:
            print_result(True, "Invalid email format correctly rejected with 422")
        else:
            print_result(False, f"Expected status 422, got {response.status_code}", 
                       f"Response: {response.text}")
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")

def test_contact_inquiry_short_message():
    """Test contact inquiry with message less than 10 characters"""
    print_test_header("Contact Inquiry - Message Too Short (< 10 chars)")
    
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "message": "Short"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/inquiries/contact", json=payload, timeout=10)
        
        if response.status_code == 422:
            print_result(True, "Short message correctly rejected with 422")
        else:
            print_result(False, f"Expected status 422, got {response.status_code}", 
                       f"Response: {response.text}")
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")

# ============================================================================
# TEST 2: POST /api/inquiries/package
# ============================================================================

def test_package_inquiry_starter():
    """Test package inquiry for Starter package"""
    print_test_header("Package Inquiry - Starter Package (All Fields)")
    
    payload = {
        "name": "Michael Brown",
        "email": "michael.b@example.com",
        "phone": "+1-555-0456",
        "package_name": "Starter",
        "message": "I'm a beginner and interested in the Starter package. What's included?"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/inquiries/package", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and "inquiry_id" in data:
                print_result(True, "Starter package inquiry accepted", 
                           f"inquiry_id: {data['inquiry_id']}")
                return data["inquiry_id"]
            else:
                print_result(False, "Response structure incorrect", 
                           f"Response: {json.dumps(data, indent=2)}")
                return None
        else:
            print_result(False, f"Expected status 200, got {response.status_code}", 
                       f"Response: {response.text}")
            return None
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")
        return None

def test_package_inquiry_professional():
    """Test package inquiry for Professional package"""
    print_test_header("Package Inquiry - Professional Package (All Fields)")
    
    payload = {
        "name": "Emily Davis",
        "email": "emily.davis@example.com",
        "phone": "+1-555-0789",
        "package_name": "Professional",
        "message": "Looking for professional services to scale my business on Amazon."
    }
    
    try:
        response = requests.post(f"{BASE_URL}/inquiries/package", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and "inquiry_id" in data:
                print_result(True, "Professional package inquiry accepted", 
                           f"inquiry_id: {data['inquiry_id']}")
                return data["inquiry_id"]
            else:
                print_result(False, "Response structure incorrect", 
                           f"Response: {json.dumps(data, indent=2)}")
                return None
        else:
            print_result(False, f"Expected status 200, got {response.status_code}", 
                       f"Response: {response.text}")
            return None
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")
        return None

def test_package_inquiry_enterprise():
    """Test package inquiry for Enterprise package"""
    print_test_header("Package Inquiry - Enterprise Package (All Fields)")
    
    payload = {
        "name": "Robert Wilson",
        "email": "robert.w@example.com",
        "phone": "+1-555-0321",
        "package_name": "Enterprise",
        "message": "Need enterprise-level support for multiple marketplaces."
    }
    
    try:
        response = requests.post(f"{BASE_URL}/inquiries/package", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and "inquiry_id" in data:
                print_result(True, "Enterprise package inquiry accepted", 
                           f"inquiry_id: {data['inquiry_id']}")
                return data["inquiry_id"]
            else:
                print_result(False, "Response structure incorrect", 
                           f"Response: {json.dumps(data, indent=2)}")
                return None
        else:
            print_result(False, f"Expected status 200, got {response.status_code}", 
                       f"Response: {response.text}")
            return None
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")
        return None

def test_package_inquiry_without_optional_fields():
    """Test package inquiry without optional phone and message"""
    print_test_header("Package Inquiry - Without Optional Fields (phone, message)")
    
    payload = {
        "name": "Lisa Anderson",
        "email": "lisa.a@example.com",
        "package_name": "Professional"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/inquiries/package", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and "inquiry_id" in data:
                print_result(True, "Package inquiry without optional fields accepted", 
                           f"inquiry_id: {data['inquiry_id']}")
                return data["inquiry_id"]
            else:
                print_result(False, "Response structure incorrect", 
                           f"Response: {json.dumps(data, indent=2)}")
                return None
        else:
            print_result(False, f"Expected status 200, got {response.status_code}", 
                       f"Response: {response.text}")
            return None
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")
        return None

def test_package_inquiry_missing_package_name():
    """Test package inquiry with missing required package_name"""
    print_test_header("Package Inquiry - Missing Required Field (package_name)")
    
    payload = {
        "name": "Test User",
        "email": "test@example.com"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/inquiries/package", json=payload, timeout=10)
        
        if response.status_code == 422:
            print_result(True, "Missing package_name correctly rejected with 422")
        else:
            print_result(False, f"Expected status 422, got {response.status_code}", 
                       f"Response: {response.text}")
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")

def test_package_inquiry_invalid_package_name():
    """Test package inquiry with invalid package_name"""
    print_test_header("Package Inquiry - Invalid package_name")
    
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "package_name": "InvalidPackage"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/inquiries/package", json=payload, timeout=10)
        
        if response.status_code == 422:
            print_result(True, "Invalid package_name correctly rejected with 422")
        else:
            print_result(False, f"Expected status 422, got {response.status_code}", 
                       f"Response: {response.text}")
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")

def test_package_inquiry_invalid_email():
    """Test package inquiry with invalid email format"""
    print_test_header("Package Inquiry - Invalid Email Format")
    
    payload = {
        "name": "Test User",
        "email": "not-an-email",
        "package_name": "Starter"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/inquiries/package", json=payload, timeout=10)
        
        if response.status_code == 422:
            print_result(True, "Invalid email format correctly rejected with 422")
        else:
            print_result(False, f"Expected status 422, got {response.status_code}", 
                       f"Response: {response.text}")
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")

# ============================================================================
# TEST 3: GET /api/inquiries
# ============================================================================

def test_get_all_inquiries():
    """Test GET inquiries without filters"""
    print_test_header("Get Inquiries - No Filters (All)")
    
    try:
        response = requests.get(f"{BASE_URL}/inquiries", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check response structure
            has_success = "success" in data and data["success"] == True
            has_count = "count" in data and isinstance(data["count"], int)
            has_inquiries = "inquiries" in data and isinstance(data["inquiries"], list)
            
            if has_success and has_count and has_inquiries:
                print_result(True, f"Retrieved all inquiries successfully", 
                           f"Count: {data['count']}")
                
                # Check if inquiries have proper structure
                if data["count"] > 0:
                    first_inquiry = data["inquiries"][0]
                    has_id = "id" in first_inquiry and isinstance(first_inquiry["id"], str)
                    has_type = "type" in first_inquiry
                    has_created_at = "created_at" in first_inquiry
                    
                    if has_id and has_type and has_created_at:
                        print_result(True, "Inquiry structure is correct", 
                                   f"Sample: {json.dumps(first_inquiry, indent=2, default=str)}")
                    else:
                        print_result(False, "Inquiry structure missing required fields")
                
                return data["inquiries"]
            else:
                print_result(False, "Response structure incorrect", 
                           f"Response: {json.dumps(data, indent=2)}")
                return None
        else:
            print_result(False, f"Expected status 200, got {response.status_code}", 
                       f"Response: {response.text}")
            return None
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")
        return None

def test_get_inquiries_by_type_contact():
    """Test GET inquiries filtered by type=contact"""
    print_test_header("Get Inquiries - Filter by type=contact")
    
    try:
        response = requests.get(f"{BASE_URL}/inquiries?type=contact", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and "inquiries" in data:
                # Verify all returned inquiries are of type 'contact'
                all_contact = all(inq.get("type") == "contact" for inq in data["inquiries"])
                
                if all_contact:
                    print_result(True, f"Retrieved contact inquiries only", 
                               f"Count: {data['count']}")
                else:
                    print_result(False, "Some inquiries are not of type 'contact'")
            else:
                print_result(False, "Response structure incorrect")
        else:
            print_result(False, f"Expected status 200, got {response.status_code}")
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")

def test_get_inquiries_by_type_package():
    """Test GET inquiries filtered by type=package"""
    print_test_header("Get Inquiries - Filter by type=package")
    
    try:
        response = requests.get(f"{BASE_URL}/inquiries?type=package", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and "inquiries" in data:
                # Verify all returned inquiries are of type 'package'
                all_package = all(inq.get("type") == "package" for inq in data["inquiries"])
                
                if all_package:
                    print_result(True, f"Retrieved package inquiries only", 
                               f"Count: {data['count']}")
                else:
                    print_result(False, "Some inquiries are not of type 'package'")
            else:
                print_result(False, "Response structure incorrect")
        else:
            print_result(False, f"Expected status 200, got {response.status_code}")
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")

def test_get_inquiries_by_status():
    """Test GET inquiries filtered by status=pending"""
    print_test_header("Get Inquiries - Filter by status=pending")
    
    try:
        response = requests.get(f"{BASE_URL}/inquiries?status=pending", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and "inquiries" in data:
                # Verify all returned inquiries have status 'pending'
                all_pending = all(inq.get("status") == "pending" for inq in data["inquiries"])
                
                if all_pending:
                    print_result(True, f"Retrieved pending inquiries only", 
                               f"Count: {data['count']}")
                else:
                    print_result(False, "Some inquiries are not of status 'pending'")
            else:
                print_result(False, "Response structure incorrect")
        else:
            print_result(False, f"Expected status 200, got {response.status_code}")
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")

def test_get_inquiries_with_limit():
    """Test GET inquiries with limit parameter"""
    print_test_header("Get Inquiries - With limit=3")
    
    try:
        response = requests.get(f"{BASE_URL}/inquiries?limit=3", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and "inquiries" in data:
                count = len(data["inquiries"])
                
                if count <= 3:
                    print_result(True, f"Limit parameter working correctly", 
                               f"Returned: {count} inquiries")
                else:
                    print_result(False, f"Limit not respected, returned {count} inquiries")
            else:
                print_result(False, "Response structure incorrect")
        else:
            print_result(False, f"Expected status 200, got {response.status_code}")
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")

def test_get_inquiries_sorted_by_created_at():
    """Test that inquiries are sorted by created_at descending"""
    print_test_header("Get Inquiries - Verify Sorting by created_at DESC")
    
    try:
        response = requests.get(f"{BASE_URL}/inquiries", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and data.get("count", 0) > 1:
                inquiries = data["inquiries"]
                
                # Check if sorted in descending order
                is_sorted = True
                for i in range(len(inquiries) - 1):
                    current = inquiries[i].get("created_at")
                    next_item = inquiries[i + 1].get("created_at")
                    
                    if current and next_item:
                        if current < next_item:
                            is_sorted = False
                            break
                
                if is_sorted:
                    print_result(True, "Inquiries correctly sorted by created_at DESC")
                else:
                    print_result(False, "Inquiries not sorted correctly")
            else:
                print_result(True, "Not enough inquiries to verify sorting (need at least 2)")
        else:
            print_result(False, f"Expected status 200, got {response.status_code}")
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")

def test_get_inquiries_objectid_converted():
    """Test that MongoDB ObjectId is converted to string in response"""
    print_test_header("Get Inquiries - Verify ObjectId Conversion to String")
    
    try:
        response = requests.get(f"{BASE_URL}/inquiries?limit=1", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and data.get("count", 0) > 0:
                inquiry = data["inquiries"][0]
                
                # Check that 'id' field exists and is a string
                has_id = "id" in inquiry
                is_string = isinstance(inquiry.get("id"), str)
                no_underscore_id = "_id" not in inquiry
                
                if has_id and is_string and no_underscore_id:
                    print_result(True, "ObjectId correctly converted to 'id' string field", 
                               f"id: {inquiry['id']}")
                else:
                    print_result(False, "ObjectId conversion issue", 
                               f"has_id: {has_id}, is_string: {is_string}, no_underscore_id: {no_underscore_id}")
            else:
                print_result(True, "No inquiries to verify ObjectId conversion")
        else:
            print_result(False, f"Expected status 200, got {response.status_code}")
    except Exception as e:
        print_result(False, f"Request failed with exception: {str(e)}")

# ============================================================================
# MAIN TEST EXECUTION
# ============================================================================

def main():
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}E-COMMERCE WITH WASAY - BACKEND API TESTS{RESET}")
    print(f"{BLUE}{'='*80}{RESET}")
    print(f"Backend URL: {BASE_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Store inquiry IDs for verification
    inquiry_ids = []
    
    # Test 1: POST /api/inquiries/contact
    print(f"\n{YELLOW}{'='*80}{RESET}")
    print(f"{YELLOW}SECTION 1: CONTACT INQUIRY API TESTS{RESET}")
    print(f"{YELLOW}{'='*80}{RESET}")
    
    id1 = test_contact_inquiry_valid_all_fields()
    if id1:
        inquiry_ids.append(id1)
    
    id2 = test_contact_inquiry_valid_without_phone()
    if id2:
        inquiry_ids.append(id2)
    
    test_contact_inquiry_missing_name()
    test_contact_inquiry_missing_email()
    test_contact_inquiry_missing_message()
    test_contact_inquiry_invalid_email()
    test_contact_inquiry_short_message()
    
    # Test 2: POST /api/inquiries/package
    print(f"\n{YELLOW}{'='*80}{RESET}")
    print(f"{YELLOW}SECTION 2: PACKAGE INQUIRY API TESTS{RESET}")
    print(f"{YELLOW}{'='*80}{RESET}")
    
    id3 = test_package_inquiry_starter()
    if id3:
        inquiry_ids.append(id3)
    
    id4 = test_package_inquiry_professional()
    if id4:
        inquiry_ids.append(id4)
    
    id5 = test_package_inquiry_enterprise()
    if id5:
        inquiry_ids.append(id5)
    
    id6 = test_package_inquiry_without_optional_fields()
    if id6:
        inquiry_ids.append(id6)
    
    test_package_inquiry_missing_package_name()
    test_package_inquiry_invalid_package_name()
    test_package_inquiry_invalid_email()
    
    # Test 3: GET /api/inquiries
    print(f"\n{YELLOW}{'='*80}{RESET}")
    print(f"{YELLOW}SECTION 3: GET INQUIRIES API TESTS{RESET}")
    print(f"{YELLOW}{'='*80}{RESET}")
    
    all_inquiries = test_get_all_inquiries()
    test_get_inquiries_by_type_contact()
    test_get_inquiries_by_type_package()
    test_get_inquiries_by_status()
    test_get_inquiries_with_limit()
    test_get_inquiries_sorted_by_created_at()
    test_get_inquiries_objectid_converted()
    
    # Print summary
    print_summary()
    
    # Print created inquiry IDs
    if inquiry_ids:
        print(f"\n{BLUE}Created Inquiry IDs:{RESET}")
        for idx, inquiry_id in enumerate(inquiry_ids, 1):
            print(f"  {idx}. {inquiry_id}")

if __name__ == "__main__":
    main()
