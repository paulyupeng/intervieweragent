"use client";

import { useState, useEffect } from "react";

export default function Admin() {
  const [activeTab, setActiveTab] = useState<"questions" | "scoring">("questions");
  const [questions, setQuestions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [selectedLanguage, setSelectedLanguage] = useState("en");

  useEffect(() => {
    fetchQuestions();
  }, [selectedLanguage]);

  const fetchQuestions = async () => {
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/questions/library?language=${selectedLanguage}`
      );
      const data = await res.json();
      setQuestions(data);
    } catch (error) {
      console.error("Failed to fetch questions:", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredQuestions =
    selectedCategory === "all"
      ? questions
      : questions.filter((q) => q.category === selectedCategory);

  const categories = [
    "all",
    ...new Set(questions.map((q) => q.category)),
  ];

  return (
    <div className="max-w-7xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">Admin</h1>

      {/* Tabs */}
      <div className="flex gap-4 mb-6 border-b dark:border-gray-700">
        <button
          onClick={() => setActiveTab("questions")}
          className={`px-4 py-2 ${
            activeTab === "questions"
              ? "border-b-2 border-blue-600 text-blue-600"
              : "text-gray-600 dark:text-gray-400"
          }`}
        >
          Question Banks
        </button>
        <button
          onClick={() => setActiveTab("scoring")}
          className={`px-4 py-2 ${
            activeTab === "scoring"
              ? "border-b-2 border-blue-600 text-blue-600"
              : "text-gray-600 dark:text-gray-400"
          }`}
        >
          Scoring Configuration
        </button>
      </div>

      {/* Questions Tab */}
      {activeTab === "questions" && (
        <div>
          {/* Filters */}
          <div className="flex gap-4 mb-6">
            <div>
              <label className="block text-sm font-medium mb-1">Language</label>
              <select
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="p-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
              >
                <option value="en">English</option>
                <option value="zh">中文</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Category</label>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="p-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
              >
                {categories.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat === "all" ? "All Categories" : cat}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Questions List */}
          {loading ? (
            <div className="text-center text-gray-600">Loading...</div>
          ) : (
            <div className="space-y-4">
              {filteredQuestions.map((q, i) => (
                <div
                  key={q.id || i}
                  className="bg-white dark:bg-gray-800 rounded-lg shadow p-6"
                >
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-xs font-medium px-2 py-1 bg-blue-100 text-blue-800 rounded">
                      {q.id || `Q${i + 1}`}
                    </span>
                    <span className="text-xs text-gray-500">
                      {q.expected_duration_seconds}s
                    </span>
                  </div>
                  <p className="text-gray-900 dark:text-white mb-3">{q.text}</p>
                  <div className="flex flex-wrap gap-2">
                    {q.evaluation_focus?.map((focus: string, j: number) => (
                      <span
                        key={j}
                        className="text-xs px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded"
                      >
                        {focus}
                      </span>
                    ))}
                  </div>
                  {q.followups && q.followups.length > 0 && (
                    <div className="mt-3 pt-3 border-t dark:border-gray-700">
                      <p className="text-xs font-medium text-gray-500 mb-1">
                        Follow-ups:
                      </p>
                      <ul className="list-disc list-inside text-sm text-gray-600 dark:text-gray-400">
                        {q.followups.map((fu: string, j: number) => (
                          <li key={j}>{fu}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Scoring Tab */}
      {activeTab === "scoring" && (
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">
              Scoring Dimensions
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Configure the weight of each evaluation dimension.
            </p>

            <div className="space-y-4">
              {/* English Proficiency */}
              <div>
                <h3 className="font-medium mb-2">English Proficiency</h3>
                <div className="grid md:grid-cols-5 gap-4">
                  <DimensionSlider name="Fluency" defaultValue={25} />
                  <DimensionSlider name="Vocabulary" defaultValue={20} />
                  <DimensionSlider name="Grammar" defaultValue={20} />
                  <DimensionSlider name="Comprehension" defaultValue={20} />
                  <DimensionSlider name="Pronunciation" defaultValue={15} />
                </div>
              </div>

              {/* Industry Understanding */}
              <div>
                <h3 className="font-medium mb-2">Industry Understanding</h3>
                <div className="grid md:grid-cols-4 gap-4">
                  <DimensionSlider name="Market Knowledge" defaultValue={30} />
                  <DimensionSlider name="Competitor Awareness" defaultValue={25} />
                  <DimensionSlider name="Regulatory Knowledge" defaultValue={20} />
                  <DimensionSlider name="Innovation Awareness" defaultValue={25} />
                </div>
              </div>

              {/* Professional Skills */}
              <div>
                <h3 className="font-medium mb-2">Professional Skills</h3>
                <div className="grid md:grid-cols-4 gap-4">
                  <DimensionSlider name="Technical Competency" defaultValue={35} />
                  <DimensionSlider name="Problem Solving" defaultValue={30} />
                  <DimensionSlider name="Domain Expertise" defaultValue={25} />
                  <DimensionSlider name="Tool Proficiency" defaultValue={10} />
                </div>
              </div>

              {/* Soft Skills */}
              <div>
                <h3 className="font-medium mb-2">Soft Skills</h3>
                <div className="grid md:grid-cols-5 gap-4">
                  <DimensionSlider name="Communication" defaultValue={25} />
                  <DimensionSlider name="Teamwork" defaultValue={20} />
                  <DimensionSlider name="Leadership" defaultValue={15} />
                  <DimensionSlider name="Adaptability" defaultValue={20} />
                  <DimensionSlider name="Emotional Intelligence" defaultValue={20} />
                </div>
              </div>
            </div>

            <button className="mt-6 w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">
              Save Scoring Configuration
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

function DimensionSlider({
  name,
  defaultValue,
}: {
  name: string;
  defaultValue: number;
}) {
  const [value, setValue] = useState(defaultValue);

  return (
    <div>
      <label className="block text-sm text-gray-600 dark:text-gray-400 mb-1">
        {name}
      </label>
      <div className="flex items-center gap-2">
        <input
          type="range"
          min="0"
          max="50"
          value={value}
          onChange={(e) => setValue(Number(e.target.value))}
          className="flex-1"
        />
        <span className="text-sm font-medium w-8">{value}%</span>
      </div>
    </div>
  );
}
