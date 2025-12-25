"""
Teacher Evaluation System with Gradio Interface (Simplified for Local Models)
==============================================================================
A beautiful web interface optimized for smaller local LMStudio models.
Uses simpler output format instead of complex structured schemas.
"""

from pathlib import Path
import gradio as gr

from agno.agent import Agent
from agno.models.lmstudio import LMStudio
from agno.tools.file import FileTools
from agno.workflow import Workflow

# Path to the ISP Way document (relative to this file)
ISP_WAY_DOCUMENT = Path(__file__).parent / "ISP_Way.txt"

# =============================================================================
# MODEL AND AGENT DEFINITIONS
# =============================================================================

# Configure LMStudio model
lmstudio_model = LMStudio(
    id="openai/gpt-oss-20b",
    base_url="http://localhost:1234/v1"
)

# Agent 1: ISP Way Document Analyst
isp_way_analyst = Agent(
    name="ISP Way Document Analyst",
    model=lmstudio_model,
    role="Analyzes teacher evaluations against the ISP Way document.",
    tools=[FileTools(base_dir=Path(__file__).parent)],
    instructions=[
        f"CRITICAL: You MUST read the ISP Way document at: {ISP_WAY_DOCUMENT}",
        "",
        "STEP 1: Use the read_file tool to read ISP_Way.txt",
        "STEP 2: Analyze the teacher evaluation against what you read",
        "STEP 3: Identify 2-3 growth areas where current practice differs from ISP Way",
        "",
        "For EACH growth area, you MUST:",
        "1. State the growth area clearly",
        "2. Find and copy an EXACT quote from the ISP Way document (word-for-word)",
        "3. Explain how the teacher's current practice differs from this quote",
        "",
        "REQUIRED FORMAT (follow exactly):",
        "## Growth Area 1: [Specific Area Name]",
        "**ISP Way Quote:** \"[Copy exact words from document - do NOT paraphrase]\"",
        "**Current Practice:** [What the teacher is doing now]",
        "**Gap:** [How current practice differs from the ISP Way quote]",
        "",
        "## Growth Area 2: [Specific Area Name]",
        "**ISP Way Quote:** \"[Copy exact words from document]\"",
        "**Current Practice:** [What the teacher is doing now]",
        "**Gap:** [How current practice differs from the ISP Way quote]",
        "",
        "IMPORTANT: The quotes MUST be actual text from ISP_Way.txt, not your own words.",
    ],
    markdown=True,
)

# Agent 2: Strategy Developer
strategy_developer = Agent(
    name="Strategy Developer",
    model=lmstudio_model,
    role="Develops practical teaching strategies.",
    instructions=[
        "Based on the growth areas provided, develop 2-3 SPECIFIC teaching strategies.",
        "",
        "For EACH strategy, you MUST provide:",
        "1. A clear, descriptive name",
        "2. A 2-3 sentence description of what it is",
        "3. 4-5 implementation steps - each step MUST include a concrete classroom example",
        "4. 2-3 specific benefits for student learning",
        "",
        "REQUIRED FORMAT (follow exactly):",
        "## Strategy 1: [Descriptive Strategy Name]",
        "",
        "**What it is:**",
        "[2-3 sentences describing the strategy]",
        "",
        "**How to implement:**",
        "",
        "**Step 1:** [Action to take]",
        "*Example:* [Specific classroom example - be concrete!]",
        "",
        "**Step 2:** [Action to take]",
        "*Example:* [Specific classroom example]",
        "",
        "**Step 3:** [Action to take]",
        "*Example:* [Specific classroom example]",
        "",
        "**Step 4:** [Action to take]",
        "*Example:* [Specific classroom example]",
        "",
        "**Benefits:**",
        "- [Specific benefit 1]",
        "- [Specific benefit 2]",
        "- [Specific benefit 3]",
        "",
        "---",
        "",
        "IMPORTANT: Examples must be CONCRETE and SPECIFIC to the classroom context.",
        "Focus on: UDL principles, active learning, student collaboration, formative assessment, differentiation",
    ],
    markdown=True,
)

