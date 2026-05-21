// S-02 Article Detail — 본문 + 댓글 (R-F-05·R-F-08·R-F-09·R-F-10·R-F-11·R-F-13). Issue #9 실 구현.

import { useEffect, useState, type FormEvent } from "react";
import { useNavigate, useParams } from "react-router-dom";

import CommentItem from "../components/CommentItem";
import Modal from "../components/Modal";
import { ApiError, apiFetch } from "../api/client";
import { useAuthStore } from "../store/auth";
import {
  extractErrorMessage,
  type ArticleResponse,
  type ArticleView,
  type CommentResponse,
  type CommentsListResponse,
  type CommentView,
} from "../types/api";

export default function ArticlePage() {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const user = useAuthStore((s) => s.user);
  const token = useAuthStore((s) => s.token);

  const [article, setArticle] = useState<ArticleView | null>(null);
  const [comments, setComments] = useState<CommentView[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [commentBody, setCommentBody] = useState("");
  const [commentError, setCommentError] = useState<string | null>(null);
  const [submittingComment, setSubmittingComment] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);

  useEffect(() => {
    if (!slug) return;
    let cancelled = false;
    setLoading(true);
    setErrorMessage(null);
    Promise.all([
      apiFetch<ArticleResponse>(`/articles/${slug}`),
      apiFetch<CommentsListResponse>(`/articles/${slug}/comments`).catch(() => ({ comments: [] })),
    ])
      .then(([articleData, commentsData]) => {
        if (cancelled) return;
        setArticle(articleData.article);
        setComments(commentsData.comments);
      })
      .catch((error) => {
        if (cancelled) return;
        if (error instanceof ApiError && error.status === 404) {
          setErrorMessage("게시글을 찾을 수 없습니다");
        } else {
          setErrorMessage("네트워크 오류");
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [slug]);

  async function handleCommentSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!slug || !commentBody.trim() || !token) return;
    setSubmittingComment(true);
    setCommentError(null);
    try {
      const response = await apiFetch<CommentResponse>(`/articles/${slug}/comments`, {
        method: "POST",
        body: JSON.stringify({ comment: { body: commentBody } }),
        token,
      });
      setComments((prev) => [response.comment, ...prev]);
      setCommentBody("");
    } catch (error) {
      setCommentError(
        error instanceof ApiError ? extractErrorMessage(error.body) : "네트워크 오류"
      );
    } finally {
      setSubmittingComment(false);
    }
  }

  async function handleCommentUpdate(commentId: number, body: string) {
    if (!slug || !token) return;
    const response = await apiFetch<CommentResponse>(`/articles/${slug}/comments/${commentId}`, {
      method: "PUT",
      body: JSON.stringify({ comment: { body } }),
      token,
    });
    setComments((prev) => prev.map((c) => (c.id === commentId ? response.comment : c)));
  }

  async function handleCommentDelete(commentId: number) {
    if (!slug || !token) return;
    await apiFetch<void>(`/articles/${slug}/comments/${commentId}`, {
      method: "DELETE",
      token,
    });
    setComments((prev) => prev.filter((c) => c.id !== commentId));
  }

  async function handleArticleDelete() {
    if (!slug || !token) return;
    try {
      await apiFetch<void>(`/articles/${slug}`, { method: "DELETE", token });
      navigate("/");
    } catch {
      setErrorMessage("삭제에 실패했습니다");
      setDeleteOpen(false);
    }
  }

  if (loading) return <p className="text-gray-500">불러오는 중...</p>;
  if (errorMessage || !article) {
    return (
      <div className="rounded border border-red-300 bg-red-50 px-3 py-2 text-sm text-red-600">
        {errorMessage ?? "게시글을 찾을 수 없습니다"}
      </div>
    );
  }

  const isAuthor = user !== null && user.username === article.author.username;

  return (
    <article className="space-y-6">
      <header className="space-y-2 border-b border-gray-200 pb-4">
        <h1 className="text-3xl font-bold">{article.title}</h1>
        <div className="flex items-center justify-between text-sm text-gray-500">
          <span>
            {article.author.username} ·{" "}
            <time dateTime={article.createdAt}>{formatDate(article.createdAt)}</time>
          </span>
          {isAuthor && (
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => navigate(`/editor/${slug}`)}
                className="rounded border border-gray-300 px-2 py-1 text-xs text-gray-700 hover:bg-gray-50"
              >
                수정
              </button>
              <button
                type="button"
                onClick={() => setDeleteOpen(true)}
                className="rounded border border-red-300 px-2 py-1 text-xs text-red-600 hover:bg-red-50"
              >
                삭제
              </button>
            </div>
          )}
        </div>
      </header>

      <div className="whitespace-pre-wrap text-base text-gray-800">{article.body}</div>

      {article.tagList.length > 0 && (
        <ul className="flex flex-wrap gap-1">
          {article.tagList.map((tag) => (
            <li
              key={tag}
              className="rounded-full border border-gray-300 px-2 py-0.5 text-xs text-gray-600"
            >
              #{tag}
            </li>
          ))}
        </ul>
      )}

      <section className="space-y-3 border-t border-gray-200 pt-6">
        <h2 className="text-xl font-semibold">댓글 ({comments.length})</h2>
        {user ? (
          <form onSubmit={handleCommentSubmit} className="space-y-2">
            <textarea
              value={commentBody}
              onChange={(e) => setCommentBody(e.target.value)}
              rows={3}
              required
              placeholder="댓글을 입력하세요"
              className="w-full rounded border border-gray-300 px-3 py-2 text-sm focus:border-blue-600 focus:outline-none"
            />
            {commentError && (
              <div className="rounded border border-red-300 bg-red-50 px-3 py-2 text-sm text-red-600">
                {commentError}
              </div>
            )}
            <div className="flex justify-end">
              <button
                type="submit"
                disabled={submittingComment}
                className="rounded bg-blue-600 px-3 py-1.5 text-sm text-white hover:bg-blue-700 disabled:bg-blue-300"
              >
                {submittingComment ? "작성 중..." : "댓글 작성"}
              </button>
            </div>
          </form>
        ) : (
          <p className="text-sm text-gray-500">로그인하면 댓글을 작성할 수 있습니다.</p>
        )}
        {comments.length === 0 ? (
          <p className="text-sm text-gray-500">첫 댓글을 작성해 보세요.</p>
        ) : (
          <ul className="space-y-2">
            {comments.map((c) => (
              <li key={c.id}>
                <CommentItem
                  comment={c}
                  currentUsername={user?.username ?? null}
                  onUpdate={handleCommentUpdate}
                  onDelete={handleCommentDelete}
                />
              </li>
            ))}
          </ul>
        )}
      </section>

      <Modal
        open={deleteOpen}
        title="게시글 삭제"
        message="이 게시글을 삭제하시겠습니까? 관련 댓글도 함께 삭제됩니다."
        confirmLabel="삭제"
        onConfirm={handleArticleDelete}
        onCancel={() => setDeleteOpen(false)}
      />
    </article>
  );
}

function formatDate(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString("ko-KR", { year: "numeric", month: "2-digit", day: "2-digit" });
}
