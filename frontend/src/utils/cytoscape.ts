import cytoscape, { Stylesheet } from 'cytoscape';
import { GraphData } from '../store/useAiStore';

export const createElements = (data: GraphData): cytoscape.ElementDefinition[] => {
  const nodes = data.entities.map((entity) => ({
    group: 'nodes',
    data: {
      id: entity.id,
      label: entity.label,
      type: entity.type,
      isAnomaly: entity.isAnomaly,
      propertyType: entity.propertyType, 
    },
  }));

  const edges = data.relationships.map((rel) => ({
    group: 'edges',
    data: {
      id: rel.id,
      source: rel.source,
      target: rel.target,
      label: rel.type,
    },
  }));

  return [...nodes, ...edges];
};

export const graphStyles: Stylesheet[] = [
  {
    selector: 'node',
    style: {
      'background-color': '#00ff44',
      'border-color': '#047857', 
      'border-width': '3px',
      'shape': 'ellipse',
      'label': 'data(label)',
      'text-valign': 'center',
      'text-halign': 'center',
      'font-size': '12px',
      'color': '#1f2937',
      'text-wrap': 'ellipsis',
      'text-max-width': '100px', 
      'padding': '1px', 
      'width': '100px', 
      'height': '100px',
      'transition-property': 'background-color, border-width',
      'transition-duration': '0.5s',
      'transition-timing-function': 'ease-in-out',
      'text-overflow-wrap': 'anywhere',
    },
  },

  {
    selector: 'node[type="Person"]',
    style: {
      'background-color': '#00ff44',
      'border-color': '#047857',
    },
  },
  {
    selector: 'node[type="Organization"]',
    style: {
      'background-color': '#D8B4FE', 
      'border-color': '#6D28D9',
    },
  },
  {
    selector: 'node[type="location"]',
    style: {
      'background-color': '#BFDBFE',
      'border-color': '#1D4ED8', 
    },
  },
  {
    selector: 'node[type="date"]',
    style: {
      'background-color': '#FDE68A', 
      'border-color': '#CA8A04', 
    },
  },
  {
    selector: 'node[type="account"]',
    style: {
      'background-color': '#FBCFE8', 
      'border-color': '#DB2777', 
    },
  },
  {
    selector: 'node[type="contact"]',
    style: {
      'background-color': '#FFDD57', 
      'border-color': '#FBBF24', 
    },
  },
  {
    selector: 'node[type="Email"]',
    style: {
      'background-color': '#60A5FA', 
      'border-color': '#2563EB', 
    },
  },
  {
    selector: 'node[type="Phone Number"]',
    style: {
      'background-color': '#34D399',
      'border-color': '#10B981', 
    },
  },
  {
    selector: 'node[type="address"]',
    style: {
      'background-color': '#FECACA', 
      'border-color': '#F87171', 
    },
  },
  {
    selector: 'node[?isAnomaly]',
    style: {
      'background-color': '#FEE2E2', 
      'border-color': '#991B1B', 
      'border-width': '5px',
    },
  },
  {
    selector: 'node[label="fraud"], node[label="scam"]',
    style: {
      'background-color': '#FECACA',
      'border-color': '#B91C1C', 
      'border-width': '5px',
    },
  },
  {
    selector: 'edge',
    style: {
      'width': 2,
      'line-color': '#9CA3AF', 
      'target-arrow-color': '#9CA3AF',
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
  {
    selector: 'edge[label="supervised"]',
    style: {
      'line-color': '#4CAF50',
      'target-arrow-color': '#4CAF50',
    },
  },
  {
    selector: 'edge[label="unsupervised"]',
    style: {
      'line-color': '#F44336',
      'target-arrow-color': '#F44336',
    },
  },
];

export const initializeGraph = (container: HTMLElement, data: GraphData) => {
  const elements = createElements(data);

  const cy = cytoscape({
    container,
    elements,
    style: graphStyles,
    layout: {
      name: 'cose',
      animate: true,
      fit: true,
      padding: 20,
      nodeRepulsion: 4000,
    },
  });

  return cy;
};
