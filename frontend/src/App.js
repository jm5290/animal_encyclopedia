import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);
  const [imageUrl, setImageUrl] = useState(null);

  useEffect(() => {
    if (retryCount > 0) {
      // Retry fetching data when retryCount changes
      fetchAnimalInfo();
    }
  }, [retryCount]);

  const fetchAnimalInfo = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:8000/get_animal_info?query=${query}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      // Check if response data is valid
      if (!validateResponse(data)) {
        throw new Error('Invalid data received');
      }
      setResult(data);
      // Fetch animal image
      fetchAnimalImage(query);
    } catch (error) {
      setError(error.message);
      // Retry request if retry count is less than 3
      if (retryCount < 3) {
        setRetryCount(retryCount + 1);
      }
    } finally {
      setLoading(false);
    }
  };

  const validateResponse = (data) => {
    // Implement your validation logic here
    // For example, check if required fields are present in the response
    return data && (data['Brief summary'] || data['Interesting facts']) && data['Scientific name'] && data['Physical description'];
  };

  const fetchAnimalImage = async (query) => {
    try {
      const response = await fetch(`http://localhost:8000/get_image?query=${query}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      setImageUrl(imageUrl);
    } catch (error) {
      console.error('Failed to fetch image:', error);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setRetryCount(0); // Reset retry count when submitting a new query
    fetchAnimalInfo();
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Animal Info Finder</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter animal name"
          />
          <button type="submit">Search</button>
        </form>
        {loading && <p>Loading...</p>}
        {error && <p>Error: {error}</p>}
        {result && (
          <div className="results">
            <h2>Results for {query}</h2>
            {result['Brief summary'] && (
              <div>
                <h3>Brief Summary:</h3>
                <p>{result['Brief summary']}</p>
              </div>
            )}
            {result['Interesting facts'] && (
              <div>
                <h3>Interesting Facts:</h3>
                <ul>
                  {result['Interesting facts'].map((fact, index) => (
                    <li key={index}>{fact}</li>
                  ))}
                </ul>
              </div>
            )}
            <h3>Scientific Name:</h3>
            <p>{result['Scientific name']}</p>
            <h3>Physical Description:</h3>
            <p>{result['Physical description']}</p>
            <h3>Habitat:</h3>
            <p>{result['Habitat']}</p>
            <h3>Diet:</h3>
            <p>{result['Diet']}</p>
            <h3>Social Structure:</h3>
            <p>{result['Social structure']}</p>
            <h3>Conservation Status:</h3>
            <p>{result['Conservation status']}</p>
            <h3>Behavior:</h3>
            <p>{result['Behavior']}</p>
            {imageUrl && <img src={imageUrl} alt="Animal" />}
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
