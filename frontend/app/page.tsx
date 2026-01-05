"use client";

import React, { useRef, useState } from "react";

type StudyResponse = {
  doc_id: string;
  mode: string;
  output: string;
  used_chunks: number;
  warnings?: string[];
};

export default function Page() {
  // ✅ useRef MUST be inside the component
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  // ✅ REQUIRED STATE
  const [docId, setDocId] = useState<string | null>(null);
  const [studyMode, setStudyMode] = useState<"summarize" | "explain" | "quiz">("summarize");
  const [studyResult, setStudyResult] = useState<StudyResponse | null>(null);

  // Upload UI
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [uploadInfo, setUploadInfo] = useState<{ chunk_count: number; preview: string } | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  // Study UI
  const [focus, setFocus] = useState("");
  const [numQuestions, setNumQuestions] = useState(5);
  const [difficulty, setDifficulty] = useState<"easy" | "medium" | "hard">("medium");
  const [isStudying, setIsStudying] = useState(false);
  const [studyError, setStudyError] = useState<string | null>(null);
  const [studyStatus, setStudyStatus] = useState<number | null>(null);

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    setUploadError(null);
    setStudyError(null);
    setStudyStatus(null);
    setStudyResult(null);

    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setIsUploading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const msg = await res.text();
        throw new Error(msg || "Upload failed");
      }

      const data = await res.json();

      setDocId(data.doc_id);
      setUploadInfo({
        chunk_count: data.chunk_count ?? 0,
        preview: data.preview ?? "",
      });
    } catch (err: any) {
      setUploadError(err.message || "Upload failed");
    } finally {
      setIsUploading(false);
    }
  }

  async function callStudy() {
    if (!docId) {
      setStudyError("Upload a PDF first");
      return;
    }

    setStudyError(null);
    setStudyStatus(null);
    setIsStudying(true);

    const payload: any = { doc_id: docId, mode: studyMode };

    // clean request: only send focus if it exists
    if (studyMode === "explain" && focus.trim()) payload.focus = focus.trim();

    // only send quiz fields in quiz mode
    if (studyMode === "quiz") {
      payload.num_questions = numQuestions;
      payload.difficulty = difficulty;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/study/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      setStudyStatus(res.status);

      if (!res.ok) {
        const msg = await res.text();
        throw new Error(msg || `Study failed (${res.status})`);
      }

      const data = (await res.json()) as StudyResponse;
      setStudyResult(data);
    } catch (err: any) {
      setStudyError(err.message || "Study failed");
    } finally {
      setIsStudying(false);
    }
  }

  function handleReset() {
    if (fileInputRef.current) fileInputRef.current.value = "";

    setDocId(null);
    setUploadInfo(null);
    setUploadError(null);

    setStudyResult(null);
    setStudyError(null);
    setStudyStatus(null);

    setStudyMode("summarize");
    setFocus("");
    setNumQuestions(5);
    setDifficulty("medium");
  }

  const styles = {
    page: {
      minHeight: "100vh",
      padding: 28,
      fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Arial",
      background:
        "radial-gradient(1200px 600px at 20% 10%, #dbeafe 0%, transparent 55%)," +
        "radial-gradient(900px 500px at 85% 20%, #fce7f3 0%, transparent 55%)," +
        "radial-gradient(900px 500px at 55% 95%, #dcfce7 0%, transparent 55%)," +
        "linear-gradient(180deg, #f8fafc 0%, #ffffff 65%)",
      color: "#0f172a",
    },
    container: { maxWidth: 980, margin: "0 auto" },

    topbar: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      marginBottom: 14,
      gap: 12,
      flexWrap: "wrap" as const,
    },
    titleWrap: { display: "flex", alignItems: "center", gap: 10 },
    logo: {
      width: 44,
      height: 44,
      borderRadius: 14,
      background: "linear-gradient(135deg, #4f46e5 0%, #db2777 55%, #16a34a 100%)",
      boxShadow: "0 10px 22px rgba(79, 70, 229, 0.18)",
      display: "grid",
      placeItems: "center",
      color: "white",
      fontWeight: 900,
      letterSpacing: "-0.02em",
    },
    title: { margin: 0, fontSize: 30, fontWeight: 900, letterSpacing: "-0.03em" },
    subtitle: { margin: 0, color: "#475569", fontSize: 14 },

    badge: {
      display: "inline-flex",
      alignItems: "center",
      gap: 8,
      background: "rgba(255,255,255,0.75)",
      border: "1px solid rgba(2,6,23,0.10)",
      borderRadius: 999,
      padding: "8px 12px",
      color: "#334155",
      fontSize: 13,
    },

    // ✅ THIS is where that grid code goes: it wraps both cards
    grid: {
      display: "grid",
      gridTemplateColumns: "1fr",
      gap: 16,
    },

    card: {
      background: "rgba(255,255,255,0.86)",
      border: "1px solid rgba(2,6,23,0.10)",
      borderRadius: 18,
      padding: 18,
      boxShadow: "0 18px 40px rgba(2, 6, 23, 0.08)",
      backdropFilter: "blur(10px)",
    },

    row: { display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap" as const },
    label: { fontSize: 13, color: "#334155", fontWeight: 800 },

    input: {
      padding: "10px 12px",
      borderRadius: 14,
      border: "1px solid rgba(2,6,23,0.12)",
      outline: "none",
      background: "rgba(255,255,255,0.95)",
    },
    select: {
      padding: "10px 12px",
      borderRadius: 14,
      border: "1px solid rgba(2,6,23,0.12)",
      background: "rgba(255,255,255,0.95)",
    },

    pill: {
      display: "inline-flex",
      alignItems: "center",
      gap: 8,
      background: "rgba(79, 70, 229, 0.10)",
      color: "#3730a3",
      border: "1px solid rgba(79, 70, 229, 0.20)",
      borderRadius: 999,
      padding: "7px 12px",
      fontSize: 13,
      fontWeight: 700,
    },

    btn: {
      padding: "10px 14px",
      borderRadius: 14,
      border: 0,
      background: "linear-gradient(135deg, #4f46e5 0%, #db2777 55%, #16a34a 100%)",
      color: "white",
      fontWeight: 900,
      cursor: "pointer",
      boxShadow: "0 10px 22px rgba(79, 70, 229, 0.22)",
    },
    btnSecondary: {
      padding: "10px 14px",
      borderRadius: 14,
      border: "1px solid rgba(2,6,23,0.12)",
      background: "rgba(255,255,255,0.9)",
      color: "#0f172a",
      fontWeight: 900,
      cursor: "pointer",
    },

    error: {
      color: "#991b1b",
      background: "rgba(254, 226, 226, 0.95)",
      border: "1px solid rgba(239, 68, 68, 0.25)",
      padding: 12,
      borderRadius: 14,
      fontWeight: 700,
    },

    resultBox: {
      border: "1px solid rgba(2,6,23,0.10)",
      borderRadius: 14,
      padding: 14,
      background: "rgba(248, 250, 252, 0.9)",
      maxHeight: 280,
      overflowY: "auto" as const,
      whiteSpace: "pre-wrap" as const,
      lineHeight: 1.6,
    },

    small: { fontSize: 12, color: "#64748b" },
  };

  return (
    <main style={styles.page}>
      <div style={styles.container}>
        <div style={styles.topbar}>
          <div style={styles.titleWrap}>
            <div style={styles.logo}>SB</div>
            <div>
              <h1 style={styles.title}>AI Study Buddy</h1>
              <p style={styles.subtitle}>Upload a PDF → pick a mode → Study ✨</p>
            </div>
          </div>

          <div style={styles.badge}>
            {docId ? (
              <>
                ✅ Ready <span style={{ opacity: 0.6 }}>•</span>
                <code>{docId.slice(0, 8)}…</code>
              </>
            ) : (
              <>📄 Upload a PDF to start</>
            )}
          </div>
        </div>

        {/* ✅ GRID WRAPS BOTH CARDS */}
        <div style={styles.grid}>
          {/* Upload Card */}
          <div style={styles.card}>
            <h2 style={{ marginTop: 0 }}>Upload</h2>

            <div style={styles.row}>
              <input
                ref={fileInputRef}
                type="file"
                accept="application/pdf"
                onChange={handleUpload}
                disabled={isUploading || isStudying}
              />

              <button
                onClick={handleReset}
                disabled={isUploading || isStudying}
                style={{
                  ...styles.btnSecondary,
                  opacity: isUploading || isStudying ? 0.55 : 1,
                }}
              >
                Reset
              </button>

              {isUploading && <span style={styles.small}>Uploading…</span>}
            </div>

            {docId && (
              <div style={{ marginTop: 12 }}>
                <span style={styles.pill}>
                  ✅ doc_id <code>{docId}</code>
                </span>
              </div>
            )}

            {uploadInfo && (
              <div style={{ marginTop: 12 }}>
                <div style={styles.small}>Chunks: {uploadInfo.chunk_count}</div>
                <div style={{ marginTop: 8, ...styles.resultBox }}>{uploadInfo.preview}</div>
              </div>
            )}

            {uploadError && <div style={{ marginTop: 12, ...styles.error }}>{uploadError}</div>}
          </div>

          {/* Study Card */}
          <div style={styles.card}>
            <h2 style={{ marginTop: 0 }}>Study</h2>

            <div style={styles.row}>
              <span style={styles.label}>Mode</span>

              <select
                value={studyMode}
                onChange={(e) => setStudyMode(e.target.value as any)}
                style={styles.select}
                disabled={isStudying}
              >
                <option value="summarize">summarize</option>
                <option value="explain">explain</option>
                <option value="quiz">quiz</option>
              </select>

              <button
                onClick={callStudy}
                disabled={!docId || isStudying || isUploading}
                style={{
                  ...styles.btn,
                  opacity: !docId || isStudying || isUploading ? 0.55 : 1,
                }}
              >
                {isStudying ? "Studying…" : "Study"}
              </button>

              {!docId && <span style={styles.small}>Upload a PDF to enable Study</span>}
            </div>

            {studyMode === "explain" && (
              <div style={{ marginTop: 12 }}>
                <div style={styles.label}>Focus (optional)</div>
                <input
                  type="text"
                  value={focus}
                  onChange={(e) => setFocus(e.target.value)}
                  placeholder="e.g. derivatives"
                  style={{ ...styles.input, width: "100%", marginTop: 6 }}
                  disabled={isStudying}
                />
              </div>
            )}

            {studyMode === "quiz" && (
              <div style={{ marginTop: 12, ...styles.row }}>
                <div>
                  <div style={styles.label}>Questions</div>
                  <input
                    type="number"
                    value={numQuestions}
                    onChange={(e) => setNumQuestions(Number(e.target.value))}
                    min={1}
                    style={{ ...styles.input, width: 90, marginTop: 6 }}
                    disabled={isStudying}
                  />
                </div>

                <div>
                  <div style={styles.label}>Difficulty</div>
                  <select
                    value={difficulty}
                    onChange={(e) => setDifficulty(e.target.value as any)}
                    style={{ ...styles.select, marginTop: 6 }}
                    disabled={isStudying}
                  >
                    <option value="easy">easy</option>
                    <option value="medium">medium</option>
                    <option value="hard">hard</option>
                  </select>
                </div>
              </div>
            )}

            {studyError && <div style={{ marginTop: 12, ...styles.error }}>{studyError}</div>}

            {studyStatus !== null && <div style={{ marginTop: 10, ...styles.small }}>HTTP status: {studyStatus}</div>}

            {studyResult && (
              <div style={{ marginTop: 14 }}>
                <div style={styles.row}>
                  <span style={styles.pill}>mode: {studyResult.mode}</span>
                  <span style={styles.pill}>used_chunks: {studyResult.used_chunks}</span>
                </div>

                <div style={{ marginTop: 12, ...styles.resultBox }}>{studyResult.output}</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
