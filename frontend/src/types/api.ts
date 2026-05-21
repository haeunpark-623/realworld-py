// RealWorld spec 응답 타입 placeholder. 실 사용은 I-08·I-09.

export type ProfileEmbed = {
  username: string;
  bio: string | null;
  image: string | null;
};

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
