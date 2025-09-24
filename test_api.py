#!/usr/bin/env python3
"""
Simple test script to verify StyleAgent API functionality
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None, headers=None):
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    if headers is None:
        headers = {"accept": "application/json"}
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        print(f"🔍 Testing {method} {endpoint}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   Response: {json.dumps(result, indent=2)}")
                print("✅ Success\n")
                return True
            except json.JSONDecodeError:
                print(f"   Response: {response.text[:100]}...")
                print("✅ Success (non-JSON response)\n")
                return True
        else:
            print(f"   Error: {response.text}")
            print("❌ Failed\n")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection failed to {url}")
        print("   Make sure the server is running on http://localhost:8000\n")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        return False

def main():
    """Run basic API tests"""
    print("🚀 StyleAgent API Test Suite")
    print("=" * 40)
    
    # Test basic endpoints
    tests = [
        ("/", "GET"),
        ("/health", "GET"),
        ("/docs", "GET"),  # This will return HTML
    ]
    
    passed = 0
    total = len(tests)
    
    for endpoint, method in tests:
        if test_endpoint(endpoint, method):
            passed += 1
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic tests passed! The API is running correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())