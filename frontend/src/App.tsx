import React, { useState, useCallback } from "react";
import Sidebar from "./components/Sidebar";
import MainContent from "./components/MainContent";
import { GraphData } from "./types/graph";
import { sampleData } from "./data/sampleData";

function App() {
  const [analysisStatus, setAnalysisStatus] = useState<
    "idle" | "analyzing" | "complete" | "error"
  >("idle");
  const [graphData, setGraphData] = useState<GraphData>(sampleData);

  const handleFilesSelected = useCallback(async (files: FileList) => {
    setAnalysisStatus("analyzing");
    const formData = new FormData();
    Array.from(files).forEach((f) => {
      formData.append("files", f);
    });
    const res = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      headers: {
        accept: "application/json",
      },
      body: formData,
    });

    const data = await res.json();

    console.log(data);

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
      />
      <MainContent data={graphData} />
    </div>
  );
}

export default App;
