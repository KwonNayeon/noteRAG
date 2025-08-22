# NoteNest

*[한국어](README.ko.md) | English*

<div align="center">
  
<img src="./assets/logo.png" alt="noteRAG Logo" width="200" height="200">

**AI-Powered Multisensory Summarization for Cognitive-Friendly Learning**

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Swift](https://img.shields.io/badge/Swift-FA7343?style=for-the-badge&logo=swift&logoColor=white)](https://developer.apple.com/swift/)
[![OpenAI API](https://img.shields.io/badge/OpenAI_API-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/api/)
[![LangChain](https://img.shields.io/badge/LangChain-000000?style=for-the-badge&logo=chainlink&logoColor=white)](https://www.langchain.com/)
[![Figma](https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white)](https://www.figma.com/)

</div>

## Overview

NoteNest transforms complex content into accessible, cognitive-friendly summaries using RAG (Retrieval Augmented Generation). Our tool creates 3-line summaries for users with diverse cognitive needs, particularly those with reading or focus difficulties, with optional expandable details for each line.

### Key Features
- **3-Line AI Summaries**: Concise summary of three key points from complex documents
- **Expandable Details**: Click any summary line to reveal 3 supporting bullet points
- **Progressive Disclosure**: Reduces cognitive load by showing details only when needed
- **Adaptive Content**: Customized to user preferences and cognitive profiles
- **Visual Representations**: Planned feature for future implementation

## Problem & Solution

Many individuals with cognitive disabilities struggle with dense content. Traditional summarizers focus on condensing information without considering cognitive accessibility. NoteNest bridges this gap with summaries designed using cognitive science principles, making learning more accessible and engaging.

## Technical Overview

### Tech Stack
- **Backend**: Python with LangChain for RAG processing
- **AI Integration**: OpenAI API for summarization
- **Frontend**: Swift iOS application
- **Design**: Figma prototypes

### Repository Structure
```
noterag/
├── backend/                  # Python RAG processing
│   ├── api.py                # API routes
│   ├── rag_pipeline.py       # LangChain flow
│   └── test_api.py           # For test
├── frontend/                 # iOS application
│   └── ProjectX/             # Swift implementation
├── scripts/                  # Development scripts
├── data/                     # Sample documents
├── prompts/                  # Prompt templates
├── README.md
└── requirements.txt
```

## Quick Start

```bash
# Clone & install
git clone https://github.com/kwonnayeon/noteRAG.git
cd noteRAG
pip install -r requirements.txt

# Set up OpenAI API key
export OPENAI_API_KEY="your_api_key_here"

# Run backend
cd backend
python api.py

# For iOS frontend
cd ../frontend/ProjectX
open noteRAG.xcodeproj
```

## Implementation Highlights

- **Learning Experience Optimization**:
  - Progressive disclosure of information (click to expand)
  - Reduced cognitive burden through targeted summaries
  - Step-by-step exploration of complex topics
  - On-demand detail visibility

- **RAG-Enhanced Learning**:
  - Smart document processing
  - Contextual understanding
  - Personalized content adaptation

## Sample Files

The `data/` directory contains example files demonstrating the input and output formats:

- **Input**: Text files (`.txt`) containing content to be summarized
- **Output**: 
  - `.json` files with structured summary data for iOS app
  - `.pdf` files with formatted summaries for viewing/sharing

You can use these samples to understand the transformation process and expected formats.

## Hackathon Project

This project was developed for Student@AI by Project X.

## License

MIT License
