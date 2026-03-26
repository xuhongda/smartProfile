import React from 'react';
import DocViewer, { DocViewerRenderers } from 'react-doc-viewer';

const PDFPreview = ({ file, url }) => {
  const documents = [
    {
      uri: url,
      fileName: file.name,
    },
  ];

  return (
    <div className="p-4 bg-white rounded-lg shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium text-gray-800">{file.name}</h3>
        <span className="text-sm text-gray-500">{file.type || 'application/pdf'}</span>
      </div>
      <div className="border border-gray-200 rounded-md overflow-hidden">
        <DocViewer 
          documents={documents} 
          pluginRenderers={DocViewerRenderers} 
          className="h-96"
        />
      </div>
    </div>
  );
};

export default PDFPreview;