"use client";

import { useState, useEffect } from "react";

export default function Settings() {
  const [config, setConfig] = useState({
    deepgram_api_key: "",
    elevenlabs_api_key: "",
    anthropic_api_key: "",
    default_language: "en",
    max_interview_duration: 60,
  });
  const [saved, setSaved] = useState(false);

  const handleChange = (key: string, value: string) => {
    setConfig({ ...config, [key]: value });
    setSaved(false);
  };

  const handleSave = () => {
    // In a real implementation, this would save to backend
    // For now, just show success message
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="max-w-2xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">Settings</h1>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 space-y-6">
        {/* API Keys Section */}
        <div>
          <h2 className="text-xl font-semibold mb-4">API Keys</h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">
                Deepgram API Key (Speech-to-Text)
              </label>
              <input
                type="password"
                value={config.deepgram_api_key}
                onChange={(e) => handleChange("deepgram_api_key", e.target.value)}
                className="w-full p-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
                placeholder="sk_..."
              />
              <p className="text-xs text-gray-500 mt-1">
                Get your key from{" "}
                <a
                  href="https://console.deepgram.com"
                  target="_blank"
                  className="text-blue-600 hover:underline"
                >
                  console.deepgram.com
                </a>
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                ElevenLabs API Key (Text-to-Speech)
              </label>
              <input
                type="password"
                value={config.elevenlabs_api_key}
                onChange={(e) => handleChange("elevenlabs_api_key", e.target.value)}
                className="w-full p-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
                placeholder="..."
              />
              <p className="text-xs text-gray-500 mt-1">
                Get your key from{" "}
                <a
                  href="https://elevenlabs.io/app/settings"
                  target="_blank"
                  className="text-blue-600 hover:underline"
                >
                  elevenlabs.io
                </a>
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Anthropic API Key (LLM Evaluation)
              </label>
              <input
                type="password"
                value={config.anthropic_api_key}
                onChange={(e) => handleChange("anthropic_api_key", e.target.value)}
                className="w-full p-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
                placeholder="sk-ant-..."
              />
              <p className="text-xs text-gray-500 mt-1">
                Get your key from{" "}
                <a
                  href="https://console.anthropic.com"
                  target="_blank"
                  className="text-blue-600 hover:underline"
                >
                  console.anthropic.com
                </a>
              </p>
            </div>
          </div>
        </div>

        {/* Interview Settings */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Interview Settings</h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">
                Default Language
              </label>
              <select
                value={config.default_language}
                onChange={(e) => handleChange("default_language", e.target.value)}
                className="w-full p-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
              >
                <option value="en">English</option>
                <option value="zh">中文 (Chinese)</option>
                <option value="es">Español (Spanish)</option>
                <option value="fr">Français (French)</option>
                <option value="de">Deutsch (German)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Max Interview Duration (minutes)
              </label>
              <input
                type="number"
                value={config.max_interview_duration}
                onChange={(e) =>
                  handleChange("max_interview_duration", e.target.value)
                }
                className="w-full p-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
              />
            </div>
          </div>
        </div>

        {/* Save Button */}
        <div className="pt-4">
          <button
            onClick={handleSave}
            className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
          >
            Save Settings
          </button>
          {saved && (
            <p className="text-center text-green-600 mt-2">
              Settings saved! (Note: In this demo, settings are not persisted)
            </p>
          )}
        </div>

        {/* Info */}
        <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
          <h3 className="text-sm font-semibold mb-2">About API Keys</h3>
          <p className="text-xs text-gray-600 dark:text-gray-400">
            For security, API keys should be configured in the{" "}
            <code className="bg-gray-200 dark:bg-gray-700 px-1 rounded">.env</code>{" "}
            file on the server. This settings page is for demonstration purposes.
          </p>
        </div>
      </div>
    </div>
  );
}
