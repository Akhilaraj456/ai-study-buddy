"use client";

import { useState } from "react";

export default function Home() {
    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [result, setResult] = useState<any>(null);

      async function handleUpload() {
      // reset UI state
      setError("");
      setResult(null);

      // validate
     if (!file) {
        setError("Please select a PDF file first.");
        return;
      }

      // build multipart/form-data
      const formData = new FormData();
      formData.append("file", file); // IMPORTANT: must be "file"

     // send request
      setLoading(true);
      try {
        const res = await fetch("http://127.0.0.1:8000/upload", {
          method: "POST",
          body: formData,
        });

        const data = await res.json();

        // handle backend errors cleanly
        if (!res.ok) {
          setError(data?.detail || "Upload failed.");
          return;
       }

        setResult(data);
    }   catch (e) {
         setError("Could not reach backend. Is it running on port 8000?");
    }   finally {
        setLoading(false);
    }
  }
  return (
    <main style={{ maxWidth: 800, margin: "40px auto", padding: 16 }}>
      <h1 style={{ fontSize: 28, fontWeight: 700 }}>AI Study Buddy — Phase 1</h1>
      <p style={{ marginTop: 8 }}>
        Upload a PDF and preview extracted text from the backend.
      </p>
        <div style={{ marginTop: 20, display: "flex", gap: 12, alignItems: "center" }}>
          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
         />

          <button onClick={handleUpload} disabled={loading}>
            {loading ? "Uploading..." : "Upload"}
           </button>
        </div>
          {error && (
           <p style={{ marginTop: 16, color: "crimson" }}>
            {error}
            </p>
      )}

      {result && (
        <div style={{ marginTop: 24 }}>
          <h2 style={{ fontSize: 18, fontWeight: 600 }}>Result</h2>

          <pre style={{ whiteSpace: "pre-wrap", background: "#f6f6f6", padding: 12, borderRadius: 8 }}>
            {JSON.stringify(result, null, 2)}
          </pre>

          <h3 style={{ marginTop: 16, fontSize: 16, fontWeight: 600 }}>Preview</h3>

          <div style={{ background: "#f6f6f6", padding: 12, borderRadius: 8 }}>
            {result.preview || "(No preview text found)"}
          </div>
        </div>
      )}


    </main>
  );
}
