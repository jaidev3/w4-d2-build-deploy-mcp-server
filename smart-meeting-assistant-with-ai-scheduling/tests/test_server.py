#!/usr/bin/env python3
"""
Basic tests for Smart Meeting Assistant Server
"""

import sys
import os
import json
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from server import MeetingAssistant, User, Meeting

def test_data_loading():
    """Test that sample data loads correctly"""
    print("Testing data loading...")
    
    # Create meeting assistant instance
    assistant = MeetingAssistant("data/sample_content.json")
    
    # Check users loaded
    assert len(assistant.users) > 0, "No users loaded"
    assert 1 in assistant.users, "User 1 not found"
    assert assistant.users[1].name == "Alice", "User 1 name incorrect"
    
    # Check meetings loaded
    assert len(assistant.meetings) > 0, "No meetings loaded"
    assert "A" in assistant.meetings, "Meeting A not found"
    
    print("✓ Data loading test passed")

def test_user_availability():
    """Test user availability checking"""
    print("Testing user availability...")
    
    assistant = MeetingAssistant("data/sample_content.json")
    
    # Test existing user
    availability = assistant.get_user_availability(1, "2025-10-01")
    assert availability["available"] == True, "User should be available"
    assert len(availability["existing_meetings"]) > 0, "Should have existing meetings"
    
    # Test non-existing user
    availability = assistant.get_user_availability(999, "2025-10-01")
    assert availability["available"] == False, "Non-existing user should not be available"
    
    print("✓ User availability test passed")

def test_meeting_suggestions():
    """Test meeting suggestions"""
    print("Testing meeting suggestions...")
    
    assistant = MeetingAssistant("data/sample_content.json")
    
    # Test with valid participants
    suggestions = assistant.suggest_meeting_time([1, 2], 60, "2025-12-01")
    assert "suggestions" in suggestions, "Should return suggestions"
    assert len(suggestions["suggestions"]) > 0, "Should have at least one suggestion"
    
    # Test with invalid participants
    suggestions = assistant.suggest_meeting_time([999], 60)
    assert "error" in suggestions, "Should return error for invalid participants"
    
    print("✓ Meeting suggestions test passed")

def test_meeting_analysis():
    """Test meeting effectiveness analysis"""
    print("Testing meeting analysis...")
    
    assistant = MeetingAssistant("data/sample_content.json")
    
    # Test analysis for specific user
    analysis = assistant.analyze_meeting_effectiveness(1)
    assert "total_meetings" in analysis, "Should return total meetings"
    assert analysis["total_meetings"] > 0, "Should have meetings to analyze"
    
    # Test analysis for all users
    analysis = assistant.analyze_meeting_effectiveness()
    assert "total_meetings" in analysis, "Should return total meetings"
    assert "insights" in analysis, "Should return insights"
    
    print("✓ Meeting analysis test passed")

def test_new_user_creation():
    """Test creating new user"""
    print("Testing new user creation...")
    
    assistant = MeetingAssistant("data/sample_content.json")
    
    # Store original user count
    original_count = len(assistant.users)
    
    # Create new user
    new_user = User(
        user_id=99,
        name="Test User",
        timezone="UTC",
        preferences="Test preferences",
        meeting_history=[]
    )
    
    assistant.users[99] = new_user
    
    # Verify user was added
    assert len(assistant.users) == original_count + 1, "User count should increase"
    assert assistant.users[99].name == "Test User", "User name should match"
    
    print("✓ New user creation test passed")

def run_all_tests():
    """Run all tests"""
    print("Running Smart Meeting Assistant Tests")
    print("="*40)
    
    try:
        test_data_loading()
        test_user_availability()
        test_meeting_suggestions()
        test_meeting_analysis()
        test_new_user_creation()
        
        print("\n" + "="*40)
        print("🎉 All tests passed!")
        print("="*40)
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        print("="*40)
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 