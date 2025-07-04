#!/usr/bin/env python3
"""
Document Analyzer MCP Server

A comprehensive MCP server for analyzing text documents with sentiment analysis,
keyword extraction, readability scoring, and document management capabilities.
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Import analysis libraries
import nltk
from textblob import TextBlob
import textstat
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

# Import FastMCP
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Document Analyzer 📄")

# Global variables for document storage
DOCUMENTS_FILE = Path(__file__).parent.parent / "data" / "sample_content.json"
documents_data = {}

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)

def load_documents():
    """Load documents from JSON file"""
    global documents_data
    try:
        with open(DOCUMENTS_FILE, 'r', encoding='utf-8') as f:
            documents_data = json.load(f)
    except FileNotFoundError:
        documents_data = {"documents": []}
    except json.JSONDecodeError:
        documents_data = {"documents": []}

def save_documents():
    """Save documents to JSON file"""
    try:
        with open(DOCUMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(documents_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise Exception(f"Failed to save documents: {str(e)}")

def calculate_sentiment(text: str) -> Dict[str, Any]:
    """Calculate sentiment analysis for text"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Determine sentiment label
    if polarity > 0.1:
        sentiment = "positive"
    elif polarity < -0.1:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return {
        "sentiment": sentiment,
        "polarity": round(polarity, 3),
        "subjectivity": round(subjectivity, 3),
        "confidence": round(abs(polarity), 3)
    }

