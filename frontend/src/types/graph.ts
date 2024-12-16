export interface Entity {
  id: string;
  label: string;
  type: 'person' | 'organization' | 'location' | 'date' | 'account' | 'phone' | 'other';
  isAnomaly?: boolean;
}

export interface Relationship {
  id: string;
  source: string;
  target: string;
  label: string;
}

export interface GraphData {
  entities: Entity[];
  relationships: Relationship[];
}