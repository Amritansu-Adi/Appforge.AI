"""
ai-service/parsers/overview_parser.py
Owner: Prateeksha
Status: STUB — implement in Phase 2.3

Build a PydanticOutputParser(pydantic_object=OverviewOutput) using Pydantic v2 BaseModel.
"""
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal

class OverviewOutput(BaseModel):
    app_name: str = Field(description="Short memorable name for the app")
    one_liner: str = Field(description="One sentence description of the app")
    target_users: list[str] = Field(description="List of user types")
    core_features: list[str] = Field(description="Main features, min 3 max 8")
    complexity: Literal["simple", "standard", "complex"]
    tech_notes: str = Field(description="Any implicit technical requirements")
    data_entities: list[str] = Field(description="Key data objects the app will manage")

overview_parser = PydanticOutputParser(pydantic_object=OverviewOutput)