# Agent 3: Report Writer
report_writer = Agent(
    name="Report Writer",
    model=lmstudio_model,
    role="Creates a comprehensive professional development report.",
    instructions=[
        "You will receive:",
        "1. ISP Way analysis with growth areas and EXACT QUOTES",
        "2. Teaching strategies with detailed implementation steps and examples",
        "",
        "Your job: Combine them into ONE complete report.",
        "",
        "REQUIRED FORMAT (follow exactly):",
        "",
        "# Professional Development Report",
        "**For [Teacher Name]**",
        "",
        "## Summary",
        "[Write 2-3 sentences summarizing the key findings]",
        "",
        "---",
        "",
        "## Growth Areas & ISP Way Alignment",
        "",
        "[Copy ALL growth areas from the analyst - include the ISP Way quotes!]",
        "",
        "---",
        "",
        "## Recommended Strategies",
        "",
        "[Copy ALL strategies from the developer - include all steps and examples!]",
        "",
        "---",
        "",
        "## Priority Actions",
        "",
        "1. **[First action]** - [Why this is most important]",
        "2. **[Second action]** - [Why this comes next]",
        "3. **[Third action]** - [Why this is third priority]",
        "",
        "---",
        "",
        "*This plan aligns with ISP Way principles and provides actionable steps for professional growth.*",
        "",
        "CRITICAL:",
        "- Copy the EXACT ISP Way quotes from the analyst (do NOT rewrite them)",
        "- Include ALL implementation steps and examples from the strategies",
        "- Maintain supportive, growth-oriented tone",
        "- Do NOT summarize or shorten the content - include everything!",
    ],
    markdown=True,
)

# =============================================================================
# WORKFLOW
# =============================================================================

def workflow_steps(workflow: Workflow, execution_input):
    """Sequential workflow: Analyst -> Developer -> Writer"""

    from agno.workflow.types import WorkflowExecutionInput
    if isinstance(execution_input, WorkflowExecutionInput):
        user_input = execution_input.get_input_as_string()
    else:
        user_input = str(execution_input)

    # Step 1: ISP Way Analysis
    analyst_result = isp_way_analyst.run(user_input)
    analyst_output = analyst_result.content if hasattr(analyst_result, 'content') else str(analyst_result)

    # Step 2: Strategy Development
    developer_result = strategy_developer.run(
        f"Based on this ISP Way analysis, develop practical strategies:\n\n{analyst_output}"
    )
    developer_output = developer_result.content if hasattr(developer_result, 'content') else str(developer_result)

    # Step 3: Report Writing
    report_input = f"""
Create a professional development report using:

{analyst_output}

{developer_output}
"""
    report_result = report_writer.run(report_input)

    # Return the markdown content
    if hasattr(report_result, 'content'):
        return report_result.content
    else:
        return str(report_result)

teacher_evaluation_workflow = Workflow(
    name="Teacher Evaluation Workflow (LMStudio)",
    description="Analyzes teacher evaluations and generates professional development recommendations",
    steps=workflow_steps,
)

# =============================================================================
# GRADIO INTERFACE
# =============================================================================

