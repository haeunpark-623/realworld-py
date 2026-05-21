// S-03 Editor — 새 글 작성 또는 수정 (R-F-06·R-F-07). 실 구현은 I-09.

import { useParams } from "react-router-dom";

export default function EditorPage() {
  const { slug } = useParams<{ slug: string }>();
  const mode = slug ? "수정" : "새 글";
  return (
    <section className="space-y-4">
      <h1 className="text-3xl font-bold">{mode} 작성</h1>
      <p className="text-gray-600">
        S-03 EditorPage placeholder (mode=<span className="font-mono text-gray-900">{mode}</span>) — 폼은 I-09에서 구현됩니다.
      </p>
    </section>
  );
}
