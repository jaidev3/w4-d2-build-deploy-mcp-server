#!/usr/bin/env python3
"""
Smart Meeting Assistant with AI Scheduling - MCP Server
A comprehensive meeting assistant that provides intelligent scheduling, 
conflict detection, and meeting effectiveness analysis.
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging
from dataclasses import dataclass, asdict
from zoneinfo import ZoneInfo

from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class User:
    user_id: int
    name: str
    timezone: str
    preferences: str
    meeting_history: List[Dict[str, Any]]

@dataclass
class Meeting:
    meeting_id: str
    title: str
    participants: List[int]
    start_time: str
    duration: int
    agenda: str
    effectiveness_score: Optional[int] = None

class MeetingAssistant:
    def __init__(self, data_file: str = "data/sample_content.json"):
        self.data_file = Path(data_file)
        self.users: Dict[int, User] = {}
        self.meetings: Dict[str, Meeting] = {}
        self.load_data()
    
    def load_data(self):
        """Load user and meeting data from JSON file"""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                # Load users
                for user_data in data.get('users', []):
                    user = User(**user_data)
                    self.users[user.user_id] = user
                
                # Load meetings
                for meeting_data in data.get('meetings', []):
                    meeting = Meeting(**meeting_data)
                    self.meetings[meeting.meeting_id] = meeting
                
                logger.info(f"Loaded {len(self.users)} users and {len(self.meetings)} meetings")
        except Exception as e:
            logger.error(f"Error loading data: {e}")
    
    def save_data(self):
        """Save current data to JSON file"""
        try:
            data = {
                'users': [asdict(user) for user in self.users.values()],
                'meetings': [asdict(meeting) for meeting in self.meetings.values()]
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info("Data saved successfully")
        except Exception as e:
            logger.error(f"Error saving data: {e}")
    
    def get_user_availability(self, user_id: int, date: str) -> Dict[str, Any]:
        """Get user availability for a specific date"""
        if user_id not in self.users:
            return {"available": False, "reason": "User not found"}
        
        user = self.users[user_id]
        
        # Check existing meetings for conflicts
        conflicts = []
        for meeting in self.meetings.values():
            if user_id in meeting.participants:
                meeting_date = datetime.fromisoformat(meeting.start_time.replace('Z', '+00:00')).date()
                if meeting_date.isoformat() == date:
                    conflicts.append({
                        "meeting_id": meeting.meeting_id,
                        "title": meeting.title,
                        "start_time": meeting.start_time,
                        "duration": meeting.duration
                    })
        
        return {
            "available": True,
            "timezone": user.timezone,
            "preferences": user.preferences,
            "existing_meetings": conflicts
        }
    
    def suggest_meeting_time(self, participants: List[int], duration: int, 
                           preferred_date: Optional[str] = None) -> Dict[str, Any]:
        """AI-powered meeting time suggestion"""
        suggestions = []
        
        # Get all participants
        participant_users = []
        for user_id in participants:
            if user_id in self.users:
                participant_users.append(self.users[user_id])
        
        if not participant_users:
            return {"error": "No valid participants found"}
        
        # Analyze preferences and find common availability
        # For demo purposes, we'll suggest a few time slots
        base_date = datetime.now() if not preferred_date else datetime.fromisoformat(preferred_date)
        
        for days_ahead in range(1, 8):  # Next 7 days
            for hour in [9, 10, 11, 14, 15, 16]:  # Common business hours
                suggested_time = base_date.replace(hour=hour, minute=0, second=0, microsecond=0) + timedelta(days=days_ahead)
                
                # Check conflicts for all participants
                has_conflict = False
                for user in participant_users:
                    availability = self.get_user_availability(user.user_id, suggested_time.date().isoformat())
                    if availability.get("existing_meetings"):
                        # Check for time conflicts
                        for meeting in availability["existing_meetings"]:
                            meeting_start = datetime.fromisoformat(meeting["start_time"].replace('Z', '+00:00'))
                            meeting_end = meeting_start + timedelta(minutes=meeting["duration"])
                            suggested_end = suggested_time + timedelta(minutes=duration)
                            
                            if (suggested_time < meeting_end and suggested_end > meeting_start):
                                has_conflict = True
                                break
                    
                    if has_conflict:
                        break
                
                if not has_conflict:
                    suggestions.append({
                        "suggested_time": suggested_time.isoformat(),
                        "confidence": 0.8,  # Demo confidence score
                        "reason": "No conflicts found, matches general business hours"
                    })
                
                if len(suggestions) >= 3:  # Limit to 3 suggestions
                    break
            
            if len(suggestions) >= 3:
                break
        
        return {
            "suggestions": suggestions[:3],
            "participants": [{"user_id": u.user_id, "name": u.name, "timezone": u.timezone} for u in participant_users]
        }
    
    def analyze_meeting_effectiveness(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Analyze meeting effectiveness and provide insights"""
        meetings_to_analyze = []
        
        if user_id:
            # Analyze meetings for specific user
            for meeting in self.meetings.values():
                if user_id in meeting.participants:
                    meetings_to_analyze.append(meeting)
        else:
            # Analyze all meetings
            meetings_to_analyze = list(self.meetings.values())
        
        if not meetings_to_analyze:
            return {"error": "No meetings found for analysis"}
        
        # Calculate statistics
        total_meetings = len(meetings_to_analyze)
        total_duration = sum(m.duration for m in meetings_to_analyze)
        avg_duration = total_duration / total_meetings if total_meetings > 0 else 0
        
        scored_meetings = [m for m in meetings_to_analyze if m.effectiveness_score is not None]
        avg_effectiveness = sum(m.effectiveness_score for m in scored_meetings if m.effectiveness_score is not None) / len(scored_meetings) if scored_meetings else 0
        
        # Insights
        insights = []
        if avg_effectiveness < 7:
            insights.append("Meeting effectiveness is below average. Consider reviewing agenda preparation and participant engagement.")
        if avg_duration > 60:
            insights.append("Average meeting duration is high. Consider breaking long meetings into shorter, focused sessions.")
        if total_meetings > 15:
            insights.append("High meeting frequency detected. Consider consolidating or eliminating unnecessary meetings.")
        
        return {
            "total_meetings": total_meetings,
            "total_duration_minutes": total_duration,
            "average_duration_minutes": round(avg_duration, 2),
            "average_effectiveness_score": round(avg_effectiveness, 2),
            "insights": insights,
            "meeting_breakdown": [
                {
                    "meeting_id": m.meeting_id,
                    "title": m.title,
                    "duration": m.duration,
                    "effectiveness_score": m.effectiveness_score
                }
                for m in meetings_to_analyze
            ]
        }

