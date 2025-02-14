import React, { useEffect, useRef, useState } from 'react';
import CytoscapeComponent from 'react-cytoscapejs';
import cytoscape from 'cytoscape';
import cola from 'cytoscape-cola';
import { createElements, graphStyles } from '../utils/cytoscape';
import { useGraphControls } from '../hooks/useGraphControls';
import { defaultLayoutOptions } from '../utils/layout';
import Controls from './Controls';
import { Tooltip as ReactTooltip } from 'react-tooltip';

cytoscape.use(cola);

const Graph = ({ data }) => {
  const cyRef = useRef<cytoscape.Core | null>(null);
  const [tooltipContent, setTooltipContent] = useState(''); 
  const [tooltipVisible, setTooltipVisible] = useState(false);

  const {
    handleZoomIn,
    handleZoomOut,
    handleFit,
    handleReset
  } = useGraphControls(cyRef);

  if (!(data.entities.length > 0 || data.relationships.length > 0)) return null;

  const handleNodeClick = (event) => {
    const node = event.target;
    const nodeData = node.data();

    setTooltipContent(`
      <strong>Label:</strong> ${nodeData.label}<br />
      <strong>Type:</strong> ${nodeData.type}<br />
      <strong>ID:</strong> ${nodeData.id}
    `);
    
    // Position the tooltip near the clicked node
    const { x, y } = node.position();
    ReactTooltip.show(document.getElementById(`node-${nodeData.id}`));
    setTooltipVisible(true);
  };

  return (
    <div className="w-full h-full relative">
      <CytoscapeComponent
        elements={createElements(data)}
        stylesheet={graphStyles}
        layout={defaultLayoutOptions}
        cy={(cy) => {
          cyRef.current = cy;
          cy.on('tap', 'node', handleNodeClick);
        }}
        className="w-full h-full"
      />
      <Controls
        onZoomIn={handleZoomIn}
        onZoomOut={handleZoomOut}
        onFit={handleFit}
        onReset={handleReset}
      />
      {tooltipVisible && (
        <ReactTooltip 
          place="top" 
          type="dark" 
          effect="float" 
          id={`node-${data.id}`} 
          html={true} 
          getContent={() => tooltipContent} 
          style={{ pointerEvents: 'none' }} 
        />
      )}
    </div>
  );
};

export default Graph;