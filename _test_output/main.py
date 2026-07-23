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
__vf944d29d = 1172538154
__r7e238b2a = 3816192950
__xba883632 = b'f259467fa576e992a666ebe81a0aa6af61a20be13c208efebcaa387fedb52d53d6ace9e8816f02c932a47f19c53d72df58c5129d3d1787103a535f8c5a27cfb37a419aa7f260bd0b0127a7fba44ada4c152ddd4404eff70a5e35f94f0437be149033dbd917a6de075ce33047d7b49cd442da0a6968eaa11fb92ad4f6e13db01b3e11edc7210eecd726f35dd17a266b74c6a23c13'
__p8746585f = 2992907
__m39d292af = 50205734343851395
__c3ae97391 = 'cfb2b091fdf90eddbffae12848a84bff2f68ed130d15689b077f897e11832b0a0c1cea08502e08522d064c7351f34d0539a31fc17f5e6855ef5f08d75eb233ac23ca2622883a8a67ccfda446244f73dc639894ebc62dc27b99bd45d336438f6206398490c4644fcf49cabc306f5d6b1bf8af13d4e4532731cdc7e051f556368a5d2e8c46794e04919cdc61e71d56'
__ka053c963 = b'b4ab618425e66e4fbe2093d0f7f3a018ce116a39c3fc7fd3bbaa00d6c80d62456aa4fda41ed670742ba42db4214bce2984ef32f7b54c6951860e'
__va8eed3c8 = b'dfd4a79c360aebdabf46ac6c4f913a59f908db86fab69ee08c873ea27aa7567705c3333b8efbc3c6e4f38d2cc8bffaf6fcea245faad3ab8ab753c9a41cf4a52cefcbeddd59213ea9f33f28de5c89470cccc8b1e789e64535f2581e5760d3f21356ffcb39'
__v06b585a2 = b'94959e0d5ffa478753500a14789b009b001c4b51a6f610b1ef55e51bcc75401530f6ad47bcdad5a727e4cf86d621c9a44bd256b2968dc801c370b22b140b656059dec5c08ecead8fe660ff968e7545fb315ae60882f7a1fab3982d3a1550baa8fd3759'
__nd464a603 = b'632d67fec5a47c6f474f12dc03f567f298286c1584b88543d2a0ec3543fb44c68f49484efb1340dede23ef2d5af5f854869662d2dfb6c416cabff407341bb748344ad7836fc181d47f7b2a7f8dbde7036761004ae2e9778835008d4fd2bc6ac6126af7b7ce9f9d3432a343f5'
__pa6ce690b = '2576777d39cf7a8dd299bcf71ad411a76dc419fe4e663df6b53428746084f738d71d109404227f94f27e36e555696bff4274361e72af87d8fd183eabbfc0ea0fb705a29b3e1a4dd9d295ec5a29128950bdb66055eabe3dc9983ef571ed300e68866c106768df45dabd2b17f2aa5f88657dde378c92e9153702255bfca6b83b19f9dbe5994916366f9fff525af98b083ce365809d0a4084b44dd322d131726dea4d704561f421182634a40272db04ad18545c2e575b29b10d692e9f24cc1b06e22301d9e3525c6f6ab1a0835a53379583fd2bfaa2a344123e4c267e88e55056f6f188e81a048bbefc4e086c9c65ec3c902e995d2f78cdf7f35b41e246a6f6b8c21b6bfadc'
__sc392214d = 42580
__w8f0e3fd2 = 3062193498
__x9738bd9b = 3284201307593103983479
__r9a00da67 = 'e1189ce5d806c8f0f7b23a7ffd7fae8146209f6fad1a5406a9e9e32fa28dbfdf1ea438d293e26d34302ff4d494be06e55b0b5d4023a8715bfd0ca30c77ceb4ef09367227fabde1d49b0b79ca483b9ccbcc54bf7450b18bda6a8ad509f292c147a40a2883b3eb5ffad6f24453606cca54ed7809c0dd9530c02af33bfdaaf59843f32e2299d7b97a542adb1b2cf9c302177ed06e5cc641b6323ddb0c4a4fd1'
__n96eae077 = 'e4ff252b2a3d1656f943c8358f4bed5b30bacf30c88226fe6f1cb268b00c7125f0f917da796a817b17566115dec48d1fd600d7690877ceed9682b99a98cc70ad3b82f996a044d2b261491f095dbb593cda0422405a789aaad45f3037043809a86aab8efc2be9f51a363d5ffd6d2e21cb30f74a95aa29c9f1b4052b'
__b5b305d31 = 959156177540
__m5ca338ef = 3746793513
__c8cf7869a = '6fae597fd9d5f970d75c5732b737e881cfbb9e455136a621cb13c1cde4d17352dfae18dc596ee2b9343ae643d3313d88e9f4fc467109393c3360d2e320c8c6b986fbe30a40835124bca8e374bf4fdc6671f72230933f8bca9ce67f5eb916a227477ae05f1c002f6c59d8aaeb37d45a90f76797e7f3a6419b3d1afdd8df94fa7ee6e6f2c45f6a508a3892ebb1e0ca6a4beb7688f816d15ba5f4a0530d5716e2b5ba34541049c0e5ab3876049adcdb2bf17990c5a1afcebe0ed8739daca2754b6e75cfb08862777819515fbc2be3fe1a75eb6a722d17b3d436b6aa17a89855498fd178450c62cd6152c5e840a0ef7d305170fb60a2b59b4ce7a5b775413e20e6bcc39770ac54946a98852b67edfaaf2985b1e6a19a'
__d64ced77f = 3868170222
__k8fa65475 = 103216775654301
__m818c6b66 = 541200059
__m8df6e366 = 1408280879
__f3e429f19 = '3e6a9ce1fc7fec65e645acdb17897d95bf9fb118cb52824f8e0363a1a832d896b56bb69c4c294dde2ae7a934cd4d5fb970ced6d24f7e539e8d6ea24dd8068e9ac52de18868556eb27be9a90ba8c5a192a2e9cbd194c133d13e64da354fef40574b7620f1a7cd9ba484544424daa84279a7f8d7335c3077d3b9cdb0edd92a51406fba5e9cea1d1b597ee9b169552cc2a8ade1757239d7ded57b0b186d68ec70e1d25ff545b5b0933784bf88a154a27d937bad7cca8be4e33025b48ca79636203674bb39594464b8d1'
__z2fa02528 = 'b0d5a9778ac59c5808b8a8c5648afb2463fb7b9c58084729309ec8a4426f3c9d547109cf1501948bd441adf997f92ae0d21fa4d6cc7d7cffe8da8bca2b55e71166d48a6802e64d45f33e51ea93b76fe46591ed294aed4fc6881b0fe3092a55f80f81afb38199d120886bddbe776a37f7f6566f63762b986d9d5d4b92c1f6d62fef9489d11d28047716c79fbd507611fea247785af089c49a43b27d5633dfc9c593fb3c1e1f65c9a8ee31731520f7f4543f12ed7638510516ae6cc44eea1a07e635810716ce8f9fa31ddec61cc4aa0df9571b9943db488adb57eb36eeeeba7c437c68d5b2'
__w353e7902 = 3500747363
__kaaf47d3e = '00dd40a7736f7b787f5907f4d474d0c71c710db0ceebcb4c368d9d281362541b8c5730c4a3bf3ae3bf8e1f0b98dc0ffa9beef407ae80e9bd837b0c6e1b2786fa1edc3590321b34a1c1b941779a46befc5fddfd2b92c44b328327eb121f5ab8b097b923c8d77a573ecaa4aeb5d73d599e5150a4534a4a5d784e50b1f241825fa82315e935e512bd1cbaf7b4a29022aa61405ef9dba53f339866749c3f338a93abddf2505ac85ad9b90863f563caa445d5a344bfe330889cf4'
__d9c60b091 = 37281270525890430
__ca7f48f8a = 12740397
__yc73dc16f = 2675346790314111458354
__0x249fb0c9db = 43309201
__yf6f8dfc7 = 647094565782
__z9f4576e9 = 68150449072214
__k61f32150 = 996413774
__y0528129e = 2384575574
__kab049be0 = 'b1dff144059327e5d5d6d8cfdff7bd8faf10a092f80cc45392b60fe1cf145a5d7c908df02f03a0a0c0a84995fd9b8a732532383b1819dad27f18cbf56155a7000f3405de92a51c6f4a3d00ce2a0e3c2efb1a3974be9c076d5184d8b9e736b38f25127d016be0d473bf05ac45e0b5e43b094a82c2125612248aae'
__q2b212e21 = 'b011d912f4a2c9fd4a366063b1fe3597fd690ba26a5ecff155b2df43ac13822159e432e9e165f2136458ea2c3f7d6209a785f96caa458e963ebd40b106ac1f3b2d6ab9ed8cc52a3193a5c99d4daffcf55ef2248f93b892f9c4bc173b2f757fb1e0b350d43fedfa96e8ed122ff902de24f6cc4666215ed94bb3d9086fc80a9eae16fa27fce0702888334e2b7adc4d055cda470e340da206b0119efa6982d4d7c97587f243c92a2b795a172372f325c8dee829a6a1e81c998bb519ffd055d2'
__pe51c7a78 = 9725703214107907236
__aa88ecd05 = 4153546555
__c62c98fb5 = 3903766714
__s7cf950b6 = '4326f53d02f13ccf3c7bf3944679c2024408d5afa4e8dac19e65bba7f00ef472cf8db1b308160eb75185bc815d9697bc5ffb168e13f4b5b47ba7581c54fc84174daeb2e38f3702e2ab30760c9078ea2bbd60ad90feff5adb38c09031233f66bd23a063ce535d1037aba9e88adf8560c5039bd675bd7c4e7003e10a9fb8ff7241c1b3b18ff92291a17297c0457a76c5e5532b'
__v774b8bd1 = b'2c50f2bc6c6aa42c160f08d4aeef36fa26182779ba44bb5a4e95765adc6c088140a231444a8b2ed51e802345d029b41da686eb8af1436a361b47248afa284112b5653f3a076ad9b0ff41fad5b06a9d1a60cf14016223056af52c4d79d15414f7020cab04cfec9b1e559a1a'
__wfa6f32f6 = b'b82418ced519a9ad2f74f043ae52c56e47f688841e1b5df06328573e129128a2751e8bc626d05776878cc02093d4304aed147a657a6b43950e39c51921d636000abee2a8373a3dcd5312c4a09f3f977a1e9a974dc9c71576a257e8e0815ef4647e7ec760876d6c97a74c9182f3f1f9b5e6fa0ff56e5e3e3cd4ee3e1caf4df72012e0c1f89bd7d1568b5f7d3cc15ff4e19a950a'
__s86ce5576 = 50570082230544
__n78cd29f0 = 703119017
__xe108ec81 = 1296243975
__k63fb139b = b'c4e773b94ce666c411ef1d95d697d6d7b6b1682ca3ff4b55adbc56106d415b60f6948b332f7ee60fd51012dd28347896241b'
__a8e7e0a54 = b'e5cd6b7481e25b051be3cba6ec17edaed62b8e26fbbbbe2a0b96afa18e810f1ba46589ae5c079ed3aed91a8e3a5653e3ed2410f3bf398663549c6dea59e4921c92cfa3c409183bc4af32bed6f00bc7f99698d9c7f4dc9cf59e5250078d407d2b7a93793f37646cf6ce0f25'
__sc6c41287 = '342eddc8e53d6101d18e6935fd8bd1aeb498ac30645e0213c31bd16b80829cdd791b034928606e42a7fc62162dc055ec7bc577a2290284d474cef7c451867db67ac42655e330f4dbed313cd86ad5f133de52a0720cd96a1aeb1f756ec51f0d66e29fb0f636dd9d9c44381666cb969a1426c47b95c44bbe4af7e3d2e5eac7d0aa743b22ca9390ad8189a1a0db9bb91b59b14643c9e42110a62c53ad71b8dec266dc4c7797efab899d248f1029ea99400daa188774574ea6b0abb9242606bdd581db27fe16286a1af0761e0d70a751'
__p9e441387 = 3990069117
__e04c0c2ba = 3428477694
__xd2d2f0a1 = '56b71074be23484a04cfaebcbb55df1c35aa297bd52f2a5bdbbeaa03f854e27dd2db88f4b3f937e14ef17f513b7b0c2587c796f7c19ad3f240931a8b60ebe50046ad99499cd4761b23afa5813622c0a0c5a3bee9c42e4a5710524053c739a2bf4f9562e5b89f010e4622ede42dbaf1c060f58fdb21f777436134c8081127d07b827b39c603f2098848e85f265a5aed22d5737f251b6c997603e41249631ec408ba05b4a3a361a173a3f4311693d2f9d14c2f8b92c43bd29ba20c4e2968f0b05d453e23677ad039c52f57b1cf76341737ee3468561308a32889c6467ca5f38c99856eafe922bb32f28400bdd36ace0a342d734933551439e4a679146d55a5c277'
_nd014f0e3 = '0aa23f65ac27'
_y5ef0d757 = 'aeb3074080486'
_bf78939e0 = 'a924bcfc86f5f'
_d2ea536ee = '0354fb4243342'
_q9675e29a = '71b00044028e0'
_p4b6e5fc3 = 'f3c5766f79304fca68ffede2'
_f3e199509 = 'cb4bf294956c9d34fe24716618'
_qc67f103b = 'fc6e5460fcb2e4bd8f1923b8c4'
_k06ecbbeb = '514219fd15d782b50552d0fc63'
_y2aa3252d = 'cecee7b3403c2f00c7df99fbbf'
'Module loader.'
import sys, os, json, hashlib, zlib, hmac
sys.dont_write_bytecode = True
_3c5adfaf1983 = getattr(sys, '_MEIPASS', None) or os.path.dirname(os.path.abspath(__file__))

