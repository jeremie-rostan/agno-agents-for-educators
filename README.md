# Agno Agents for Educators

A collection of AI agent examples built with [Agno](https://github.com/agno-agi/agno) designed specifically for educational use cases.

## Overview

This repository showcases practical multi-agent systems that help educators with various tasks, from teacher evaluations to curriculum development. Each example demonstrates how to build sophisticated AI workflows using Agno's agent framework.

## Examples

### 1. Teacher Evaluation Multi-Agent System

A team of three specialized agents that collaboratively analyze teacher evaluations and generate professional development reports.

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

## Getting Started

### Prerequisites

- Python 3.10+
- Google API key (for Gemini models)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/agno-agents-for-educators.git
cd agno-agents-for-educators

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
agno-agents-for-educators/
├── examples/
│   └── teacher-evaluation/
│       ├── app.py              # Main application
│       ├── ISP_Way.txt         # Sample institutional document
│       └── README.md           # Example-specific documentation
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
