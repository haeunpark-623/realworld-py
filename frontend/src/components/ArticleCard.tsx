// M-FE-Components ArticleCard — Issue #9.

import { Link } from "react-router-dom";

import type { ArticleView } from "../types/api";

type Props = {
  article: ArticleView;
};

export default function ArticleCard({ article }: Props) {
  return (
    <article className="rounded border border-gray-200 p-4 hover:shadow">
      <div className="mb-2 flex items-center gap-2 text-sm text-gray-500">
        <span className="font-medium text-gray-700">{article.author.username}</span>
        <span>·</span>
        <time dateTime={article.createdAt}>{formatDate(article.createdAt)}</time>
      </div>
      <Link to={`/article/${article.slug}`} className="block space-y-2">
        <h2 className="text-2xl font-semibold text-gray-900 hover:text-blue-600">{article.title}</h2>
        {article.description && <p className="text-gray-700">{article.description}</p>}
        {article.tagList.length > 0 && (
          <ul className="mt-2 flex flex-wrap gap-1">
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
      </Link>
    </article>
  );
}

function formatDate(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString("ko-KR", { year: "numeric", month: "2-digit", day: "2-digit" });
}
