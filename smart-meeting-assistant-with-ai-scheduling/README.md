# Smart Meeting Assistant with AI Scheduling

A comprehensive MCP (Model Context Protocol) server that provides intelligent meeting scheduling, conflict detection, and meeting effectiveness analysis using fastmcp.

## Features

### 🤖 AI-Powered Scheduling
- Intelligent meeting time suggestions based on participant availability
- Conflict detection across multiple participants
- Timezone-aware scheduling
- Preference-based recommendations

### 👥 User Management
- Create and manage user profiles
- Customizable preferences and timezones
- Meeting history tracking
- Availability checking

### 📊 Meeting Analytics
- Meeting effectiveness scoring and analysis
- Insights and recommendations for better meetings
- Duration and frequency analysis
- Performance tracking

### 🔧 MCP Integration
- Full MCP server implementation using fastmcp
- Easy integration with Claude Desktop and other MCP clients
- Comprehensive tool set for meeting management

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd smart-meeting-assistant-with-ai-scheduling
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

```bash
python src/server.py
```

The server will start and load sample data from `data/sample_content.json`.

### Available Tools

#### User Management Tools

1. **`get_user_profile(user_id: int)`**
   - Get user profile including preferences and meeting history
   - Returns user details, timezone, and meeting history

2. **`create_user(name: str, timezone: str, preferences: str)`**
   - Create a new user profile
   - Returns the new user ID and confirmation

3. **`update_user_preferences(user_id: int, preferences: str)`**
   - Update user preferences
   - Returns success confirmation

4. **`check_availability(user_id: int, date: str)`**
   - Check user availability for a specific date (YYYY-MM-DD)
   - Returns availability status and existing meetings

#### Meeting Scheduling Tools

5. **`schedule_meeting(title: str, participants: List[int], start_time: str, duration: int, agenda: str)`**
   - Schedule a new meeting with conflict detection
   - Returns meeting ID or conflict information

6. **`get_meeting_suggestions(participants: List[int], duration: int, preferred_date: Optional[str])`**
   - Get AI-powered meeting time suggestions
   - Returns up to 3 optimal time slots

7. **`get_meeting_details(meeting_id: str)`**
   - Get details of a specific meeting
   - Returns complete meeting information

8. **`list_upcoming_meetings(user_id: Optional[int], days_ahead: int = 7)`**
   - List upcoming meetings for a user or all users
   - Returns sorted list of upcoming meetings

#### Analytics Tools

9. **`analyze_meeting_effectiveness(user_id: Optional[int])`**
   - Analyze meeting effectiveness and provide insights
   - Returns statistics and actionable recommendations

10. **`update_meeting_effectiveness(meeting_id: str, effectiveness_score: int)`**
    - Update meeting effectiveness score (1-10)
    - Returns confirmation of update

## Example Usage

### 1. Check User Availability
```json
{
  "tool": "check_availability",
  "arguments": {
    "user_id": 1,
    "date": "2025-01-15"
  }
}
```

### 2. Get Meeting Suggestions
```json
{
  "tool": "get_meeting_suggestions",
  "arguments": {
    "participants": [1, 2, 3],
    "duration": 60,
    "preferred_date": "2025-01-15"
  }
}
```

### 3. Schedule a Meeting
```json
{
  "tool": "schedule_meeting",
  "arguments": {
    "title": "Team Planning Session",
    "participants": [1, 2, 3],
    "start_time": "2025-01-15T14:00:00Z",
    "duration": 60,
    "agenda": "Discuss Q1 goals and project timeline"
  }
}
```

### 4. Analyze Meeting Effectiveness
```json
{
  "tool": "analyze_meeting_effectiveness",
  "arguments": {
    "user_id": 1
  }
}
```

## Data Structure

The server uses JSON data storage with the following structure:

### Users
```json
{
  "user_id": 1,
  "name": "Alice",
  "timezone": "UTC-5",
  "preferences": "Working hours: 9 AM - 5 PM",
  "meeting_history": [...]
}
```

### Meetings
```json
{
  "meeting_id": "M001",
  "title": "Project Kickoff",
  "participants": [1, 2],
  "start_time": "2025-01-15T14:00:00Z",
  "duration": 60,
  "agenda": "Project overview, team roles",
  "effectiveness_score": 8
}
```

## Claude Desktop Integration

To use with Claude Desktop, add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "smart-meeting-assistant": {
      "command": "python",
      "args": ["/path/to/smart-meeting-assistant-with-ai-scheduling/src/server.py"]
    }
  }
}
```

## AI Scheduling Algorithm

The assistant uses several factors for intelligent scheduling:

1. **Conflict Detection**: Checks for overlapping meetings across all participants
2. **Preference Analysis**: Considers user-defined working hours and preferences
3. **Timezone Awareness**: Handles multiple timezones for global teams
4. **Historical Patterns**: Learns from past meeting effectiveness scores
5. **Business Hours**: Prioritizes standard business hours when possible

## Meeting Effectiveness Insights

The system provides actionable insights based on:

- **Duration Analysis**: Identifies meetings that are too long
- **Frequency Analysis**: Detects meeting overload
- **Effectiveness Scoring**: Tracks meeting success rates
- **Participation Patterns**: Analyzes attendance and engagement

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Adding New Features
1. Add new tools to `src/server.py`
2. Update data models if needed
3. Add tests for new functionality
4. Update documentation

## Configuration

### Environment Variables
- `DATA_FILE`: Path to JSON data file (default: `data/sample_content.json`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

### Sample Data
The `data/sample_content.json` file contains sample users and meetings for testing. You can modify this file or create your own data structure.

## Troubleshooting

### Common Issues

1. **Import Error for fastmcp**: Ensure fastmcp is installed: `pip install fastmcp>=2.0.0`
2. **Data Loading Error**: Check that `data/sample_content.json` exists and is valid JSON
3. **Timezone Issues**: Ensure timezone strings are valid (e.g., "UTC-5", "UTC+1")

### Logs
Check the console output for detailed logging information about data loading, scheduling conflicts, and errors.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please open an issue in the repository or contact the development team.
