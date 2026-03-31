"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

export default function Dashboard() {
  const [interviews, setInterviews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInterviews();
  }, []);

  const fetchInterviews = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/interviews/`);
      const data = await res.json();
      setInterviews(data);
    } catch (error) {
      console.error("Failed to fetch interviews:", error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
        return "bg-green-100 text-green-800";
      case "in_progress":
        return "bg-blue-100 text-blue-800";
      case "scheduled":
        return "bg-yellow-100 text-yellow-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getRecommendationColor = (rec: string) => {
    switch (rec) {
      case "PROCEED":
        return "text-green-600";
      case "HOLD":
        return "text-yellow-600";
      case "REJECT":
        return "text-red-600";
      default:
        return "text-gray-600";
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <Link
          href="/interview/start"
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          New Interview
        </Link>
      </div>

      {/* Stats */}
      <div className="grid md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <div className="text-3xl font-bold text-blue-600">
            {interviews.length}
          </div>
          <div className="text-gray-600 dark:text-gray-400">Total Interviews</div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <div className="text-3xl font-bold text-green-600">
            {interviews.filter((i) => i.status === "completed").length}
          </div>
          <div className="text-gray-600 dark:text-gray-400">Completed</div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <div className="text-3xl font-bold text-yellow-600">
            {interviews.filter((i) => i.status === "scheduled").length}
          </div>
          <div className="text-gray-600 dark:text-gray-400">Scheduled</div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <div className="text-3xl font-bold text-purple-600">
            {interviews.filter(
              (i) => i.hiring_recommendation === "PROCEED"
            ).length}
          </div>
          <div className="text-gray-600 dark:text-gray-400">Recommended</div>
        </div>
      </div>

      {/* Interviews Table */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b dark:border-gray-700">
          <h2 className="text-lg font-semibold">Recent Interviews</h2>
        </div>

        {loading ? (
          <div className="p-8 text-center text-gray-600">Loading...</div>
        ) : interviews.length === 0 ? (
          <div className="p-8 text-center text-gray-600">
            No interviews yet.{" "}
            <Link href="/interview/start" className="text-blue-600 hover:underline">
              Start your first interview
            </Link>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Candidate
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Recommendation
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {interviews.map((interview) => (
                  <tr key={interview.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-gray-900 dark:text-white">
                        Candidate {interview.candidate_id?.slice(0, 8)}...
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                      {new Date(interview.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4">
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(
                          interview.status
                        )}`}
                      >
                        {interview.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">
                      {interview.overall_score?.toFixed(1) ?? "-"}
                    </td>
                    <td className="px-6 py-4">
                      <span
                        className={`text-sm font-medium ${getRecommendationColor(
                          interview.hiring_recommendation
                        )}`}
                      >
                        {interview.hiring_recommendation ?? "-"}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      {interview.status === "completed" && (
                        <Link
                          href={`/interview/results?session=${interview.id}`}
                          className="text-blue-600 hover:underline text-sm"
                        >
                          View Results
                        </Link>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
