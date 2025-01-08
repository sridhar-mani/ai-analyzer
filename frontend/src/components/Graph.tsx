import React, { useEffect, useRef, useState } from 'react';
import CytoscapeComponent from 'react-cytoscapejs';
import cytoscape from 'cytoscape';
import cola from 'cytoscape-cola';
import tippy from 'tippy.js';
import 'tippy.js/dist/tippy.css'
import { createElements, graphStyles } from '../utils/cytoscape';
import { useGraphControls } from '../hooks/useGraphControls';
import { defaultLayoutOptions } from '../utils/layout';
import Controls from './Controls';

cytoscape.use(cola);


const Graph = ({ data }) => {
  const cyRef = useRef<cytoscape.Core | null>(null);

  const [nodeData,setNodeData ] = useState(null)
  const {
    handleZoomIn,
    handleZoomOut,
    handleFit,
    handleReset
  } = useGraphControls(cyRef);

  useEffect(()=>{
if(cyRef.current){
  const cy = cyRef.current;

  cy.on('mouseover','node',(e)=>{
const node = e?.target;
const nodeData = node.data();

tippy(
  node.popperRef(),{
    content:`
    <strong>Label:</strong> ${nodeData.Label}<br>
                <strong>Type:</strong> ${nodeData.type}<br>
            <strong>ID:</strong> ${nodeData.id}
    `,
    allowHTML:true,
    arrow:true,
    placement:'top'
  }
)

  })

  cy.on('mouseout','node',()=>{
    tippy.destroy()
  })
}
  },[])

  if(!(data.entities.length>0 || data.relationships.length>0)) return

  const handleNodeClick = (event)=>{
    const node = event.target
    const nodeData = node.data()
    setNodeData(nodeData)
    console.log(nodeData);
  }

  return (
    <div className="w-full h-full relative">
      <CytoscapeComponent
        elements={createElements(data)}
        stylesheet={graphStyles}
        layout={defaultLayoutOptions}
        cy={(cy) => {
          cyRef.current = cy;
          cy.on('tap','node',handleNodeClick)
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