import { GraphData } from "../store/useAiStore";

export const sanitizeGraphData = (data: any): GraphData => {

  const entities = Array.isArray(data.entities) ? data.entities : [];
  
  const relationships = Array.isArray(data.relationships) ? data.relationships : [];
  

  const validRelationships = relationships.filter(rel => {
    if (!rel?.source || !rel?.target) return false;
    

    const sourceExists = entities.some(entity => entity.id === rel.source);
    const targetExists = entities.some(entity => entity.id === rel.target);
    
    return sourceExists && targetExists;
  });
  
  return {
    entities,
    relationships: validRelationships
  };
};

export const validateEntity = (entity: any) => {
  return {
    id: entity?.id || `node-${Math.random().toString(36).substr(2, 9)}`,
    label: entity?.label || 'Unnamed',
    type: entity?.type || 'default',
    isAnomaly: !!entity?.isAnomaly
  };
};