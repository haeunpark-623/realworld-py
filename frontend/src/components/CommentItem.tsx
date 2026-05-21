// M-FE-Components CommentItem — Issue #9 (R-F-13 인라인 편집 P2 컷 후보, 본 PR 구현).

import { useState } from "react";

import type { CommentView } from "../types/api";

type Props = {
  comment: CommentView;
  currentUsername: string | null;
  onUpdate: (commentId: number, body: string) => Promise<void>;
  onDelete: (commentId: number) => Promise<void>;
};

export default function CommentItem({ comment, currentUsername, onUpdate, onDelete }: Props) {
  const isAuthor = currentUsername !== null && currentUsername === comment.author.username;
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(comment.body);
  const [submitting, setSubmitting] = useState(false);

  async function handleSave() {
    if (!draft.trim()) return;
    setSubmitting(true);
    try {
      await onUpdate(comment.id, draft);
      setEditing(false);
    } finally {
      setSubmitting(false);
    }
  }

  async function handleDelete() {
    setSubmitting(true);
    try {
      await onDelete(comment.id);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <article className="rounded border border-gray-200 p-3">
      {editing ? (
        <div className="space-y-2">
          <textarea
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            rows={3}
            className="w-full rounded border border-gray-300 px-2 py-1 text-sm focus:border-blue-600 focus:outline-none"
          />
          <div className="flex justify-end gap-2">
            <button
              type="button"
              onClick={() => {
                setEditing(false);
                setDraft(comment.body);
              }}
              className="rounded border border-gray-300 px-2 py-1 text-xs text-gray-700"
            >
              취소
            </button>
            <button
              type="button"
              onClick={handleSave}
              disabled={submitting}
              className="rounded bg-blue-600 px-2 py-1 text-xs text-white disabled:bg-blue-300"
            >
              저장
            </button>
          </div>
        </div>
      ) : (
        <>
          <p className="whitespace-pre-wrap text-sm text-gray-800">{comment.body}</p>
          <div className="mt-2 flex items-center justify-between text-xs text-gray-500">
            <span>
              {comment.author.username} ·{" "}
              <time dateTime={comment.createdAt}>{formatDate(comment.createdAt)}</time>
            </span>
            {isAuthor && (
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => setEditing(true)}
                  className="text-blue-600 hover:underline"
                >
                  수정
                </button>
                <button
                  type="button"
                  onClick={handleDelete}
                  disabled={submitting}
                  className="text-red-600 hover:underline disabled:text-red-300"
                >
                  삭제
                </button>
              </div>
            )}
          </div>
        </>
      )}
    </article>
  );
}

function formatDate(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString("ko-KR", { year: "numeric", month: "2-digit", day: "2-digit" });
}
