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
  setFileData: (FileData: FileData) => void;
  setTotalData: (totalData: TotalDatas) => void;
  analysisStatus: "idle" | "analyzing" | "complete" | "error";
  setAnalysisStatus: (
    analysis: "idle" | "analyzing" | "complete" | "error"
  ) => void;
}

const useAiStore = create<Store>((set) => ({}));