def _6111d10545(_t406e19ba, __b45f76bedf09):
    _m29841e30a1, _c35bb95043d3d2 = (bytearray(), 0)
    while len(_m29841e30a1) < _t406e19ba:
        _m29841e30a1.extend(hashlib.sha256(__b45f76bedf09 + _c35bb95043d3d2.to_bytes(4, 'big')).digest())
        _c35bb95043d3d2 += 1
    return bytes(_m29841e30a1[:_t406e19ba])

def _fe(_41c5f815b87610):
    _v5096_dc6e = {}
    for _tff36a5946a in range(1, 6):
        _v5462_4573 = f'k{_tff36a5946a}'
        if _v5462_4573 in _41c5f815b87610:
            _v5096_dc6e[_v5462_4573] = bytes.fromhex(_41c5f815b87610[_v5462_4573])
    if not _v5096_dc6e:
        return b''
    _3e93eb52cb0091 = bytearray(32)
    for _h2988 in _v5096_dc6e.values():
        for _tff36a5946a in range(min(32, len(_h2988))):
            _3e93eb52cb0091[_tff36a5946a] ^= _h2988[_tff36a5946a]
    _q4a6754_2 = hashlib.sha256(bytes(_3e93eb52cb0091)).hexdigest()[5:13] == _41c5f815b87610.get('f1', '')
    for _v5462_4573, _td95e9d5a31 in _v5096_dc6e.items():
        try:
            import blake3 as _b3
            _a602 = _b3.blake3(_td95e9d5a31).hexdigest()[3:11] == _41c5f815b87610.get('f2', '')
        except:
            _a602 = hashlib.sha256(b'f2-domain:' + _td95e9d5a31).hexdigest()[8:16] == _41c5f815b87610.get('f2', '')
        _e60703271a212f = hmac.new(_td95e9d5a31, b'S-Protect-v6-key-verify', 'sha256').hexdigest()[:8] == _41c5f815b87610.get('f3', '')
        if _q4a6754_2 and _a602 and _e60703271a212f:
            return _td95e9d5a31
    return b''
_92701_a93a35 = [_nd014f0e3, _y5ef0d757, _bf78939e0, _d2ea536ee, _q9675e29a, _p4b6e5fc3, _f3e199509, _qc67f103b, _k06ecbbeb, _y2aa3252d]

def _0xe200cab4():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    _cdd6ee6f648 = bytes.fromhex(''.join((_92701_a93a35[_tff36a5946a] for _tff36a5946a in [0, 1, 2, 3, 4])))
    _41c5f815b87610 = json.loads(open(os.path.join(_3c5adfaf1983, '_runtime', 'loader.pye'), 'rb').read().decode())
    _x6c0efebe4dbe = _fe(_41c5f815b87610) or _cdd6ee6f648
    _pb9f974_b = bytes.fromhex(_41c5f815b87610['d'])
    _r51641 = AESGCM(_x6c0efebe4dbe).decrypt(_pb9f974_b[:12], _pb9f974_b[12:], b'')
    _r51641 = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_r51641, _6111d10545(len(_r51641), _x6c0efebe4dbe))))
    try:
        _r51641 = ChaCha20Poly1305(_x6c0efebe4dbe).decrypt(_r51641[:12], _r51641[12:], b'')
    except Exception:
        pass
    return zlib.decompress(_r51641).decode()

def _c8052bab2():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    _cdd6ee6f648 = bytes.fromhex(''.join((_92701_a93a35[_tff36a5946a] for _tff36a5946a in [0, 1, 2, 3, 4])))
    _41c5f815b87610 = json.loads(open(os.path.join(_3c5adfaf1983, '_runtime', 'loader.pye'), 'rb').read().decode())
    _x6c0efebe4dbe = _fe(_41c5f815b87610) or _cdd6ee6f648
    _pb9f974_b = bytes.fromhex(_41c5f815b87610['d'])
    _r51641 = AESGCM(_x6c0efebe4dbe).decrypt(_pb9f974_b[:12], _pb9f974_b[12:], b'')
    _r51641 = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_r51641, _6111d10545(len(_r51641), _x6c0efebe4dbe))))
    try:
        _r51641 = ChaCha20Poly1305(_x6c0efebe4dbe).decrypt(_r51641[:12], _r51641[12:], b'')
    except Exception:
        pass
    return zlib.decompress(_r51641).decode()
_51587 = compile(_c8052bab2(), '', 'exec')
exec(_51587)
run('main', _3c5adfaf1983)

def _f77bf5cc4():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib, hmac
    try:
        _cdd6ee6f648 = bytes.fromhex(''.join(([_nd014f0e3, _y5ef0d757, _bf78939e0, _d2ea536ee, _q9675e29a, _p4b6e5fc3, _f3e199509, _qc67f103b, _k06ecbbeb, _y2aa3252d][_tff36a5946a] for _tff36a5946a in [9, 7, 3])))
        _41c5f815b87610 = json.loads(open(os.path.join(_3c5adfaf1983, '_runtime', 'loader.pye'), 'rb').read().decode())
        _x6c0efebe4dbe = _cdd6ee6f648
        _v5096_dc6e = {}
        for _tff36a5946a in range(1, 6):
            _v5462_4573 = f'k{_tff36a5946a}'
            if _v5462_4573 in _41c5f815b87610:
                _v5096_dc6e[_v5462_4573] = bytes.fromhex(_41c5f815b87610[_v5462_4573])
        if _v5096_dc6e:
            _3e93eb52cb0091 = bytearray(32)
            for _h2988 in _v5096_dc6e.values():
                for _tff36a5946a in range(min(32, len(_h2988))):
                    _3e93eb52cb0091[_tff36a5946a] ^= _h2988[_tff36a5946a]
            _q4a6754_2 = hashlib.sha256(bytes(_3e93eb52cb0091)).hexdigest()[5:13] == _41c5f815b87610.get('f1', '')
            for _v5462_4573, _td95e9d5a31 in _v5096_dc6e.items():
                try:
                    import blake3 as _b3
                    _a602 = _b3.blake3(_td95e9d5a31).hexdigest()[3:11] == _41c5f815b87610.get('f2', '')
                except:
                    _a602 = hashlib.sha256(b'f2-domain:' + _td95e9d5a31).hexdigest()[8:16] == _41c5f815b87610.get('f2', '')
                _e60703271a212f = hmac.new(_td95e9d5a31, b'S-Protect-v6-key-verify', 'sha256').hexdigest()[:8] == _41c5f815b87610.get('f3', '')
                if _q4a6754_2 and _a602 and _e60703271a212f:
                    _x6c0efebe4dbe = _td95e9d5a31
                    break
        _pb9f974_b = bytes.fromhex(_41c5f815b87610['d'])
        _r51641 = AESGCM(_x6c0efebe4dbe).decrypt(_pb9f974_b[:12], _pb9f974_b[12:], b'')
        _r51641 = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_r51641, _6111d10545(len(_r51641), _x6c0efebe4dbe))))
        _r51641 = ChaCha20Poly1305(_x6c0efebe4dbe).decrypt(_r51641[:12], _r51641[12:], b'')
        _m29841e30a1 = zlib.decompress(_r51641)
    except Exception:
        _m29841e30a1 = b''
    return _m29841e30a1

