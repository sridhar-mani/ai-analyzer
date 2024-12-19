from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class DocumentAnalysisRequest(BaseModel):
    documents: List[str]
    language: Optional[str] = "en"

class EntityModel(BaseModel):
    value: str
    type: str
    context: Optional[str] = None
    confidence: float = Field(default=0.5, ge=0, le=1)

class RelationModel(BaseModel):
    source: str
    target: str
    type: str
    confidence: float = Field(default=0.5, ge=0, le=1)

class AnomalyModel(BaseModel):
    description: str
    severity: str = Field(default="MEDIUM")
    related_entities: List[str] = Field(default_factory=list)
    potential_impact: Optional[str] = None

class CaseInfo(BaseModel):
    headline: str = ""
    type: str
    page_number: int

class GraphVizModel(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    
    class Config:
        arbitrary_types_allowed = True

class CaseAnalysis(BaseModel):
    entities: List[EntityModel] = Field(default_factory=list)
    relationships: List[RelationModel] = Field(default_factory=list)
    anomalies: List[AnomalyModel] = Field(default_factory=list)
    graph_data: Optional[GraphVizModel] = None

class CaseInfo(BaseModel):
    case_id: str
    headline: str
    type: str
    page_number: int
    content: str
    ai_analysis: Optional[CaseAnalysis] = None

class DocumentAnalysisResponse(BaseModel):
    filename: str
    cases: List[CaseInfo]