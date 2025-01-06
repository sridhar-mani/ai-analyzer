import React, { useState, useCallback, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import MainContent from "./components/MainContent";
import useAiStore from "./store/useAiStore";
import { sanitizeGraphData } from "./utils/validation";

function App() {
  const {
    fileData,
    setFileData,
    totalData,
    addFileData,
    curCase,
    setCurCase,
    graphData,
    setGraphData,
    analysisStatus,
    setAnalysisStatus
  } = useAiStore();

  const handleFilesSelected = useCallback(async (files: FileList) => {
    setAnalysisStatus("analyzing");
    const formData = new FormData();
    Array.from(files).forEach((f) => {
      formData.append("files", f);
      console.log("sending file", f.name);
    });
    try {
      const res = await fetch("http://localhost:8380/analyze", {
        method: "POST",
        headers: {
          accept: "application/json",
        },
        body: formData,
      });

      

      console.log("initial response", res);

      const data = await res.json();

        if (!data?.data?.[curCase]?.cases?.[curCase]?.ai_analysis) {
          throw new Error('Invalid data structure received from server');
        }

      

      console.log(data.data[curCase].cases[curCase].ai_analysis);
      addFileData(data)
      setFileData(data.data[curCase])
      setCurCase(0)
    } catch (er) {
      console.log("Error in fetching the response", er);
    }

    setTimeout(() => {
      setAnalysisStatus("complete");
    }, 2000);
  }, []);

  useEffect(()=>{

    if (fileData?.cases?.[curCase]?.ai_analysis) {
      const rawGraphData = {
        entities: fileData.cases[curCase].ai_analysis.nodes || [],
        relationships: fileData.cases[curCase].ai_analysis.edges || []
      };
      

      const sanitizedData = sanitizeGraphData(rawGraphData);
      setGraphData(sanitizedData);
    }

  },[curCase,fileData])

  

  const handleEntityClick = useCallback((entity:{}) => {
    console.log("Entity clicked:", entity);
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