def format_markdown_to_html(markdown_text: str) -> str:
    """Convert markdown report to styled HTML."""
    import re

    # Simple markdown to HTML conversion
    html = markdown_text

    # Headers
    html = re.sub(r'^# (.+)$', r'<h1 style="color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px;">\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2 style="color: #2c3e50; margin-top: 25px; border-bottom: 2px solid #e74c3c; padding-bottom: 8px;">\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3 style="color: #27ae60; margin-top: 15px;">\1</h3>', html, flags=re.MULTILINE)

    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

    # Lists
    html = re.sub(r'^- (.+)$', r'<li style="margin: 8px 0;">\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'^\d+\. (.+)$', r'<li style="margin: 8px 0;">\1</li>', html, flags=re.MULTILINE)

    # Wrap lists
    html = re.sub(r'(<li.*?</li>\n)+', r'<ul style="line-height: 1.8;">\g<0></ul>', html)

    # Quotes (look for lines starting with ")
    html = re.sub(r'^"(.+)"$', r'<blockquote style="background: #fef9e7; border-left: 4px solid #f39c12; padding: 15px; margin: 15px 0; font-style: italic; border-radius: 4px;">"\1"</blockquote>', html, flags=re.MULTILINE)

    # Paragraphs
    lines = html.split('\n')
    formatted_lines = []
    for line in lines:
        if line.strip() and not line.strip().startswith('<'):
            formatted_lines.append(f'<p style="line-height: 1.6; color: #333;">{line}</p>')
        else:
            formatted_lines.append(line)

    html = '\n'.join(formatted_lines)

    # Wrap in container
    html = f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px;">
        {html}
    </div>
    """

    return html


def process_evaluation(teacher_name: str, evaluation_text: str, progress=gr.Progress()) -> tuple:
    """Process the teacher evaluation through the workflow."""

    if not evaluation_text.strip():
        return "<p style='color: red;'>Please provide evaluation feedback.</p>", ""

    try:
        progress(0, desc="Initializing workflow...")

        # Prepare input
        input_text = f"Teacher Evaluation"
        if teacher_name.strip():
            input_text += f" for {teacher_name}"
        input_text += f":\n\n{evaluation_text}"

        progress(0.3, desc="Analyzing ISP Way document...")

        # Run workflow
        result = teacher_evaluation_workflow.run(input_text)

        progress(0.9, desc="Generating report...")

        # Extract markdown content
        markdown_report = None
        if isinstance(result, str):
            markdown_report = result
        elif hasattr(result, 'content'):
            if isinstance(result.content, str):
                markdown_report = result.content
            elif hasattr(result.content, 'content'):
                markdown_report = str(result.content.content)

        if not markdown_report:
            return f"<p style='color: red;'>Error: Could not extract report content</p><pre>{str(result)[:1000]}</pre>", str(result)

        progress(1.0, desc="Complete!")

        # Convert to HTML
        html_output = format_markdown_to_html(markdown_report)

        return html_output, markdown_report

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"<p style='color: red;'>Error: {str(e)}</p><pre>{error_details[:1000]}</pre>", error_details


# Custom CSS
custom_css = """
.gradio-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}
.header {
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    margin-bottom: 20px;
}
"""

with gr.Blocks(css=custom_css, title="Teacher Evaluation System", theme=gr.themes.Soft()) as demo:

    gr.HTML("""
        <div class="header">
            <h1 style="margin: 0; font-size: 2.5em;">🎓 Teacher Evaluation System</h1>
            <p style="margin: 10px 0 0 0; font-size: 1.2em;">Powered by Local LMStudio (Simplified Version)</p>
        </div>
    """)

    gr.Markdown("""
        ### 📋 How It Works

        This system analyzes teacher evaluations against the **ISP Way** and generates development recommendations.

        **Optimized for local models** - uses simpler output format for better compatibility with smaller models.

        **You'll get:**
        - 📖 Exact quotes from ISP Way document
        - 🎯 Specific growth areas
        - 💡 Practical teaching strategies with examples
        - 🚀 Prioritized action items
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📝 Input")

            teacher_name_input = gr.Textbox(
                label="Teacher Name (Optional)",
                placeholder="e.g., Ms. Johnson",
                lines=1
            )

            evaluation_input = gr.Textbox(
                label="Evaluation Feedback",
                placeholder="""Enter evaluation feedback here. For example:

- Lessons are primarily teacher-led
- Uses mainly worksheets
- Limited student interaction
- Assessment doesn't inform instruction""",
                lines=12
            )

            submit_btn = gr.Button("🚀 Generate Development Plan", variant="primary", size="lg")

            gr.Markdown("""
                **⚠️ Note:** Make sure LMStudio is running with `openai/gpt-oss-20b` loaded (port 1234)
            """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📊 Professional Development Report")

            with gr.Tab("📄 Report"):
                html_output = gr.HTML(label="Formatted Report")

            with gr.Tab("📝 Markdown"):
                markdown_output = gr.Code(label="Markdown Source", language="markdown")

    # Connect the button
    submit_btn.click(
        fn=process_evaluation,
        inputs=[teacher_name_input, evaluation_input],
        outputs=[html_output, markdown_output]
    )

    # Examples
    gr.Examples(
        examples=[
            ["Ms. Johnson", "- Lessons are primarily teacher-led\n- Uses mainly worksheets\n- Limited student interaction\n- Assessment is primarily summative"],
            ["Mr. Chen", "- Strong lectures but passive students\n- Recall-based questions\n- No collaboration\n- Same lesson for all students"],
        ],
        inputs=[teacher_name_input, evaluation_input],
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
