// S-04 Login (R-F-02). Issue #8 실 구현.

import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";

import { ApiError, apiFetch } from "../api/client";
import { useAuthStore } from "../store/auth";
import { extractErrorMessage, type UserResponse } from "../types/api";

export default function LoginPage() {
  const navigate = useNavigate();
  const login = useAuthStore((state) => state.login);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErrorMessage(null);
    setSubmitting(true);
    try {
      const response = await apiFetch<UserResponse>("/users/login", {
        method: "POST",
        body: JSON.stringify({ user: { email, password } }),
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
      <h1 className="text-3xl font-bold">로그인</h1>
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
          <label htmlFor="login-email" className="block text-sm font-medium text-gray-700">
            이메일
          </label>
          <input
            id="login-email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoComplete="email"
            onInvalid={(e) => {
              const el = e.currentTarget;
              if (el.validity.valueMissing) el.setCustomValidity("이메일을 입력해 주세요");
              else if (el.validity.typeMismatch) el.setCustomValidity("이메일 형식이 올바르지 않습니다");
            }}
            onInput={(e) => e.currentTarget.setCustomValidity("")}
            className="w-full rounded border border-gray-300 px-3 py-2 text-base focus:border-blue-600 focus:outline-none"
          />
        </div>
        <div className="space-y-1">
          <label htmlFor="login-password" className="block text-sm font-medium text-gray-700">
            비밀번호
          </label>
          <input
            id="login-password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="current-password"
            onInvalid={(e) =>
              e.currentTarget.setCustomValidity("비밀번호를 입력해 주세요")
            }
            onInput={(e) => e.currentTarget.setCustomValidity("")}
            className="w-full rounded border border-gray-300 px-3 py-2 text-base focus:border-blue-600 focus:outline-none"
          />
        </div>
        <button
          type="submit"
          disabled={submitting}
          className="w-full rounded bg-blue-600 px-3 py-2 text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-300"
        >
          {submitting ? "로그인 중..." : "로그인"}
        </button>
      </form>
    </section>
  );
}
