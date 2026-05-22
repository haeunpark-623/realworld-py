import { useEffect } from "react";
import { Route, Routes } from "react-router-dom";

import Header from "./components/Header";
import RequireAuth from "./components/RequireAuth";
import ArticlePage from "./pages/ArticlePage";
import EditorPage from "./pages/EditorPage";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import ProfilePage from "./pages/ProfilePage";
import RegisterPage from "./pages/RegisterPage";
import { useAuthStore } from "./store/auth";

export default function App() {
  useEffect(() => {
    useAuthStore.getState().loadFromStorage();
  }, []);

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <Header />
      <main className="mx-auto max-w-4xl p-8">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/article/:slug" element={<ArticlePage />} />
          <Route path="/editor" element={<RequireAuth><EditorPage /></RequireAuth>} />
          <Route path="/editor/:slug" element={<RequireAuth><EditorPage /></RequireAuth>} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/profile/:username"
            element={<RequireAuth><ProfilePage /></RequireAuth>}
          />
        </Routes>
      </main>
    </div>
  );
}
