"use client";

import { useState, useEffect, useRef } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import {
  LiveKitRoom,
  RoomAudioRenderer,
  StartAudio,
  useTracks,
} from "@livekit/components-react";
import { Track } from "livekit-client";

export default function InterviewRoom() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const sessionId = searchParams.get("session");
  const token = searchParams.get("token");
  const roomName = searchParams.get("room");

  const [connected, setConnected] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState("");
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [transcript, setTranscript] = useState<string[]>([]);
  const [interviewComplete, setInterviewComplete] = useState(false);

  const serverUrl = process.env.NEXT_PUBLIC_LIVEKIT_URL || "ws://localhost:7880";

  const handleConnected = () => {
    setConnected(true);
    console.log("Connected to interview room");
  };

  const handleDisconnected = () => {
    setConnected(false);
    console.log("Disconnected from interview room");
  };

  const endInterview = async () => {
    if (!sessionId) return;

    try {
      await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/interviews/${sessionId}/complete`,
        { method: "POST" }
      );
    } catch (error) {
      console.error("Failed to complete interview:", error);
    }

    router.push(`/interview/results?session=${sessionId}`);
  };

  if (!sessionId || !token || !roomName) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Invalid Interview Session</h1>
          <p className="text-gray-600">
            Missing session parameters. Please start a new interview.
          </p>
          <button
            onClick={() => router.push("/interview/start")}
            className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Start New Interview
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-semibold">Interview in Progress</h1>
          <div className="flex items-center gap-4">
            <span className={`px-3 py-1 rounded-full text-sm ${
              connected ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"
            }`}>
              {connected ? "Connected" : "Connecting..."}
            </span>
            <button
              onClick={endInterview}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
            >
              End Interview
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-4">
        <div className="grid md:grid-cols-3 gap-4">
          {/* Video/Audio Area */}
          <div className="md:col-span-2">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
              <LiveKitRoom
                video={true}
                audio={true}
                token={token}
                serverUrl={serverUrl}
                onConnected={handleConnected}
                onDisconnected={handleDisconnected}
                data-lk-theme="default"
              >
                <div className="aspect-video bg-gray-900 rounded-lg overflow-hidden">
                  <VideoTrack />
                </div>
                <RoomAudioRenderer />
                <StartAudio label="Click to enable audio" />
              </LiveKitRoom>
            </div>
          </div>

          {/* Interview Panel */}
          <div className="space-y-4">
            {/* Current Question */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
              <h2 className="text-lg font-semibold mb-4">Current Question</h2>
              <div className="min-h-[120px] p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                {currentQuestion ? (
                  <p className="text-gray-800 dark:text-gray-200">{currentQuestion}</p>
                ) : (
                  <p className="text-gray-500 dark:text-gray-400">
                    Waiting for interviewer...
                  </p>
                )}
              </div>
            </div>

            {/* Status */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
              <h2 className="text-lg font-semibold mb-4">Status</h2>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">AI Speaking:</span>
                  <span className={isSpeaking ? "text-green-600" : "text-gray-400"}>
                    {isSpeaking ? "Yes" : "No"}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Recording:</span>
                  <span className="text-green-600">Yes</span>
                </div>
              </div>
            </div>

            {/* Transcript Preview */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
              <h2 className="text-lg font-semibold mb-4">Transcript</h2>
              <div className="max-h-64 overflow-y-auto space-y-2">
                {transcript.length > 0 ? (
                  transcript.map((line, i) => (
                    <p key={i} className="text-sm text-gray-600 dark:text-gray-400">
                      {line}
                    </p>
                  ))
                ) : (
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    No transcript yet...
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function VideoTrack() {
  const tracks = useTracks();

  return (
    <div className="w-full h-full flex items-center justify-center">
      {tracks.length > 0 ? (
        <video
          ref={(el) => {
            if (el && tracks[0].source === Track.Source.Camera) {
              tracks[0].publication?.attach(el);
            }
          }}
          className="w-full h-full object-cover"
          autoPlay
          muted
        />
      ) : (
        <div className="text-gray-400">
          <p>Waiting for camera...</p>
        </div>
      )}
    </div>
  );
}