def extract_keywords_tfidf(text: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Extract keywords using TF-IDF"""
    try:
        # Preprocess text
        words = nltk.word_tokenize(text.lower())
        stop_words = set(nltk.corpus.stopwords.words('english'))
        words = [word for word in words if word.isalpha() and word not in stop_words and len(word) > 2]
        
        if not words:
            return []
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(max_features=limit*2, ngram_range=(1, 2))
        
        # Fit and transform the text
        tfidf_matrix = vectorizer.fit_transform([' '.join(words)])
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray()[0]
        
        # Get top keywords
        keyword_scores = list(zip(feature_names, tfidf_scores))
        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        
        keywords = []
        for word, score in keyword_scores[:limit]:
            if score > 0:
                keywords.append({
                    "keyword": word,
                    "score": round(score, 4),
                    "frequency": words.count(word) if ' ' not in word else 0
                })
        
        return keywords
    except Exception as e:
        # Fallback to simple frequency-based extraction
        words = nltk.word_tokenize(text.lower())
        stop_words = set(nltk.corpus.stopwords.words('english'))
        words = [word for word in words if word.isalpha() and word not in stop_words and len(word) > 2]
        
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [{"keyword": word, "score": freq/len(words), "frequency": freq} 
                for word, freq in sorted_words[:limit]]

def calculate_readability(text: str) -> Dict[str, Any]:
    """Calculate readability scores"""
    try:
        return {
            "flesch_reading_ease": round(textstat.flesch_reading_ease(text), 2),
            "flesch_kincaid_grade": round(textstat.flesch_kincaid_grade(text), 2),
            "automated_readability_index": round(textstat.automated_readability_index(text), 2),
            "coleman_liau_index": round(textstat.coleman_liau_index(text), 2),
            "reading_level": textstat.text_standard(text, float_output=False)
        }
    except Exception as e:
        return {
            "flesch_reading_ease": 0,
            "flesch_kincaid_grade": 0,
            "automated_readability_index": 0,
            "coleman_liau_index": 0,
            "reading_level": "Unknown",
            "error": str(e)
        }

def calculate_basic_stats(text: str) -> Dict[str, Any]:
    """Calculate basic text statistics"""
    sentences = nltk.sent_tokenize(text)
    words = nltk.word_tokenize(text)
    
    # Count different types of words
    word_chars = [word for word in words if word.isalpha()]
    
    return {
        "word_count": len(word_chars),
        "sentence_count": len(sentences),
        "character_count": len(text),
        "character_count_no_spaces": len(text.replace(' ', '')),
        "average_words_per_sentence": round(len(word_chars) / len(sentences), 2) if sentences else 0,
        "average_characters_per_word": round(len(''.join(word_chars)) / len(word_chars), 2) if word_chars else 0
    }

def get_document_by_id(doc_id: str) -> Optional[Dict[str, Any]]:
    """Get document by ID"""
    for doc in documents_data.get("documents", []):
        if doc["id"] == doc_id:
            return doc
    return None

def search_documents_by_content(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search documents by content using TF-IDF similarity"""
    docs = documents_data.get("documents", [])
    if not docs or not query.strip():
        return []
    
    try:
        # Prepare documents for search
        doc_contents = [doc["content"] for doc in docs]
        doc_contents.append(query)
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        tfidf_matrix = vectorizer.fit_transform(doc_contents)
        
        # Calculate similarity
        query_vector = tfidf_matrix[-1]
        doc_vectors = tfidf_matrix[:-1]
        
        similarities = cosine_similarity(query_vector, doc_vectors).flatten()
        
        # Get top matches
        doc_similarities = list(zip(docs, similarities))
        doc_similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for doc, similarity in doc_similarities[:limit]:
            if similarity > 0:
                result = doc.copy()
                result["similarity_score"] = round(similarity, 4)
                results.append(result)
        
        return results
    except Exception as e:
        # Fallback to simple text search
        results = []
        query_lower = query.lower()
        for doc in docs:
            if query_lower in doc["content"].lower() or query_lower in doc["title"].lower():
                results.append(doc)
        return results[:limit]

# Initialize documents on startup
load_documents()

# MCP Tools Implementation

@mcp.tool
def analyze_document(document_id: str) -> Dict[str, Any]:
    """
    Perform comprehensive analysis of a document by ID.
    
    Args:
        document_id: The ID of the document to analyze
    
    Returns:
        Complete analysis including sentiment, keywords, readability, and basic stats
    """
    doc = get_document_by_id(document_id)
    if not doc:
        return {"error": f"Document with ID '{document_id}' not found"}
    
    content = doc["content"]
    
    # Perform all analyses
    sentiment = calculate_sentiment(content)
    keywords = extract_keywords_tfidf(content, limit=10)
    readability = calculate_readability(content)
    basic_stats = calculate_basic_stats(content)
    
    return {
        "document_id": document_id,
        "title": doc["title"],
        "author": doc.get("author", "Unknown"),
        "category": doc.get("category", "Uncategorized"),
        "analysis": {
            "sentiment": sentiment,
            "keywords": keywords,
            "readability": readability,
            "basic_stats": basic_stats
        },
        "metadata": doc.get("metadata", {})
    }

@mcp.tool
def get_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze sentiment of any text.
    
    Args:
        text: The text to analyze for sentiment
    
    Returns:
        Sentiment analysis results
    """
    if not text.strip():
        return {"error": "Text cannot be empty"}
    
    return calculate_sentiment(text)

@mcp.tool
def extract_keywords(text: str, limit: int = 10) -> Dict[str, Any]:
    """
    Extract top keywords from text.
    
    Args:
        text: The text to extract keywords from
        limit: Maximum number of keywords to return (default: 10)
    
    Returns:
        List of top keywords with scores
    """
    if not text.strip():
        return {"error": "Text cannot be empty"}
    
    if limit < 1 or limit > 50:
        return {"error": "Limit must be between 1 and 50"}
    
    keywords = extract_keywords_tfidf(text, limit)
    return {
        "keywords": keywords,
        "total_found": len(keywords),
        "limit_applied": limit
    }

@mcp.tool
def add_document(document_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a new document to the collection.
    
    Args:
        document_data: Document data including title, content, author, etc.
    
    Returns:
        Success message with document ID
    """
    required_fields = ["title", "content"]
    for field in required_fields:
        if field not in document_data or not document_data[field].strip():
            return {"error": f"Required field '{field}' is missing or empty"}
    
    # Generate new document ID
    existing_ids = [doc["id"] for doc in documents_data.get("documents", [])]
    doc_num = 1
    while f"doc_{doc_num:03d}" in existing_ids:
        doc_num += 1
    
    new_doc_id = f"doc_{doc_num:03d}"
    
    # Create new document
    new_doc = {
        "id": new_doc_id,
        "title": document_data["title"],
        "content": document_data["content"],
        "author": document_data.get("author", "Unknown"),
        "category": document_data.get("category", "Uncategorized"),
        "date": document_data.get("date", datetime.now().strftime("%Y-%m-%d")),
        "tags": document_data.get("tags", []),
        "metadata": {
            "source": document_data.get("source", "User Added"),
            "word_count": len(document_data["content"].split()),
            "language": document_data.get("language", "en")
        }
    }
    
    # Add to documents
    if "documents" not in documents_data:
        documents_data["documents"] = []
    
    documents_data["documents"].append(new_doc)
    
    # Save to file
    try:
        save_documents()
        return {
            "success": True,
            "message": f"Document added successfully with ID: {new_doc_id}",
            "document_id": new_doc_id
        }
    except Exception as e:
        # Remove the document if save failed
        documents_data["documents"] = [doc for doc in documents_data["documents"] if doc["id"] != new_doc_id]
        return {"error": f"Failed to save document: {str(e)}"}

@mcp.tool
def search_documents(query: str, limit: int = 10) -> Dict[str, Any]:
    """
    Search documents by content using semantic similarity.
    
    Args:
        query: Search query text
        limit: Maximum number of results to return (default: 10)
    
    Returns:
        List of matching documents with similarity scores
    """
    if not query.strip():
        return {"error": "Search query cannot be empty"}
    
    if limit < 1 or limit > 50:
        return {"error": "Limit must be between 1 and 50"}
    
    results = search_documents_by_content(query, limit)
    
    return {
        "query": query,
        "results": results,
        "total_found": len(results),
        "limit_applied": limit
    }

@mcp.tool
def get_document_list() -> Dict[str, Any]:
    """
    Get a list of all available documents with basic information.
    
    Returns:
        List of all documents with metadata
    """
    docs = documents_data.get("documents", [])
    
    document_list = []
    for doc in docs:
        document_list.append({
            "id": doc["id"],
            "title": doc["title"],
            "author": doc.get("author", "Unknown"),
            "category": doc.get("category", "Uncategorized"),
            "date": doc.get("date", "Unknown"),
            "word_count": doc.get("metadata", {}).get("word_count", 0),
            "tags": doc.get("tags", [])
        })
    
    return {
        "documents": document_list,
        "total_count": len(document_list)
    }

@mcp.tool
def get_document_stats() -> Dict[str, Any]:
    """
    Get overall statistics about the document collection.
    
    Returns:
        Statistics about the document collection
    """
    docs = documents_data.get("documents", [])
    
    if not docs:
        return {"message": "No documents found"}
    
    # Calculate statistics
    total_docs = len(docs)
    total_words = sum(doc.get("metadata", {}).get("word_count", 0) for doc in docs)
    
    categories: Dict[str, int] = {}
    authors: Dict[str, int] = {}
    
    for doc in docs:
        category = doc.get("category", "Uncategorized")
        author = doc.get("author", "Unknown")
        
        categories[category] = categories.get(category, 0) + 1
        authors[author] = authors.get(author, 0) + 1
    
    return {
        "total_documents": total_docs,
        "total_words": total_words,
        "average_words_per_document": round(total_words / total_docs, 2) if total_docs > 0 else 0,
        "categories": dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)),
        "authors": dict(sorted(authors.items(), key=lambda x: x[1], reverse=True)),
        "top_category": max(categories.items(), key=lambda x: x[1])[0] if categories else None,
        "most_prolific_author": max(authors.items(), key=lambda x: x[1])[0] if authors else None
    }

