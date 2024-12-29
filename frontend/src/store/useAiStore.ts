import { create } from "zustand";

type Entity = {
  id: string;
  label: string;
  type?: string;
  isAnomaly?: boolean;
  location?:string;
  role?:string;
  contact?:string;
  affiliation?:string;
  
discovery_date?:string
relationship_strength?:string; 

propertyType?:string
email?:string;

};

type rel = {
  id: string;
  label: string;
  type?: string;
  isAnomaly?: boolean;
  location?:string;
  role?:string;
  contact?:string;
  affiliation?:string;
  source?:string;
  target?:string;
  propertyType?:string
  
discovery_date?:string
relationship_strength?:string; 

email?:string;

}

export interface GraphData {
  entities: Entity[];
  relationships: rel[];
}

export interface FileData {
  filename: string;
  cases: unknown[];
}

export interface TotalDatas {
  datas: FileData[];
}

interface Store {
  fileData: FileData;
  totalData: TotalDatas;
  setFileData: (fileData: FileData) => void;
  analysisStatus: "idle" | "analyzing" | "complete" | "error";
  setAnalysisStatus: (
    analysis: "idle" | "analyzing" | "complete" | "error"
  ) => void;
  curCase: number;
  setCurCase: (cur: number) => void;
  graphData: GraphData;
  setGraphData: (graphData: GraphData) => void;
  addFileData: (file: FileData)=> void
}

const useAiStore = create<Store>((set) => ({
  fileData: { filename: "", cases: [] },
  analysisStatus: "idle",
  totalData: { datas: [] },
  setFileData: (fileData) => set({ fileData }),
  setAnalysisStatus: (status) => set({ analysisStatus: status }),
  addFileData: (newFileData:FileData) =>
    set((state) => ({
      totalData: {
        datas: [...state.totalData.datas, newFileData],
      },
    })),
  curCase: 0,
  setCurCase: (cur) => set({ curCase: cur }),
  graphData: {entities:[],relationships:[]},
  setGraphData: (graphData: GraphData)=>set({graphData})

}));

export default useAiStore;
