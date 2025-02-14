import React, { useState, useCallback, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import MainContent from "./components/MainContent";
import useAiStore from "./store/useAiStore";
import { sanitizeGraphData } from "./utils/validation";
import {ChromaDBUI} from '@sridhar-mani/chromadb-ui'
import { isMobile } from "react-device-detect";

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
    setAnalysisStatus,
    model,
    setModel
  } = useAiStore();


  navigator.storage.persist().then((granted) => {
    console.log(granted ? 'Persistent storage granted' : 'Persistent storage denied');
  });
  
  
  const aiModel = ()=>{
  }

  const handleFilesSelected = async (files: any) => {
    setAnalysisStatus("analyzing");


    const formData = new FormData();

    console.log(analysisStatus)
    

    if(typeof files==="object"){
      Object.entries(files).forEach(([key,value])=>{
        formData.append(key as string,value as string)
      })
      console.log(formData)
    }else{
      Array.from(files).forEach((f) => {
        formData.append("files", f);
        console.log("sending file", f.name);
      });
    }

   
    try {

      console.log(formData)
      const res = await fetch("http://localhost:8380/analyze", {
        method: "POST",
        headers: {
          accept: "application/json",
        },
        body: formData,
      });


      console.log(isMobile)

      if(typeof res!=="object"){
        console.log(isMobile)
      }

      

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
  }

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
    <div className="flex min-w-full min-h-screen bg-gray-900">
      <Sidebar
        status={analysisStatus}
        entities={graphData.entities}
        onFilesSelected={handleFilesSelected}
        onEntityClick={handleEntityClick}
      />
      <MainContent data={graphData} />
      {/* <ChromaDBUI config={{
        serverUrl:'http://localhost:6789',
        tenant: 'default_tenant',     
        database: 'default_database'
      }}></ChromaDBUI> */}
    </div>
  );
}

export default App;
