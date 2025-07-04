# Document Analyzer MCP Server 📄

A comprehensive MCP (Model Context Protocol) server for analyzing text documents with advanced features including sentiment analysis, keyword extraction, readability scoring, and document management capabilities.

## Features

### 📊 Analysis Capabilities
- **Sentiment Analysis**: Determine positive/negative/neutral sentiment with polarity and subjectivity scores
- **Keyword Extraction**: Extract top keywords using TF-IDF algorithm with scoring
- **Readability Scoring**: Multiple readability metrics (Flesch Reading Ease, Flesch-Kincaid Grade, etc.)
- **Basic Statistics**: Word count, sentence count, character count, and averages

### 📚 Document Management
- **Document Storage**: 17 pre-loaded sample documents with metadata
- **Document Search**: Semantic search using TF-IDF similarity
- **Document Addition**: Add new documents with automatic ID generation
- **Batch Analysis**: Analyze multiple texts simultaneously

### 🛠️ MCP Tools Available
1. `analyze_document(document_id)` - Full document analysis
2. `get_sentiment(text)` - Sentiment analysis for any text
3. `extract_keywords(text, limit)` - Extract top keywords
4. `add_document(document_data)` - Add new documents
5. `search_documents(query)` - Search documents by content
6. `get_document_list()` - List all available documents
7. `get_document_stats()` - Collection statistics
8. `analyze_text_batch(texts, analysis_type)` - Batch text analysis

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or navigate to the document-analyzer directory**
   ```bash
   cd document-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data (automatic on first run)**
   The server will automatically download required NLTK data on first startup.

4. **Run the MCP server**
   ```bash
   python src/server.py
   ```

## Usage Examples

### **Available MCP Tools:**

The server provides 8 powerful tools for document analysis:

1. **`analyze_document(document_id)`** - Complete analysis of a document
2. **`get_sentiment(text)`** - Sentiment analysis for any text
3. **`extract_keywords(text, limit)`** - Extract top keywords
4. **`add_document(document_data)`** - Add new documents
5. **`search_documents(query)`** - Search documents by content
6. **`get_document_list()`** - List all available documents
7. **`get_document_stats()`** - Collection statistics
8. **`analyze_text_batch(texts, analysis_type)`** - Batch analysis

### **1. 📋 List Available Documents**
```python
# Get all documents with their basic information
get_document_list()
```
This will show you all 17 sample documents with their IDs, titles, authors, categories, and word counts.

### **2. 🔍 Analyze a Specific Document**
```python
# Analyze document with ID "doc_001" (AI article)
analyze_document("doc_001")
```
This provides:
- **Sentiment**: positive/negative/neutral with confidence scores
- **Keywords**: Top 10 keywords with TF-IDF scores
- **Readability**: Multiple readability metrics
- **Statistics**: Word count, sentence count, averages

### **3. 💭 Quick Sentiment Analysis**
```python
# Analyze sentiment of custom text
get_sentiment("I love this amazing new technology!")
# Returns: {"sentiment": "positive", "polarity": 0.6, "subjectivity": 0.9, "confidence": 0.6}
```

### **4. 🔑 Extract Keywords**
```python
# Extract top 5 keywords from text
extract_keywords("Machine learning and artificial intelligence are transforming modern technology", limit=5)
```

### **5. 🔍 Search Documents**
```python
# Search for documents about AI
search_documents("artificial intelligence", limit=3)
# Returns documents ranked by similarity with scores
```

### **6. ➕ Add New Documents**
```python
# Add your own document
add_document({
    "title": "My Research Paper",
    "content": "This is the full text of my research paper...",
    "author": "Your Name",
    "category": "Research",
    "tags": ["research", "analysis"]
})
```

### **7. 📊 Get Collection Statistics**
```python
# View statistics about all documents
get_document_stats()
# Shows total documents, words, top categories, most prolific authors
```

### **8. 🔄 Batch Analysis**
```python
# Analyze multiple texts at once
analyze_text_batch([
    "This is fantastic news!",
    "I'm feeling quite disappointed.",
    "The weather is okay today."
], analysis_type="sentiment")
```

### **Example Analysis Results:**

Here's what you get when analyzing a document:

```json
{
  "document_id": "doc_001",
  "title": "The Future of Artificial Intelligence",
  "author": "Dr. Sarah Chen",
  "category": "Technology",
  "analysis": {
    "sentiment": {
      "sentiment": "positive",
      "polarity": 0.125,
      "subjectivity": 0.4,
      "confidence": 0.125
    },
    "keywords": [
      {"keyword": "artificial intelligence", "score": 0.3456, "frequency": 2},
      {"keyword": "machine learning", "score": 0.2134, "frequency": 1},
      {"keyword": "technology", "score": 0.1987, "frequency": 1}
    ],
    "readability": {
      "flesch_reading_ease": 45.2,
      "flesch_kincaid_grade": 12.8,
      "reading_level": "13th and 14th grade"
    },
    "basic_stats": {
      "word_count": 98,
      "sentence_count": 6,
      "average_words_per_sentence": 16.33
    }
  }
}
```

## **How to Connect to the Server:**

The MCP server runs locally and can be connected to by MCP clients such as:

- **Claude Desktop** (with MCP configuration)
- **Custom MCP clients**
- **Other AI applications** that support MCP

### **Server Connection Details:**
- **Protocol**: MCP (Model Context Protocol)
- **Transport**: Standard MCP transport
- **Endpoint**: Displayed when server starts

### **Connecting with Claude Desktop:**

1. **Follow the detailed setup guide**: See `CLAUDE_SETUP.md` for step-by-step instructions
2. **Use the sample configuration**: Copy from `claude_desktop_config.json` and customize paths
3. **Add to your Claude Desktop MCP settings** - the server will appear as "Document Analyzer 📄"
4. **Test the connection** - you can then use all the MCP tools directly in your Claude conversations

**Quick Setup:**
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
Replace `/path/to/your/document-analyzer` with your actual directory path.

### **Testing the Server:**

You can test if the server is working by trying these commands through your MCP client:

```python
# Test basic functionality
get_document_list()

