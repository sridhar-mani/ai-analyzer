import React, { useCallback } from "react";
import { Upload } from "lucide-react";

interface FileUploadProps {
  onFilesSelected: (files: FileList) => void;
  acceptedTypes?: string;
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFilesSelected,
  acceptedTypes = ".pdf,.doc,.docx,.xlsx,.xls",
}) => {
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      const { files } = e.dataTransfer;
      if (files && files.length > 0) {
        onFilesSelected(files);
      }
    },
    [onFilesSelected]
  );

  return (
    <div
      className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-indigo-500 transition-colors"
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      <Upload className="w-12 h-12 mx-auto text-gray-400 mb-4" />
      <label className="block">
        <span className="text-gray-700">
          Drag and drop files here, or{" "}
          <span className="text-indigo-600 hover:text-indigo-500 cursor-pointer">
            browse
          </span>
        </span>
        <input
          type="file"
          className="hidden"
          multiple
          accept={acceptedTypes}
          onChange={(e) => e.target.files && onFilesSelected(e.target.files)}
        />
      </label>
      <p className="text-sm text-gray-500 mt-2">
        Supported formats: PDF, Word, Excel
      </p>
    </div>
  );
};

export default FileUpload;
