import { useState } from 'react';

const DragAndDropUpload = ({onChange}: {onChange: any}) => {
  const [dragging, setDragging] = useState(false);
  const [files, setFiles] = useState<any[]>([]);

  const handleDragOver = (e: { preventDefault: () => void; }) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = () => {
    setDragging(false);
  };

  const handleDrop = (e: { preventDefault: () => void; dataTransfer: { files: Iterable<unknown> | ArrayLike<unknown>; }; }) => {
    e.preventDefault();
    setDragging(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    setFiles(droppedFiles);
    onChange(droppedFiles);
  };

  const handleClick = () => {
    const fileInput = document.getElementById('file-input');
    if(fileInput){
      fileInput.click();
    }
  };

  const handleChange = (e: { target: { files: Iterable<unknown> | ArrayLike<unknown>; }; }) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles(selectedFiles);
    onChange(selectedFiles);
  };

  return (
    <div
      className={`my-1 drop-zone ${dragging ? 'active' : ''}`}
      onClick={handleClick}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <input
        type="file"
        id="file-input"
        className="file-input"
        //@ts-ignore
        onChange={handleChange}
        accept="image/*"
      />
      {files && files.length > 0 ? files.map((file)=> (<p key={file.name}>{file.name}</p>)): <p>Upload File</p>}
    </div>
  );
};

export default DragAndDropUpload;
