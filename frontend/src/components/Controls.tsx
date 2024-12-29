import React from 'react';
import { ZoomIn, ZoomOut, Maximize2, RotateCcw } from 'lucide-react';


export interface ControlsProps {
  onZoomIn: () => void;
  onZoomOut: () => void;
  onFit: () => void;
  onReset: () => void;
}

const Controls: React.FC<ControlsProps> = ({ 
  onZoomIn, 
  onZoomOut, 
  onFit, 
  onReset 
}) => {
  const buttonClass = "p-2 bg-white rounded-lg shadow-md hover:bg-gray-50";

  return (
    <div className="absolute bottom-4 right-4 flex gap-2">
      <button
        onClick={onZoomIn}
        className={buttonClass}
        title="Zoom In"
      >
        <ZoomIn className="w-5 h-5" />
      </button>
      <button
        onClick={onZoomOut}
        className={buttonClass}
        title="Zoom Out"
      >
        <ZoomOut className="w-5 h-5" />
      </button>
      <button
        onClick={onFit}
        className={buttonClass}
        title="Fit to View"
      >
        <Maximize2 className="w-5 h-5" />
      </button>
      <button
        onClick={onReset}
        className={buttonClass}
        title="Reset Layout"
      >
        <RotateCcw className="w-5 h-5" />
      </button>
    </div>
  );
};

export default Controls;