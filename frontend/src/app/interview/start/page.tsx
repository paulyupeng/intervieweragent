"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

export default function StartInterview() {
  const router = useRouter();
  const [candidates, setCandidates] = useState<any[]>([]);
  const [jobs, setJobs] = useState<any[]>([]);
  const [selectedCandidate, setSelectedCandidate] = useState("");
  const [selectedJob, setSelectedJob] = useState("");
  const [language, setLanguage] = useState("en");
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);

  useEffect(() => {
    fetchCandidates();
    fetchJobs();
  }, []);

  const fetchCandidates = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/candidates/`);
      const data = await res.json();
      setCandidates(data);
    } catch (error) {
      console.error("Failed to fetch candidates:", error);
    }
  };

  const fetchJobs = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/jobs/`);
      const data = await res.json();
      setJobs(data);
    } catch (error) {
      console.error("Failed to fetch jobs:", error);
    }
  };

  const startInterview = async () => {
    if (!selectedCandidate) {
      alert("Please select a candidate");
      return;
    }

    setStarting(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/interviews/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          candidate_id: selectedCandidate,
          job_description_id: selectedJob || null,
          language,
        }),
      });

      const session = await res.json();

      // Start the interview
      const startRes = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/interviews/${session.id}/start`,
        { method: "POST" }
      );

      const { token, room_name } = await startRes.json();

      // Navigate to interview room
      router.push(`/interview/room?session=${session.id}&token=${token}&room=${room_name}`);
    } catch (error) {
      console.error("Failed to start interview:", error);
      alert("Failed to start interview");
    } finally {
      setStarting(false);
    }
  };

  if (loading) {
    return <div className="flex justify-center p-8">Loading...</div>;
  }

  return (
    <div className="max-w-2xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">Start New Interview</h1>

      <div className="space-y-6">
        {/* Candidate Selection */}
        <div>
          <label className="block text-sm font-medium mb-2">
            Select Candidate
          </label>
          <select
            value={selectedCandidate}
            onChange={(e) => setSelectedCandidate(e.target.value)}
            className="w-full p-3 border rounded-lg dark:bg-gray-800 dark:border-gray-700"
          >
            <option value="">-- Select a candidate --</option>
            {candidates.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name} {c.email ? `(${c.email})` : ""}
              </option>
            ))}
          </select>
        </div>

        {/* Job Selection (Optional) */}
        <div>
          <label className="block text-sm font-medium mb-2">
            Job Description (Optional)
          </label>
          <select
            value={selectedJob}
            onChange={(e) => setSelectedJob(e.target.value)}
            className="w-full p-3 border rounded-lg dark:bg-gray-800 dark:border-gray-700"
          >
            <option value="">-- No job description --</option>
            {jobs.map((j) => (
              <option key={j.id} value={j.id}>
                {j.title} {j.company ? `at ${j.company}` : ""}
              </option>
            ))}
          </select>
        </div>

        {/* Language Selection */}
        <div>
          <label className="block text-sm font-medium mb-2">
            Interview Language
          </label>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="w-full p-3 border rounded-lg dark:bg-gray-800 dark:border-gray-700"
          >
            <option value="en">English</option>
            <option value="zh">中文 (Chinese)</option>
          </select>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4 pt-4">
          <button
            onClick={startInterview}
            disabled={starting || !selectedCandidate}
            className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {starting ? "Starting..." : "Start Interview"}
          </button>
          <button
            onClick={() => router.push("/candidates")}
            className="px-6 py-3 border rounded-lg hover:bg-gray-100 dark:border-gray-700 dark:hover:bg-gray-800"
          >
            Add Candidate
          </button>
        </div>
      </div>
    </div>
  );
}
