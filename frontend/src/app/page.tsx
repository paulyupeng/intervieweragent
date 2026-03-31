"use client";

import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <div className="max-w-4xl w-full space-y-8">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white">
            Interviewer Agent
          </h1>
          <p className="mt-4 text-xl text-gray-600 dark:text-gray-300">
            AI-powered voice interview system for candidate assessment
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 mt-12">
          {/* Start Interview Card */}
          <Link
            href="/interview/start"
            className="block p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg hover:shadow-xl transition-shadow"
          >
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
              Start Interview
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Begin a new voice interview session. The AI will ask questions
              and evaluate responses in real-time.
            </p>
          </Link>

          {/* Dashboard Card */}
          <Link
            href="/dashboard"
            className="block p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg hover:shadow-xl transition-shadow"
          >
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
              Dashboard
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              View past interviews, candidate evaluations, and scoring reports.
            </p>
          </Link>

          {/* Candidates Card */}
          <Link
            href="/candidates"
            className="block p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg hover:shadow-xl transition-shadow"
          >
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
              Candidates
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Manage candidate profiles, upload resumes, and track interview status.
            </p>
          </Link>

          {/* Jobs Card */}
          <Link
            href="/jobs"
            className="block p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg hover:shadow-xl transition-shadow"
          >
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
              Job Descriptions
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Create and manage job descriptions. Auto-extract requirements and match candidates.
            </p>
          </Link>

          {/* Admin Card */}
          <Link
            href="/admin"
            className="block p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg hover:shadow-xl transition-shadow"
          >
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
              Admin
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Manage question banks, scoring configurations, and system settings.
            </p>
          </Link>

          {/* Settings Card */}
          <Link
            href="/settings"
            className="block p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg hover:shadow-xl transition-shadow"
          >
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
              Settings
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Configure API keys, voice settings, and interview preferences.
            </p>
          </Link>
        </div>

        <div className="mt-12 p-6 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            How it works
          </h3>
          <ol className="list-decimal list-inside space-y-2 text-gray-600 dark:text-gray-400">
            <li>Create a job description or select an existing one</li>
            <li>Add candidate information and upload resume</li>
            <li>Start a voice interview session</li>
            <li>AI asks questions across 4 dimensions: English, Industry Knowledge, Professional Skills, Soft Skills</li>
            <li>Receive automated scoring and evaluation report</li>
          </ol>
        </div>
      </div>
    </main>
  );
}