def _z02ad2eb2():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib, hmac
    try:
        _cdd6ee6f648 = bytes.fromhex(''.join(([_nd014f0e3, _y5ef0d757, _bf78939e0, _d2ea536ee, _q9675e29a, _p4b6e5fc3, _f3e199509, _qc67f103b, _k06ecbbeb, _y2aa3252d][_tff36a5946a] for _tff36a5946a in [1, 1, 4, 8])))
        _41c5f815b87610 = json.loads(open(os.path.join(_3c5adfaf1983, '_runtime', 'loader.pye'), 'rb').read().decode())
        _x6c0efebe4dbe = _cdd6ee6f648
        _v5096_dc6e = {}
        for _tff36a5946a in range(1, 6):
            _v5462_4573 = f'k{_tff36a5946a}'
            if _v5462_4573 in _41c5f815b87610:
                _v5096_dc6e[_v5462_4573] = bytes.fromhex(_41c5f815b87610[_v5462_4573])
        if _v5096_dc6e:
            _3e93eb52cb0091 = bytearray(32)
            for _h2988 in _v5096_dc6e.values():
                for _tff36a5946a in range(min(32, len(_h2988))):
                    _3e93eb52cb0091[_tff36a5946a] ^= _h2988[_tff36a5946a]
            _q4a6754_2 = hashlib.sha256(bytes(_3e93eb52cb0091)).hexdigest()[5:13] == _41c5f815b87610.get('f1', '')
            for _v5462_4573, _td95e9d5a31 in _v5096_dc6e.items():
                try:
                    import blake3 as _b3
                    _a602 = _b3.blake3(_td95e9d5a31).hexdigest()[3:11] == _41c5f815b87610.get('f2', '')
                except:
                    _a602 = hashlib.sha256(b'f2-domain:' + _td95e9d5a31).hexdigest()[8:16] == _41c5f815b87610.get('f2', '')
                _e60703271a212f = hmac.new(_td95e9d5a31, b'S-Protect-v6-key-verify', 'sha256').hexdigest()[:8] == _41c5f815b87610.get('f3', '')
                if _q4a6754_2 and _a602 and _e60703271a212f:
                    _x6c0efebe4dbe = _td95e9d5a31
                    break
        _pb9f974_b = bytes.fromhex(_41c5f815b87610['d'])
        _r51641 = AESGCM(_x6c0efebe4dbe).decrypt(_pb9f974_b[:12], _pb9f974_b[12:], b'')
        _r51641 = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_r51641, _6111d10545(len(_r51641), _x6c0efebe4dbe))))
        _r51641 = ChaCha20Poly1305(_x6c0efebe4dbe).decrypt(_r51641[:12], _r51641[12:], b'')
        _m29841e30a1 = zlib.decompress(_r51641)
    except Exception:
        _m29841e30a1 = b''
    return _m29841e30a1

def _maece3625():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib, hmac
    try:
        _cdd6ee6f648 = bytes.fromhex(''.join(([_nd014f0e3, _y5ef0d757, _bf78939e0, _d2ea536ee, _q9675e29a, _p4b6e5fc3, _f3e199509, _qc67f103b, _k06ecbbeb, _y2aa3252d][_tff36a5946a] for _tff36a5946a in [8, 3, 5, 0])))
        _41c5f815b87610 = json.loads(open(os.path.join(_3c5adfaf1983, '_runtime', 'loader.pye'), 'rb').read().decode())
        _x6c0efebe4dbe = _cdd6ee6f648
        _v5096_dc6e = {}
        for _tff36a5946a in range(1, 6):
            _v5462_4573 = f'k{_tff36a5946a}'
            if _v5462_4573 in _41c5f815b87610:
                _v5096_dc6e[_v5462_4573] = bytes.fromhex(_41c5f815b87610[_v5462_4573])
        if _v5096_dc6e:
            _3e93eb52cb0091 = bytearray(32)
            for _h2988 in _v5096_dc6e.values():
                for _tff36a5946a in range(min(32, len(_h2988))):
                    _3e93eb52cb0091[_tff36a5946a] ^= _h2988[_tff36a5946a]
            _q4a6754_2 = hashlib.sha256(bytes(_3e93eb52cb0091)).hexdigest()[5:13] == _41c5f815b87610.get('f1', '')
            for _v5462_4573, _td95e9d5a31 in _v5096_dc6e.items():
                try:
                    import blake3 as _b3
                    _a602 = _b3.blake3(_td95e9d5a31).hexdigest()[3:11] == _41c5f815b87610.get('f2', '')
                except:
                    _a602 = hashlib.sha256(b'f2-domain:' + _td95e9d5a31).hexdigest()[8:16] == _41c5f815b87610.get('f2', '')
                _e60703271a212f = hmac.new(_td95e9d5a31, b'S-Protect-v6-key-verify', 'sha256').hexdigest()[:8] == _41c5f815b87610.get('f3', '')
                if _q4a6754_2 and _a602 and _e60703271a212f:
                    _x6c0efebe4dbe = _td95e9d5a31
                    break
        _pb9f974_b = bytes.fromhex(_41c5f815b87610['d'])
        _r51641 = AESGCM(_x6c0efebe4dbe).decrypt(_pb9f974_b[:12], _pb9f974_b[12:], b'')
        _r51641 = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_r51641, _6111d10545(len(_r51641), _x6c0efebe4dbe))))
        _r51641 = ChaCha20Poly1305(_x6c0efebe4dbe).decrypt(_r51641[:12], _r51641[12:], b'')
        _m29841e30a1 = zlib.decompress(_r51641)
    except Exception:
        _m29841e30a1 = b''
    return _m29841e30a1

def _z4a321fc1():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib, hmac
    try:
        _cdd6ee6f648 = bytes.fromhex(''.join(([_nd014f0e3, _y5ef0d757, _bf78939e0, _d2ea536ee, _q9675e29a, _p4b6e5fc3, _f3e199509, _qc67f103b, _k06ecbbeb, _y2aa3252d][_tff36a5946a] for _tff36a5946a in [3, 3, 9, 4, 0])))
        _41c5f815b87610 = json.loads(open(os.path.join(_3c5adfaf1983, '_runtime', 'loader.pye'), 'rb').read().decode())
        _x6c0efebe4dbe = _cdd6ee6f648
        _v5096_dc6e = {}
        for _tff36a5946a in range(1, 6):
            _v5462_4573 = f'k{_tff36a5946a}'
            if _v5462_4573 in _41c5f815b87610:
                _v5096_dc6e[_v5462_4573] = bytes.fromhex(_41c5f815b87610[_v5462_4573])
        if _v5096_dc6e:
            _3e93eb52cb0091 = bytearray(32)
            for _h2988 in _v5096_dc6e.values():
                for _tff36a5946a in range(min(32, len(_h2988))):
                    _3e93eb52cb0091[_tff36a5946a] ^= _h2988[_tff36a5946a]
            _q4a6754_2 = hashlib.sha256(bytes(_3e93eb52cb0091)).hexdigest()[5:13] == _41c5f815b87610.get('f1', '')
            for _v5462_4573, _td95e9d5a31 in _v5096_dc6e.items():
                try:
                    import blake3 as _b3
                    _a602 = _b3.blake3(_td95e9d5a31).hexdigest()[3:11] == _41c5f815b87610.get('f2', '')
                except:
                    _a602 = hashlib.sha256(b'f2-domain:' + _td95e9d5a31).hexdigest()[8:16] == _41c5f815b87610.get('f2', '')
                _e60703271a212f = hmac.new(_td95e9d5a31, b'S-Protect-v6-key-verify', 'sha256').hexdigest()[:8] == _41c5f815b87610.get('f3', '')
                if _q4a6754_2 and _a602 and _e60703271a212f:
                    _x6c0efebe4dbe = _td95e9d5a31
                    break
        _pb9f974_b = bytes.fromhex(_41c5f815b87610['d'])
        _r51641 = AESGCM(_x6c0efebe4dbe).decrypt(_pb9f974_b[:12], _pb9f974_b[12:], b'')
        _r51641 = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_r51641, _6111d10545(len(_r51641), _x6c0efebe4dbe))))
        _r51641 = ChaCha20Poly1305(_x6c0efebe4dbe).decrypt(_r51641[:12], _r51641[12:], b'')
        _m29841e30a1 = zlib.decompress(_r51641)
    except Exception:
        _m29841e30a1 = b''
    return _m29841e30a1

def _w9d7aad09():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib, hmac
    try:
        _cdd6ee6f648 = bytes.fromhex(''.join(([_nd014f0e3, _y5ef0d757, _bf78939e0, _d2ea536ee, _q9675e29a, _p4b6e5fc3, _f3e199509, _qc67f103b, _k06ecbbeb, _y2aa3252d][_tff36a5946a] for _tff36a5946a in [7, 4, 7])))
        _41c5f815b87610 = json.loads(open(os.path.join(_3c5adfaf1983, '_runtime', 'loader.pye'), 'rb').read().decode())
        _x6c0efebe4dbe = _cdd6ee6f648
        _v5096_dc6e = {}
        for _tff36a5946a in range(1, 6):
            _v5462_4573 = f'k{_tff36a5946a}'
            if _v5462_4573 in _41c5f815b87610:
                _v5096_dc6e[_v5462_4573] = bytes.fromhex(_41c5f815b87610[_v5462_4573])
        if _v5096_dc6e:
            _3e93eb52cb0091 = bytearray(32)
            for _h2988 in _v5096_dc6e.values():
                for _tff36a5946a in range(min(32, len(_h2988))):
                    _3e93eb52cb0091[_tff36a5946a] ^= _h2988[_tff36a5946a]
            _q4a6754_2 = hashlib.sha256(bytes(_3e93eb52cb0091)).hexdigest()[5:13] == _41c5f815b87610.get('f1', '')
            for _v5462_4573, _td95e9d5a31 in _v5096_dc6e.items():
                try:
                    import blake3 as _b3
                    _a602 = _b3.blake3(_td95e9d5a31).hexdigest()[3:11] == _41c5f815b87610.get('f2', '')
                except:
                    _a602 = hashlib.sha256(b'f2-domain:' + _td95e9d5a31).hexdigest()[8:16] == _41c5f815b87610.get('f2', '')
                _e60703271a212f = hmac.new(_td95e9d5a31, b'S-Protect-v6-key-verify', 'sha256').hexdigest()[:8] == _41c5f815b87610.get('f3', '')
                if _q4a6754_2 and _a602 and _e60703271a212f:
                    _x6c0efebe4dbe = _td95e9d5a31
                    break
        _pb9f974_b = bytes.fromhex(_41c5f815b87610['d'])
        _r51641 = AESGCM(_x6c0efebe4dbe).decrypt(_pb9f974_b[:12], _pb9f974_b[12:], b'')
        _r51641 = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_r51641, _6111d10545(len(_r51641), _x6c0efebe4dbe))))
        _r51641 = ChaCha20Poly1305(_x6c0efebe4dbe).decrypt(_r51641[:12], _r51641[12:], b'')
        _m29841e30a1 = zlib.decompress(_r51641)
    except Exception:
        _m29841e30a1 = b''
    return _m29841e30a1

def _t7af5761f(_s187a25537):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('bf0ffc4ee27c760bbaf4ebec8323d8c7c156c27cdc8e8a44c45aa673a72858eb210e4e7fb6fe0883649f33e6')
        _d = bytes.fromhex('ce92053d212c37e6089e7719ce3b5bd618121a1f6bb617049ec7045ee3a941c9a28a4168452db3b4b777cab723f4ffc48e75119eccf71fe9fe0f6b36afedc12475e3dcf4a571f3adb09ec388fccdc1a7e67db1a4f22d8bb9bdd135a7a4f96b8311e32dc87634db0a091990d5790f4dc05a9c69d823c74d62675b511e00f4de87913b547c9c526461fe928b5411b709c112f5e322dc')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'd416db04':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 1265857802
        _r = zlib.decompress(_x)
    except Exception as __a3e3acba1:
        _r = b''
    return _r
'S-Protect loader v3.4.'

