import React, { useState, useEffect } from "react";

export interface Architecture {
  name: string;
  description: string;
  summary: string;
  category?: string;
  services: string[];
  timestamp: string;
}

const API_BASE = import.meta.env.VITE_API_BASE || "";

const formatDate = (dateStr: string) => {
  try {
    return new Date(dateStr).toLocaleString();
  } catch {
    return dateStr;
  }
};

const App: React.FC = () => {
  const [architectures, setArchitectures] = useState<Architecture[]>([]);
  const [loading, setLoading] = useState(false);
  const [scraping, setScraping] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchArchitectures = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/architectures`);
      if (!res.ok) throw new Error(`Failed to fetch architectures: ${res.statusText}`);
      const data = await res.json();
      setArchitectures(data);
    } catch (err: any) {
      setError(err.message || "Unknown error");
    }
    setLoading(false);
  };

  const handleScrape = async () => {
    setScraping(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/scrape`, { method: "POST" });
      if (!res.ok) throw new Error(`Scrape failed: ${res.statusText}`);
      await fetchArchitectures();
    } catch (err: any) {
      setError(err.message || "Unknown error");
    }
    setScraping(false);
  };

  useEffect(() => {
    fetchArchitectures();
  }, []);

  return (
    <main style={{ padding: 24, fontFamily: "Segoe UI, Tahoma, Geneva, Verdana, sans-serif", maxWidth: 900, margin: "auto" }}>
      <h1>Cloud Architecture Parser</h1>

      <button
        onClick={handleScrape}
        disabled={scraping}
        style={{
          backgroundColor: scraping ? "#ccc" : "#007acc",
          color: "#fff",
          border: "none",
          padding: "12px 24px",
          borderRadius: 6,
          cursor: scraping ? "not-allowed" : "pointer",
          marginBottom: 24,
          fontWeight: "bold",
          fontSize: 16,
        }}
        aria-busy={scraping}
      >
        {scraping ? "Scraping..." : "Scrape New Architectures"}
      </button>

      {error && (
        <div
          role="alert"
          style={{ color: "white", backgroundColor: "#e74c3c", padding: 12, borderRadius: 6, marginBottom: 24 }}
        >
          {error}
        </div>
      )}

      {loading ? (
        <p>Loading architectures...</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
          {architectures.map((arch) => (
            <li
              key={`${arch.name}-${arch.timestamp}`}
              style={{
                border: "1px solid #ddd",
                borderRadius: 8,
                padding: 16,
                marginBottom: 16,
                boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
              }}
            >
              <h2 style={{ marginTop: 0 }}>{arch.name}</h2>

              <p style={{ fontStyle: "italic", color: "#555" }}>{arch.summary}</p>

              {arch.services.length > 0 && (
                <p>
                  <strong>Services:</strong> {arch.services.join(", ")}
                </p>
              )}

              {arch.category && (
                <p>
                  <strong>Category:</strong> {arch.category}
                </p>
              )}

              <p style={{ fontSize: 12, color: "#888" }}>
                <time dateTime={arch.timestamp}>{formatDate(arch.timestamp)}</time>
              </p>

              <p>{arch.description}</p>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
};

export default App;
