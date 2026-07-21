from sprotect.crypto import derive_layer_key

def test_derive_layer_key_deterministic():
    mk = b"test_master_key_32_bytes_long!!"
    k1, s1 = derive_layer_key(mk, "sprotect:serpent")
    k2, s2 = derive_layer_key(mk, "sprotect:serpent")
    assert k1 == k2
    assert s1 == s2
    assert len(k1) == 32

def test_derive_layer_key_domain_sep():
    mk = b"test_master_key_32_bytes_long!!"
    k1, _ = derive_layer_key(mk, "sprotect:serpent")
    k2, _ = derive_layer_key(mk, "sprotect:twofish")
    assert k1 != k2


from sprotect.crypto_extra import (
    encrypt_serpent, decrypt_serpent,
    encrypt_twofish, decrypt_twofish,
    encrypt_camellia, decrypt_camellia,
    encrypt_salsa20, decrypt_salsa20,
)

def test_serpent_roundtrip():
    data = b"Hello Serpent AES!" * 100
    key = b"k" * 32
    iv = b"i" * 16
    ct = encrypt_serpent(data, key, iv)
    assert ct != data
    pt = decrypt_serpent(ct, key, iv)
    assert pt == data

def test_serpent_wrong_key():
    data = b"test data here!!"
    key = b"k" * 32
    iv = b"i" * 16
    ct = encrypt_serpent(data, key, iv)
    wrong = decrypt_serpent(ct, b"x" * 32, iv)
    assert wrong != data

def test_twofish_roundtrip():
    data = b"Hello Twofish CBC!" * 50
    key = b"t" * 32
    iv = b"i" * 16
    ct = encrypt_twofish(data, key, iv)
    assert ct != data
    pt = decrypt_twofish(ct, key, iv)
    assert pt == data

def test_camellia_roundtrip():
    data = b"Hello Camellia CBC!" * 50
    key = b"c" * 32
    iv = b"i" * 16
    ct = encrypt_camellia(data, key, iv)
    assert ct != data
    pt = decrypt_camellia(ct, key, iv)
    assert pt == data

def test_salsa20_roundtrip():
    data = b"Hello Salsa20 stream!" * 50
    key = b"s" * 32
    nonce = b"n" * 8
    ct = encrypt_salsa20(data, key, nonce)
    assert ct != data
    pt = decrypt_salsa20(ct, key, nonce)
    assert pt == data