def _qcffa6845(_wf4c61ae8a65a):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('3d0de3c1c80e10c2df40f0bcb4f4b743704ba68b8600d4650e6ff32e9110e4cb7f')
        _d = bytes.fromhex('483dec39bee5b13dc751f2b53acdb505a94f28e186dcc092e9f2ba83c92e3def7699c1b57cf92511affd21e0aa0157fe078d7b1302a51f260d95bf6ce1883bdebb942b465b0f070f02a0ec996df38b66ea08ab5da3ff99d31cb0c6fb2123322c9789838f52517c73acd026471fa4b66733fa64c25b4864a702848a771b728afb71dc7889b8')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '884ff19f':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __0x201678df72:
        _r = b''
    return _r

def _vbd8fb713(_wf4c61ae8a65a):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('ed96566fb4f2dbb9c90abf83b0f4e6f6a26f9d6784037d3831b1019ac7d4f52527ae2adf49268c')
        _d = bytes.fromhex('d7b58076d3e551cf6f66c52044264a3a8cd3d0257bdc3c1394df44a3c3f4a0029a68299b97bac4ba342e3fd0521fddc91adcbc075ed7d28bf3365b8e62a1186511521d50aed68eb3887806696049c093a2c367ef2d890db1d2b9d008369cabaf42eb218206d79edab9ae731be3ed65a75fdef78c5c24d43b62359561f63e7a14ca98b1c0bac38e4d')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 644375576
        _r = zlib.decompress(_x)
    except Exception as __r5a516656:
        _r = b''
    return _r

def _pbbf65a1d(_a93e82830d, _0xbbb1faf5):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('ba7acc6af6183e200e9d98cdcd254c6c1ac4a6c1859a2cb9dd453a1b09a3d9394d72e6db709a0c810d80')
        _d = bytes.fromhex('e4a84d7aefc479757fab8a08b8c33cc51137bf186158e57f334c91da6059d822b17c9cf8a10cb180fe9ee907e95ce8d3a9130ba1ff79eb021561d90d7c93d50aeec8c2869a05061724')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _r = zlib.decompress(_x)
    except Exception as __ba56a6a27:
        _r = b''
    return _r

def _zc30b5f54(_a93e82830d, _0xbbb1faf5):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('b03dd7e1976ff0a1d269159a13f2700499362939578b12b270262d3cd5b02111bf16524344b5c6474dd662')
        _d = bytes.fromhex('2d4f4fe696ee0def2cdd5e366638bf3e24af1c47e942e9b4b7728cac30357df536f58ae5facb155ae280d6a4a26979b7903c3c7da75244582998d5aba2b0c628aaf7b43d80e207c370b0ed04a3a3fe0826d658')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _crc = zlib.crc32(_x) & 939188731
        _r = zlib.decompress(_x)
    except Exception as __x4e5b0b7c:
        _r = b''
    return _r

def _qe783591d(_wf4c61ae8a65a):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('396b81df4d2238e4bf0ddea6cc865103b21b3fb483a2f120de810b53709cc31efb40c5671c')
        _d = bytes.fromhex('d8a2b47714034c6ab7a2d590be7d03b1c4b47e98fedf4191d417e670c644ee7dd322ecf0b568931f3930fd54a3a9a11df840b1ae5aa5457e3947a26661acf8e9e5a1cd392bde5c095d1ad2cc43676c8eddcb60c841a52086ec')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '85f67335':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 2557594907
        _r = zlib.decompress(_x)
    except Exception as __z65c4216b:
        _r = b''
    return _r
'Loader v3.0.'

def _qf58fea5b(_s187a25537):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('edacb9cb13f2adfd5127cff0b8a459c95e7983882356810a58d9f72c731d21a6ba10376bf112008349ed')
        _d = bytes.fromhex('e858eb1d84a9ec4a87f3f307aa199bc1f5e226c62b96da2a20853492d9e523b90c9cf9f347c391db7057529ab05faa2dbe5ac7100e6e6491f1a53f3b3db5dab3901333cd2dea7d15ebda528abe975d903df006a1bd93f509df')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '6b65f0d6':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 817542218
        _r = zlib.decompress(_x)
    except Exception as __p71c76164:
        _r = b''
    return _r

def _p09bf212b(_62f74fbd91bc):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('2c301dc554114ddba785b241b9d1de7bac03e20a4fcc9b757127a2a7c9d832741507b3d2978ebc5cce4a03682f5d')
        _d = bytes.fromhex('13d11a341c24af201f20ca45ab765ec51764d2ab681267f379a697c2e4206878b0f9fb15bd32a69573303d39881948af3cd3225b0b7567d021cd5a8a7346fd7009be35a55d03b00b247b2f9bcd8f00130628735d4bb9801fb0d0b54831da1eb3eeac21d56574cbe49dacc7ac1906')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _r = zlib.decompress(_x)
    except Exception as __z72dc08dd:
        _r = b''
    return _r
'S-Protect loader v5.7.'

def _cea584219(_s187a25537, _60503_802e07):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('f0258215d8ca1a8f7fc0aa788bfb08e1a580f212cecfee419d6a2e13acac662387ba565f26')
        _d = bytes.fromhex('15fe23ec004f796460aba361f81b0748ae6bbe97d403a01f0d9e66595b020c695bb06a3dbaf9c8375da22d24651459dfb49f834ad9c98b10008ea8fcd44be09d0e4dd0fec64a75fcb9a6e5519a6f7dad4bdaecd77c67adbda2913db83c5f89689d364897e520bb65ece75f5a6a3393b609fe0e43490f90565e00805d31d69f8702dcbe10bf36387e0a')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 1477564458
        _r = zlib.decompress(_x)
    except Exception as __b32e9dce5:
        _r = b''
    return _r

def _rd07ddd9d(_62f74fbd91bc):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('0403bcbe1040d67e375d4d2b38fa3e5f56e9c9436080893f0467a062c65d36e11f526213d1')
        _d = bytes.fromhex('632895245603293531279f030a035b6084ddc466ee148d2bd41a77afdd8e7dd8c47423422c4b1a649e42f61ecf9223fe490f849ba14bf72325ac20c56451ec688361be7bcaadf6d7160b8f98105af14c9cc5c3eba46f1990b16246a924d809208563ac16b13053401d00c95b5a4594598ad53a2d345c591e03')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'f244fe65':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __t7fa54734:
        _r = b''
    return _r
'S-Protect loader v5.9.'

def _e794fc73c(_wf4c61ae8a65a, _84502):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('9e91d5086689d6a18f3e2afe0ade2b1ee21ee95ff690b7308b3df90cab71aac4cf6f13f72e4897')
        _d = bytes.fromhex('30fea71bf873b5053e25f269d9fd1a74c934f1138b9d5b6f8a33c6579f6812ac876c1e9d700d2b5cbe491e56c74c731fa82ab9c34c840bb3945f06fba774191ec79ce8d38418cb35aa')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _r = zlib.decompress(_x)
    except Exception as __z6e615c6c:
        _r = b''
    return _r

def _w117daf11(_s187a25537, _60503_802e07):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('30a17f5d3fccfc5aaec7987b8e43c632c0329c224c510f42abd7f657e98f8f2e69')
        _d = bytes.fromhex('2af10676c5af96e7f4fb7a90c2b6ea3b24631b73e40fbc669d5251ecfcd50c256538a221cc17f91ec13fc68e6fda362238c0d1bde33f1f130a4555a416baf1d0efbee4441334233aaa0956d3fc1d7e38a44daac8a03655aa2c538ddcf1a1ddf8')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _r = zlib.decompress(_x)
    except Exception as __r71dba857:
        _r = b''
    return _r

def _s8c651261(_s187a25537, _60503_802e07):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('479249cf6e8f3ffd2b8b031bbbae05dd3554f1d7b032642bc077ca09ec6775a4')
        _d = bytes.fromhex('5d85ef1294304fe2ff8cff069b22d36d3a743954fbf684880040f36da75c9122bc8862666511ebb42560d51a94261d367708d26c11fcfc46a4d69c906d44115aa24d0ae0f1e3f875de4d6f0fbca8f2c12d7ae77945d5f3baee0cb308b64c8858c47885b5f14a30134d8359c8af0510d2e9b34f5897c7f4b09462d1e5c6d1cd4575fabb4276ace60304b5f28b5fe5dc23bb7c')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 3218937153
        _r = zlib.decompress(_x)
    except Exception as __n29dba8ec:
        _r = b''
    return _r

def _b2ed29c71(_tf1b3e3e6):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('6285891f67b2077ad89f22d5d541cae23efb4e70c33db8b08b72baeb629615a018b7d81e7d641f40fc08cae164cf25')
        _d = bytes.fromhex('bc5b0bbe397bc34432a51a165f98974727dd2b0be08b484f326e64fed9bd3c304476bc9e079e6123e1f35aa4c5d253770be11278e4659225c7e3538d202e4139cf0e375cf7a95c5db011fda3d6581d2ced40cff155ad78e0c97219da856fa30c9718ab6fcd560d2b863b880b')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _crc = zlib.crc32(_x) & 1893831704
        _r = zlib.decompress(_x)
    except Exception as __n26a3270d:
        _r = b''
    return _r
'Loader v4.3.'

def _r4ae1f027(_62f74fbd91bc):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('859aa5efb826b064b58eebd3c093d2add5156de474ca34acadf5c1dd6de986f6ecfe64dd3a2f04b2ec5534eac46ad0')
        _d = bytes.fromhex('7697b868e9d6acf450b419a799e823b6fb1e0ebc152e6350bb9f97f95b4defbec6dd74f276b42cdff2e3542d7d5a51c9a6c9dee90b3da2751eb26680f2c7b3f947cece527186c92fa511242c995cc54889955b53a19a4915f47375be61e3994633c04f6f21e3db3a1a3af0a71304a226b83da9855aede5a8c1152c332773be8aa75a0cc711d5e1d7de4108bcbb0416')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 3396996012
        _r = zlib.decompress(_x)
    except Exception as __p16b85a2a:
        _r = b''
    return _r

def _c37904c82(_62f74fbd91bc):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('dc51d18797bf7c5ec86c49ad3fac371ed5df63f649518dcde29f502bd30dc20765ed96e2d1fa25')
        _d = bytes.fromhex('a69b0c4c224776d9705b92bff57275fd8029b76074e56a247f8fda6bedeba3976bc6b6839c72aac98ec2a7ac34adc75b4bb1b952121da94b5839f99c6dd19a636f696972e63778ec5dc22664c5534b05adfdb7042f1439c76d')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '1fb4b5f1':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __s5c89ef67:
        _r = b''
    return _r
'S-Protect loader v5.6.'

def _z8c4a385f(_s187a25537):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('793cbae38c9a6737dbbaa3bcc9e945c2e4b4e5068082b820a2e202a569a54cda8cacf690858e7d12b628482083')
        _d = bytes.fromhex('e9089d99f0644b95fd2a4792271686c2fb790f154d838847770c18574e775d0a7d41d0a4f78517e180680c521f33045dab04c203ef9e49ff246f936fc2f00f97f9b91f54cc')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _r = zlib.decompress(_x)
    except Exception as __v108ee41a:
        _r = b''
    return _r
