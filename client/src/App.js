import React, { useState } from 'react';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [message, setMessage] = useState('');
  const [downloading, setDownloading] = useState(false);

  const handleInputChange = (event) => {
    setUrl(event.target.value);
  };

  const handleDownload = async () => {
    if (!url) {
      setMessage('Please enter a YouTube URL');
      return;
    }

    setDownloading(true);
    setMessage('');

    try {
      const response = await fetch(`127.0.0.1:8000/download/?url=${url}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.setAttribute('download', 'video.mp4');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);

      setMessage('Download started!');
    } catch (error) {
      setMessage('Error downloading video: ' + error.message);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>YouTube Video Downloader</h1>
        <input
          type="text"
          value={url}
          onChange={handleInputChange}
          placeholder="Enter YouTube URL"
          disabled={downloading}
        />
        <button onClick={handleDownload} disabled={downloading}>
          {downloading ? 'Downloading...' : 'Download'}
        </button>
        {message && <p>{message}</p>}
      </header>
    </div>
  );
}

export default App;
