# Agno Apps for Educators

> **Part of the [AI Apps for Educators](../) collection**

A collection of AI applications built with the [Agno](https://github.com/agno-agi/agno) framework, designed specifically for educational use cases. These applications demonstrate how to build sophisticated multi-agent systems, chatbots, and tools using Agno's powerful framework.

## Overview

This folder contains Agno-based applications that help educators with various tasks, from teacher evaluations to curriculum development. Each example demonstrates how to build sophisticated AI workflows using Agno's agent framework.

## Examples

### 1. Teacher Evaluation Multi-Agent System (Cloud-based)

A team of three specialized agents that collaboratively analyze teacher evaluations and generate professional development reports using Google Gemini.

**What it does:**
- Analyzes teacher evaluations against institutional teaching standards (ISP Way document)
- Identifies specific growth areas aligned with best practices
- Searches the web for evidence-based teaching strategies from high-quality sources
- Generates structured professional development reports with actionable recommendations

**Key Features:**
- Uses Gemini's File Search to query institutional documents
- Web search integration for finding current educational resources
- Structured output using Pydantic models
- AgentOS integration for easy deployment

**Agents:**
1. **ISP Way Analyst** - Reviews evaluations against teaching standards
2. **Strategy Researcher** - Finds evidence-based strategies from educational sources
3. **Report Writer** - Synthesizes findings into structured reports

[View Example →](examples/teacher-evaluation/)

### 2. Teacher Evaluation Multi-Agent System (Local Model)

The same teacher evaluation workflow, but optimized to run completely locally using LMStudio with open-source models.

**What it does:**
- 100% local processing (no cloud APIs required)
- Analyzes evaluations against ISP Way document using local file access
- Generates professional development reports with detailed strategies
- Beautiful Gradio web interface

**Key Features:**
- Privacy-focused: All data stays on your machine
- Runs on local LMStudio models (tested with 20B parameter models)
- Simplified markdown output format for better compatibility with smaller models
- No API costs or internet connection required

**Agents:**
1. **ISP Way Document Analyst** - Reads and analyzes against teaching standards
2. **Strategy Developer** - Creates actionable teaching strategies
3. **Report Writer** - Combines findings into comprehensive reports

[View Example →](examples/teacher-evaluation-lmstudio/)

## Getting Started

### Prerequisites

- Python 3.10+
- Google API key (for Gemini models)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/AI-Apps-for-Educators.git
cd AI-Apps-for-Educators/agno-apps

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### Running an Example

```bash
# Navigate to an example directory
cd examples/teacher-evaluation

# Run the AgentOS server
python app.py
```

The server will start at `http://localhost:7777`. You can interact with the agent team through the web interface or API.

## Project Structure

```
agno-apps/
├── examples/
│   ├── teacher-evaluation/          # Cloud-based (Gemini)
│   │   ├── app.py                   # Main application
│   │   ├── ISP_Way.txt              # Sample institutional document
│   │   └── README.md                # Example-specific documentation
│   └── teacher-evaluation-lmstudio/ # Local model (LMStudio)
│       ├── app.py                   # Main application
│       ├── ISP_Way.txt              # Sample institutional document
│       └── README.md                # Example-specific documentation
├── requirements.txt
├── .env.example
└── README.md
```

## About Agno

[Agno](https://github.com/agno-agi/agno) is a powerful framework for building multi-agent AI systems. It provides:
- Simple agent and team abstractions
- Built-in tools (web search, file search, code execution)
- Support for multiple LLM providers
- AgentOS for easy deployment and management

## Contributing

Contributions are welcome! If you have educational use cases that could benefit from multi-agent systems, feel free to submit a pull request.

## License

MIT License - See LICENSE file for details

## Resources

- [Agno Documentation](https://docs.agno.sh)
- [Agno GitHub Repository](https://github.com/agno-agi/agno)
- [Google AI for Developers](https://ai.google.dev)