'Loader v1.9.'

def _v108be66d(_62f74fbd91bc):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('3e2427a31e36df137b12e6784f439251f756e61b12c63632bc50abf6e732e101f228d397ff7595097ecd')
        _d = bytes.fromhex('23ae00146caab8223e0952071dbdc67df5d3b6778c12360e8c93e216e42d6624937ee640d404b3eb43b535b4267005276d5e2e4aaea100ebe4ecba7f621c6fc165d9baa1')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _r = zlib.decompress(_x)
    except Exception as __q32b291db:
        _r = b''
    return _r

def _pa70a4a88(_a93e82830d):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('c1c223f567116bdf1a956269e26dfde7bb61376e29ec9d7630251f76825e999e5a68ec')
        _d = bytes.fromhex('f309ddd2a85c1694bc24a90d1f15f08a1f5bdf5d42fcc8fe6051ea3ca5dc351f49790eeb8d75b1337febfc63501451fdc4053472e75132e5695f1c34aebabb7ac230fbfcce2f482e7c64029b2ca3')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '703d8544':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 3706803795
        _r = zlib.decompress(_x)
    except Exception as __effa94a0b:
        _r = b''
    return _r
'Loader v5.7.'

def _p6d0e131b(_wf4c61ae8a65a, _84502):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('41e85e61e60f2b62e1a3d8272a0a17bad456225f2276c96d0f39baaa48ea68617c2b23b03ca548a0678c98')
        _d = bytes.fromhex('6f2351feedb32acbdbd76a22a52b612920bb585b2a829103f54d3c07ed8dbe2e25f3cf92ad83018c2260441063c9c7ae51cc6cf3d5b7b7856add13675fb26e0beb8a41f298af7c6af8e2ebd290')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '2678b2f8':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 2993049233
        _r = zlib.decompress(_x)
    except Exception as __maf417daa:
        _r = b''
    return _r
'S-Protect loader v2.0.'

def _w89e02f95(_wf4c61ae8a65a, _84502):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('3d7596658fd8831abfe1914fa4a89b6e73cc56914a08e24185ce19cf950abb1d3d46')
        _d = bytes.fromhex('6e72fb9dff1b17d11156a7287e18579039a8aa5de2622ba4748cb86b5908ea64eecd79825298d13ded125920d856ad40bb5ca853aac012aa9ec21cbd1b07cf148dd1e80d99b44118db')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '024a0699':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 213493335
        _r = zlib.decompress(_x)
    except Exception as __v86342b0b:
        _r = b''
    return _r

def _we9d51508(_62f74fbd91bc, __0355ad6471b4):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('73be6bcbd10e0edc2c2e95496f5237844c5180692cdbdf72d6eac519064c752c686a985889f3327e054840f27c7694')
        _d = bytes.fromhex('42cef87e18c374b58ea696de51a5a3c897c7a4d32197814074e4c2c6fee29ddde9eb265db88cad1efb42c5176893cdd183421f653d0aa1fcb52ab925dcb17f2c966701bb301f07aa215a6b57571c068ae5bc8f0810621d45106c8f71f4789edc055d4da9a853d54523262cc677a3a1a6f4b83f8da452e61ce8fc2878fd392d7c81c9efce55ae7c843b')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '51383865':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 1956079914
        _r = zlib.decompress(_x)
    except Exception as __v64c8bc28:
        _r = b''
    return _r

def _c044dd626():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('8a75cb0feda82e840a176c4d76bfdf37f26446c06cb21a2c7eb1d07134f04cb6a51e853c39eec7d19de10f7956c6')
        _d = bytes.fromhex('9a337d72bbc9697a25f2635b121befdb5ef926581eb8af32f141b3fbc7e41154bd4f73a1440e862f1989288b50d004c87af33af4f835d7539e7ed66603d26ca0facb12b95fba6a97feb96b89de8dfc17b8868b2e10')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _crc = zlib.crc32(_x) & 1844604102
        _r = zlib.decompress(_x)
    except Exception as __mdcf8230e:
        _r = b''
    return _r

def _y8e246bbf():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('ef73b69e3792d289121aac6e59f3a265fa0c9e8b1969dc5c85ee6073e662618d9bf000ed65b33a')
        _d = bytes.fromhex('406e544d337d3b9f91dd92db58846910caa0325d0be88e50b570b152aa2704dead8985fb3b77cc25ad9d5090e344cfb032ccb754fbe54a028aeebb3578cda1f20f66135b7d61e69eea6872259fceca36b1b380790b92ea53133f757603c72b29509fc8ae1e54f9c4196d026841680f14169487f51424e764')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _crc = zlib.crc32(_x) & 2551950838
        _r = zlib.decompress(_x)
    except Exception as __ka34be889:
        _r = b''
    return _r
'S-Protect loader v4.7.'

def _z3294d7b2():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('7f47ee20b31c3d87d9d050a8201af03f297eeae0201022fe6b9addb9ab263865805696e27323a187ecf5')
        _d = bytes.fromhex('8a5c977412772fba40de8176c55cb472d7bbaa12939bce919d120a4edc47af6d28cb9b930b300574d46aedd1c5de808d56198d265ff544f54d162bc40996a79acf5d97f5910217eadd438b0c9cc149e5aab75b12a59418a51fc9492cacafa24e38ab9d462f138974c82f')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _crc = zlib.crc32(_x) & 2668996466
        _r = zlib.decompress(_x)
    except Exception as __r58072123:
        _r = b''
    return _r
'Loader v3.3.'

def _r39038405():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('d11ef681bd653a6b2a5d758ec7d1c46ddcbe95484c97dd6e6a01a80820a1c1e1bd78022f35fc')
        _d = bytes.fromhex('b1fa3b553af0e1b50a839caa0695a98b705854d955cef03bd5231d0155c9f85ef76a24ec8a2e9f2acafa595a5ed9fd14c0b7bbf2ee0d98ae03c8e408056a9b7e1b3604ecbf60eef39742204c28e4588c8278')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 2747287990
        _r = zlib.decompress(_x)
    except Exception as __0xb4f56fd84b:
        _r = b''
    return _r

def _z1a9d5e1a():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('a0eba21ede0728b10530baf85c9122f51cee2b47bc5e4ffd2a73d567cf30dfebaa')
        _d = bytes.fromhex('a69c7bbc7fcda9db16085b0ddf9d88e33de79b931692d5b4f982f2147ceee9e8c283984b74421eacbaf095ca759c3017152fb059f5ee04d67b707d22c15e1d5e69955c39b9c6d5b73c1ebfdc7c64944c6452f767715df8f687433b3267b198b579cbe0d2db90bce674a857d686e78bbeee379ee437ad654acb5f408683cef6104a')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 818373600
        _r = zlib.decompress(_x)
    except Exception as __v4880940a:
        _r = b''
    return _r
'S-Protect loader v2.2.'

def _v119cd81d():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('9c32abf3a505fcf5b95eb51b652f8622047a115b48b150781eb0cff71e3812076949752ecda15505')
        _d = bytes.fromhex('af9625b5a172b59a68087f43a3be949c845dd2e8bc176529583d204c699074500bc597490a401087ce8c197ef433f574ec240d6b1eae4b4e81895f51dc02c939280fee28cc36a6b7ebfc6445ec5c8e')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'd30f5fc3':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __fd79179fd:
        _r = b''
    return _r
'S-Protect loader v3.6.'

def _yc3bf16eb():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('c2f130deac1849907b54d3dbb8bcfab9a2c4c3feff24d152ee1c67b6ba1f8c8bb47aefda244561d87d4b5364625f')
        _d = bytes.fromhex('eb3bf9ea8800c760b138005df6f8809d08363fcb185eb91d9f95d1898628f3e559db5c51acb3b09abcd369ebdf3a6942741db1a05a3dd86a9ac98ebb47aa612e2f89b27ab33e876bce523dc15242a3dbc31314297f900a037ad5e1cd8d8f352ae165')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '81295338':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 518866827
        _r = zlib.decompress(_x)
    except Exception as __d909a6679:
        _r = b''
    return _r

def _p89603581():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('bcd923ac31c7444fe57a186df6c5d83a55bd32451b413c1181b12177e6f50f0481e02eb3d2')
        _d = bytes.fromhex('9973a5d37371910c63046402bb4bfbae992117f2503abba25c6583f3630103d221e1d837b364ab1d265c2756321f16cae5502cf34d7f220a15384767e77b9ac2cde3e1df11b3448c55')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '0bcd196b':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 2121040837
        _r = zlib.decompress(_x)
    except Exception as __ze60bbd09:
        _r = b''
    return _r

def _f3ae41f61():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('d0ea909a96588264ce45aedaeda8f622853811278bf57cba0944f1dffe841598f5')
        _d = bytes.fromhex('109464cb9390ae7027d91b27bbc45ee2f0e3e1aa4803f172caadd09251ad5956ebde6ec39e28935cb1578b00b006ae5ecbb6278c14d410f3c4f55c32d02bf04db3f1f697f9064c83450d7813f0a95849b3f33e84652cf3694be2fd9e1afc641043e15f2b028f63f97ba1577781617a23594ba6')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _r = zlib.decompress(_x)
    except Exception as __n36533c5c:
        _r = b''
    return _r

def _d76aaa19d():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('069dce739e09bd8ec2c3444094dc1a09586a55227b19b918afafedcd4df58aa56043d0')
        _d = bytes.fromhex('95b632b5602c06ecfeb439c88bc30138654f3793b6dad3029f03c4d47d2fc982956bc076b8647e3425b2e08109f14ea1a70e085a067ad990e0c5cf97ef2e46dbc6b8d3a5dcb225544fc64ea510389367b2a16761ebc27f94b42560e75b6bc995514c')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '701c0ea0':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __a15d03f20:
        _r = b''
    return _r

def _p95188b34():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('d0d4f20412f7f3ba717e4a602712031b0b0aca2a3e84a56dc330c068ed3b04f2912fbf8af7d218')
        _d = bytes.fromhex('74203ab21e36b2283095113fbedae50b301f491391edaf622c10ca0e11f88a75ed697f75e5182af178facd6e0597875e2f1638956cdf862149656efec4dea3e44edd1d124ddeccc3b39337418759218f118cd0f61d56e6e76c9c9d')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _r = zlib.decompress(_x)
    except Exception as __s42c82561:
        _r = b''
    return _r

def _e231f8553():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('554441b6b21d22f79df5e8f087588e08c63e5db89cfc7de8a8411b535d11ac32f00f25dd016e')
        _d = bytes.fromhex('6a5089e61b2fcd567f050f5422af97aed790b5f14195bf37ecdac18a670cd5cf5122615c31cead96b157b61a9786b6f7a26150a9a40167e36eaecd31a6625724259506db744cb4cc1562e9dd4ab9ba1e534f4614f27ecaeb5645830ddd6e08f8ad29d20f2c382f')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _crc = zlib.crc32(_x) & 1349001668
        _r = zlib.decompress(_x)
    except Exception as __kb4971dd6:
        _r = b''
    return _r

