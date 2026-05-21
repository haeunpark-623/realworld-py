import re
import unicodedata
from typing import Protocol

_FALLBACK_SLUG = "article"
_NON_ALNUM = re.compile(r"[^a-z0-9]+")


class _SlugExistenceChecker(Protocol):
    async def exists_by_slug(self, slug: str) -> bool: ...


def slugify(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii").lower()
    kebab = _NON_ALNUM.sub("-", ascii_only).strip("-")
    return kebab or _FALLBACK_SLUG


async def unique_slug(repo: _SlugExistenceChecker, base: str) -> str:
    candidate = base
    counter = 2
    while await repo.exists_by_slug(candidate):
        candidate = f"{base}-{counter}"
        counter += 1
    return candidate