# Initialize the meeting assistant
meeting_assistant = MeetingAssistant()

# Create FastMCP server
mcp = FastMCP("Smart Meeting Assistant")

@mcp.tool()
def get_user_profile(user_id: int) -> Dict[str, Any]:
    """Get user profile including preferences and meeting history"""
    if user_id not in meeting_assistant.users:
        return {"error": f"User {user_id} not found"}
    
    user = meeting_assistant.users[user_id]
    return {
        "user_id": user.user_id,
        "name": user.name,
        "timezone": user.timezone,
        "preferences": user.preferences,
        "meeting_history": user.meeting_history
    }

@mcp.tool()
def create_user(name: str, timezone: str, preferences: str) -> Dict[str, Any]:
    """Create a new user profile"""
    # Generate new user ID
    new_user_id = max(meeting_assistant.users.keys()) + 1 if meeting_assistant.users else 1
    
    user = User(
        user_id=new_user_id,
        name=name,
        timezone=timezone,
        preferences=preferences,
        meeting_history=[]
    )
    
    meeting_assistant.users[new_user_id] = user
    meeting_assistant.save_data()
    
    return {
        "success": True,
        "user_id": new_user_id,
        "message": f"User '{name}' created successfully"
    }

@mcp.tool()
def update_user_preferences(user_id: int, preferences: str) -> Dict[str, Any]:
    """Update user preferences"""
    if user_id not in meeting_assistant.users:
        return {"error": f"User {user_id} not found"}
    
    meeting_assistant.users[user_id].preferences = preferences
    meeting_assistant.save_data()
    
    return {
        "success": True,
        "message": f"Preferences updated for user {user_id}"
    }

@mcp.tool()
def check_availability(user_id: int, date: str) -> Dict[str, Any]:
    """Check user availability for a specific date (YYYY-MM-DD)"""
    return meeting_assistant.get_user_availability(user_id, date)

