from app.core.security import decrypt_text, encrypt_text, hash_cpf


def test_fernet_roundtrip():
    token = encrypt_text("sensivel")
    assert token != "sensivel"
    assert decrypt_text(token) == "sensivel"


def test_cpf_hash_is_stable_and_not_plain():
    digest = hash_cpf("111.444.777-35", "salt")
    assert digest == hash_cpf("11144477735", "salt")
    assert "11144477735" not in digest
    assert len(digest) == 64
