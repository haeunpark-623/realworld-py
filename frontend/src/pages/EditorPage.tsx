// S-03 Editor — 새 글 작성 또는 수정 (R-F-06·R-F-07). Issue #9 실 구현.

import { useEffect, useState, type FormEvent } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { ApiError, apiFetch } from "../api/client";
import { useAuthStore } from "../store/auth";
import { extractErrorMessage, type ArticleResponse } from "../types/api";

export default function EditorPage() {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const token = useAuthStore((s) => s.token);
  const isEditMode = Boolean(slug);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [body, setBody] = useState("");
  const [tagList, setTagList] = useState(""); // 쉼표 split
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(isEditMode);

  useEffect(() => {
    if (!isEditMode || !slug) return;
    let cancelled = false;
    setLoading(true);
    apiFetch<ArticleResponse>(`/articles/${slug}`)
      .then((data) => {
        if (cancelled) return;
        setTitle(data.article.title);
        setDescription(data.article.description ?? "");
        setBody(data.article.body);
        setTagList(data.article.tagList.join(", "));
      })
      .catch(() => {
        if (cancelled) return;
        setErrorMessage("게시글을 불러올 수 없습니다");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [slug, isEditMode]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!token) {
      setErrorMessage("로그인이 필요합니다");
      return;
    }
    setSubmitting(true);
    setErrorMessage(null);
    const payload = {
      article: {
        title,
        description: description || null,
        body,
        tagList: tagList
          .split(",")
          .map((t) => t.trim())
          .filter((t) => t.length > 0),
      },
    };
    try {
      const path = isEditMode ? `/articles/${slug}` : "/articles";
      const method = isEditMode ? "PUT" : "POST";
      const response = await apiFetch<ArticleResponse>(path, {
        method,
        body: JSON.stringify(payload),
        token,
      });
      navigate(`/article/${response.article.slug}`);
    } catch (error) {
      setErrorMessage(
        error instanceof ApiError ? extractErrorMessage(error.body) : "네트워크 오류"
      );
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) return <p className="text-gray-500">불러오는 중...</p>;

  return (
    <section className="mx-auto max-w-2xl space-y-4">
      <h1 className="text-3xl font-bold">{isEditMode ? "게시글 수정" : "새 글 작성"}</h1>
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
          <label htmlFor="editor-title" className="block text-sm font-medium text-gray-700">
            제목
          </label>
          <input
            id="editor-title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            maxLength={255}
            onInvalid={(e) =>
              e.currentTarget.setCustomValidity("제목을 입력해 주세요")
            }
            onInput={(e) => e.currentTarget.setCustomValidity("")}
            className="w-full rounded border border-gray-300 px-3 py-2 text-base focus:border-blue-600 focus:outline-none"
          />
        </div>
        <div className="space-y-1">
          <label htmlFor="editor-description" className="block text-sm font-medium text-gray-700">
            요약
          </label>
          <input
            id="editor-description"
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="(선택)"
            className="w-full rounded border border-gray-300 px-3 py-2 text-base focus:border-blue-600 focus:outline-none"
          />
        </div>
        <div className="space-y-1">
          <label htmlFor="editor-body" className="block text-sm font-medium text-gray-700">
            본문
          </label>
          <textarea
            id="editor-body"
            value={body}
            onChange={(e) => setBody(e.target.value)}
            required
            rows={10}
            onInvalid={(e) =>
              e.currentTarget.setCustomValidity("본문을 입력해 주세요")
            }
            onInput={(e) => e.currentTarget.setCustomValidity("")}
            className="w-full rounded border border-gray-300 px-3 py-2 text-base focus:border-blue-600 focus:outline-none"
          />
        </div>
        <div className="space-y-1">
          <label htmlFor="editor-tags" className="block text-sm font-medium text-gray-700">
            태그 (쉼표로 구분)
          </label>
          <input
            id="editor-tags"
            type="text"
            value={tagList}
            onChange={(e) => setTagList(e.target.value)}
            placeholder="예: python, fastapi, react"
            className="w-full rounded border border-gray-300 px-3 py-2 text-base focus:border-blue-600 focus:outline-none"
          />
        </div>
        <div className="flex justify-end gap-2">
          <button
            type="button"
            onClick={() => navigate(slug ? `/article/${slug}` : "/")}
            className="rounded border border-gray-300 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50"
          >
            취소
          </button>
          <button
            type="submit"
            disabled={submitting}
            className="rounded bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700 disabled:bg-blue-300"
          >
            {submitting ? "저장 중..." : isEditMode ? "수정 저장" : "작성"}
          </button>
        </div>
      </form>
    </section>
  );
}