@mcp.tool()
def schedule_meeting(title: str, participants: List[int], start_time: str, 
                    duration: int, agenda: str) -> Dict[str, Any]:
    """Schedule a new meeting"""
    # Generate meeting ID
    meeting_id = f"M{len(meeting_assistant.meetings) + 1:03d}"
    
    # Validate participants
    invalid_participants = [p for p in participants if p not in meeting_assistant.users]
    if invalid_participants:
        return {"error": f"Invalid participants: {invalid_participants}"}
    
    # Check for conflicts
    conflicts = []
    for participant in participants:
        availability = meeting_assistant.get_user_availability(
            participant, 
            datetime.fromisoformat(start_time.replace('Z', '+00:00')).date().isoformat()
        )
        
        if availability.get("existing_meetings"):
            for existing_meeting in availability["existing_meetings"]:
                meeting_start = datetime.fromisoformat(existing_meeting["start_time"].replace('Z', '+00:00'))
                meeting_end = meeting_start + timedelta(minutes=existing_meeting["duration"])
                new_start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                new_end = new_start + timedelta(minutes=duration)
                
                if (new_start < meeting_end and new_end > meeting_start):
                    conflicts.append({
                        "participant": participant,
                        "conflicting_meeting": existing_meeting["title"],
                        "conflict_time": existing_meeting["start_time"]
                    })
    
    if conflicts:
        return {
            "error": "Scheduling conflicts detected",
            "conflicts": conflicts
        }
    
    # Create meeting
    meeting = Meeting(
        meeting_id=meeting_id,
        title=title,
        participants=participants,
        start_time=start_time,
        duration=duration,
        agenda=agenda
    )
    
    meeting_assistant.meetings[meeting_id] = meeting
    
    # Update user meeting history
    for participant in participants:
        meeting_assistant.users[participant].meeting_history.append({
            "meeting_id": meeting_id,
            "date": datetime.fromisoformat(start_time.replace('Z', '+00:00')).date().isoformat(),
            "duration": duration
        })
    
    meeting_assistant.save_data()
    
    return {
        "success": True,
        "meeting_id": meeting_id,
        "message": f"Meeting '{title}' scheduled successfully"
    }

@mcp.tool()
def get_meeting_suggestions(participants: List[int], duration: int, 
                           preferred_date: Optional[str] = None) -> Dict[str, Any]:
    """Get AI-powered meeting time suggestions"""
    return meeting_assistant.suggest_meeting_time(participants, duration, preferred_date)

@mcp.tool()
def get_meeting_details(meeting_id: str) -> Dict[str, Any]:
    """Get details of a specific meeting"""
    if meeting_id not in meeting_assistant.meetings:
        return {"error": f"Meeting {meeting_id} not found"}
    
    meeting = meeting_assistant.meetings[meeting_id]
    return {
        "meeting_id": meeting.meeting_id,
        "title": meeting.title,
        "participants": [
            {"user_id": uid, "name": meeting_assistant.users[uid].name}
            for uid in meeting.participants
            if uid in meeting_assistant.users
        ],
        "start_time": meeting.start_time,
        "duration": meeting.duration,
        "agenda": meeting.agenda,
        "effectiveness_score": meeting.effectiveness_score
    }

@mcp.tool()
def analyze_meeting_effectiveness(user_id: Optional[int] = None) -> Dict[str, Any]:
    """Analyze meeting effectiveness and provide insights"""
    return meeting_assistant.analyze_meeting_effectiveness(user_id)

@mcp.tool()
def update_meeting_effectiveness(meeting_id: str, effectiveness_score: int) -> Dict[str, Any]:
    """Update meeting effectiveness score (1-10)"""
    if meeting_id not in meeting_assistant.meetings:
        return {"error": f"Meeting {meeting_id} not found"}
    
    if not (1 <= effectiveness_score <= 10):
        return {"error": "Effectiveness score must be between 1 and 10"}
    
    meeting_assistant.meetings[meeting_id].effectiveness_score = effectiveness_score
    meeting_assistant.save_data()
    
    return {
        "success": True,
        "message": f"Effectiveness score updated for meeting {meeting_id}"
    }

@mcp.tool()
def list_upcoming_meetings(user_id: Optional[int] = None, days_ahead: int = 7) -> Dict[str, Any]:
    """List upcoming meetings for a user or all users"""
    current_time = datetime.now()
    cutoff_time = current_time + timedelta(days=days_ahead)
    
    upcoming_meetings = []
    
    for meeting in meeting_assistant.meetings.values():
        meeting_time = datetime.fromisoformat(meeting.start_time.replace('Z', '+00:00'))
        
        if meeting_time > current_time and meeting_time <= cutoff_time:
            if user_id is None or user_id in meeting.participants:
                upcoming_meetings.append({
                    "meeting_id": meeting.meeting_id,
                    "title": meeting.title,
                    "start_time": meeting.start_time,
                    "duration": meeting.duration,
                    "participants": [
                        {"user_id": uid, "name": meeting_assistant.users[uid].name}
                        for uid in meeting.participants
                        if uid in meeting_assistant.users
                    ]
                })
    
    # Sort by start time
    upcoming_meetings.sort(key=lambda x: x["start_time"])
    
    return {
        "upcoming_meetings": upcoming_meetings,
        "total_count": len(upcoming_meetings)
    }

if __name__ == "__main__":
    mcp.run()
