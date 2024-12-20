import React, { useState, useCallback } from "react";
import Sidebar from "./components/Sidebar";
import MainContent from "./components/MainContent";
import { GraphData, FileData, TotalDatas } from "./types/graph";

function App() {
  const [analysisStatus, setAnalysisStatus] = useState<
 
  >("idle");
  const [graphData, setGraphData] = useState<GraphData>({
    entities: [],
    relationships: [],
  });
  const [fileData, setFileData] = useState<FileData>({
    filename: "",
    cases: [],
  });
  const [totalData, setTotalData] = useState<TotalDatas>({ datas: [] });
  const [curCase, setCurCase] = useState<number>(0);

  const handleFilesSelected = useCallback(async (files: FileList) => {
    setAnalysisStatus("analyzing");
    const formData = new FormData();
    Array.from(files).forEach((f) => {
      formData.append("files", f);
      console.log("sending file", f.name);
    });
    try {
      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: {
          accept: "application/json",
        },
        body: formData,
      });

      console.log("initial response", res);

      const data = await res.json();

      console.log(data);
    } catch (er) {
      console.log("Error in fetching the response", er);
    }

    // Simulate document analysis
    setTimeout(() => {
      setAnalysisStatus("complete");
      // In a real application, you would process the files here
      // and update the graph data with the results
    }, 2000);
  }, []);

  const handleEntityClick = useCallback((entity) => {
    console.log("Entity clicked:", entity);
    // Implement entity focus/highlight logic here
  }, []);

  return (
    <div className="flex w-full min-h-screen bg-gray-900">
      <Sidebar
        status={analysisStatus}
        entities={graphData.entities}
        onFilesSelected={handleFilesSelected}
        onEntityClick={handleEntityClick}
        curCase={curCase}
        setCurCase={setCurCase}
      />
      <MainContent data={graphData} curCase={curCase} />
    </div>
  );
}

export default App;
