// S-02 Article Detail — 본문 + 댓글 (R-F-05·R-F-09~R-F-13). 실 구현은 I-09.

import { useParams } from "react-router-dom";

export default function ArticlePage() {
  const { slug } = useParams<{ slug: string }>();
  return (
    <section className="space-y-4">
      <h1 className="text-3xl font-bold">게시글 상세</h1>
      <p className="text-gray-600">
        S-02 ArticlePage placeholder (slug=<span className="font-mono text-gray-900">{slug}</span>) — 본문·댓글은 I-09에서 구현됩니다.
      </p>
    </section>
  );
}
