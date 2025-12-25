"""
Teacher Evaluation Multi-Agent System
=====================================
A team of agents that:
1. Receives teacher evaluation input (via AgentOS)
2. Searches the ISP Way document to identify growth areas
3. Searches online for high-quality teaching strategies
4. Generates a structured professional development report
"""

from typing import List, Optional
from pathlib import Path
from pydantic import BaseModel, Field
import time

from agno.agent import Agent
from agno.team.team import Team
from agno.models.google import Gemini
from agno.os import AgentOS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Path to the ISP Way document (relative to this file)
ISP_WAY_DOCUMENT = Path(__file__).parent / "ISP_Way.txt"


# =============================================================================
# PYDANTIC MODELS FOR STRUCTURED OUTPUT
# =============================================================================

class Strategy(BaseModel):
    """A specific teaching strategy with implementation details."""
    name: str = Field(description="Name of the teaching strategy")
    description: str = Field(description="Brief description of the strategy")
    implementation_steps: List[str] = Field(description="Step-by-step guide to implement this strategy")
    source_title: str = Field(description="Title of the source article or resource")
    source_url: str = Field(description="URL link to the source")


class GrowthArea(BaseModel):
    """An area where the teacher can improve, aligned with ISP Way expectations."""
    area: str = Field(description="The specific area needing growth")
    isp_way_alignment: str = Field(description="How this aligns with ISP Way expectations and principles")
    current_gap: str = Field(description="Description of the gap between current practice and ISP Way standards")


class TeacherDevelopmentReport(BaseModel):
    """Structured report for teacher professional development."""
    teacher_name: Optional[str] = Field(default=None, description="Name of the teacher being evaluated")
    evaluation_summary: str = Field(description="Brief summary of the evaluation findings")
    growth_areas: List[GrowthArea] = Field(description="Areas identified for professional growth")
    recommended_strategies: List[Strategy] = Field(description="Specific strategies to address growth areas")
    priority_actions: List[str] = Field(description="Top 3-5 priority actions for immediate implementation")


# =============================================================================
# FILE SEARCH SETUP FOR ISP WAY DOCUMENT
# =============================================================================

def create_isp_way_model() -> tuple[Gemini, str]:
    """
    Creates a Gemini model configured with File Search on the ISP Way document.
    Returns the configured model and the store name for cleanup.
    """
    model = Gemini(id="gemini-2.5-flash-lite")
    
    # Create a File Search store
    store = model.create_file_search_store(display_name="ISP Way Documents")
    
    # Upload the ISP Way document to the store
    operation = model.upload_to_file_search_store(
        file_path=ISP_WAY_DOCUMENT,
        store_name=store.name,
        display_name="The ISP Way - Teaching and Learning Philosophy",
    )
    
    # Wait for the upload/indexing to complete
    model.wait_for_operation(operation)
    
    # Configure the model to use this File Search store
    model.file_search_store_names = [store.name]
    
    return model, store.name


# Create the model with File Search configured
isp_way_model, isp_way_store_name = create_isp_way_model()


# =============================================================================
# AGENT DEFINITIONS
# =============================================================================

# Agent 1: ISP Way Analyst
# Uses File Search to analyze evaluation against ISP Way standards
isp_way_analyst = Agent(
    name="ISP Way Analyst",
    model=isp_way_model,  # Model configured with File Search
    role="Analyzes teacher evaluations against the ISP Way document to identify areas for growth.",
    instructions=[
        "You have access to the ISP Way document via File Search, which outlines teaching expectations at ISP.",
        "When given a teacher evaluation, search the ISP Way document to find relevant standards.",
        "Identify specific areas where the teacher's practice does not align with ISP Way expectations.",
        "Be specific about which ISP Way principles or practices are not being met.",
        "Focus on actionable growth areas, not general criticism.",
        "Reference specific sections of the ISP Way in your analysis.",
    ],
    markdown=True,
)

