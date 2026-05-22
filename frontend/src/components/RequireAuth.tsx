// M-FE-Components RequireAuth — Issue #21.
// 비로그인 시 /login으로 즉시 리다이렉트 (PRD F-02 실패-2 + F-01 실패-3).

import { Navigate } from "react-router-dom";

import { useAuthStore } from "../store/auth";

type Props = {
  children: React.ReactNode;
};

export default function RequireAuth({ children }: Props) {
  const token = useAuthStore((state) => state.token);
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
}
