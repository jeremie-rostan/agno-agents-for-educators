# Teacher Evaluation Multi-Agent System

A collaborative AI system that analyzes teacher evaluations and generates professional development reports with evidence-based strategies.

## Overview

This example demonstrates how to build a multi-agent system using Agno that:
1. Analyzes teacher evaluations against institutional standards using document search
2. Identifies specific growth areas aligned with best practices
3. Researches evidence-based teaching strategies from high-quality educational sources
4. Generates structured professional development reports with actionable recommendations

## Architecture

### Agents

1. **ISP Way Analyst**
   - Uses Gemini's File Search to query the ISP Way document
   - Identifies gaps between current practice and institutional standards
   - References specific sections and principles from the document

2. **Strategy Researcher**
   - Uses web search to find evidence-based teaching strategies
   - Focuses on high-quality educational sources (Edutopia, ASCD, Cult of Pedagogy, etc.)
   - Provides implementation steps and verified source URLs

3. **Report Writer**
   - Synthesizes findings into a structured report
   - Uses Pydantic models to ensure consistent output format
   - Matches growth areas with relevant strategies

### Team Workflow

The agents work together in a coordinated workflow:
1. ISP Way Analyst reviews the evaluation and identifies growth areas
2. Strategy Researcher finds specific strategies for each growth area
3. Report Writer combines everything into a structured professional development report

## Setup

### Prerequisites

- Python 3.10+
- Google API key (for Gemini models)

### Installation

```bash
# Navigate to this example directory
cd examples/teacher-evaluation

# Install dependencies (from repository root)
pip install -r ../../requirements.txt

# Set up environment variables
cp ../../.env.example ../../.env
# Edit .env and add your GOOGLE_API_KEY
```

### Running the Application

```bash
python app.py
```

The AgentOS server will start at `http://localhost:7777`.

## Usage

### Via Web Interface

1. Open your browser to `http://localhost:7777`
2. Enter a teacher evaluation as input
3. The agent team will collaboratively analyze it and generate a report

### Via API

```bash
curl -X POST http://localhost:7777/v1/teams/teacher-evaluation-team/runs \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Teacher showed good classroom management but struggled with differentiating instruction for diverse learners. Students were engaged but lessons followed a one-size-fits-all approach."
  }'
```

## Example Input

```
Teacher: Ms. Johnson
Subject: 5th Grade Math

Observation Notes:
- Classroom management is excellent, students are attentive and respectful
- Lesson followed a traditional lecture format with limited student interaction
- All students received the same worksheet regardless of ability level
- No evidence of formative assessment during the lesson
- Students with IEPs were not provided accommodations
- Limited use of technology or manipulatives
```

## Example Output Structure

```json
{
  "teacher_name": "Ms. Johnson",
  "evaluation_summary": "...",
  "growth_areas": [
    {
      "area": "Differentiated Instruction",
      "isp_way_alignment": "...",
      "current_gap": "..."
    }
  ],
  "recommended_strategies": [
    {
      "name": "Universal Design for Learning (UDL)",
      "description": "...",
      "implementation_steps": ["...", "..."],
      "source_title": "...",
      "source_url": "https://..."
    }
  ],
  "priority_actions": ["...", "..."]
}
```

## Customization

### Using Your Own Institutional Document

Replace `ISP_Way.txt` with your own teaching standards document. The File Search feature will automatically index and search your document.

### Modifying the Output Structure

Edit the Pydantic models in `app.py`:
- `Strategy` - Structure for teaching strategies
- `GrowthArea` - Structure for areas needing improvement
- `TeacherDevelopmentReport` - Overall report structure

### Adding More Agents

You can extend the team with additional agents, such as:
- A data analyst to track progress over time
- A resource curator to build a personalized library
- A goal-setting coach to create SMART goals

## Technical Details

### File Search Setup

The application uses Gemini's File Search to query the ISP Way document:

```python
model = Gemini(id="gemini-2.5-flash-lite")
store = model.create_file_search_store(display_name="ISP Way Documents")
model.upload_to_file_search_store(file_path=ISP_WAY_DOCUMENT, store_name=store.name)
model.file_search_store_names = [store.name]
```

### Structured Output

The Report Writer agent uses Pydantic models for structured output:

```python
report_writer = Agent(
    name="Report Writer",
    output_schema=TeacherDevelopmentReport,
    # ...
)
```

## License

MIT License