def _dbdaa80af():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('1ad340f43acb47ca31f31f87560147db8b596b8e5671044285c1a7692b1eca600a03d380f28a2dfc')
        _d = bytes.fromhex('9fd3f1895513d46d54f426267d7e4ec725f98e17a62e5d04cffb825cb85f4ff940c250d1f1d4daef99946e895616908dd224ce43593732bc21a45a7c38d88969dbfe25bc5a7ab575a7609e38a6')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _crc = zlib.crc32(_x) & 3985889005
        _r = zlib.decompress(_x)
    except Exception as __vf18eba8d:
        _r = b''
    return _r

def _0x3cf4a33b9f():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('51173e40309179d26c80afdbc807a27d16eb7f582dab7c062aea839ab58f141d875a57f3557adfacdcc70f88d8')
        _d = bytes.fromhex('44d199b358ff7858d3643d3ca15de8bc4fa8c5a9dac525f1f83aa98ea48e4862419a57c1c7a0f487b29da18c1361813ee5a6')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _r = zlib.decompress(_x)
    except Exception as __k91bc3f98:
        _r = b''
    return _r

def _d836b233e():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('a4aac012314391edcbdf65fcab364182ced3629988ef2dec2e0756cad84bfad3ebfe563dd5198d')
        _d = bytes.fromhex('bdd7f5bcf98d95fb57f00bea958e5679cc103fce1aa53a927f1460b8f3b8e2567f3965936458d821d5d1f960ff7cda4ea2e97bd2d0f1fd7031')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _r = zlib.decompress(_x)
    except Exception as __t66b9f309:
        _r = b''
    return _r

def _m682a1835():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('5f165368cf907d0a71dab3ab3e9eb879115d3500710db0d53a28e5fee024a9913b4808231df58761fe7925')
        _d = bytes.fromhex('eb1b2cc34fb9f20d6a857e78c59c96aeabf49ecca889012a5108e6af9181c952e4c116c4c344e238838463553703db86c0a14ebc492583e8901b759622ea900a4237bf48ba365e9989f3')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'cb640f69':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 1482870296
        _r = zlib.decompress(_x)
    except Exception as __bbf9f6c97:
        _r = b''
    return _r
'S-Protect loader v5.5.'

def _d16677738():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('eff31aa65fc209940cbe011fa834b4abc72e19ad0f5771e3e837f7080f7c21f90b73e3f6ef9a7777533a')
        _d = bytes.fromhex('e7a85ebe6ce5265e73b80d19d9adab8e684adb53a274fb8c76f7ec0c2f3596385774b1bb7a5dde5af1a66ca456ae72f42c824dfb19fc2ecafe12159506')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 2766221166
        _r = zlib.decompress(_x)
    except Exception as __q44087ce1:
        _r = b''
    return _r

def _vda0b1315():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('38f5b941141c6fc842f5fb4097b632c07a74e7e22949086bc771d2fd4293fcabfebd35746b37e5970e65')
        _d = bytes.fromhex('baec0c5aa74a040f56054a51e9f5a71f897d077501e0fb61031873a4fcaa49fd6cd94c07a402100add2ab9f96bc480870417764864bdcb708d0f662020c3afbf7125bde10e78ececbd8dca209256c8bc405044')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '6155a6b1':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 743585542
        _r = zlib.decompress(_x)
    except Exception as __0x54119f3979:
        _r = b''
    return _r

def _y5a7d4f29():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('75ff9ca0c785e6a41f3c25feafb25a00c930aa9ed50980930b63724be6cccdca9aa0daf89d87')
        _d = bytes.fromhex('f746e01d9dee7d0a1d5b4b5f34fb2f6fb8a50e6e33463fedb059bb5a30d84b0dee5cd5d10146c59e00eb67d7af15f2cb261bbd81f87803e8417c89e664bec3f7567e2f6eeab7bf25eed6eb348b87bbf64bd22a98697eb07ffb34b410d99c5d5ce1780f81f1dd832d1e6510a2')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 847426023
        _r = zlib.decompress(_x)
    except Exception as __c50a51169:
        _r = b''
    return _r
'S-Protect loader v2.0.'

def _sa8b456ef():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('54ea47def458c70d3b932e2395d8b7284edd73bc1c5ff8e3177443a390325a8dfb41aab3')
        _d = bytes.fromhex('137e62877b49919ac21603c816056b97f323708231719fa8bbfa231e2dd1b89e98e3d6a7ac3aae7b58392f03a0838e40f5be77db90a3abb6b2bd4bf6ba8501fe39c290ac3cf8a69220bb3302b8e6d49be6ca9375fc7c2b1cc76d3deaa3be900987261281111ee3cf860320639d')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'ee93bfd5':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 365996898
        _r = zlib.decompress(_x)
    except Exception as __f8a006407:
        _r = b''
    return _r
'Loader v3.8.'

def _v591f4f9d():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('c50196be3ae3cbe7672cccf7905346f5f0ec58a3ca9ad34f6362a71ab1ca4eadc4')
        _d = bytes.fromhex('13e347d8c9a45f52d079128aa575d618a864a37260bcc63f6a8f851fe4ea38f152c50587721ade9c828de6294815c69d47687702a298a8d4f5052e989a51c5ffaff509addb57cd5b2fb158c12082b96a8788f684fdb13a6cfd39132a708832b68e37')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _crc = zlib.crc32(_x) & 3270505537
        _r = zlib.decompress(_x)
    except Exception as __rb1ccac5a:
        _r = b''
    return _r
'Loader v4.7.'

def _qbe559a45():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('3eda1ba4c412db58aa6ea17b50a7592161c16694cd39916ac58e1b5598ea43f2b2e37b')
        _d = bytes.fromhex('bcd74a0c0e6b9a7a16b1f1769c61c69f7785bff2bb7c7004b6c0c01c9de937a1fff6fbbe556537b662d00fb0b07287fb41274039cd2c4648a01f')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '505b85b0':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 2098307201
        _r = zlib.decompress(_x)
    except Exception as __pb6cbb2bc:
        _r = b''
    return _r

def _xb79dcd44():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('fe88b0611b490c245d4f752fc9bc3b041782930f9a20c77ddc4ed63dc4452348df6e')
        _d = bytes.fromhex('7f81d95c2b448557c96302147fa3c10c957c7818dce76183a4ef1193dbd839d848f7e655b2a129d74e941b5c0e6308690750621515e34d555e4f196e3358a4906f176d697f7cf3cdf87256b66e07bf2fdddb96c21b54dac26fbc6ac88acf22b63a9e779ad94f7a05bd209b775520129dc2bd247dfef7077bae22ba4e71333557401c516af34aa0a377b0431a5f4944')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'ce530dca':
            _x = _x[::-1]
# type: ignore
# monkey patch for compatibility
# DEBUG: remove before production

        _crc = zlib.crc32(_x) & 3043469756
        _r = zlib.decompress(_x)
    except Exception as __zedf1a730:
        _r = b''
    return _r
'Loader v4.1.'

def _ae0f48362():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('93b8424082606756799fd6ee79b3b63d5826d384dc798b0b4f225a34df0dbffc7f')
        _d = bytes.fromhex('a517114217ed012d2cd224a34f7ae691a8d0d3121a97169d13507b13c9e557a0a42de7f702834f3d49da61bc298b2e833f1b31d5fcfaa9806d250d3e500ed2d15c07b51583b5baee73a9c5ff78d7aff41aacc508740d72e28059ed01d4bbabd9a238b472391db556fb0c0a80a6ad09e020d26db7ec1aa586c86aabae27ca3c7e08da9b9166126cd2067ab9d5780b')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 1704609293
        _r = zlib.decompress(_x)
    except Exception as __e7ded4e61:
        _r = b''
    return _r

def _xcf0251ea():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('88dfd67b42778d278a5583a438d59b4454cb4dff4c8f2047e9403cf2f499bf17a841bb8d7a07bec63aa7')
        _d = bytes.fromhex('2f905874d5aeba9bf8bb4dc9b4894b03ca31e0884f09a4a5d98f01f3bde896e3a0cc3ea66753f98a59ae2bf24bc0f10bd673b56e1a1e4ddc93e5ab6351')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 2517346904
        _r = zlib.decompress(_x)
    except Exception as __zc8b758af:
        _r = b''
    return _r
'Loader v3.0.'

def _cdff69201():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('b2e653c808405b88ba26e427a683de7641c032b82a55c880defab7f11433e884039397e51e')
        _d = bytes.fromhex('52c7c0539605463d26da5bbc11862f72459bb6d3d814d263a88599aa5842ba026d608b18719c5d388c094cd1c87a56f32ce3a5201708bc291bf8bbb943b85da3ac43be545a49b99291b1c48aa8cfb255ef920f213b20825b5e446d237c39951e29c268cbb8d8')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _r = zlib.decompress(_x)
    except Exception as __z291f6b15:
        _r = b''
    return _r

def _f7336caca():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('d67c6756062a193e8c416e94a5028385bec4492fc2a1f40d67af5ac11d23f47d3f83b9de39a9b022')
        _d = bytes.fromhex('7e5a90e8c9aa46d62483c912986be6ea1264ad51bf4a6aa410fa2e60d05917014112af15daa5d9d179359ce1614ed9a46b8a1aed9a504d052c980056be617a')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '705cb771':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 3047873583
        _r = zlib.decompress(_x)
    except Exception as __b39620d9a:
        _r = b''
    return _r
'Loader v4.2.'

def _eb9300420():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('20d77e1a7a790beca901b9623545855eec348338e1fe499f0fd3dcc449ec189b7a2fe0b75e88a26b0fe0c0')
        _d = bytes.fromhex('f975971d3e402154cf5bcd4930feb39672ea06237f7bc7af6a0bbf55584765f0e9decedb4c144b7bc94d307477dd5369c17f44fa01886ec6bea11926fdd9331a319d7c939bd22ed27fd48905ca34796c2befbb504254710c69bfcfbcd8a5cccf28db2466dc239affa07f0e98042bfa520c144eba6b82c7a96109895d6ac3dba2262c045933b6e756d92f70c0be')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'c525b77e':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __cbbf9e2d1:
        _r = b''
    return _r

def _c7c435332():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('8daf81b48eb92c978b4563094213a8d4f0f4d8360ebce2d95d4fd5394e2eef46370ff8edb830')
        _d = bytes.fromhex('1500baf7e65278c6957c2d5e13cb748519d54a794b79056eb992eca9ba92c50e21d147c62f55a100a048b756cf66d38dbae9728250004deb0ecd6a468b82e387ef379fcc323c4e6f7f550c16f77b30bded7ad66303a16f81563e11d41c3166453a1b438aac867991b265ee24b31a97e9c31bb3266e7869a113d1')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _crc = zlib.crc32(_x) & 1436642417
        _r = zlib.decompress(_x)
    except Exception as __ed6073e8c:
        _r = b''
    return _r

