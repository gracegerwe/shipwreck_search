"use client";

import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const search = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await fetch(`https://shipwreck-backend.onrender.com/wiki-summary?query=${encodeURIComponent(query)}`);
      const data = await res.json();

      if (data.error) {
        setError(data.error);
      } else {
        setResult(data);
      }
    } catch (err) {
      setError("Something went wrong.");
    }

    setLoading(false);
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-6 bg-gray-50">
      <h1 className="text-3xl font-bold mb-6">🔎 Shipwreck Search</h1>

      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Try 'Atocha' or 'Titanic'"
          className="p-2 border rounded w-80"
        />
        <button onClick={search} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Search
        </button>
      </div>

      {loading && <p className="text-gray-600">Searching...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {result && (
        <div className="mt-6 bg-white shadow-md rounded p-4 max-w-xl">
          <h2 className="text-xl font-semibold">{result.title}</h2>
          <p className="mt-2 text-gray-700">{result.summary}</p>
        </div>
      )}
    </main>
  );
}
