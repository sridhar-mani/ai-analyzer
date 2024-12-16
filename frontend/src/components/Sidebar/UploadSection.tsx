import React from 'react';
import FileUpload from '../FileUpload';
import AnalysisStatus from '../AnalysisStatus';

interface UploadSectionProps {
  status: 'idle' | 'analyzing' | 'complete' | 'error';
  onFilesSelected: (files: FileList) => void;
}

const UploadSection: React.FC<UploadSectionProps> = ({ status, onFilesSelected }) => {
  return (
    <div className="space-y-4">
      <div className="bg-gray-50 rounded-lg p-4">
        <h2 className="text-sm font-semibold text-gray-700 mb-3">Upload Documents</h2>
        <FileUpload onFilesSelected={onFilesSelected} />
      </div>
      <AnalysisStatus status={status} />
    </div>
  );
};

export default UploadSection;