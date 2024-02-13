#!/usr/bin/env python

import os
from collections import defaultdict
from urllib.parse import urljoin
import requests

from flask import Flask
from flask import render_template

app = Flask(__name__)

probely_api_token = os.getenv("PROBELY_API_TOKEN") or exit("PROBELY_API_TOKEN environment variable is required")

def api_headers(api_token):
  """Get the appropriate API headers for Probely"""
  return {
      "Authorization": f"JWT {api_token}",
      "Content-Type": "application/json"
      }

@app.route('/')
def hello_world():

  #Count high vulnerabilities 
  API_BASE_URL = "https://api.probely.com"
  account_findings_endpoint = urljoin(
      API_BASE_URL, "findings/?severity=30&state=notfixed&length=0"
  )

  response= requests.get(account_findings_endpoint,
                          headers=api_headers(probely_api_token),
                          timeout=30)

  response_json = response.json()
  vulnerability_count_high = response_json['count']
  
  # #Count medium vulnerabilities
  API_BASE_URL = "https://api.probely.com"
  account_findings_endpoint = urljoin(
      API_BASE_URL, "findings/?severity=20&state=notfixed&length=0"
  )

  response = requests.get(account_findings_endpoint,
                          headers=api_headers(probely_api_token),
                          timeout=30)

  response_json = response.json()
  vulnerability_count_medium = response_json['count']

  #Count low vulnerabilities
  API_BASE_URL = "https://api.probely.com"
  account_findings_endpoint = urljoin(
      API_BASE_URL, "findings/?severity=10&state=notfixed&length=0"
  )

  response = requests.get(account_findings_endpoint,
                          headers=api_headers(probely_api_token),
                          timeout=30)

  response_json = response.json()
  vulnerability_count_low = response_json['count']


  return render_template('dashboard.html', title='Security dashboard', vulnerability_count_high=vulnerability_count_high ,vulnerability_count_medium=vulnerability_count_medium,vulnerability_count_low=vulnerability_count_low)
