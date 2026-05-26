import { Routes, Route, Navigate } from "react-router-dom";

// Pages — Prateeksha will implement these components
// Import placeholders until frontend phase begins
const PlaceholderPage = ({ name }) => (
  <div className="flex items-center justify-center h-screen bg-gray-950 text-white">
    <div className="text-center">
      <h1 className="text-3xl font-bold mb-2">AppForge AI</h1>
      <p className="text-gray-400">{name} — coming soon</p>
    </div>
  </div>
);

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<PlaceholderPage name="Landing Page" />} />
      <Route path="/login" element={<PlaceholderPage name="Login Page" />} />
      <Route path="/register" element={<PlaceholderPage name="Register Page" />} />
      <Route path="/idea" element={<PlaceholderPage name="Idea Page" />} />
      <Route path="/overview" element={<PlaceholderPage name="Overview Page" />} />
      <Route path="/questions" element={<PlaceholderPage name="Questions Page" />} />
      <Route path="/diagrams" element={<PlaceholderPage name="Diagrams Page" />} />
      <Route path="/docs" element={<PlaceholderPage name="Docs Page" />} />
      <Route path="/code" element={<PlaceholderPage name="Code Generation Page" />} />
      <Route path="/complete" element={<PlaceholderPage name="Complete Page" />} />
      <Route path="/history" element={<PlaceholderPage name="History Page" />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}