# Test analysis
analyze_document("doc_001")

# Test sentiment analysis
get_sentiment("This is a test message!")
```

## Sample Documents

The server comes with 17 diverse sample documents covering various topics:

1. **Technology**: AI, Blockchain, Electric Vehicles, Digital Divide
2. **Environment**: Climate Change, Biodiversity, Urban Gardening
3. **Health & Wellness**: Mental Health, Sleep Science, Meditation
4. **Society**: Remote Work, Future of Work, Storytelling
5. **Lifestyle**: Minimalism, Sustainable Fashion, Cooking
6. **Science**: Space Exploration, Various Research Topics

Each document includes:
- Unique ID
- Title and content
- Author information
- Category classification
- Publication date
- Tags for categorization
- Metadata (source, word count, language)

## Analysis Details

### Sentiment Analysis
- **Polarity**: -1 (negative) to +1 (positive)
- **Subjectivity**: 0 (objective) to 1 (subjective)
- **Confidence**: Absolute value of polarity
- **Categories**: Positive (>0.1), Negative (<-0.1), Neutral (between)

### Keyword Extraction
- **Algorithm**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Features**: Unigrams and bigrams
- **Filtering**: Removes stop words and short words
- **Scoring**: Normalized TF-IDF scores
- **Fallback**: Frequency-based extraction if TF-IDF fails

### Readability Metrics
- **Flesch Reading Ease**: 0-100 scale (higher = easier)
- **Flesch-Kincaid Grade**: U.S. grade level
- **Automated Readability Index**: Grade level estimate
- **Coleman-Liau Index**: Grade level based on characters
- **Reading Level**: Text difficulty description

### Basic Statistics
- Word count (alphabetic words only)
- Sentence count
- Character count (with and without spaces)
- Average words per sentence
- Average characters per word

## API Reference

### analyze_document(document_id: str)
Performs comprehensive analysis of a document by ID.

**Parameters:**
- `document_id`: String ID of the document to analyze

**Returns:**
- Complete analysis object with sentiment, keywords, readability, and stats

### get_sentiment(text: str)
Analyzes sentiment of any text input.

**Parameters:**
- `text`: Text string to analyze

**Returns:**
- Sentiment analysis results with polarity, subjectivity, and confidence

### extract_keywords(text: str, limit: int = 10)
Extracts top keywords from text using TF-IDF.

**Parameters:**
- `text`: Text string to analyze
- `limit`: Maximum number of keywords (1-50, default: 10)

**Returns:**
- List of keywords with scores and frequencies

### add_document(document_data: Dict[str, Any])
Adds a new document to the collection.

**Parameters:**
- `document_data`: Dictionary containing document information
  - `title` (required): Document title
  - `content` (required): Document content
  - `author` (optional): Author name
  - `category` (optional): Document category
  - `tags` (optional): List of tags
  - `date` (optional): Publication date
  - `source` (optional): Document source

**Returns:**
- Success message with new document ID

### search_documents(query: str, limit: int = 10)
Searches documents using semantic similarity.

**Parameters:**
- `query`: Search query string
- `limit`: Maximum number of results (1-50, default: 10)

**Returns:**
- List of matching documents with similarity scores

### get_document_list()
Returns a list of all available documents with basic information.

**Returns:**
- List of documents with ID, title, author, category, date, word count, and tags

### get_document_stats()
Returns statistics about the document collection.

**Returns:**
- Collection statistics including counts, categories, authors, and totals

### analyze_text_batch(texts: List[str], analysis_type: str = "all")
Analyzes multiple texts in batch.

**Parameters:**
- `texts`: List of text strings (max 20)
- `analysis_type`: Type of analysis ("sentiment", "keywords", "readability", "stats", "all")

**Returns:**
- Batch analysis results for all provided texts

## Troubleshooting

### **Common Issues and Solutions:**

#### **1. Server Won't Start**
```bash
# Make sure you're in the correct directory
cd document-analyzer

