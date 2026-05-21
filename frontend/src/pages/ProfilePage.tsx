// S-06 Profile — author 필터 글 목록 (R-F-12). Issue #9 실 구현.

import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import ArticleCard from "../components/ArticleCard";
import { apiFetch } from "../api/client";
import type { ArticlesListResponse, ArticleView } from "../types/api";

export default function ProfilePage() {
  const { username } = useParams<{ username: string }>();
  const [articles, setArticles] = useState<ArticleView[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!username) return;
    let cancelled = false;
    setLoading(true);
    setErrorMessage(null);
    apiFetch<ArticlesListResponse>(`/articles?author=${encodeURIComponent(username)}&limit=20`)
      .then((data) => {
        if (cancelled) return;
        setArticles(data.articles);
      })
      .catch(() => {
        if (cancelled) return;
        setErrorMessage("불러올 수 없습니다");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [username]);

  return (
    <section className="space-y-4">
      <h1 className="text-3xl font-bold">{username} 님의 글</h1>
      {loading && <p className="text-gray-500">불러오는 중...</p>}
      {errorMessage && (
        <div className="rounded border border-red-300 bg-red-50 px-3 py-2 text-sm text-red-600">
          {errorMessage}
        </div>
      )}
      {!loading && !errorMessage && articles.length === 0 && (
        <p className="text-gray-500">작성한 글이 없습니다.</p>
      )}
      {!loading && articles.length > 0 && (
        <ul className="space-y-3">
          {articles.map((article) => (
            <li key={article.slug}>
              <ArticleCard article={article} />
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
