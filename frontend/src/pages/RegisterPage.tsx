// S-05 Register (R-F-01). Issue #8 실 구현.

import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";

import { ApiError, apiFetch } from "../api/client";
import { useAuthStore } from "../store/auth";
import { extractErrorMessage, type UserResponse } from "../types/api";

export default function RegisterPage() {
  const navigate = useNavigate();
  const login = useAuthStore((state) => state.login);

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErrorMessage(null);
    setSubmitting(true);
    try {
      const response = await apiFetch<UserResponse>("/users", {
        method: "POST",
        body: JSON.stringify({ user: { username, email, password } }),
      });
      login({ username: response.user.username, email: response.user.email }, response.user.token);
      navigate("/");
    } catch (error) {
      if (error instanceof ApiError) {
        setErrorMessage(extractErrorMessage(error.body));
      } else {
        setErrorMessage("네트워크 오류가 발생했습니다");
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="mx-auto max-w-sm space-y-4">
      <h1 className="text-3xl font-bold">가입</h1>
      {errorMessage && (
        <div
          role="alert"
          className="rounded border border-red-300 bg-red-50 px-3 py-2 text-sm text-red-600"
        >
          {errorMessage}
        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="space-y-1">
          <label htmlFor="register-username" className="block text-sm font-medium text-gray-700">
            사용자명
          </label>
          <input
            id="register-username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            minLength={1}
            maxLength={64}
            autoComplete="username"
            className="w-full rounded border border-gray-300 px-3 py-2 text-base focus:border-blue-600 focus:outline-none"
          />
        </div>
        <div className="space-y-1">
          <label htmlFor="register-email" className="block text-sm font-medium text-gray-700">
            이메일
          </label>
          <input
            id="register-email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoComplete="email"
            className="w-full rounded border border-gray-300 px-3 py-2 text-base focus:border-blue-600 focus:outline-none"
          />
        </div>
        <div className="space-y-1">
          <label htmlFor="register-password" className="block text-sm font-medium text-gray-700">
            비밀번호
          </label>
          <input
            id="register-password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
            maxLength={128}
            autoComplete="new-password"
            className="w-full rounded border border-gray-300 px-3 py-2 text-base focus:border-blue-600 focus:outline-none"
          />
          <p className="text-xs text-gray-500">최소 8자 이상</p>
        </div>
        <button
          type="submit"
          disabled={submitting}
          className="w-full rounded bg-blue-600 px-3 py-2 text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-300"
        >
          {submitting ? "가입 중..." : "가입하기"}
        </button>
      </form>
    </section>
  );
}