def _ta834c72b():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('5aff95e43df754478cfa15c3ea07829556443a527b09f3fb4bae176eec9fb9140e91bbe0379425df')
        _d = bytes.fromhex('102fd391971aab974a08c74b21dc5ec115d2684999d552e9c39833b10f926ed9c04876a4832ef69bacb1b8670090e129f86975e0e915c49ac6d3833988440c514ad0e2d83cf13d59c798bfd0ee759ea4960acc07b32556b2')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _crc = zlib.crc32(_x) & 3640646765
        _r = zlib.decompress(_x)
    except Exception as __d81e3f8f9:
        _r = b''
    return _r
'S-Protect loader v1.6.'

def _r17ea9c96():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('621cca14e3abe9154bb123f95812b48338259c5b50291789ed19f9a8e5005af9')
        _d = bytes.fromhex('452b356bcfc414e1bec0e0982e4610b9fc8041b6291c7f5c69bab179fa4d9178f17633fe76ec5b9b1944dca80e83b5a38745eb683aafbb1b5d78fde058b57680568766801616a2714a58fc991dca6033af5ef866026381')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'e9328f70':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __c75cce463:
        _r = b''
    return _r

def _p417cc061():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('b6b3e4fbad40060bf9514596eecf9b47e2395ca903dfb4ae7594c9d8107745b4b118a1')
        _d = bytes.fromhex('6f9cbc39eeaed64a0cfb0d320455289da98cd4688234e9235ec5a640b79f33582598ace9f4df38a3de6906877f38fe89e3abcc4203dbab8e31bc7b54c34382cc656757fe0f7d1f0acacbb6473765107a05130190f86e56462c36345566828baea6a10d42015553354ed071ecb3841048e500d3f1862563f18c501eb280a590ac577e05e87e8ebb8ac0410756b801b1a302')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'a1f4f0a0':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __y97c738a3:
        _r = b''
    return _r

def _q201ca0da():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('715fe1928a9c67ebd93c40c58c655d5bfafc5febab6606d4734fb41be82c624168febc7dd194c047487ff9ea6c')
        _d = bytes.fromhex('9fadc1d4a7d8038c69d1636f7031c19e8082b1ee1227b277a554c42595a08364a0be23c28a9d10ed40097a66549042d7a7afb624809c793d615d8a1d4f21677049f06c16a65d89b098df2ba489dd342e8fd0142b8d1baacd6a0537a425b67afb4a0b25709b8b77e4a15357f318a8c57c5958525b367f3092f45f585c332f7e7ca31195e730a374f0')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '0929c3f1':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __nbb167c8a:
        _r = b''
    return _r

def _x4ef6b3e5():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('499128b461c635b7814c29d89ee80ad77ea17d528b476402c45b62b72c48da5ab11ced2d477236')
        _d = bytes.fromhex('c3ddecfb94bf373face7d94e417c75d3bbf0f533364f3abdcc34a364e920391306ec265c9d1de5d97c23b407c83eb214924c4d1d17256b8cec77652a718c3f05ee7ba55f9dade113c9618041031a47b96562d8e456c5c76e6f6a2d67da3d2747c6a357ae4a00cc395a1fd34fe831c070cf5b3a02f2e5d8')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _crc = zlib.crc32(_x) & 1070712773
        _r = zlib.decompress(_x)
    except Exception as __r311a28da:
        _r = b''
    return _r
'Loader v4.0.'

def _afa29e3c7():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('475beb1fc9f043f76525e74c81e8e9b9a3c81e134923277f273a1c168f57a0a805695a16996a6530889803a2230bed')
        _d = bytes.fromhex('7c34a9f972511e61e528adb50fabd65a7fdb6221ebd9b6a6b273762798d0831fb26f4d9ed19ad318a69b3263e6cc9d42092c1a1fbcce76871e')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 664400148
        _r = zlib.decompress(_x)
    except Exception as __xbc56b6a2:
        _r = b''
    return _r
'Loader v4.6.'

def _ac813722a():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('566e87772307b68f31f5da0bda88930c6460eb23c6ebf7b47513d2dffc13caad477a2e1e5a32813f2f00a01e')
        _d = bytes.fromhex('013293d60de170fcc871c228750f87c49058423d332a9c72cb4ac406faebadb24c9c9ba78502682e7532b40715b56bff213949a5a9d17d3774db3946f89b5f40703432273cbf2b2b6b6a3a019a65b593e552d18e0248f1409532a678')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _r = zlib.decompress(_x)
    except Exception as __k5ec82e78:
        _r = b''
    return _r
'S-Protect loader v4.6.'

def _x014e296c():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('00c63c54fdf762bac641553eb2426052c0e2e341bf4813753d384e17c8a32c17a2f2759780c0')
        _d = bytes.fromhex('ae53f6197a3e57f8dcbd4d06dae85304efac3ad820212c08e1ec6c33f4ad6b25bbd441d8985c3a823d404973a4e4e99311aec4dbca30611cab7c2fe3a6c1afbf54ba8d47f3ec8f2f63eeff438da56b5e2c567765e81befa9b0e1c91dd34f9bc843e3c40634cea11ef26f2b8155e5f4918f048fc6e12376187ebda1023f1b20')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'eefaa94e':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __a20f61623:
        _r = b''
    return _r

def _eff2039fb():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('d90c19414ee546e479355f6557a25311b1275a78d740d63045d4abda8656a07861719b260268dd864b')
        _d = bytes.fromhex('beb584ced23b9539dc986bc45bae894b3434614f1065eff10d9384aec821be4ffd1cd162d9a8ddb13c272879530b09759df0e5bea7dc29')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != 'f19e59fe':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __y0291626a:
        _r = b''
    return _r

def _xbf00e258():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('453b96c2dbb66f4df328dd389b1800c7a1b4e77e7f4911f29e763af6861897b5')
        _d = bytes.fromhex('6eda3ba5abae84fea1620dc7099ff559d45ad8df71bb37380604cd496643326aeb843c2b6f4a6a3c8e60bb19c6c9b43d398d51421f6ccafff0ed4cce7244fc9740f50764efcc7fefadc3b0497dd0f7ffc59b6b4f476a05d154d1631b6441fcd7ed9e121e80795a962d60b604305a746f85b9ffe9f37d32ebd7b8beec5b5f536d377c9a')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _r = zlib.decompress(_x)
    except Exception as __n4731c297:
        _r = b''
    return _r

def _v781a78c8():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('2804c875b491a7b498ebbb2f01c79d79a3a6f5c93edc1024b9ed0d4a17c5777abf36b1746e526addcac7a658')
        _d = bytes.fromhex('688e31bbfb638c889029292139723c8bc0d8547819edf1425cd5b28e8264d0ce7cd1960e72b743955cd1a69ee58a24582f52bf56a3e7fdf8b7bbeb6ac99dd2589b161fd4de56e4453046806cee49fe9014abd09198bcf1d8c8132636e268c01649d9d69dd84ffd39ca4e15b206b4d17f8f039e9bde433206b981be6b3e2e8d4d98ba627ac1193803c172a1b3e1a0fdffa0')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '7ebbc575':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __s739b63e6:
        _r = b''
    return _r
'S-Protect loader v4.2.'

def _a86835c92():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('6a2e9c8c6ccc495c1f572166f88b8f41125c7050c9ae84ad6b8ee758e441b53665e3050a1033')
        _d = bytes.fromhex('0b51652ab17865a29b0198a964a24211f079c4eb39dc36059d023c4c59cd52ae1ac833064cf3dab8663df9cef0e39d987fca05ee066431a6c7')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '8b5952ad':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __e831db5f6:
        _r = b''
    return _r
'Loader v4.7.'

def _k6bf961c7():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('0db44435d6c357b4896b5c739b2412557962efe17040d55063a63bacbbde58fa32f365a5c7b75f0a685e25')
        _d = bytes.fromhex('84281b086a02ab29a5f5762beb3fff551d3bc1b86076c21b81b5b5725091f8d05e4809092affd8ed24340254f4402d3935aab3f7bfd5ce3737981c73eaccec94722dd628fd37ec5fb84acabaf3dc146924f2526d6222f70785b883acd0b4f278')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '2a9f8438':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __k63c52f26:
        _r = b''
    return _r

def _fabe69877():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('9e8cc3727106a1e831cb4d6517a0137c376d6d5a8e6c02086aa5b77b572200b61f632692c30b46')
        _d = bytes.fromhex('f6016ee2766581f6f07fa4ca4a5f20c8a1608b5fb55d836e93129d50aaf59d76e617664cdd35d77365b33046c5bcb745e3865989aa2585646fbd5f5c79373b38faed53c889147c9c65a2cae03ad5d77aa4aa79684e59e2ae77eb4b4f02206c0aceb4213b6b72458f316ca85885142bc5849b4f16a4cc6e1927c667cbbdb65469aa145543b9af615d3fdd47141021ee32f56f')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _r = zlib.decompress(_x)
    except Exception as __sdb97b3a7:
        _r = b''
    return _r

def _p99d21d8f():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('29da9f9b0d08b01a21c05b43fd578a07b14a785d948194a4e94cc34163f57f874e078d2dc728a35f')
        _d = bytes.fromhex('ef41dabe4e68d5c41c1ce403a9f81108d9be270fda3bd7ed3b2ad28e1c5238b41f42aac8d9293af250a5320449491aea21b0ee9cd565d363981b8c1e51')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 4162695708
        _r = zlib.decompress(_x)
    except Exception as __b5f40f7bd:
        _r = b''
    return _r

def _w29bf283f():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('6b3e0676920917f45f4da0db6911d21c751ee506c5ef50d2fde4b8e0bb902f23')
        _d = bytes.fromhex('5835b9caa9dd3cf3600585006cfb997e35bda7a2dc59b672306c7c2516d1be3023cb30483fae4a7715359d7dbb9cd360c11c9bbeb7056ff0fc22')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _crc = zlib.crc32(_x) & 423247312
        _r = zlib.decompress(_x)
    except Exception as __ac6576ea6:
        _r = b''
    return _r
'S-Protect loader v1.3.'

def _f43451e9a():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('6a21e9923ab3835ffeddb25472c3f214eb04b2b9aa3dc3e77b8e5162418e0470f86dc27f6f3cb369c160d3')
        _d = bytes.fromhex('496989bcbb5685ffc0a536a8e934081d9eb9843e9e00e90c46a88976dcfe044d47e78cf911fd75532dfb691f83dc2ef793930cbc43aa3dd4072f9dd73e07154474789461d208dbc368eb2c47f0777060d98148b9efbed82564e7c22b40609074b8cb295b103b14b5531e5a9340b6f7818748ccbf0407e70d2d8f21500c1db69d47c2d7')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _r = zlib.decompress(_x)
    except Exception as __z503de21c:
        _r = b''
    return _r
'S-Protect loader v3.1.'

def _ffb924bee():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('13bf47cf05c63a517d6c9c5f4cebd4e9bae578a9b2f7209283fc110b1df634c467f8b7d180bb1621b4142120')
        _d = bytes.fromhex('f35ef44f23e15b5702647aa6b95f68af61588ca7f3eccc15f3b621b562bcc358f5f68e3ad5410b2c31a354e65bee0362c18ebdafaa42a426531996367623c2b37256081839ca8d720ed40b6378c68bc1d6ac')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '831b71f3':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __x229f78c2:
        _r = b''
    return _r
