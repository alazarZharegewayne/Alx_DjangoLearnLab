#!/usr/bin/env python
"""
Test runner script for comprehensive API testing.
Run with: python test_runner.py
"""

import os
import sys
import django
from django.test.utils import get_runner
from django.conf import settings

def run_tests():
    """Run the Django test suite for the API app."""
    os.environ['DJANGO_SETTINGS_MODULE'] = 'advanced_api_project.settings'
    django.setup()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=True)
    
    failures = test_runner.run_tests(['api'])
    
    return failures

if __name__ == '__main__':
    failures = run_tests()
    sys.exit(bool(failures))
