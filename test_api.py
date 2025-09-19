#!/usr/bin/env python3
"""
Test script for the FastAPI service

This script tests all API endpoints to ensure they work correctly.
"""

import requests
import json
import time
import os
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
TEST_IMAGE_PATH = "assets/images/living_room.png"

def test_health():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_templates():
    """Test template generation endpoint"""
    print("🔍 Testing template generation...")
    try:
        data = {
            "template_type": "text",
            "subject": "modern sofa",
            "style": "photorealistic",
            "context": "interior design"
        }
        response = requests.post(f"{BASE_URL}/api/templates", json=data)
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ Template generation passed")
                print(f"   Generated: {result['data']['template']}")
                return True
            else:
                print(f"❌ Template generation failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Template generation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Template generation error: {e}")
        return False

def test_styles():
    """Test styles endpoint"""
    print("🔍 Testing styles endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/styles")
        if response.status_code == 200:
            data = response.json()
            print("✅ Styles endpoint passed")
            print(f"   Available styles: {len(data.get('styles', []))}")
            print(f"   Available angles: {len(data.get('angles', []))}")
            return True
        else:
            print(f"❌ Styles endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Styles endpoint error: {e}")
        return False

def test_generate():
    """Test image generation endpoint"""
    print("🔍 Testing image generation...")
    try:
        data = {
            "prompt": "a simple test image",
            "style": "photorealistic",
            "output_filename": "test_generate"
        }
        response = requests.post(f"{BASE_URL}/api/generate", json=data)
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ Image generation passed")
                return True
            else:
                print(f"❌ Image generation failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Image generation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Image generation error: {e}")
        return False

def test_edit():
    """Test image editing endpoint"""
    print("🔍 Testing image editing...")
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"⚠️  Test image not found: {TEST_IMAGE_PATH}")
        return True  # Skip this test
    
    try:
        with open(TEST_IMAGE_PATH, 'rb') as f:
            files = {'file': f}
            data = {
                'prompt': 'add a test element',
                'output_filename': 'test_edit'
            }
            response = requests.post(f"{BASE_URL}/api/edit", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ Image editing passed")
                return True
            else:
                print(f"❌ Image editing failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Image editing failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Image editing error: {e}")
        return False

def test_clean():
    """Test room cleaning endpoint"""
    print("🔍 Testing room cleaning...")
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"⚠️  Test image not found: {TEST_IMAGE_PATH}")
        return True  # Skip this test
    
    try:
        with open(TEST_IMAGE_PATH, 'rb') as f:
            files = {'file': f}
            data = {
                'objects': 'test objects',
                'maintain_layout': True,
                'output_filename': 'test_clean'
            }
            response = requests.post(f"{BASE_URL}/api/clean", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ Room cleaning passed")
                return True
            else:
                print(f"❌ Room cleaning failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Room cleaning failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Room cleaning error: {e}")
        return False

def test_style():
    """Test style transfer endpoint"""
    print("🔍 Testing style transfer...")
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"⚠️  Test image not found: {TEST_IMAGE_PATH}")
        return True  # Skip this test
    
    try:
        with open(TEST_IMAGE_PATH, 'rb') as f:
            files = {'file': f}
            data = {
                'target_style': 'artistic',
                'output_filename': 'test_style'
            }
            response = requests.post(f"{BASE_URL}/api/style", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ Style transfer passed")
                return True
            else:
                print(f"❌ Style transfer failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Style transfer failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Style transfer error: {e}")
        return False

def test_composition():
    """Test multi-image composition endpoint"""
    print("🔍 Testing multi-image composition...")
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"⚠️  Test image not found: {TEST_IMAGE_PATH}")
        return True  # Skip this test
    
    try:
        with open(TEST_IMAGE_PATH, 'rb') as f:
            files = [('files', f), ('files', f)]  # Use same image twice
            data = {
                'goal': 'test composition',
                'blending': 'seamless',
                'output_filename': 'test_composition'
            }
            response = requests.post(f"{BASE_URL}/api/composition", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ Multi-image composition passed")
                return True
            else:
                print(f"❌ Multi-image composition failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Multi-image composition failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Multi-image composition error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting API tests...")
    print(f"   Base URL: {BASE_URL}")
    print(f"   Test image: {TEST_IMAGE_PATH}")
    print()
    
    tests = [
        test_health,
        test_templates,
        test_styles,
        test_generate,
        test_edit,
        test_clean,
        test_style,
        test_composition
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1

if __name__ == "__main__":
    exit(main())
