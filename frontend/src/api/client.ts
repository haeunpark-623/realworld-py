// M-FE-ApiClient — fetch 래퍼. Authorization 헤더 자동 첨부.
// Issue #21: 401 응답 시 중앙 인터셉터로 자동 logout + /login 리다이렉트 (PRD F-01 실패-3).

import { useAuthStore } from "../store/auth";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api";

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly body: unknown
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export type ApiFetchOptions = RequestInit & { token?: string | null };

export async function apiFetch<T>(path: string, options: ApiFetchOptions = {}): Promise<T> {
  const { token, headers, ...rest } = options;
  const url = `${API_BASE_URL}${path}`;
  const response = await fetch(url, {
    ...rest,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Token ${token}` } : {}),
      ...headers,
    },
  });

  if (response.status === 204) {
    return undefined as T;
  }

  const text = await response.text();
  const body: unknown = text ? JSON.parse(text) : null;

  if (response.status === 401 && token) {
    // 만료된 token 보유 + 401: 자동 logout + /login (PRD F-01 실패-3, Issue #21)
    useAuthStore.getState().logout();
    if (typeof window !== "undefined" && window.location.pathname !== "/login") {
      window.location.assign("/login");
    }
  }

  if (!response.ok) {
    throw new ApiError(`API ${response.status}`, response.status, body);
  }

  return body as T;
}