'Loader v4.3.'

def _s168785dd():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('20172c84f80a95936d308d4c77b7bb613d7a2884781829e581f2f1b8a26485b5')
        _d = bytes.fromhex('12067d27f85937badcee217e37ab232ece2053e15b3a4e2c9b9de163b043000f57f8b0805d258ca8d2f30d90a6543dfe0a8e2c6c18bba46a049217053a3f299f50759428985f37090cc2d148639cbd0b8598f6efb0fb57d4f2ea90014c710a5b0b4cc194cded3834e51baf3467418a36268887607bc2cbcc124a8f2bb8f3da6d01e5ee87f3ac09c3')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _r = zlib.decompress(_x)
    except Exception as __e4ae54c39:
        _r = b''
    return _r

def _q660306e0():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('ad41b8ec491321d67f218a23cf332c2b0cbe7d2517c7d33234ba207243ee8284')
        _d = bytes.fromhex('71bb9b4691e63fb7bf859a284eedb88cc10d485a5cf55d856d26fac34aed0c89c5a33459210f5fe25d6c862a392f7fa7cbf3d94e9139679e312126acf39ef692cce4743ddf75337d1e')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 396510865
        _r = zlib.decompress(_x)
    except Exception as __v330d6486:
        _r = b''
    return _r

def _yd2ba6306():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('f33bc21dbbd2f69f1428a1364a4492dbf71d70ae38145bc77acb84420ac834f26e3ff9')
        _d = bytes.fromhex('7b44675a3f30b8ecc4d79a54eb6b50a558f74e04d27eb26080b8e06e1e767efe0bc6591fcac73fdcdfbef07b100a831eaabba3350f0f81257adf1524216d60194e2618eae118cde1f34c2301e5b97038d760c3877cc12ded7333f5d1be5262d60fe5825649a035e631be6b7880dcb01fecb32b67a42fda474f855b7413f546b64771f6')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _crc = zlib.crc32(_x) & 3267546281
        _r = zlib.decompress(_x)
    except Exception as __b45a5c80b:
        _r = b''
    return _r
'S-Protect loader v5.5.'

def _x29d46379():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('070bc7cd521fbb7696fe282aba520e963d56e4038582ea4fa80b8e6c5990954404a3cc08b26665ee9ae5')
        _d = bytes.fromhex('2f8c4f8e49274fb3a4e882622c9ef91a66e5061cba781c880659b5ad9e789c50401951dc6e2a655cf26c44979bc9998a48aec5e82a72f75e52c26753a424cf86fb90ae2d475a')
        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()
        _x = _c.update(_d[16:]) + _c.finalize()
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _crc = zlib.crc32(_x) & 3582420323
        _r = zlib.decompress(_x)
    except Exception as __f03a7c446:
        _r = b''
    return _r
'S-Protect loader v5.5.'

def _t2d189e5c():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('09ea39ec4364d17dfee31b55afd0eebf460804a95a21f69be8d9cd3586fb55d142ae745526d04d4c')
        _d = bytes.fromhex('866d87c606cac56188fe8890b51505c19a59bd73230aa7c21a6938d469d281d57029b65b57d67ff43a7290a552774c6505d18d578c0d7742d66721f61be7f882519dd849fb9e3c35d787ad6fdd1c166d57da5bc7c1bba8dbd5e5a69ad5d2d9add30a08636c0e869a827b3667e683635f75b7bd008103f9531b1ea2c10c6c39b4a4c166006905077f0abdf99dba')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _r = zlib.decompress(_x)
    except Exception as __a4863adc9:
        _r = b''
    return _r
'Loader v2.7.'

def _q2cee596c():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('7a65cb714d951dd730aa561951e7db37b6709df85c21ef53ef044415b2e5755dc696321f87ee7dcb')
        _d = bytes.fromhex('27193b1c21f1fe08bc31039a55b857c48e4bea4e7dbe4b5ee83d67d5c15a1d7a008b0e9594813c4f27cc94286caf886968c1fa11672677242a2a44a4d1430460ec4e')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '58fd645e':
            _x = _x[::-1]
        _crc = zlib.crc32(_x) & 2014212718
        _r = zlib.decompress(_x)
    except Exception as __xdbd1b79a:
        _r = b''
    return _r

def _f80270f8b():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('bf2147494436b86faf104e3211e2de1b9b4025c6fadb478681c21175da5ccda1b2e0b946c0da1160edc10477')
        _d = bytes.fromhex('5277f5305901c85b5bd99e01b6401455c411015fe2680c7bce11ba5a5870b950787178bed6bc76babce742992e7024975c6f2547d6d1fee14709e13348f8b79220d666b0ebe8e19b15bd1516ce39539bb9a1c45fc6f86c5b6f4fb8eb63fbaeab0f5a224c8afd9c9294e1')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _r = zlib.decompress(_x)
    except Exception as __q26bd7353:
        _r = b''
    return _r
'S-Protect loader v5.9.'

def _a154b0d7e():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('f1c48f61d16a54093d8e9cdf6561a9e1d1daef30622786a81bd10cd061f6ae7be7a1d6fd92a23bf948')
        _d = bytes.fromhex('b8af2b10ed397deb6f4328803f60034cc56836214d73ffe48574a64e0d3d687029a76075e645d2762284ad3dc27182db3f8e05e322f41554ac4481dbf2c6d9522639cf325c6a3949553353c0d897d85ef62159f8b689645a626ecc156f7b1b7f8d187e395ac84d6f7e212ed02326797a3eb0e75a233090eb8818fb061f12b649767214a554e81362a1486361')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, _k * 99)))[:len(_x)]
        _r = zlib.decompress(_x)
    except Exception as __te756a5a0:
        _r = b''
    return _r

def _db24a1c1b():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('a9ab6ada12ba614c5f48437d7b59900c6ef582d226d3409d75790d427376303d71825273c0097c39e870dc1bb1fa29')
        _d = bytes.fromhex('5be1e4380de839bb4cb2364bf44439a67edca8ecb6cb9c62b9b8890e2dbceb8ee4b5edaaa1897baea5a8fb8b1adc19244cca2fbd38c6540df762545873c9')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '2d530e5f':
            _x = _x[::-1]
        _r = zlib.decompress(_x)
    except Exception as __0xc9120a1d23:
        _r = b''
    return _r
'S-Protect loader v2.8.'

def _medfeecb0():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import hashlib, json, os, zlib
    try:
        _k = bytes.fromhex('876c3eb28064feee34f698b3a60ad568fc494f9beb23b9aa845ca6a743f455f443110f')
        _d = bytes.fromhex('f4c59d7ba84f5593446003a60fc2f0dbdadb06c7877d0c7b856d9390db7d3eddc86c6744146e78bf388bff7caeccf044939b44731ceef74386a36cf7b425091fb50acdf660dd3fee0c23233fbb5d6f2b4a8b0e8d6e672b51d912fe3b2baa1c3d4411d8e12c790aeae20d1103e7c313d3fcec26322d84e8222f9d0db4c91a8fba7d09b7f88b3df07608ad5bdb6c5593755b02de')
        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')
        _x = bytes((_q8629cd_36 ^ _b46dd634330 for _q8629cd_36, _b46dd634330 in zip(_x, hashlib.sha256(_k).digest() * 99)))[:_x]
        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')
        _crc = zlib.crc32(_x) & 1310027416
        _r = zlib.decompress(_x)
    except Exception as __w3e574bb4:
        _r = b''
    return _r
try:
    _e = compile(_dbdaa80af(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_0x3cf4a33b9f(), '', 'exec')
exec(_e)
try:
    _e = compile(_d836b233e(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_f77bf5cc4(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_m682a1835(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_d16677738(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_vda0b1315(), '', 'exec')
exec(_e)
try:
    _e = compile(_y5a7d4f29(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_sa8b456ef(), '', 'exec')
exec(_e)
_e = compile(_yd2ba6306(), '', 'exec')
exec(_e)
_e = compile(_x29d46379(), '', 'exec')
exec(_e)
_e = compile(_t2d189e5c(), '', 'exec')
exec(_e)
_e = compile(_w9d7aad09(), '', 'exec')
exec(_e)
try:
    _e = compile(_q2cee596c(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_f80270f8b(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_a154b0d7e(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_db24a1c1b(), '', 'exec')
exec(_e)
try:
    _e = compile(_medfeecb0(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_c044dd626(), '', 'exec')
exec(_e)
try:
    _e = compile(_y8e246bbf(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_z3294d7b2(), '', 'exec')
exec(_e)
try:
    _e = compile(_r39038405(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_z1a9d5e1a(), '', 'exec')
exec(_e)
_e = compile(_v119cd81d(), '', 'exec')
exec(_e)
_e = compile(_c8052bab2(), '', 'exec')
exec(_e)
try:
    _e = compile(_yc3bf16eb(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_p89603581(), '', 'exec')
exec(_e)
_e = compile(_f3ae41f61(), '', 'exec')
exec(_e)
try:
    _e = compile(_d76aaa19d(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_p95188b34(), '', 'exec')
exec(_e)
try:
    _e = compile(_e231f8553(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_ta834c72b(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_r17ea9c96(), '', 'exec')
exec(_e)
try:
    _e = compile(_p417cc061(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_q201ca0da(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_maece3625(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_x4ef6b3e5(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_afa29e3c7(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_ac813722a(), '', 'exec')
exec(_e)
try:
    _e = compile(_x014e296c(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_eff2039fb(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_xbf00e258(), '', 'exec')
exec(_e)
try:
    _e = compile(_v781a78c8(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_a86835c92(), '', 'exec')
exec(_e)
try:
    _e = compile(_k6bf961c7(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_fabe69877(), '', 'exec')
exec(_e)
_e = compile(_z4a321fc1(), '', 'exec')
exec(_e)
_e = compile(_p99d21d8f(), '', 'exec')
exec(_e)
_e = compile(_w29bf283f(), '', 'exec')
exec(_e)
_e = compile(_f43451e9a(), '', 'exec')
exec(_e)
try:
    _e = compile(_ffb924bee(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_s168785dd(), '', 'exec')
exec(_e)
_e = compile(_q660306e0(), '', 'exec')
exec(_e)
try:
    _e = compile(_v591f4f9d(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_qbe559a45(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_xb79dcd44(), '', 'exec')
exec(_e)
try:
    _e = compile(_z02ad2eb2(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_ae0f48362(), '', 'exec')
exec(_e)
try:
    _e = compile(_xcf0251ea(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_cdff69201(), '', 'exec')
exec(_e)
try:
    _e = compile(_f7336caca(), '', 'exec')
    exec(_e)
except Exception:
    pass
_e = compile(_eb9300420(), '', 'exec')
exec(_e)
try:
    _e = compile(_c7c435332(), '', 'exec')
    exec(_e)
except Exception:
    pass