# Check if all dependencies are installed
pip install -r requirements.txt

# Run the server
python src/server.py
```

#### **2. Import Errors**
If you see import errors, ensure all packages are installed:
```bash
pip install fastmcp textblob nltk textstat scikit-learn numpy pandas
```

#### **3. NLTK Data Missing**
The server automatically downloads NLTK data on first run. If you encounter NLTK errors:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
```

#### **4. File Path Issues**
Ensure the `data/sample_content.json` file exists and is readable. The server will create an empty document collection if the file is missing.

#### **5. MCP Client Connection Issues**
- Verify the server is running and showing the correct endpoint
- Check your MCP client configuration
- Ensure the server name matches: "Document Analyzer 📄"

### **Server Logs**
The server provides detailed logging for debugging. Check the console output for:
- Startup messages
- Error details
- Tool execution logs

## Error Handling

The server includes comprehensive error handling:
- Input validation for all parameters
- Graceful fallbacks for analysis failures
- Detailed error messages for debugging
- Automatic recovery from file system issues

## File Structure

```
document-analyzer/
├── data/
│   └── sample_content.json           # Sample documents storage
├── src/
│   └── server.py                     # Main MCP server implementation
├── claude_desktop_config.json        # Sample Claude Desktop configuration
├── claude_desktop_config_examples.json # Configuration examples for different systems
├── CLAUDE_SETUP.md                   # Detailed Claude Desktop setup guide
├── requirements.txt                  # Python dependencies
└── README.md                         # This documentation
```

## Dependencies

- **fastmcp**: FastMCP framework for MCP server creation
- **textblob**: Natural language processing and sentiment analysis
- **nltk**: Natural Language Toolkit for text processing
- **textstat**: Text readability statistics
- **scikit-learn**: Machine learning library for TF-IDF
- **numpy**: Numerical computing
- **pandas**: Data manipulation and analysis

## Contributing

Feel free to contribute improvements, bug fixes, or new features:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or feature requests, please create an issue in the project repository.

## **Next Steps**

### **Getting Started:**
1. **Install and run** the server following the installation instructions
2. **Connect your MCP client** (like Claude Desktop)
3. **Try the examples** listed in the Usage Examples section
4. **Explore the sample documents** to understand the available content

### **Advanced Usage:**
1. **Add your own documents** using the `add_document` tool
2. **Use batch analysis** for processing multiple texts efficiently
3. **Experiment with different analysis types** (sentiment, keywords, readability, stats)
4. **Build custom workflows** combining multiple tools

### **Development:**
1. **Extend the server** with additional analysis features
2. **Integrate with other systems** using the MCP protocol
3. **Customize the sample documents** for your specific domain
4. **Add new analysis algorithms** to the existing framework

---

**Built with FastMCP** - The fast, Pythonic way to build MCP servers and clients.
For more information about FastMCP, visit: https://gofastmcp.com

