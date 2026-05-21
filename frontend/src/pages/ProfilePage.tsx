// S-06 Profile (R-F-12, P2 컷 후보). 실 구현은 I-09.

import { useParams } from "react-router-dom";

export default function ProfilePage() {
  const { username } = useParams<{ username: string }>();
  return (
    <section className="space-y-4">
      <h1 className="text-3xl font-bold">프로필</h1>
      <p className="text-gray-600">
        S-06 ProfilePage placeholder (username=<span className="font-mono text-gray-900">{username}</span>) — 내 글 목록은 I-09에서 구현됩니다.
      </p>
    </section>
  );
}
