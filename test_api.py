#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Baidu API Proxy Service
"""

import requests
import json
import time
import subprocess
import sys
from threading import Thread

def start_server():
    """Start the Flask server in background"""
    import os
    # Change to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    subprocess.run([sys.executable, 'app.py'], cwd=script_dir)

def test_health_endpoint():
    """Test health check endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200
        assert response.json()['status'] == 'healthy'
        print("✓ Health check passed\n")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}\n")
        return False

def test_index_endpoint():
    """Test index endpoint"""
    print("Testing index endpoint...")
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200
        assert 'service' in response.json()
        print("✓ Index endpoint passed\n")
        return True
    except Exception as e:
        print(f"✗ Index endpoint failed: {e}\n")
        return False

def test_translate_endpoint():
    """Test translation endpoint (will fail without valid credentials)"""
    print("Testing translate endpoint...")
    try:
        data = {
            "query": "Hello",
            "from": "en",
            "to": "zh"
        }
        response = requests.post('http://localhost:5000/api/translate', json=data, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        # This will likely fail without valid credentials, but endpoint should respond
        print("✓ Translate endpoint is accessible\n")
        return True
    except Exception as e:
        print(f"✗ Translate endpoint failed: {e}\n")
        return False

def test_sentiment_endpoint():
    """Test sentiment analysis endpoint (will fail without valid credentials)"""
    print("Testing sentiment analysis endpoint...")
    try:
        data = {
            "text": "这个很好"
        }
        response = requests.post('http://localhost:5000/api/nlp/sentiment', json=data, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        # This will likely fail without valid credentials, but endpoint should respond
        print("✓ Sentiment endpoint is accessible\n")
        return True
    except Exception as e:
        print(f"✗ Sentiment endpoint failed: {e}\n")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Baidu API Proxy Service Test Suite")
    print("=" * 60)
    print()
    
    # Start server in background thread
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    print()
    
    # Run tests
    results = []
    results.append(test_health_endpoint())
    results.append(test_index_endpoint())
    results.append(test_translate_endpoint())
    results.append(test_sentiment_endpoint())
    
    # Summary
    print("=" * 60)
    print(f"Tests completed: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    sys.exit(0 if all(results) else 1)
