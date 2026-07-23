import os
from sprotect.crypto import derive_layer_key

def _key32(): return os.urandom(32)
def _iv16(): return os.urandom(16)

def test_derive_layer_key_deterministic():
    mk = _key32()
    k1, s1 = derive_layer_key(mk, "sprotect:serpent")
    k2, s2 = derive_layer_key(mk, "sprotect:serpent")
    assert k1 == k2
    assert s1 == s2
    assert len(k1) == 32

def test_derive_layer_key_domain_sep():
    mk = _key32()
    k1, _ = derive_layer_key(mk, "sprotect:serpent")
    k2, _ = derive_layer_key(mk, "sprotect:twofish")
    assert k1 != k2


from sprotect.crypto_extra import (
    encrypt_aes_cbc_1, decrypt_aes_cbc_1,
    encrypt_aes_cbc_2, decrypt_aes_cbc_2,
    encrypt_aes_cbc_3, decrypt_aes_cbc_3,
    encrypt_salsa20, decrypt_salsa20,
)

def test_aes_cbc_1_roundtrip():
    data = b"Hello AES-CBC layer1!" * 100
    key = _key32()
    iv = _iv16()
    ct = encrypt_aes_cbc_1(data, key, iv)
    assert ct != data
    pt = decrypt_aes_cbc_1(ct, key, iv)
    assert pt == data

def test_aes_cbc_1_wrong_key():
    data = b"test data here!!"
    key = _key32()
    iv = _iv16()
    ct = encrypt_aes_cbc_1(data, key, iv)
    wrong = decrypt_aes_cbc_1(ct, _key32(), iv)
    assert wrong != data

def test_aes_cbc_2_roundtrip():
    data = b"Hello AES-CBC layer2!" * 50
    key = _key32()
    iv = _iv16()
    ct = encrypt_aes_cbc_2(data, key, iv)
    assert ct != data
    pt = decrypt_aes_cbc_2(ct, key, iv)
    assert pt == data

def test_aes_cbc_3_roundtrip():
    data = b"Hello AES-CBC layer3!" * 50
    key = _key32()
    iv = _iv16()
    ct = encrypt_aes_cbc_3(data, key, iv)
    assert ct != data
    pt = decrypt_aes_cbc_3(ct, key, iv)
    assert pt == data

def test_salsa20_roundtrip():
    data = b"Hello Salsa20 stream!" * 50
    key = _key32()
    nonce = os.urandom(8)
    ct = encrypt_salsa20(data, key, nonce)
    assert ct != data
    pt = decrypt_salsa20(ct, key, nonce)
    assert pt == data


from sprotect.crypto import encrypt_payload_v2, decrypt_payload_v2

def test_encrypt_payload_v2_no_extra():
    data = b"test source code here"
    key = _key32()
    ct, hdr = encrypt_payload_v2(data, key, [])
    assert "version" in hdr
    assert hdr["extra_layers"] == []
    pt = decrypt_payload_v2(ct, key, hdr)
    assert pt == data

def test_encrypt_payload_v2_with_serpent():
    data = b"test source with serpent" * 100
    key = _key32()
    ct, hdr = encrypt_payload_v2(data, key, ["serpent"])
    assert "serpent" in hdr["layer_ivs"]
    pt = decrypt_payload_v2(ct, key, hdr)
    assert pt == data

def test_encrypt_payload_v2_all_layers():
    data = b"test source ALL layers" * 200
    key = _key32()
    ct, hdr = encrypt_payload_v2(data, key, ["serpent", "twofish", "camellia", "salsa20"])
    for algo in ["serpent", "twofish", "camellia", "salsa20"]:
        assert algo in hdr["layer_ivs"]
    pt = decrypt_payload_v2(ct, key, hdr)
    assert pt == data


from sprotect.decrypt import encrypt_to_pye, decrypt_from_pye

def test_pye_v2_header_roundtrip():
    data = b"def foo(): pass"
    key = _key32()
    pye = encrypt_to_pye(data, key, ["serpent"])
    pt = decrypt_from_pye(pye)
    assert pt == data

def test_pye_v2_no_extra_roundtrip():
    data = b"print('hello')" * 50
    key = _key32()
    pye = encrypt_to_pye(data, key, [])
    pt = decrypt_from_pye(pye)
    assert pt == data


from sprotect.crypto import (
    rsa_generate_keypair, rsa_encrypt_master_key, rsa_decrypt_master_key,
    ecc_generate_keypair, ecc_encrypt_master_key, ecc_decrypt_master_key,
)

def test_rsa_roundtrip():
    mk = _key32()
    pub, priv = rsa_generate_keypair(2048)
    enc = rsa_encrypt_master_key(mk, pub)
    dec = rsa_decrypt_master_key(enc, priv)
    assert dec == mk

def test_rsa_passphrase():
    mk = _key32()
    pub, priv = rsa_generate_keypair(2048, "test123")
    enc = rsa_encrypt_master_key(mk, pub)
    dec = rsa_decrypt_master_key(enc, priv, "test123")
    assert dec == mk

def test_ecc_roundtrip():
    mk = _key32()
    pub, priv = ecc_generate_keypair("P-256")
    enc = ecc_encrypt_master_key(mk, pub)
    dec = ecc_decrypt_master_key(enc, priv)
    assert dec == mk
