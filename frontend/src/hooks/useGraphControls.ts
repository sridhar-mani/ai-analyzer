import { useCallback } from 'react';
import { Core } from 'cytoscape';
import { defaultLayoutOptions } from '../utils/layout';

export const useGraphControls = (cyRef: React.MutableRefObject<Core | null>) => {
  const handleZoomIn = useCallback(() => {
    if (cyRef.current) {
      const currentZoom = cyRef.current.zoom();
      cyRef.current.animate({
        zoom: currentZoom * 1.2,
        duration: 200
      });
    }
  }, [cyRef]);

  const handleZoomOut = useCallback(() => {
    if (cyRef.current) {
      const currentZoom = cyRef.current.zoom();
      cyRef.current.animate({
        zoom: currentZoom * 0.8,
        duration: 200
      });
    }
  }, [cyRef]);

  const handleFit = useCallback(() => {
    if (cyRef.current) {
      cyRef.current.animate({
        fit: {
          padding: 50
        },
        duration: 200
      });
    }
  }, [cyRef]);

  const handleReset = useCallback(() => {
    if (cyRef.current) {
      cyRef.current.layout({
        ...defaultLayoutOptions,
        animate: true,
        randomize: true,
        fit: true,
        padding: 50
      }).run();
    }
  }, [cyRef]);

  return {
    handleZoomIn,
    handleZoomOut,
    handleFit,
    handleReset
  };
};