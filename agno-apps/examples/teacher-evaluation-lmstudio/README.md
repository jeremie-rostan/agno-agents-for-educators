# Teacher Evaluation System (LMStudio Local Model)

A multi-agent system that provides professional development recommendations for teachers using a **locally-running LMStudio model**. No cloud APIs required!

## Features

- **100% Local Processing**: Uses your own LMStudio model (no data sent to cloud services)
- **ISP Way Document Analysis**: Searches and quotes directly from the ISP Way document
- **Beautiful Gradio Interface**: Professional web UI with formatted reports
- **Markdown Output**: Easy to read and export
- **Optimized for Small Models**: Uses simplified output format for better compatibility with 20B parameter models

## Architecture

The system uses three specialized agents in a sequential workflow:

1. **ISP Way Document Analyst**:
   - Uses FileTools to read and search the ISP Way document
   - Extracts exact quotes relevant to the evaluation
   - Identifies 2-3 specific gaps between current practice and ISP Way standards

2. **Strategy Developer**:
   - Creates 2-3 detailed, actionable teaching strategies
   - Provides implementation steps with concrete classroom examples
   - Ensures alignment with ISP Way principles (UDL, active learning, differentiation)

3. **Report Writer**:
   - Combines findings into a comprehensive markdown report
   - Matches strategies to growth areas
   - Prioritizes top 3 actions by impact and feasibility

## Prerequisites

### 1. LMStudio Setup

1. Download and install [LMStudio](https://lmstudio.ai/)
2. Download a model (tested with `openai/gpt-oss-20b`, but compatible with other models)
3. Start the LMStudio local server:
   - Open LMStudio
   - Go to the "Local Server" tab
   - Load your model
   - Click "Start Server"
   - Note the port (default: `1234`)

### 2. Python Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

If your LMStudio server runs on a different port or you want to use a different model, edit `app.py`:

```python
lmstudio_model = LMStudio(
    id="your-model-name",  # Change to your model
    base_url="http://localhost:YOUR_PORT/v1"  # Change port if needed
)
```

## Usage

### Running the Application

```bash
python app.py
```

The application will start on `http://localhost:7860`

### Using the Interface

1. Make sure LMStudio is running (see Prerequisites)
2. Run `python app.py`
3. Open your browser to `http://localhost:7860`
4. Enter teacher name (optional) and evaluation feedback
5. Click "🚀 Generate Development Plan"
6. The system will:
   - Analyze the evaluation against ISP Way standards
   - Extract exact quotes from the ISP Way document
   - Develop detailed strategies with implementation steps and examples
   - Generate a beautifully formatted professional development report
7. View the report in formatted HTML or raw Markdown

### Example Input

```
Teacher: Ms. Johnson
Evaluation Feedback:
- Lessons are primarily teacher-led with limited student interaction
- Uses mainly worksheets and textbook activities
- Assessment is primarily summative (tests and quizzes)
- Students work individually most of the time
- Limited use of technology in instruction
```

### Example Output

The system generates a markdown report with:

- **Summary**: 2-3 sentence overview of findings
- **Growth Areas**: 2-3 areas with:
  - Clear description of the area
  - Exact quote from ISP Way document
  - Explanation of the gap
- **Recommended Strategies**: 2-3 strategies with:
  - Strategy name and description
  - 3-4 implementation steps with concrete examples
  - Expected benefits for students
- **Priority Actions**: Top 3 actions ranked by impact

The Gradio interface automatically converts the markdown to beautifully styled HTML.

## Files

- `app.py`: Main Gradio application with all agents and workflow
- `ISP_Way.txt`: The ISP Way teaching philosophy document
- `requirements.txt`: Python dependencies
- `README.md`: This file

## Optimized for Smaller Local Models

Unlike complex structured output formats (JSON schemas), this version uses:

- ✅ **Simple Markdown format** - much easier for 20B parameter models
- ✅ **Clear formatting instructions** - models just follow markdown patterns
- ✅ **No nested JSON** - avoids complex schema validation
- ✅ **Graceful degradation** - works with various model sizes

### Key Differences from Cloud Version

| Feature | Cloud Version | LMStudio Version |
|---------|--------------|------------------|
| Model | Google Gemini | Local LMStudio (openai/gpt-oss-20b) |
| Output Format | Complex JSON Schema | Simple Markdown |
| ISP Way Access | Gemini File Search API | Local FileTools |
| Web Search | Yes (Gemini search) | No (local only) |
| Data Privacy | Sent to Google | 100% local |
| Model Requirements | N/A | 20B+ parameters recommended |

### Advantages of Local Model

1. **Privacy**: All data stays on your machine
2. **Cost**: No API fees
3. **Control**: Full control over the model and data
4. **Offline**: Works without internet connection
5. **Customizable**: Can swap models easily

## Limitations

- No web search for current teaching strategies (uses model knowledge)
- Strategy quality depends on your local model's capabilities
- Requires sufficient local compute resources (16GB+ RAM recommended)
- Initial model loading time (one-time per session)

## Troubleshooting

### "Connection error" when running app

- Ensure LMStudio is running and the server is started
- Check that the port in `app.py` matches your LMStudio server port (default: 1234)
- Verify your model is loaded in LMStudio

### "File not found" errors

- Ensure `ISP_Way.txt` is in the same directory as `app.py`
- Check file permissions

### Slow responses

- Local models are slower than cloud APIs
- 20B parameter models need good hardware (GPU recommended)
- Consider using a smaller/faster model if speed is critical
- Ensure sufficient RAM (16GB minimum, 32GB recommended)

### Poor quality outputs

- Larger models (30B+) will produce better results
- Try adjusting the temperature in the model settings
- Ensure the model is fully loaded before running

## Customization

### Using a Different Model

Edit the model configuration in `app.py`:

```python
lmstudio_model = LMStudio(
    id="your-model-name-here",  # e.g., "mistral-7b-instruct"
    base_url="http://localhost:1234/v1"
)
```

Models tested:
- ✅ `openai/gpt-oss-20b` - Works well

### Changing Report Format

Edit agent instructions in `app.py` to customize:
- Number of growth areas (default: 2-3)
- Number of strategies (default: 2-3)
- Number of implementation steps per strategy (default: 3-4)
- Number of priority actions (default: 3)

### Adding More Documents

Extend the FileTools to include additional reference documents:

```python
tools=[FileTools(base_dir=Path(__file__).parent)]
```

Then reference them in the agent instructions.

## License

See the main repository license.
