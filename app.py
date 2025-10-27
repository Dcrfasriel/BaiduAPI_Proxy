#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baidu API Proxy Service (百度API转接服务)
A proxy service for forwarding requests to Baidu APIs
"""

import json
import hashlib
import random
import requests
from flask import Flask, request, jsonify
from pathlib import Path

app = Flask(__name__)

# Load configuration
def load_config():
    """Load configuration from config.json"""
    config_path = Path(__file__).parent / 'config.json'
    if not config_path.exists():
        # Try loading example config for demo purposes
        config_path = Path(__file__).parent / 'config.example.json'
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

config = load_config()

def generate_sign(query, salt, app_id, secret_key):
    """
    Generate sign for Baidu Translation API
    Formula: md5(appid + query + salt + secret_key)
    """
    sign_str = app_id + query + str(salt) + secret_key
    md5 = hashlib.md5()
    md5.update(sign_str.encode('utf-8'))
    return md5.hexdigest()

@app.route('/')
def index():
    """API service index"""
    return jsonify({
        'service': 'Baidu API Proxy Service',
        'description': '百度API转接服务',
        'version': '1.0.0',
        'endpoints': [
            '/api/translate - Baidu Translation API',
            '/api/nlp/sentiment - Baidu NLP Sentiment Analysis',
            '/health - Health check'
        ]
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'baidu-api-proxy'})

@app.route('/api/translate', methods=['POST'])
def translate():
    """
    Proxy for Baidu Translation API
    Expected JSON payload:
    {
        "query": "text to translate",
        "from": "source language (e.g., 'en', 'zh')",
        "to": "target language (e.g., 'zh', 'en')"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        query = data.get('query', '')
        from_lang = data.get('from', 'auto')
        to_lang = data.get('to', 'zh')
        
        if not query:
            return jsonify({'error': 'Query text is required'}), 400
        
        # Prepare request to Baidu API
        app_id = config['baidu']['app_id']
        secret_key = config['baidu']['secret_key']
        salt = random.randint(32768, 65536)
        
        sign = generate_sign(query, salt, app_id, secret_key)
        
        # Baidu Translation API endpoint
        url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
        
        params = {
            'q': query,
            'from': from_lang,
            'to': to_lang,
            'appid': app_id,
            'salt': salt,
            'sign': sign
        }
        
        # Forward request to Baidu API
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        
        return jsonify(result), response.status_code
        
    except Exception as e:
        app.logger.error(f'Translation error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/nlp/sentiment', methods=['POST'])
def sentiment_analysis():
    """
    Proxy for Baidu NLP Sentiment Analysis API
    Expected JSON payload:
    {
        "text": "text to analyze"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Get access token for Baidu AI APIs
        api_key = config['baidu']['api_key']
        secret_key = config['baidu']['secret_key']
        
        # OAuth 2.0 token endpoint
        token_url = 'https://aip.baidubce.com/oauth/2.0/token'
        token_params = {
            'grant_type': 'client_credentials',
            'client_id': api_key,
            'client_secret': secret_key
        }
        
        token_response = requests.post(token_url, params=token_params, timeout=10)
        token_data = token_response.json()
        
        if 'access_token' not in token_data:
            return jsonify({'error': 'Failed to get access token', 'details': token_data}), 500
        
        access_token = token_data['access_token']
        
        # Sentiment analysis endpoint
        sentiment_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify'
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        params = {
            'access_token': access_token
        }
        
        payload = {
            'text': text
        }
        
        # Forward request to Baidu NLP API
        response = requests.post(
            sentiment_url,
            params=params,
            headers=headers,
            json=payload,
            timeout=10
        )
        
        result = response.json()
        
        return jsonify(result), response.status_code
        
    except Exception as e:
        app.logger.error(f'Sentiment analysis error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    host = config.get('server', {}).get('host', '0.0.0.0')
    port = config.get('server', {}).get('port', 5000)
    debug = config.get('server', {}).get('debug', False)
    
    print(f'Starting Baidu API Proxy Service on {host}:{port}')
    app.run(host=host, port=port, debug=debug)
