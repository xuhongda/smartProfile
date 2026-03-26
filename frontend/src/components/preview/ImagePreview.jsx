import React from 'react';

const ImagePreview = ({ file, url }) => {
  return (
    <div className="p-4 bg-white rounded-lg shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium text-gray-800">{file.name}</h3>
        <span className="text-sm text-gray-500">{file.type || 'image/*'}</span>
      </div>
      <div className="flex justify-center items-center p-4 bg-gray-50 rounded-md border border-gray-200">
        <img 
          src={url} 
          alt={file.name} 
          className="max-w-full max-h-96 object-contain"
          onError={(e) => {
            e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iI2Q4ZDg0OCIvPjxyZWN0IHdpZHRoPSI4MCIgaGVpZ2h0PSI2MCIgZmlsbD0iI2Q4ZDg0OCIgeD0iNjAiIHk9IjcwIi8+PHRleHQgeD0iMTAwIiB5PSIxNTAiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzY2NiIgdGV4dC1hbmNob3I9Im1pZGRsZSI+SW1hZ2UgSW5mcmFzdHJ1Y3R1cmU8L3RleHQ+PC9zdmc+';
          }}
        />
      </div>
    </div>
  );
};

export default ImagePreview;