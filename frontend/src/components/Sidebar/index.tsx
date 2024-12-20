import React from "react";
import UploadSection from "./UploadSection";
import EntitySection from "./EntitySection";
import { Entity } from "../../types/graph";

interface SidebarProps {
  status: "idle" | "analyzing" | "complete" | "error";
  entities: Entity[];
  onFilesSelected: (files: FileList) => void;
  onEntityClick: (entity: Entity) => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  status,
  entities,
  onFilesSelected,
  onEntityClick,
}) => {
  return (
    <div className="h-screen w-80 bg-gray-900 border-r border-gray-200 flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <h1 className="text-xl font-bold text-white">Document Analysis</h1>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <UploadSection status={status} onFilesSelected={onFilesSelected} />
        <EntitySection entities={entities} onEntityClick={onEntityClick} />
      </div>
    </div>
  );
};

export default Sidebar;
