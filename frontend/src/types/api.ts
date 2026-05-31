// RealWorld spec 응답 타입.

export type ProfileEmbed = {
  username: string;
  bio: string | null;
  image: string | null;
};

export type ErrorBody = {
  errors: {
    body: string[];
  };
};

export function isErrorBody(value: unknown): value is ErrorBody {
  if (typeof value !== "object" || value === null) return false;
  const errors = (value as { errors?: unknown }).errors;
  if (typeof errors !== "object" || errors === null) return false;
  const body = (errors as { body?: unknown }).body;
  return Array.isArray(body) && body.every((item) => typeof item === "string");
}

export function extractErrorMessage(value: unknown): string {
  if (isErrorBody(value) && value.errors.body.length > 0) {
    return value.errors.body[0];
  }
  return "알 수 없는 오류가 발생했습니다";
}

export type UserResponse = {
  user: {
    username: string;
    email: string;
    token: string;
    bio: string | null;
    image: string | null;
  };
};

export type ArticleView = {
  slug: string;
  title: string;
  description: string | null;
  body: string;
  tagList: string[];
  createdAt: string;
  updatedAt: string;
  author: ProfileEmbed;
};

export type ArticleResponse = {
  article: ArticleView;
};

export type ArticlesListResponse = {
  articles: ArticleView[];
  articlesCount: number;
};

export type CommentView = {
  id: number;
  body: string;
  createdAt: string;
  updatedAt: string;
  author: ProfileEmbed;
};

export type CommentResponse = {
  comment: CommentView;
};

export type CommentsListResponse = {
  comments: CommentView[];
};

export type TagsListResponse = {
  tags: string[];
};
