// food-nutrition-app/src/App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fileName, setFileName] = useState('');

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setPreview(URL.createObjectURL(file));
      setFileName(file.name);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    const fileInput = document.querySelector('input[type="file"]');
    formData.append('foodImage', fileInput.files[0]);

    try {
      setLoading(true);
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      if (data.error) {
        setResult('에러: ' + data.error);
      } else {
        setResult(data.nutrition);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('분석 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>음식 영양 분석</h1>
      
      <form onSubmit={handleSubmit} className="upload-form">
        <input
          type="file"
          id="foodImage"
          accept="image/*"
          onChange={handleImageChange}
          required
        />
        <label htmlFor="foodImage" className="file-label">이미지 선택</label>
        {fileName && <div className="selected-file-name">선택된 파일: {fileName}</div>}
        <button type="submit">분석하기</button>
      </form>

      {loading && <div className="loading">분석 중...</div>}
      {preview && <img src={preview} alt="Preview" className="preview" />}
      {result && <div className="result">{result}</div>}
    </div>
  );
}

export default App;