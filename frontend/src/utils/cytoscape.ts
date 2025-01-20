import cytoscape, { Stylesheet } from 'cytoscape';
import { GraphData } from '../store/useAiStore';
import 'tippy.js/dist/tippy.css';
import tippy from 'tippy.js';

export const createElements = (data: GraphData): cytoscape.ElementDefinition[] => {
  const nodes = data.entities.map((entity) => ({
    group: 'nodes',
    data: {
      id: entity.id,
      label: entity.label || entity.name,
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

  const toolTip = document.createElement("div")
  toolTip.classList.add('bg-gray-800', 'text-white', 'p-4', 'rounded-lg', 'shadow-lg', 'max-w-sm')

  const tip = tippy(
    container,{
      content: toolTip,
      trigger: 'manual',
      interactive: true,
      arrow: true,
      placement: 'top',
      hideOnClick: true,
      theme: 'custom',
    }
  )

  cy.on(
    'tap','node', function(evt) {
    const node = evt.target;
    const nodeData = node.data();
    
    // Create tooltip content
    toolTip.innerHTML = `
      <div class="space-y-2">
        <h3 class="font-semibold">${nodeData.label}</h3>
        <div class="text-sm">
          <p><span class="font-medium">Type:</span> ${nodeData.type}</p>
          ${nodeData.propertyType ? `<p><span class="font-medium">Property Type:</span> ${nodeData.propertyType}</p>` : ''}
          ${nodeData.isAnomaly ? '<p class="text-red-400 font-medium">⚠️ Anomaly Detected</p>' : ''}
        </div>
      </div>
    `;

    // Position tooltip near the node
    const renderedPosition = node.renderedPosition();
    const containerBox = container.getBoundingClientRect();
    
    tip.setProps({
      getReferenceClientRect: () => ({
        width: 0,
        height: 0,
        left: containerBox.left + renderedPosition.x,
        right: containerBox.left + renderedPosition.x,
        top: containerBox.top + renderedPosition.y,
        bottom: containerBox.top + renderedPosition.y,
      }),
    });

    tip.show();
  }
  )

  cy.on('tap', function(evt) {
    if (evt.target === cy) {
      tip.hide();
    }
  });

  return cy;
};


const tooltipStyles = `
.tippy-box[data-theme~='custom'] {
  background-color: #1f2937;
  color: white;
}

.tippy-box[data-theme~='custom'][data-placement^='top'] > .tippy-arrow::before {
  border-top-color: #1f2937;
}
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = tooltipStyles;
document.head.appendChild(styleSheet);