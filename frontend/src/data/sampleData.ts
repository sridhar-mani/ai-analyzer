import { GraphData } from '../types/graph';

export const sampleData: GraphData = {
  entities: [
    { id: '1', label: 'John Doe', type: 'person' },
    { id: '2', label: 'Acme Corp', type: 'organization' },
    { id: '3', label: 'New York', type: 'location' },
    { id: '4', label: '2024-03-15', type: 'date' },
    { id: '5', label: 'ACC123456', type: 'account', isAnomaly: true },
  ],
  relationships: [
    { id: 'r1', source: '1', target: '2', label: 'works at' },
    { id: 'r2', source: '2', target: '3', label: 'located in' },
    { id: 'r3', source: '1', target: '5', label: 'owns' },
    { id: 'r4', source: '5', target: '4', label: 'created on' },
  ],
};