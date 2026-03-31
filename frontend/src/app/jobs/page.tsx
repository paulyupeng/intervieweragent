"use client";

import { useState, useEffect } from "react";

export default function Jobs() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: "",
    company: "",
    jd_text: "",
  });

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/jobs/`);
      const data = await res.json();
      setJobs(data);
    } catch (error) {
      console.error("Failed to fetch jobs:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const formDataToSend = new FormData();
    formDataToSend.append("title", formData.title);
    if (formData.company) formDataToSend.append("company", formData.company);
    formDataToSend.append("jd_text", formData.jd_text);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/jobs/`, {
        method: "POST",
        body: formDataToSend,
      });

      if (res.ok) {
        setShowForm(false);
        setFormData({ title: "", company: "", jd_text: "" });
        fetchJobs();
      }
    } catch (error) {
      console.error("Failed to create job:", error);
    }
  };

  const parseJob = async (id: string) => {
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/jobs/${id}/parse`,
        { method: "POST" }
      );
      if (res.ok) {
        alert("Job requirements extracted successfully!");
        fetchJobs();
      }
    } catch (error) {
      console.error("Failed to parse job:", error);
      alert("Failed to parse job description");
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Job Descriptions</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          {showForm ? "Cancel" : "Add Job Description"}
        </button>
      </div>

      {/* Add Job Form */}
      {showForm && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Add Job Description</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Job Title *</label>
              <input
                type="text"
                required
                value={formData.title}
                onChange={(e) =>
                  setFormData({ ...formData, title: e.target.value })
                }
                className="w-full p-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Company</label>
              <input
                type="text"
                value={formData.company}
                onChange={(e) =>
                  setFormData({ ...formData, company: e.target.value })
                }
                className="w-full p-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">
                Job Description *
              </label>
              <textarea
                required
                rows={8}
                value={formData.jd_text}
                onChange={(e) =>
                  setFormData({ ...formData, jd_text: e.target.value })
                }
                className="w-full p-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
                placeholder="Paste the full job description here..."
              />
            </div>
            <button
              type="submit"
              className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
            >
              Save Job Description
            </button>
          </form>
        </div>
      )}

      {/* Jobs List */}
      <div className="grid md:grid-cols-2 gap-6">
        {loading ? (
          <div className="text-center text-gray-600">Loading...</div>
        ) : jobs.length === 0 ? (
          <div className="col-span-2 p-8 text-center text-gray-600">
            No job descriptions yet. Add your first job description to get started.
          </div>
        ) : (
          jobs.map((job) => (
            <div
              key={job.id}
              className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6"
            >
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold">{job.title}</h3>
                  {job.company && (
                    <p className="text-gray-600 dark:text-gray-400">{job.company}</p>
                  )}
                </div>
                {!job.requirements && (
                  <button
                    onClick={() => parseJob(job.id)}
                    className="px-3 py-1 text-sm bg-purple-100 text-purple-800 rounded hover:bg-purple-200"
                  >
                    Parse Requirements
                  </button>
                )}
              </div>

              <div className="text-sm text-gray-600 dark:text-gray-400 line-clamp-4 mb-4">
                {job.jd_text}
              </div>

              {job.requirements && (
                <div className="mt-4">
                  <h4 className="text-sm font-semibold mb-2">Requirements</h4>
                  <div className="flex flex-wrap gap-2">
                    {job.requirements.required_skills?.slice(0, 5).map(
                      (skill: string, i: number) => (
                        <span
                          key={i}
                          className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded"
                        >
                          {skill}
                        </span>
                      )
                    )}
                    {job.requirements.required_skills?.length > 5 && (
                      <span className="text-xs text-gray-500">
                        +{job.requirements.required_skills.length - 5} more
                      </span>
                    )}
                  </div>
                </div>
              )}

              <div className="mt-4 text-xs text-gray-500">
                Created: {new Date(job.created_at).toLocaleDateString()}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
