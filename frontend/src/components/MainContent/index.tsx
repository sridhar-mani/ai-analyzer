import React from "react";
import Graph from "../Graph";
import { GraphData } from "../../types/graph";

interface MainContentProps {
  data: GraphData;
  curCase: number;
}

const MainContent: React.FC<MainContentProps> = ({ data, curCase }) => {
  return (
    <div className="flex-1 h-screen flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-xl font-bold text-white">
          Entity Relationship Graph
        </h2>
      </div>
      <div className="flex-1 relative">
        <Graph data={data} />
      </div>
    </div>
  );
};

export default MainContent;
