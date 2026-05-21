from realworld.utils.security import hash_password, verify_password


def test_hash_password_starts_with_bcrypt_marker() -> None:
    hashed = hash_password("correct horse battery staple")
    assert hashed.startswith("$2b$12$")


def test_verify_password_returns_true_for_match() -> None:
    plain = "correct horse battery staple"
    hashed = hash_password(plain)
    assert verify_password(plain, hashed) is True


def test_verify_password_returns_false_for_mismatch() -> None:
    hashed = hash_password("correct horse battery staple")
    assert verify_password("wrong password", hashed) is False
