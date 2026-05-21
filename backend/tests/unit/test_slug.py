import pytest

from realworld.utils.slug import slugify, unique_slug


def test_slugify_english_title_to_kebab() -> None:
    assert slugify("My First Article") == "my-first-article"


def test_slugify_special_chars_and_non_ascii() -> None:
    assert slugify("Hello, World! 안녕하세요") == "hello-world"


def test_slugify_empty_or_pure_non_ascii_falls_back() -> None:
    assert slugify("") == "article"
    assert slugify("한글만") == "article"


class _FakeRepo:
    def __init__(self, existing: set[str]) -> None:
        self._existing = existing

    async def exists_by_slug(self, slug: str) -> bool:
        return slug in self._existing


@pytest.mark.asyncio
async def test_unique_slug_returns_base_when_no_conflict() -> None:
    repo = _FakeRepo(existing=set())
    assert await unique_slug(repo, "my-post") == "my-post"


@pytest.mark.asyncio
async def test_unique_slug_progresses_through_suffix_on_conflict() -> None:
    repo = _FakeRepo(existing={"my-post", "my-post-2"})
    assert await unique_slug(repo, "my-post") == "my-post-3"
