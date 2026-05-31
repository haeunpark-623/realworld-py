// S-01 Home — 게시글 목록 (R-F-04). Issue #9 실 구현 + Issue #25 태그 필터.

import { useEffect, useState } from "react";

import ArticleCard from "../components/ArticleCard";
import { ApiError, apiFetch } from "../api/client";
import type { ArticlesListResponse, ArticleView, TagsListResponse } from "../types/api";

const PAGE_SIZE = 20;

export default function HomePage() {
  const [articles, setArticles] = useState<ArticleView[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [tags, setTags] = useState<string[]>([]);
  const [selectedTag, setSelectedTag] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    apiFetch<TagsListResponse>("/tags")
      .then((data) => {
        if (!cancelled) setTags(data.tags);
      })
      .catch(() => {
        // tags 로드 실패는 silent — 핵심 UX 영향 0
      });
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setErrorMessage(null);
    const offset = (page - 1) * PAGE_SIZE;
    const tagParam = selectedTag ? `&tag=${encodeURIComponent(selectedTag)}` : "";
    apiFetch<ArticlesListResponse>(`/articles?limit=${PAGE_SIZE}&offset=${offset}${tagParam}`)
      .then((data) => {
        if (cancelled) return;
        setArticles(data.articles);
        setTotal(data.articlesCount);
      })
      .catch((error) => {
        if (cancelled) return;
        setErrorMessage(error instanceof ApiError ? `API ${error.status}` : "네트워크 오류");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [page, selectedTag]);

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  function handleTagClick(tag: string) {
    setSelectedTag(tag);
    setPage(1);
  }

  function handleClearTag() {
    setSelectedTag(null);
    setPage(1);
  }

  return (
    <section className="space-y-4">
      <h1 className="text-3xl font-bold">최근 게시글</h1>
      {tags.length > 0 && (
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-sm text-gray-500">태그:</span>
          {tags.map((tag) => (
            <button
              key={tag}
              type="button"
              onClick={() => handleTagClick(tag)}
              className={
                tag === selectedTag
                  ? "rounded-full bg-blue-600 px-3 py-1 text-xs text-white"
                  : "rounded-full border border-gray-300 px-3 py-1 text-xs text-gray-700 hover:bg-gray-50"
              }
            >
              #{tag}
            </button>
          ))}
          {selectedTag && (
            <button
              type="button"
              onClick={handleClearTag}
              className="ml-2 text-xs text-gray-500 underline hover:text-gray-700"
            >
              전체 보기
            </button>
          )}
        </div>
      )}
      {loading && <p className="text-gray-500">불러오는 중...</p>}
      {errorMessage && (
        <div className="rounded border border-red-300 bg-red-50 px-3 py-2 text-sm text-red-600">
          {errorMessage}
          <button
            type="button"
            onClick={() => setPage((p) => p)}
            className="ml-2 underline"
          >
            재시도
          </button>
        </div>
      )}
      {!loading && !errorMessage && articles.length === 0 && (
        <p className="text-gray-500">아직 게시글이 없습니다.</p>
      )}
      {!loading && articles.length > 0 && (
        <>
          <ul className="space-y-3">
            {articles.map((article) => (
              <li key={article.slug}>
                <ArticleCard article={article} />
              </li>
            ))}
          </ul>
          {totalPages > 1 && (
            <nav className="flex items-center justify-center gap-1 pt-4">
              <button
                type="button"
                disabled={page === 1}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                className="rounded border border-gray-300 px-3 py-1 text-sm disabled:opacity-50"
              >
                ‹
              </button>
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((n) => (
                <button
                  key={n}
                  type="button"
                  onClick={() => setPage(n)}
                  aria-current={n === page ? "page" : undefined}
                  className={
                    n === page
                      ? "rounded border border-blue-600 bg-blue-600 px-3 py-1 text-sm text-white"
                      : "rounded border border-gray-300 px-3 py-1 text-sm hover:bg-gray-50"
                  }
                >
                  {n}
                </button>
              ))}
              <button
                type="button"
                disabled={page === totalPages}
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                className="rounded border border-gray-300 px-3 py-1 text-sm disabled:opacity-50"
              >
                ›
              </button>
            </nav>
          )}
        </>
      )}
    </section>
  );
}
