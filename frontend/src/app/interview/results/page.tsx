"use client";

import { useState, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";

export default function InterviewResults() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const sessionId = searchParams.get("session");
  const [evaluation, setEvaluation] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (sessionId) {
      fetchEvaluation();
    }
  }, [sessionId]);

  const fetchEvaluation = async () => {
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/interviews/${sessionId}/evaluation`
      );
      const data = await res.json();
      setEvaluation(data);
    } catch (error) {
      console.error("Failed to fetch evaluation:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading evaluation...</p>
        </div>
      </div>
    );
  }

  if (!evaluation) {
    return (
      <div className="max-w-2xl mx-auto p-8 text-center">
        <h1 className="text-2xl font-bold mb-4">Evaluation Not Available</h1>
        <p className="text-gray-600">
          The evaluation is still being processed. Please check back later.
        </p>
        <button
          onClick={() => router.push("/dashboard")}
          className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Go to Dashboard
        </button>
      </div>
    );
  }

  const getRecommendationColor = (recommendation: string) => {
    switch (recommendation) {
      case "PROCEED":
        return "bg-green-100 text-green-800";
      case "HOLD":
        return "bg-yellow-100 text-yellow-800";
      case "REJECT":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">Interview Evaluation</h1>

      {/* Overall Score */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Overall Assessment</h2>
          <span className={`px-4 py-2 rounded-full font-semibold ${getRecommendationColor(
            evaluation.hiring_recommendation
          )}`}>
            {evaluation.hiring_recommendation}
          </span>
        </div>

        <div className="text-center py-8">
          <div className="text-6xl font-bold text-blue-600 mb-2">
            {evaluation.overall_score?.toFixed(1)}%
          </div>
          <p className="text-gray-600 dark:text-gray-400">Overall Score</p>
        </div>

        {/* Dimension Scores */}
        <div className="grid md:grid-cols-2 gap-4 mt-6">
          {evaluation.dimension_scores &&
            Object.entries(evaluation.dimension_scores).map(([dim, data]: [string, any]) => (
              <div key={dim} className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <h3 className="font-semibold capitalize mb-2">
                  {dim.replace(/_/g, " ")}
                </h3>
                <div className="flex items-center gap-3">
                  <div className="flex-1 bg-gray-200 dark:bg-gray-600 rounded-full h-3">
                    <div
                      className="bg-blue-600 h-3 rounded-full"
                      style={{
                        width: `${(data.score / data.max_score) * 100}%`,
                      }}
                    ></div>
                  </div>
                  <span className="font-medium">
                    {data.score?.toFixed(1)} / {data.max_score?.toFixed(1)}
                  </span>
                </div>
              </div>
            ))}
        </div>
      </div>

      {/* Recommendations */}
      {evaluation.recommendations && evaluation.recommendations.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Recommendations</h2>
          <ul className="list-disc list-inside space-y-2">
            {evaluation.recommendations.map((rec: string, i: number) => (
              <li key={i} className="text-gray-700 dark:text-gray-300">
                {rec}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Transcript */}
      {evaluation.transcript && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Full Transcript</h2>
          <div className="max-h-96 overflow-y-auto whitespace-pre-wrap text-gray-700 dark:text-gray-300">
            {evaluation.transcript}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-4">
        <button
          onClick={() => router.push("/dashboard")}
          className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Back to Dashboard
        </button>
        <button
          onClick={() => window.print()}
          className="px-6 py-3 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
        >
          Print Report
        </button>
      </div>
    </div>
  );
}
