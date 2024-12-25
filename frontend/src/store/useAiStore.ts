import { create } from "zustand";

export interface GraphData {
  entities: unknown[];
  relationships: unknown[];
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
