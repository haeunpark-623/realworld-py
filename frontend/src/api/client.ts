// M-FE-ApiClient — fetch 래퍼. 실 사용은 I-08(인증)·I-09(게시판).
// Authorization 헤더 자동 첨부 + 401 → logout + redirect는 I-08에서 구현.

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

  if (!response.ok) {
    throw new ApiError(`API ${response.status}`, response.status, body);
  }

  return body as T;
}
