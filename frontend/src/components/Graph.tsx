import React, { useRef } from 'react';
import CytoscapeComponent from 'react-cytoscapejs';
import cytoscape from 'cytoscape';
import cola from 'cytoscape-cola';
import { GraphData } from '../types/graph';
import { createElements, graphStyles } from '../utils/cytoscape';
import { useGraphControls } from '../hooks/useGraphControls';
import { defaultLayoutOptions } from '../utils/layout';
import Controls from './Controls';

// Register the cola layout
cytoscape.use(cola);

interface GraphProps {
  data: GraphData;
}

const Graph: React.FC<GraphProps> = ({ data }) => {
  const cyRef = useRef<cytoscape.Core | null>(null);
  const {
    handleZoomIn,
    handleZoomOut,
    handleFit,
    handleReset
  } = useGraphControls(cyRef);

  return (
    <div className="w-full h-full relative">
      <CytoscapeComponent
        elements={createElements(data)}
        stylesheet={graphStyles}
        layout={defaultLayoutOptions}
        cy={(cy) => {
          cyRef.current = cy;
        }}
        className="w-full h-full"
      />
      <Controls
        onZoomIn={handleZoomIn}
        onZoomOut={handleZoomOut}
        onFit={handleFit}
        onReset={handleReset}
      />
    </div>
  );
};

export default Graph;