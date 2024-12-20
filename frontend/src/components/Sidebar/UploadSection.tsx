import React, { useState } from "react";
import FileUpload from "../FileUpload";
import AnalysisStatus from "../AnalysisStatus";

interface UploadSectionProps {
  status: "idle" | "analyzing" | "complete" | "error";
  onFilesSelected: (files: FileList) => void;
}

const UploadSection: React.FC<UploadSectionProps> = ({
  status,
  onFilesSelected,
}) => {
  const [isPromptInput, setIsPromptInput] = useState(false);

  const handlePromptInputClick = () => {
    setIsPromptInput(true);
  };

  const handleDocumentUploadClick = () => {
    setIsPromptInput(false);
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-start space-x-4 mb-4">
        <button
          onClick={handleDocumentUploadClick}
          className={`py-2 px-3 rounded-lg text-md text-center font-medium focus:outline-none transition duration-300 ease-in-out transform ${
            !isPromptInput
              ? "bg-blue-500 text-white hover:bg-blue-600 active:bg-blue-700"
              : "bg-blue-200 text-gray-600 cursor-pointer"
          }`}
        >
          Document Upload
        </button>
        <button
          onClick={handlePromptInputClick}
          className={`py-2 px-6 rounded-lg text-md font-medium focus:outline-none transition duration-300 ease-in-out transform ${
            isPromptInput
              ? "bg-green-500 text-white hover:bg-green-600 active:bg-green-700"
              : "bg-green-200 text-gray-600 cursor-pointer"
          }`}
        >
          Prompt Input
        </button>
      </div>

      {!isPromptInput ? (
        <div className="bg-gray-50 rounded-lg p-6 shadow-lg">
          <h2 className="text-xl font-semibold text-gray-700 text-center mb-3">
            Upload Documents
          </h2>
          <FileUpload onFilesSelected={onFilesSelected} />
        </div>
      ) : (
        <div className="bg-gray-50 rounded-lg p-3 shadow-lg">
          <h2 className="text-xl text-center font-semibold text-gray-700 mb-3">
            Prompt Input
          </h2>
          <div className="space-y-4">
            <div>
              <input
                id="headline"
                type="text"
                placeholder="Enter headline"
                className="block w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
            </div>
            <div>
              <textarea
                id="content"
                placeholder="Enter content"
                className="block w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                rows={6}
              />
            </div>
          </div>
        </div>
      )}

      <AnalysisStatus status={status} />
    </div>
  );
};

export default UploadSection;
