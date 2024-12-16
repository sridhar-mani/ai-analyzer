import { GraphData } from '../types/graph';
import { EdgeDefinition, NodeDefinition, Stylesheet } from 'cytoscape';

export const createElements = (data: GraphData): (NodeDefinition | EdgeDefinition)[] => {
  const nodes = data.entities.map((entity) => ({
    group: 'nodes' as const,
    data: {
      id: entity.id,
      label: entity.label,
      type: entity.type,
      isAnomaly: entity.isAnomaly,
    },
  }));

  const edges = data.relationships.map((rel) => ({
    group: 'edges' as const,
    data: {
      id: rel.id,
      source: rel.source,
      target: rel.target,
      label: rel.label,
    },
  }));

  return [...nodes, ...edges];
};

export const graphStyles: Stylesheet[] = [
  {
    selector: 'node',
    style: {
      'background-color': '#6366f1',
      'label': 'data(label)',
      'text-valign': 'center',
      'text-halign': 'center',
      'font-size': '12px',
      'width': '80px',
      'height': '80px',
      'color': '#ffffff',
      'text-wrap': 'wrap',
      'text-max-width': '80px',
    },
  },
  {
    selector: 'node[type="person"]',
    style: {
      'background-color': '#3b82f6',
    },
  },
  {
    selector: 'node[type="organization"]',
    style: {
      'background-color': '#8b5cf6',
    },
  },
  {
    selector: 'node[type="location"]',
    style: {
      'background-color': '#10b981',
    },
  },
  {
    selector: 'node[type="date"]',
    style: {
      'background-color': '#f59e0b',
    },
  },
  {
    selector: 'node[type="account"]',
    style: {
      'background-color': '#ec4899',
    },
  },
  {
    selector: 'node[?isAnomaly]',
    style: {
      'background-color': '#ef4444',
      'border-width': '3px',
      'border-color': '#991b1b',
    },
  },
  {
    selector: 'edge',
    style: {
      'width': 2,
      'line-color': '#94a3b8',
      'target-arrow-color': '#94a3b8',
      'target-arrow-shape': 'triangle',
      'curve-style': 'bezier',
      'label': 'data(label)',
      'font-size': '10px',
      'text-rotation': 'autorotate',
      'text-background-color': '#ffffff',
      'text-background-opacity': 1,
      'text-background-padding': '2px',
    },
  },
];