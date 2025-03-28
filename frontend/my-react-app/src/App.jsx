import { useState, useEffect } from "react";

function App() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Tambahkan timeout untuk menghindari hanging
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000);

        const response = await fetch("http://localhost:5000/api/items", {
          signal: controller.signal
        });
        
        clearTimeout(timeoutId);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setItems(data);
        setError(null);
      } catch (error) {
        console.error("Error fetching data:", error);
        setError(`Failed to connect to server: ${error.message}`);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Loading data...</div>;
  }

  if (error) {
    return (
      <div style={{ color: 'red', padding: '20px' }}>
        <h2>Connection Error</h2>
        <p>{error}</p>
        <p>Please ensure:</p>
        <ul>
          <li>Flask server is running (python app.py)</li>
          <li>Server is accessible at http://localhost:5000</li>
          <li>No other application is using port 5000</li>
        </ul>
      </div>
    );
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>React & Flask Integration</h1>
      {items.length > 0 ? (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {items.map((item) => (
            <li key={item.id} style={{ margin: "10px 0", padding: "10px", border: "1px solid #ddd" }}>
              <strong>{item.name}</strong>: {item.description}
            </li>
          ))}
        </ul>
      ) : (
        <p>No items found in database</p>
      )}
    </div>
  );
}

export default App;