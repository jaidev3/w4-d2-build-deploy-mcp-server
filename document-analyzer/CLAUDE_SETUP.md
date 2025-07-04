# Claude Desktop Setup Guide

This guide will help you connect the Document Analyzer MCP server to Claude Desktop.
<!-- 
{
  "mcpServers": {
    "document-analyzer": {
      "command": "python",
      "args": [
        "C:\\Users\\dev\\Desktop\\My Files\\GitHub\\misogiai\\w4-d2-build-deploy-mcp-server\\document-analyzer\\src\\server.py",
        "${user_config.allowed_directories}"
      ]
    }
  }
} -->


## Prerequisites

1. **Claude Desktop** installed on your system
2. **Python 3.8+** installed and accessible from command line
3. **Document Analyzer** dependencies installed (`pip install -r requirements.txt`)

## Step 1: Locate Claude Desktop Config File

### Windows
```
%APPDATA%\Claude\claude_desktop_config.json
```
**Full path example:**
```
C:\Users\YourUsername\AppData\Roaming\Claude\claude_desktop_config.json
```

### macOS
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Linux
```
~/.config/Claude/claude_desktop_config.json
```

## Step 2: Get Your Document Analyzer Path

Find the full path to your document-analyzer directory. For example:

### Windows Examples:
```
C:\Users\YourUsername\Desktop\My Files\GitHub\misogiai\w4-d2-build-deploy-mcp-server\document-analyzer
C:\Users\YourUsername\Documents\document-analyzer
C:\Users\YourUsername\GitHub\document-analyzer
```

### macOS/Linux Examples:
```
/Users/YourUsername/Documents/document-analyzer
/home/yourusername/document-analyzer
/Users/YourUsername/GitHub/document-analyzer
```

## Step 3: Configuration Options

Choose the configuration that matches your system:

### Option A: Basic Configuration (Recommended)

```json
{
  "mcpServers": {
    "document-analyzer": {
      "command": "python",
      "args": ["src/server.py"],
      "cwd": "/path/to/your/document-analyzer"
    }
  }
}
```

### Option B: Windows with Full Python Path

```json
{
  "mcpServers": {
    "document-analyzer": {
      "command": "C:\\Python313\\python.exe",
      "args": ["src/server.py"],
      "cwd": "C:\\Users\\YourUsername\\path\\to\\document-analyzer"
    }
  }
}
```

### Option C: macOS/Linux

```json
{
  "mcpServers": {
    "document-analyzer": {
      "command": "python3",
      "args": ["src/server.py"],
      "cwd": "/Users/YourUsername/path/to/document-analyzer"
    }
  }
}
```

### Option D: Virtual Environment

```json
{
  "mcpServers": {
    "document-analyzer": {
      "command": "/path/to/your/venv/bin/python",
      "args": ["src/server.py"],
      "cwd": "/path/to/your/document-analyzer"
    }
  }
}
```


## Step 4: Update Configuration

1. **Open** the Claude Desktop config file in a text editor
2. **Replace** `/path/to/your/document-analyzer` with your actual path
3. **Save** the file
4. **Restart** Claude Desktop

## Step 5: Verify Connection

After restarting Claude Desktop, you should see "Document Analyzer 📄" in your available MCP servers.

Test the connection by asking Claude to:
```
Can you list the available documents using the document analyzer?
```

Claude should respond with a list of the 17 sample documents.

## Example Complete Configuration

Here's a complete example for Windows:

```json
{
  "mcpServers": {
    "document-analyzer": {
      "command": "python",
      "args": ["src/server.py"],
      "cwd": "C:\\Users\\dev\\Desktop\\My Files\\GitHub\\misogiai\\w4-d2-build-deploy-mcp-server\\document-analyzer"
    }
  }
}
```

## Troubleshooting

### Problem: "Server failed to start"
**Solution:** 
- Check that Python is installed and accessible
- Verify the path to your document-analyzer directory
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### Problem: "Command not found"
**Solution:**
- Use the full path to Python executable
- On Windows: `"C:\\Python313\\python.exe"`
- On macOS/Linux: `"/usr/bin/python3"`

### Problem: "Import errors"
**Solution:**
- Add PYTHONPATH environment variable:
```json
{
  "mcpServers": {
    "document-analyzer": {
      "command": "python",
      "args": ["src/server.py"],
      "cwd": "/path/to/your/document-analyzer",
      "env": {
        "PYTHONPATH": "/path/to/your/document-analyzer"
      }
    }
  }
}
```

### Problem: "Path with spaces"
**Solution:**
- Paths with spaces should work fine in JSON
- If issues persist, try moving to a path without spaces

## Testing Commands

Once connected, try these commands with Claude:

1. **List documents:**
   ```
   Show me all available documents in the analyzer
   ```

2. **Analyze a document:**
   ```
   Analyze document doc_001 for sentiment and keywords
   ```

3. **Search documents:**
   ```
   Search for documents about artificial intelligence
   ```

4. **Get statistics:**
   ```
   Show me statistics about the document collection
   ```

## Advanced Configuration

For advanced users, you can add additional environment variables:

```json
{
  "mcpServers": {
    "document-analyzer": {
      "command": "python",
      "args": ["src/server.py"],
      "cwd": "/path/to/your/document-analyzer",
      "env": {
        "PYTHONPATH": "/path/to/your/document-analyzer",
        "NLTK_DATA": "/path/to/nltk_data",
        "LOG_LEVEL": "INFO"
      },
      "disabled": false
    }
  }
}
```

## Support

If you encounter issues:
1. Check the Claude Desktop logs
2. Verify the server runs independently: `python src/server.py`
3. Ensure all paths use the correct format for your operating system
4. Restart Claude Desktop after any configuration changes

---

**Ready to analyze documents!** 🚀

Once connected, you'll have access to all 8 MCP tools for comprehensive document analysis including sentiment analysis, keyword extraction, readability scoring, and more. 