# Agent 2: Strategy Researcher
# Uses web search to find high-quality teaching strategies
strategy_researcher = Agent(
    name="Strategy Researcher",
    model=Gemini(id="gemini-2.5-flash-lite", search=True),  # Built-in web search
    role="Searches for evidence-based teaching strategies from high-quality educational resources.",
    instructions=[
        "CRITICAL: You MUST use the web search tool to find strategies. Do NOT make up or guess URLs.",
        "CRITICAL: ONLY provide URLs that appear in your actual search results.",
        "CRITICAL: If you cannot find a URL in your search results, do NOT include that strategy.",
        "",
        "Search for specific, actionable teaching strategies to address identified growth areas.",
        "Focus on high-quality educational sources such as:",
        "  - Edutopia (edutopia.org)",
        "  - ASCD (ascd.org)",
        "  - Cult of Pedagogy (cultofpedagogy.com)",
        "  - TeachThought (teachthought.com)",
        "  - Harvard Graduate School of Education",
        "  - Stanford Center for Opportunity Policy in Education",
        "  - ISTE (iste.org)",
        "  - Learning Sciences International",
        "  - Educational Leadership journal",
        "  - Peer-reviewed educational research",
        "",
        "For each strategy found through web search:",
        "  1. Extract the exact URL from the search result",
        "  2. Extract the exact title from the search result",
        "  3. Provide the name of the strategy",
        "  4. Provide a clear description",
        "  5. Provide step-by-step implementation guidance",
        "",
        "VERIFICATION STEPS:",
        "  - Before providing a URL, verify it appeared in your search results",
        "  - Do NOT construct URLs based on domain names (e.g., do NOT create edutopia.org/article/...)",
        "  - Do NOT provide generic homepage URLs (e.g., just edutopia.org)",
        "  - Each URL must link to a specific article or resource from your search results",
        "  - If you cannot find a verified URL for a strategy, exclude that strategy from your response",
        "",
        "Prioritize strategies that are practical and classroom-ready.",
        "Ensure strategies align with UDL principles when possible.",
    ],
    markdown=True,
)

# Agent 3: Report Writer
# Synthesizes findings into a structured report
report_writer = Agent(
    name="Report Writer",
    model=Gemini(id="gemini-2.5-flash-lite"),
    role="Synthesizes analysis and strategies into a structured professional development report.",
    instructions=[
        "Create a comprehensive but concise professional development report.",
        "Ensure all growth areas reference specific ISP Way expectations.",
        "Match each growth area with relevant strategies from the researcher.",
        "Include clear implementation steps for each strategy.",
        "Prioritize actions based on impact and feasibility.",
        "Maintain a supportive, growth-oriented tone throughout.",
        "",
        "CRITICAL URL HANDLING:",
        "- You will receive strategies with URLs from the Strategy Researcher",
        "- You MUST copy the EXACT URLs provided by the researcher into the source_url field",
        "- Do NOT modify, shorten, or fabricate URLs",
        "- Do NOT create URLs that were not provided by the researcher",
        "- If a strategy from the researcher does not have a URL, do NOT include that strategy",
        "- The source_url field must contain the EXACT URL string from the researcher's output",
    ],
    output_schema=TeacherDevelopmentReport,
    markdown=True,
)


# =============================================================================
# TEAM CONFIGURATION
# =============================================================================

teacher_evaluation_team = Team(
    name="Teacher Evaluation Team",
    model=Gemini(id="gemini-2.5-flash-lite"),
    members=[isp_way_analyst, strategy_researcher, report_writer],
    instructions=[
        "You are a team that helps teachers grow professionally based on evaluation feedback.",
        "",
        "WORKFLOW:",
        "1. First, ask the ISP Way Analyst to review the teacher evaluation and identify",
        "   specific areas where practice does not align with ISP Way expectations.",
        "",
        "2. Then, for each growth area identified, ask the Strategy Researcher to find",
        "   specific, evidence-based strategies from high-quality educational resources.",
        "   CRITICAL: The researcher MUST use web search and ONLY provide URLs that appear",
        "   in actual search results. No made-up or constructed URLs are acceptable.",
        "",
        "3. Finally, ask the Report Writer to synthesize everything into a structured",
        "   professional development report with:",
        "   - Summary of evaluation findings",
        "   - Growth areas with ISP Way alignment",
        "   - Recommended strategies with implementation steps and sources",
        "   - Priority actions for immediate focus",
        "   CRITICAL: The Report Writer must use the EXACT URLs provided by the Strategy Researcher.",
        "   Do not allow the Report Writer to modify or fabricate URLs.",
        "",
        "4. Ensure the final output matches the TeacherDevelopmentReport structure:",
        "   - teacher_name (optional)",
        "   - evaluation_summary",
        "   - growth_areas (list of GrowthArea objects)",
        "   - recommended_strategies (list of Strategy objects with verified URLs)",
        "   - priority_actions (list of strings)",
        "",
        "IMPORTANT:",
        "- Be specific and actionable in all recommendations.",
        "- Maintain a supportive, growth-oriented tone.",
        "- Ensure all strategies have proper source attribution with VERIFIED URLs from search results.",
        "- Focus on practical, classroom-ready solutions.",
        "- Do NOT accept strategies without verified URLs from actual web search results.",
    ],
    add_member_tools_to_context=True,
    markdown=True,
    show_members_responses=True,
)


# =============================================================================
# AGENTOS APPLICATION
# =============================================================================

# Create the AgentOS with the team directly
agent_os = AgentOS(teams=[teacher_evaluation_team])

# Get the FastAPI app for deployment
app = agent_os.get_app()

if __name__ == "__main__":
    # Default port is 7777; change with port=...
    agent_os.serve(app="app:app", reload=True)