@mcp.tool
def analyze_text_batch(texts: List[str], analysis_type: str = "all") -> Dict[str, Any]:
    """
    Analyze multiple texts in batch.
    
    Args:
        texts: List of texts to analyze
        analysis_type: Type of analysis ("sentiment", "keywords", "readability", "stats", "all")
    
    Returns:
        Batch analysis results
    """
    if not texts:
        return {"error": "No texts provided"}
    
    if len(texts) > 20:
        return {"error": "Maximum 20 texts allowed per batch"}
    
    valid_types = ["sentiment", "keywords", "readability", "stats", "all"]
    if analysis_type not in valid_types:
        return {"error": f"Invalid analysis type. Must be one of: {valid_types}"}
    
    results = []
    
    for i, text in enumerate(texts):
        if not text.strip():
            results.append({"index": i, "error": "Empty text"})
            continue
        
        analysis: Dict[str, Any] = {"index": i}
        
        try:
            if analysis_type in ["sentiment", "all"]:
                analysis["sentiment"] = calculate_sentiment(text)
            
            if analysis_type in ["keywords", "all"]:
                analysis["keywords"] = extract_keywords_tfidf(text, limit=5)
            
            if analysis_type in ["readability", "all"]:
                analysis["readability"] = calculate_readability(text)
            
            if analysis_type in ["stats", "all"]:
                analysis["basic_stats"] = calculate_basic_stats(text)
            
            results.append(analysis)
            
        except Exception as e:
            results.append({"index": i, "error": str(e)})
    
    return {
        "analysis_type": analysis_type,
        "total_texts": len(texts),
        "results": results
    }

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
