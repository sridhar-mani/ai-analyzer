import { LayoutOptions } from 'cytoscape';

export const defaultLayoutOptions: LayoutOptions = {
  name: 'cola',
  nodeSpacing: 100,
  edgeLength: 200,
  animate: true,
  randomize: false,
  maxSimulationTime: 2000,
  padding: 50,
  infinite: false,
  fit: true,
  animationDuration: 1000,
  refresh: 1,
  ungrabifyWhileSimulating: false,
  dragify: true,
};