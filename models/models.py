from pydantic import BaseModel, Field, ConfigDict
from typing import List,Dict, Optional,Any

class DocumentAnalysisRequest(BaseModel):
    documents : List[str]
    language: Optional[str]="en"
    
class EntityModel(BaseModel):
    value: str
    type: str
    context: Optional[str] =None
    confidence: float = Field(default=0.5,ge=0,le=1)
    
class RelationModel(BaseModel):
    source: str
    target: str
    type: str
    confidence: float = Field(default=0.5,ge=0,le=1)
    
class AnomalyModel(BaseModel):
    description: str
    severity: str = Field(default="MEDIUM")
    related_entities: List[str]=[]
    potential_impact: Optional[str] = None
    
class GraphVizModel(BaseModel):
    nodes:List[Dict[str,Any]]
    edges:List[Dict[str,Any]]
    model_config=ConfigDict(arbitrary_types_allowed=True)

    
class DocumentAnalysisResponce(BaseModel):
    entities: List[EntityModel]
    relations: List[RelationModel]
    anomalies: List[AnomalyModel]
    graph_data: Optional[GraphVizModel]
    
