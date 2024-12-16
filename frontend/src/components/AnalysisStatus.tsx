import React from 'react';
import { Loader2 } from 'lucide-react';

interface AnalysisStatusProps {
  status: 'idle' | 'analyzing' | 'complete' | 'error';
  message?: string;
}

const AnalysisStatus: React.FC<AnalysisStatusProps> = ({ status, message }) => {
  const getStatusContent = () => {
    switch (status) {
      case 'analyzing':
        return (
          <div className="flex items-center space-x-2 text-indigo-600">
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>Analyzing documents...</span>
          </div>
        );
      case 'complete':
        return (
          <div className="text-green-600">
            Analysis complete
          </div>
        );
      case 'error':
        return (
          <div className="text-red-600">
            {message || 'An error occurred during analysis'}
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow-sm">
      {getStatusContent()}
    </div>
  );
};

export default AnalysisStatus;