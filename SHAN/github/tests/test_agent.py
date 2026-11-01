"""Automated Unit and Integration Tests for VoiceOps 2026 Support Agent.
Author: Balasundaram Shanmugaraj
Repository: https://github.com/balasundaramshanmugaraj/VoiceOps_Project
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.test_person1 import TestPerson1


class TestSupportAgent(TestPerson1):
    """Test suite covering dataset parsing, BM25 retrieval, business day calculations,
    caller verification gating, ticket escalation, speech normalization, and voice pipeline.
    """
    pass


if __name__ == '__main__':
    unittest.main()
