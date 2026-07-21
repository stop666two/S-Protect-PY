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
__ta59d4ecd = 138998801
__wcdb0751b = 1479710095
__n55710e22 = 655653342
__s6182d13a = 2898382100
__k792928de = 156374760
__m84437ef3 = 18134259940180480272
__z82617219 = 37511
__qe2609c55 = 'fb9bd68b212f77872ecee37b595a5db539d8d8c6dbb49d160ed89eeb06eb7e15f1df99c34f139f12547e929c8780995336356d33f9ade0e5575514b470d81d39afbc64eac6ad6a340f76ef4859fae23dbac0b045f5a42b22c18b11a9b6b6ad144b3bf6ede84dad6f9add3795ef4260b4535827f018389dcf30085d33b1b19d3c3c1467c9c7e81cad341b27eece29b4704c16beb8059738f5c66b63fb409753965efa2a974a9225c6e7ce9644fe547f14a7e8ec8aa1238c6a45cb2b9e1c080675061a45239d0b388a12ba5d1b12508afaf600f435d9f976b044a4668823dc'
__y8901dca4 = b'5a15b676d19ca94732fe217a9e4d1349ca596cc6123411d4d5b41a0c6e5f2feba0b92a3d0c12b817a1608cbf2647d7bcb5dfea1bc2ff5560a654986fbca9e611df0f2276797c82da3436c35bac215b74bfad386ca2736ff02220f26345d9d3eec4497e48da460bfb6f6877972cf0de1bb231d43e9f6d5fd553'
__db9f44898 = '62739e93634638abd175a0f2168139ed6fd431910c88f33c842280b89d64c091f6ae860b81ad14dd5687c3505f332e29237d35879083b85d1154ead9e20f9a7e462872a1893552758a9a721cb87dd1cb63f100c478b6aec774f590fb20ef9dd5c63354af95fb7e5c33a69440e5b145507a97f1682a'
__bc00ae41e = b'20f98a14b0d53ffe03c0e2f2599c2069817477210671d8d93806c24281290aafd46137f6c969ca8983f3134ce37f15b2b4bfcd74252879ad98251df1108903ddbdc25f40c4920ac987ed37fd61ac32b5cd1165b02059627387e46250eab4efe887fab84fd7f56251021d0918cdfca39e3a1534'
__f07e6516e = 599087354510352
__fd074c8f0 = '1c7a33be111a3938d9048841c1bb790329c6e7f3dcfcca6cafc42f341824ec94d3ae1131b79ff7724375a55704a4de97e8e30a4afb4bc98fdf8edb1c576ded04e9f949d701d1db8d0c7baa67329dd6d0b5fc494fe7158eb75a64b55131307278de288a8f9f651c029e752ad5a9'
__d31e44392 = 'ef04a780d7681a3ccd2682a5293034310009544cce42d43abb74b8d20f24f94324f0135f3ef182c7415a2a08cfb5aa13d55bdb5733c50aae61153a43e3355df39366196bc2f93338a664f7b70a97d328b672dba11f099ab952666fa6b37c61694c7f60fe395ff63628ff6c7c81bd9b8b00a4803bcb3afc22e7b24384cf7ead6402e8f43594511622be68e3ab4db7b11fdc0d970b6c8a73daf865aec95cb49628d8c25333562d8d6f5692c5a8a20360e9b821eb430d3dffd4d59636296be697'
__t5c005f64 = 3678598420
__e9a079dc3 = b'c773361bd139192058ba56cb5d164e89747cc28b699b5cafa894b75f4e8ceab21cda03695ce7626200bf4ef52e00ddc8bc80f72dab5d905d89694b08ef4f68c729b30e96980a3b1847845bdfb606cc5b2d54a98bfe9c62e8f64331a29149578be84c737c07ece7fd41db67401f17df'
__n2f4b36d4 = b'99c60f7bc802ae961034b0a18d028783fdc599ea8e87505800ef550c33bb63f3d8039666757761e22c3bd390032de350a00303f58dc7d62497de65a3d96ea1c01db3d4cc4eaf5e86569669b81543fd17846b98ba765c4fd5ce832316dcd39a3c23b762d7be3757c6a3f3dc43758b91c20f'
__a9137c943 = 3615493013
__0x040776a627 = 'b1b1c4109662211e5d84910cfc91bcab7b65b3d51e717f55d8e2edd2dbd3bc67e6d87d628edf47e05dc06448f527e2d7602589cc84f58eefaad008495d3e1b8485415472c1db152207fadb49333c0e5800a69e0ddac74d55c1d2c3ade81522d2fb6e1250979a0015b9d83bfd7114cc28295639c27baf0c09322e906f239de1dd22e19c4d5e0c375445336efb6430ad0a4e276d944f90a947455aaf1760f730c3eadb46d385721249b8f80be8f238dc00105b8676af5a9a8e264d1bafdb12f5b419dd374efd90fe4ff8a9e97896c48c0a82b8b8257716af43b3255def9364633b06987cc27d6a18b473318468a781651302520606d3098fa1f668fe6493b150a20822'
__r48c04b72 = 2304901876
__v4dae5090 = b'25898bb2fb211c2e4a18ab255657a861b5cfcd3cbd58ca6cc16d9f26b8c25ec8a6a7f3a87eabec43a409a6fc36cf949fcd7b496d6bc9977247153153469af3b0cabf62332c8b23d2dbbff9cc9b643efd36823f8cb356f19d422403a8d52ef64b4843ee15670c48f4ee2fa2fee1ef8faf433d383cf9a9b2fd50f4dfbc3ddc4bcf04ad281d87e41cc1ca63e4c7e69f'
__n002cc732 = b'2f3224d061097b11d5f4af467763e1d6e562b84aab8361fec467de68f989de5b94503465199be3bd7b2fac739d3f89df93341d2b6a15c367601fa4e67a24269b6df5f277c97299d41913a5d0deabe0681f84121cc93e5e5ed0364376188005672b7dd6d5fdbd12cc55017bf5605987a4f445c71c53f6b214'
__mb5e7e0bc = 56201
__yf3170064 = 14325811734528878
__q9db3f7a7 = 4253738811
__x0b467924 = 1015575817
__a64234446 = b'c80bab56f6e23a398c4977fed262dd361108933127a57884fe3ae93f99ce2aacc59aed956681d038fdebb22d2510fbb4b56f01d4880ff348448c404b23b01eb499e05340dc8b010c45159c657b4dafe3b0c045b15f24d14d829428'
__effc900ed = 1770243
__pfcae1e03 = b'201a425beed60cc4fd181f9c82431b8b5fc6b48f0e99b7ccfc3ea03f2495b9f8d1cb4659fa3c6bb4c95709659fede8846bc5e00c75853818c2e0c02d9a18514f8d3666c9068938b8aa8ac22d65a3524647ba60d1d19d129f403fcd863a4b2a52406e23d1b8b7210cf1a92ac16fd3d16805d06411bd'
__v5ffeed43 = '2dea85a0351459689b448b32358e81f1d28a92f98988f8adff8b849d0ebfbc091fdfba45e86fe67182f9782bba010405e4ad6e69774f50c9501707013026cdc3a515bfc710fd9c93f34599f20599f26ae77d567df46d0ebac1e4fdfc32c7205c3e5542e173aca3e336acfb3fe0a6ef866815ba18f26e144cab33503a419af7a8b63cb40d6635f8128de1fa15ec6cb3da415bc54451284ab6a8afbb3957168bb3e67441eed58944a094cef9d85cba794db101fc4f3c31ecbcd0290462a23c6eb17f1f2a061ae3ea14ced7e6e4abb02c386c4ded6b14cfc1fb0a2e8b3077bed9c481680759746c23e73a97baa4d9c0baf183442253b1be71e830afb83b74a58721d17f965fbb814692ef95d637c79c5bc3a9e0523fd2a9b713398cb3b7f97cb4b5'
__t3b1b9987 = b'c773e7e6a4d1de62e302b418ca9653659d739cd039908c0071a024b8ee67ee3546da4bba8cbbce5c3952aad3c39fbc2545349e1488a8e2311dea1a91cb6ff06fbb09b7d58a8fb8c020f0490757df43d39b9714c9b325bec2e0464febe74278d7b2c366a0a07cb71dd1d8419cc52cacac6d26849752df17c5bed3d8265ec576334a804a2b'
__e71a06be5 = b'125e880c75d848ba27a195f1f6bdc5cfd75f3f226a8ab3e85ed7006721247dd2581eec137dd8971e9c31b3fe7b7b4329c6fc7442212d8ffd21d56b7bd3b7beec9ac48c559e1e400a5dcd7831e2475780b573d1c6b836b3d8655195e6efddcd8fc8ef450d0718d4fe80d6553e0605b740828eb9db6fc1cdf499e4b0784802d4c6801383c91abb0334ca89842290ce861370fc9f5e'
__r04921789 = 'ad1341c19c7fa4070766cc138473347588a7cec37048d1b6b22bd4d2c5a3d9bec4ac0f3b6ee4b6e9d4a24f3870bdb7e6e4f04df7cc3b56da6874cc6cfb5a851674797ab3a102a580d058dbacd36fe03e75ca5a66427c82c55cb1bc836d3b9bcc7be46842bf721a4d175e6a6d9edf489b8849972179'
__sf777aa93 = 1999498601
__sdea9fa6e = 457199650090791804626
__p11b06012 = 'ca6034ea88f59d4e844b95c84f430e21f5e19235201cb27227dbc28a925ab24de1472851acc80ac8ed6d0d89a6773f58530ca5da6f480e72d4b8edd146c25c597db100f3d8db0ce4adeefc74c7b703a1e0e47b429c1382c6281fcd473564ca574fa52ed56935c80d3cd2f1b7bd57107551c1724fa815bd9132f8f82f15ab63996625cccdbc8cb98a9abfad5f91193db72fcd175c'
__m7f70f9cd = 872246105546
__nce30483a = b'408de28f0621392b07c638f7ccea3a4eeec8f871938f7849acac2e2d8d1adc6d4cf094ff01e9c3cda1e615fc2109c32c7919662fe26c388244ebcb6504817aaeb6be3568113fa463ba2a2c16c173169ae66f3443a07b757d425722b506171c87cbc294100476b72165583731518658de7b4b3eec9fa1486ade68272684c5949859bfd611c866fdc1a590'
__c0ee62095 = 6332171293384706509
__d79895101 = 1102233225
__k958a67e2 = b'b773cb7e08d1e0b83aaef610d6277e03256a512832a6d20c494029efdd98bf734b7981802f74636fb5f0156e1b87bf79c75faa728e70c715c36664d5a834ae13468951dc2dd724add4f4e4c1a8502b076c5b39bc8cd5624499942dfb7be86a01bde75cf70f683dc65706694703f17ed71a62846870749a29824f9c3cbe4f744224'
__ma6c3c167 = 3144502769
__m6d822fb7 = 438659151505
__kd571f26d = 4262236792
__q8fb649f6 = b'a45503ee389f7758101ecbbc091202d19f7f215e5787a6862657afc974361ef342c8ee850b8305d8d1e70526202e49a2e100c3b3c86482accf860949417cd39a95806f9f121483c57f24079f5f342f3bf7e2a3a0c2160c136be0c4f5602897cb3e7f2f964786e6b396b9da5177689b4737468818dad542b22a60b17c9febbe39d777bfd0509bda0a23b6fad2fca6701a3c61'
__yd70baaaa = '90df52cb93881c24861b76489531c93b258433876f12cff8c466c5504199910414c41f5eb8df97d52831ef74934348990c8c20ec7d03ec740d071dc497073593c7ba2fb34968d66b08651565453acb06bf4b8137d9a47dee6616f03aaca2133a03e9ea6eb9b1d29c2092ea06bf1a8527e64b16b0cf0fcc26e20ba7e001f0b0220200a625bd99961b1e7ade4303196fed00ac913359ee8db4b595160e5d32301e647d4c2b7889a7316afbe7a33a41b43ed398c9b48cfb3e7554d65a380714c38e94f0966f8e04c8002c764ead56c14da78288bcce48d384fd81d1570e4130ad21d44d8f668413254e34130754fafaaec6f8bf750ce6f1d76a8d24114e145cdbe6b6862f085b854fc3674a55649416266743aa'
__yaa9fa640 = '48d66582be8e91cab22688b74841ab8fa85173866c5fc5c0e5924c0c27da528dd2bf57e0845a1a6fd09e1c79220d39ec1bee7881136a31a9503636e2b65ee5aed99c5392267a8fa0e6b8ace984690631e005eb6d761d78a00b152be96fc7dc72a768f1d03aa2394a'
__q3a62fada = b'9657b51d37b6ab38e51eaadb3052283e8dc40ee40c602535c062eaa2727e237153bbd25940ed4f3ba92d9e6cb788ee079ad932fee7539d1990b0680a6b26b348e5d4a09ec08138ec885a32ddcaa53d5d200bf77f7bb1dda730e714f313e438d409ec0a4374fa911aceb6a82092696f22e9e9ae9d46e7eba79f0ed1391e82'
__a5601ec06 = b'09938eab1c061104d9ccc1862cefef4b5092dcb80464701fec124228e391675d57192e0c973d3fa03896eec1a57fddadd9383156fd1375fbec65f147af8a9574136ad16dd0ee1436340b2d79786e11'
__q31f986e2 = 333914857
__cf399ba75 = 3589672775
__c9caff7dc = '73df7a02e21f8e073dd7ccd28bd39a223fa0f9b689a549e50ae276ebd1c1ba2e38371d2fc84fcf87c2b0d3070b0e7c3fe3b7fdfa4b231df29ec5aa1988542cd6c58efd4fa625596e4819fd9c456d3f4947006c92620836689c76369954e95348d87ea5e1dc87dc0da8810a4a20aa57ea50fd6e5cdc37bdf6a17df394119d23433bb45ab0e7bbf19f7fa432d24784945102b844c7e2e78c03df5e593d6ca4712b0c6bcb3602509d'
__m7f22dd09 = 3034
__r832d8a98 = b'ef1d85f7120da5e3d63160c769e0c3afba8a97c261268ae1ebcdcd5253293ece3d299424cc5201fe6e5326392630dfb73f41f41ed549970f9b5de298d95eae693bc36f09fc8a649325d16773a5fca9b3329960298c841e14d5218a33f14a52cd42'
__a14029964 = 10997450
__pf160b87d = 3256710871
__ef9b4be5e = '5c126a4d1d44c1dcd4871fb845a4721f60b4adf30a71f72df5e05f14af2ff825e41ee6d4bd8f5ab49df1447102e68234788c84c172a84939e6c6a2b8a23a6e1e19788281e2c63025a9011043d3f37fd3dc15b52e3604845cc24c60973639187a45d8886a43b0165badbed91c28e7cf4dd41c4faef262d2852435259ff85995315ff9a9f91407a83d164aa8be250d64364bd49846514913b81666f3d8d88240756ca862dcef16b227427ec8ec346697e96d682385272ec4aa58aee6dd2f7481de08dcc186d298ce338a62f79101996e12c40c3b96541fb3d74daf4fcbffb8e221d7348014b8a506948cb35ef011f15806bc4b8b1e75caf2ed2fac23c4331aac989889b813e62b607bf484618c327e2dce3fcbba7d3d50fe0982fc109cbc55948b2c33163c'
__qe4a6aadb = b'837463614419554163ed8d5421bc3157ed9e19c6eafa9be3df669456682675a238e7b88938633ec90072bd0447b7e4f18a23aa5a45af00cfda5969da3f67a7622e4782c5df6a2fbb6f7445609ebd7efb05d4d3a607863ea8063f5503acf02dca2476a9640ae84e0fbb4e4871eaac58156629a09c715ce5c4915c2b20fdd36d5e0544f07311d0c9'
__b2a25fda7 = 2627493913
__qfbdecec1 = '6927ba480e1e9f6dd2343e3fb8d20d49dbcdea80ce15db91765e7ea95005ffcf65b33ba7bb89bf1d8c0312146376a8a4c36a845b5880cca5cfbc524c18d677bcd307ca4b89b4ce29ee5e0ed73363ac40ef55ade40c4860866b935061db297659c9aaa303a5858a19ae1d017a7f3ac4d67047d9929b5f6c3103a0cf9d2e150df22c370fe7b67182ae0a73fc433b4f9bee5bee449830f58e3f8f3a7ee1fc1050517061dc7804912c1f3772bfbc68e8d36f873b31d9e29fc10c3758bb68877b419af00357a556f703a03eb7090981eb77'
__m6b2936ed = 2640108264
__b5973a306 = b'a575c689143934a92568ac7c9e4c4fd4a2f373f13e5848b347212e057795908847b82793b0655272d96d624f74d4405c62ebcd85b5e20dd0c01e7db2f6715a6421ff9d00e83ceee130ad9150fedcefd08bf2e2'
__me33beff6 = 3810410292
__kd1c5841d = 'a44c854a28f8eba6f6d01614af4cb9e7b6332adaf085fbfd67499d8426a2276b9b2397c1a35a5b9becaf82d2cec19bcf4c5b1f258196bc2742c65236a66063de2ff37fa6867f2d299ef615cc89593a5c019a9232ebc68c550fa8ed1f27278035fe35946c06dc42f307ade18f3b42b5d5bf29a21d2a3b5e5f24102cf4707a6c90d0822ee116829b92eb2580bcd7'
__dafa8933b = 1804419451
__f64b27898 = 464446682
_t91a0b74a = '4948928b'
_c01e7ad7b = '66e8978d'
_m28493c79 = 'e2147783'
_w99b7ff0c = '85983d9d'
_bd1bfecff = '94b41495'
_bc327e408 = '7b23ffe3'
_a611d6a00 = '85213393'
_f06416921 = '48a9698d'
_t1776ec44 = 'd9427ace07be4294'
_sf5f0e8b9 = '05c0977638ea7fdb'
_s8a593e01 = '3868874bb66ea71d'
_fbc236b25 = '4389d176350af01f'
_m83cd87db = 'fa807579bde58dc4'
_f73c0d6a1 = 'd218a10b89040af5'
_cb39a96ff = 'ea0463b7eeef3c2e'
_sdbb96965 = 'd4fc5ba366ea0f72'
_x725324b1 = '4948928b'
_r5f14f302 = '66e8978d'
_z333c7a68 = 'e2147783'
_wad3c7791 = '85983d9d'
_0x83865d75b3 = '94b41495'
_r097e801d = '7b23ffe3'
_a6a7957ce = '85213393'
_c2447329b = '48a9698d'
_qf34eee05 = 'd9427ace07be4294'
_a08b7a2f9 = '05c0977638ea7fdb'
_s82facc31 = '3868874bb66ea71d'
_e589cf461 = '4389d176350af01f'
_0x1305052139 = 'fa807579bde58dc4'
_k34af24b4 = 'd218a10b89040af5'
_rf8e09ab5 = 'ea0463b7eeef3c2e'
_dc148ffe3 = 'd4fc5ba366ea0f72'

def _ndb5201e1():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v8999_ed30 = bytes.fromhex('ecc23d1e4080e2ad6badd710206e47cfd1d1f72d8a7ecbf7f4351db34f1c2d52f83c3b09e02c43743bb177bcaf9967cbf571c20715c5cdbc8cb7d89658975b01')
        _t8cef47f25e = json.loads(open(os.path.join(_5d279f4f4d2a, '_runtime', 'loader.pye'), 'rb').read().decode())
        _4e830eaa5560f6 = _v8999_ed30
        for _b6542 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _b6542 in _t8cef47f25e:
                _p79912b_x = bytes.fromhex(_t8cef47f25e[_b6542])
                if hashlib.sha256(_p79912b_x).digest()[:4].hex() == _t8cef47f25e.get('f1', '')[:8]:
                    _4e830eaa5560f6 = _p79912b_x
                    break
        _q16421b_85 = bytes.fromhex(_t8cef47f25e['d'])
        _9bb3310e386 = AESGCM(_4e830eaa5560f6).decrypt(_q16421b_85[:12], _q16421b_85[12:], b'')
        _9bb3310e386 = bytes((_n0c1d27ecbd ^ _sea570e704 for _n0c1d27ecbd, _sea570e704 in zip(_9bb3310e386, _7bf27adc1f(len(_9bb3310e386), _4e830eaa5560f6))))
        _9bb3310e386 = ChaCha20Poly1305(_4e830eaa5560f6).decrypt(_9bb3310e386[:12], _9bb3310e386[12:], b'')
        _r0723105c = zlib.decompress(_9bb3310e386)
    except Exception:
        _r0723105c = b''
    return _r0723105c

def _xf08449fc():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v8999_ed30 = bytes.fromhex('35d98dcb8b812f03da4e468bf558d8467e1354d06eff9821a7a50915c8e4caf3bee20fef7446864267ac1dc09f8dbaa28e1dc538e96bb46b6bb45adc3ebbd34e')
        _t8cef47f25e = json.loads(open(os.path.join(_5d279f4f4d2a, '_runtime', 'loader.pye'), 'rb').read().decode())
        _4e830eaa5560f6 = _v8999_ed30
        for _b6542 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _b6542 in _t8cef47f25e:
                _p79912b_x = bytes.fromhex(_t8cef47f25e[_b6542])
                if hashlib.sha256(_p79912b_x).digest()[:4].hex() == _t8cef47f25e.get('f1', '')[:8]:
                    _4e830eaa5560f6 = _p79912b_x
                    break
        _q16421b_85 = bytes.fromhex(_t8cef47f25e['d'])
        _9bb3310e386 = AESGCM(_4e830eaa5560f6).decrypt(_q16421b_85[:12], _q16421b_85[12:], b'')
        _9bb3310e386 = bytes((_n0c1d27ecbd ^ _sea570e704 for _n0c1d27ecbd, _sea570e704 in zip(_9bb3310e386, _7bf27adc1f(len(_9bb3310e386), _4e830eaa5560f6))))
        _9bb3310e386 = ChaCha20Poly1305(_4e830eaa5560f6).decrypt(_9bb3310e386[:12], _9bb3310e386[12:], b'')
        _r0723105c = zlib.decompress(_9bb3310e386)
    except Exception:
        _r0723105c = b''
    return _r0723105c

def _f3a19dda3():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v8999_ed30 = bytes.fromhex('a86e7585c23b6a4769b84de3c6ae782ac0b8709e3d3f361aa92732022d40a516a70ecb1f5927ce8d76ed0bb770a027d22159752e3e8f3bec3832072193d558b9')
        _t8cef47f25e = json.loads(open(os.path.join(_5d279f4f4d2a, '_runtime', 'loader.pye'), 'rb').read().decode())
        _4e830eaa5560f6 = _v8999_ed30
        for _b6542 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _b6542 in _t8cef47f25e:
                _p79912b_x = bytes.fromhex(_t8cef47f25e[_b6542])
                if hashlib.sha256(_p79912b_x).digest()[:4].hex() == _t8cef47f25e.get('f1', '')[:8]:
                    _4e830eaa5560f6 = _p79912b_x
                    break
        _q16421b_85 = bytes.fromhex(_t8cef47f25e['d'])
        _9bb3310e386 = AESGCM(_4e830eaa5560f6).decrypt(_q16421b_85[:12], _q16421b_85[12:], b'')
        _9bb3310e386 = bytes((_n0c1d27ecbd ^ _sea570e704 for _n0c1d27ecbd, _sea570e704 in zip(_9bb3310e386, _7bf27adc1f(len(_9bb3310e386), _4e830eaa5560f6))))
        _9bb3310e386 = ChaCha20Poly1305(_4e830eaa5560f6).decrypt(_9bb3310e386[:12], _9bb3310e386[12:], b'')
        _r0723105c = zlib.decompress(_9bb3310e386)
    except Exception:
        _r0723105c = b''
    return _r0723105c

def _r5c9b62e9():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v8999_ed30 = bytes.fromhex('278f98a03fb320473f67fbdffaf63553df8ecfe429387a01acce0677c419195e6df4b5c7090383a9302231536bdca90a6d3abba69e0163bdfde8c509c769e6d8')
        _t8cef47f25e = json.loads(open(os.path.join(_5d279f4f4d2a, '_runtime', 'loader.pye'), 'rb').read().decode())
        _4e830eaa5560f6 = _v8999_ed30
        for _b6542 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _b6542 in _t8cef47f25e:
                _p79912b_x = bytes.fromhex(_t8cef47f25e[_b6542])
                if hashlib.sha256(_p79912b_x).digest()[:4].hex() == _t8cef47f25e.get('f1', '')[:8]:
                    _4e830eaa5560f6 = _p79912b_x
                    break
        _q16421b_85 = bytes.fromhex(_t8cef47f25e['d'])
        _9bb3310e386 = AESGCM(_4e830eaa5560f6).decrypt(_q16421b_85[:12], _q16421b_85[12:], b'')
        _9bb3310e386 = bytes((_n0c1d27ecbd ^ _sea570e704 for _n0c1d27ecbd, _sea570e704 in zip(_9bb3310e386, _7bf27adc1f(len(_9bb3310e386), _4e830eaa5560f6))))
        _9bb3310e386 = ChaCha20Poly1305(_4e830eaa5560f6).decrypt(_9bb3310e386[:12], _9bb3310e386[12:], b'')
        _r0723105c = zlib.decompress(_9bb3310e386)
    except Exception:
        _r0723105c = b''
    return _r0723105c

def _v45984e89():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v8999_ed30 = bytes.fromhex('90fce2302ba610e0be4683759834a502f5083b5bc17768d852bd37d1ad0ae652573f31491cb65e9cb52c363a5839e5d85fae99bba1d47d956b55b71b84994266')
        _t8cef47f25e = json.loads(open(os.path.join(_5d279f4f4d2a, '_runtime', 'loader.pye'), 'rb').read().decode())
        _4e830eaa5560f6 = _v8999_ed30
        for _b6542 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _b6542 in _t8cef47f25e:
# FIXME: memory leak here
# OPTIMIZE: slow loop here
# NOTE: deprecated in 3.12
# XXX: known issue
# DEBUG: remove before production

                _p79912b_x = bytes.fromhex(_t8cef47f25e[_b6542])
                if hashlib.sha256(_p79912b_x).digest()[:4].hex() == _t8cef47f25e.get('f1', '')[:8]:
                    _4e830eaa5560f6 = _p79912b_x
                    break
        _q16421b_85 = bytes.fromhex(_t8cef47f25e['d'])
        _9bb3310e386 = AESGCM(_4e830eaa5560f6).decrypt(_q16421b_85[:12], _q16421b_85[12:], b'')
        _9bb3310e386 = bytes((_n0c1d27ecbd ^ _sea570e704 for _n0c1d27ecbd, _sea570e704 in zip(_9bb3310e386, _7bf27adc1f(len(_9bb3310e386), _4e830eaa5560f6))))
        _9bb3310e386 = ChaCha20Poly1305(_4e830eaa5560f6).decrypt(_9bb3310e386[:12], _9bb3310e386[12:], b'')
        _r0723105c = zlib.decompress(_9bb3310e386)
    except Exception:
        _r0723105c = b''
    return _r0723105c

def _db9b7cdf5():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v8999_ed30 = bytes.fromhex('119fca5926021f986288e909f7fa8033306eb4fcc0038a2c9ad07a7752267605ab8345ebefbed7ce8abe1442f6c1fb5b2fa30a9253358248f011147a94afe673')
        _t8cef47f25e = json.loads(open(os.path.join(_5d279f4f4d2a, '_runtime', 'loader.pye'), 'rb').read().decode())
        _4e830eaa5560f6 = _v8999_ed30
        for _b6542 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _b6542 in _t8cef47f25e:
                _p79912b_x = bytes.fromhex(_t8cef47f25e[_b6542])
                if hashlib.sha256(_p79912b_x).digest()[:4].hex() == _t8cef47f25e.get('f1', '')[:8]:
                    _4e830eaa5560f6 = _p79912b_x
                    break
        _q16421b_85 = bytes.fromhex(_t8cef47f25e['d'])
        _9bb3310e386 = AESGCM(_4e830eaa5560f6).decrypt(_q16421b_85[:12], _q16421b_85[12:], b'')
        _9bb3310e386 = bytes((_n0c1d27ecbd ^ _sea570e704 for _n0c1d27ecbd, _sea570e704 in zip(_9bb3310e386, _7bf27adc1f(len(_9bb3310e386), _4e830eaa5560f6))))
        _9bb3310e386 = ChaCha20Poly1305(_4e830eaa5560f6).decrypt(_9bb3310e386[:12], _9bb3310e386[12:], b'')
        _r0723105c = zlib.decompress(_9bb3310e386)
    except Exception:
        _r0723105c = b''
    return _r0723105c

def _a4475d195():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v8999_ed30 = bytes.fromhex('5de28a952f2aca0c6f295dddc07182d1d68c589305a74e0ed77ec9dde7852924527c7e49679b774f2a560cb3f376c4379bcdbbf39bf96f82efc8ea48c49c2f58')
        _t8cef47f25e = json.loads(open(os.path.join(_5d279f4f4d2a, '_runtime', 'loader.pye'), 'rb').read().decode())
        _4e830eaa5560f6 = _v8999_ed30
        for _b6542 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _b6542 in _t8cef47f25e:
                _p79912b_x = bytes.fromhex(_t8cef47f25e[_b6542])
                if hashlib.sha256(_p79912b_x).digest()[:4].hex() == _t8cef47f25e.get('f1', '')[:8]:
                    _4e830eaa5560f6 = _p79912b_x
                    break
        _q16421b_85 = bytes.fromhex(_t8cef47f25e['d'])
        _9bb3310e386 = AESGCM(_4e830eaa5560f6).decrypt(_q16421b_85[:12], _q16421b_85[12:], b'')
        _9bb3310e386 = bytes((_n0c1d27ecbd ^ _sea570e704 for _n0c1d27ecbd, _sea570e704 in zip(_9bb3310e386, _7bf27adc1f(len(_9bb3310e386), _4e830eaa5560f6))))
        _9bb3310e386 = ChaCha20Poly1305(_4e830eaa5560f6).decrypt(_9bb3310e386[:12], _9bb3310e386[12:], b'')
        _r0723105c = zlib.decompress(_9bb3310e386)
    except Exception:
        _r0723105c = b''
    return _r0723105c

def _ma7b912fe():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v8999_ed30 = bytes.fromhex('7fda60cb7c2baff7fd97531d009129787dca0dc83172a2b2f6d9dd9b0a0171ed4ffcbd4ba988b7e3d1f373b080ab463c629f14fc2f2c69d1e46bfe35e1f6a001')
        _t8cef47f25e = json.loads(open(os.path.join(_5d279f4f4d2a, '_runtime', 'loader.pye'), 'rb').read().decode())
        _4e830eaa5560f6 = _v8999_ed30
        for _b6542 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _b6542 in _t8cef47f25e:
                _p79912b_x = bytes.fromhex(_t8cef47f25e[_b6542])
                if hashlib.sha256(_p79912b_x).digest()[:4].hex() == _t8cef47f25e.get('f1', '')[:8]:
                    _4e830eaa5560f6 = _p79912b_x
                    break
        _q16421b_85 = bytes.fromhex(_t8cef47f25e['d'])
        _9bb3310e386 = AESGCM(_4e830eaa5560f6).decrypt(_q16421b_85[:12], _q16421b_85[12:], b'')
        _9bb3310e386 = bytes((_n0c1d27ecbd ^ _sea570e704 for _n0c1d27ecbd, _sea570e704 in zip(_9bb3310e386, _7bf27adc1f(len(_9bb3310e386), _4e830eaa5560f6))))
        _9bb3310e386 = ChaCha20Poly1305(_4e830eaa5560f6).decrypt(_9bb3310e386[:12], _9bb3310e386[12:], b'')
        _r0723105c = zlib.decompress(_9bb3310e386)
    except Exception:
        _r0723105c = b''
    return _r0723105c

def _w76327700():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v8999_ed30 = bytes.fromhex('f29382cf460ce65df9e89d739a860dcea3fda515485990008c26f7afdf37badee9ddf2ed22053af1e567074790f9b73bc2d837ce8784aa3d04f73816bd459e2b')
        _t8cef47f25e = json.loads(open(os.path.join(_5d279f4f4d2a, '_runtime', 'loader.pye'), 'rb').read().decode())
        _4e830eaa5560f6 = _v8999_ed30
        for _b6542 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _b6542 in _t8cef47f25e:
                _p79912b_x = bytes.fromhex(_t8cef47f25e[_b6542])
                if hashlib.sha256(_p79912b_x).digest()[:4].hex() == _t8cef47f25e.get('f1', '')[:8]:
                    _4e830eaa5560f6 = _p79912b_x
                    break
        _q16421b_85 = bytes.fromhex(_t8cef47f25e['d'])
        _9bb3310e386 = AESGCM(_4e830eaa5560f6).decrypt(_q16421b_85[:12], _q16421b_85[12:], b'')
        _9bb3310e386 = bytes((_n0c1d27ecbd ^ _sea570e704 for _n0c1d27ecbd, _sea570e704 in zip(_9bb3310e386, _7bf27adc1f(len(_9bb3310e386), _4e830eaa5560f6))))
        _9bb3310e386 = ChaCha20Poly1305(_4e830eaa5560f6).decrypt(_9bb3310e386[:12], _9bb3310e386[12:], b'')
        _r0723105c = zlib.decompress(_9bb3310e386)
    except Exception:
        _r0723105c = b''
    return _r0723105c

def _x42343cd0():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v8999_ed30 = bytes.fromhex('d0469e56165aeb0a0a807b1cb56ce07f5c6f2584388308420d263ee655155d08c2cee7150ea8c7d0589e2318a9e4f15c244411c1fd1be25846b270f60eef2dd1')
        _t8cef47f25e = json.loads(open(os.path.join(_5d279f4f4d2a, '_runtime', 'loader.pye'), 'rb').read().decode())
        _4e830eaa5560f6 = _v8999_ed30
        for _b6542 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _b6542 in _t8cef47f25e:
                _p79912b_x = bytes.fromhex(_t8cef47f25e[_b6542])
                if hashlib.sha256(_p79912b_x).digest()[:4].hex() == _t8cef47f25e.get('f1', '')[:8]:
                    _4e830eaa5560f6 = _p79912b_x
                    break
        _q16421b_85 = bytes.fromhex(_t8cef47f25e['d'])
        _9bb3310e386 = AESGCM(_4e830eaa5560f6).decrypt(_q16421b_85[:12], _q16421b_85[12:], b'')
        _9bb3310e386 = bytes((_n0c1d27ecbd ^ _sea570e704 for _n0c1d27ecbd, _sea570e704 in zip(_9bb3310e386, _7bf27adc1f(len(_9bb3310e386), _4e830eaa5560f6))))
        _9bb3310e386 = ChaCha20Poly1305(_4e830eaa5560f6).decrypt(_9bb3310e386[:12], _9bb3310e386[12:], b'')
        _r0723105c = zlib.decompress(_9bb3310e386)
    except Exception:
        _r0723105c = b''
    return _r0723105c

def _d7c7d9380():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v8999_ed30 = bytes.fromhex('400a19ece4f68fe11d2a0112bc33c7667913e324ec155cb3805ebbdc33eb929b96e997c6811b72a76e9f6239592658aeee02e3fed85e1130172ac8bfa465569c')
        _t8cef47f25e = json.loads(open(os.path.join(_5d279f4f4d2a, '_runtime', 'loader.pye'), 'rb').read().decode())
        _4e830eaa5560f6 = _v8999_ed30
        for _b6542 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _b6542 in _t8cef47f25e:
                _p79912b_x = bytes.fromhex(_t8cef47f25e[_b6542])
                if hashlib.sha256(_p79912b_x).digest()[:4].hex() == _t8cef47f25e.get('f1', '')[:8]:
                    _4e830eaa5560f6 = _p79912b_x
                    break
        _q16421b_85 = bytes.fromhex(_t8cef47f25e['d'])
        _9bb3310e386 = AESGCM(_4e830eaa5560f6).decrypt(_q16421b_85[:12], _q16421b_85[12:], b'')
        _9bb3310e386 = bytes((_n0c1d27ecbd ^ _sea570e704 for _n0c1d27ecbd, _sea570e704 in zip(_9bb3310e386, _7bf27adc1f(len(_9bb3310e386), _4e830eaa5560f6))))
        _9bb3310e386 = ChaCha20Poly1305(_4e830eaa5560f6).decrypt(_9bb3310e386[:12], _9bb3310e386[12:], b'')
        _r0723105c = zlib.decompress(_9bb3310e386)
    except Exception:
        _r0723105c = b''
    return _r0723105c

def _dd6ace1dd():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v8999_ed30 = bytes.fromhex('f9aeb42ed49f0e012bc460fa93dde8a7c865c43ebebf7fc5b93cc6dd8b6e4e14bdbb37aee327a4ce9632bb35dd393a70de3f233f61958040dbe45f5982b90d8b')
        _t8cef47f25e = json.loads(open(os.path.join(_5d279f4f4d2a, '_runtime', 'loader.pye'), 'rb').read().decode())
        _4e830eaa5560f6 = _v8999_ed30
        for _b6542 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _b6542 in _t8cef47f25e:
                _p79912b_x = bytes.fromhex(_t8cef47f25e[_b6542])
                if hashlib.sha256(_p79912b_x).digest()[:4].hex() == _t8cef47f25e.get('f1', '')[:8]:
                    _4e830eaa5560f6 = _p79912b_x
                    break
        _q16421b_85 = bytes.fromhex(_t8cef47f25e['d'])
        _9bb3310e386 = AESGCM(_4e830eaa5560f6).decrypt(_q16421b_85[:12], _q16421b_85[12:], b'')
        _9bb3310e386 = bytes((_n0c1d27ecbd ^ _sea570e704 for _n0c1d27ecbd, _sea570e704 in zip(_9bb3310e386, _7bf27adc1f(len(_9bb3310e386), _4e830eaa5560f6))))
        _9bb3310e386 = ChaCha20Poly1305(_4e830eaa5560f6).decrypt(_9bb3310e386[:12], _9bb3310e386[12:], b'')
        _r0723105c = zlib.decompress(_9bb3310e386)
    except Exception:
        _r0723105c = b''
    return _r0723105c

def _t8e5365b4():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v8999_ed30 = bytes.fromhex('ca37e0f0c73ad0e68fdb0facb759609575fde284ed3c157b8a569ebfa608a7d6b28c554fad9354a0e2c406917da252aaa7efd25fbad012816c8042785681eeb9')
        _t8cef47f25e = json.loads(open(os.path.join(_5d279f4f4d2a, '_runtime', 'loader.pye'), 'rb').read().decode())
        _4e830eaa5560f6 = _v8999_ed30
        for _b6542 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _b6542 in _t8cef47f25e:
                _p79912b_x = bytes.fromhex(_t8cef47f25e[_b6542])
                if hashlib.sha256(_p79912b_x).digest()[:4].hex() == _t8cef47f25e.get('f1', '')[:8]:
                    _4e830eaa5560f6 = _p79912b_x
                    break
        _q16421b_85 = bytes.fromhex(_t8cef47f25e['d'])
        _9bb3310e386 = AESGCM(_4e830eaa5560f6).decrypt(_q16421b_85[:12], _q16421b_85[12:], b'')
        _9bb3310e386 = bytes((_n0c1d27ecbd ^ _sea570e704 for _n0c1d27ecbd, _sea570e704 in zip(_9bb3310e386, _7bf27adc1f(len(_9bb3310e386), _4e830eaa5560f6))))
        _9bb3310e386 = ChaCha20Poly1305(_4e830eaa5560f6).decrypt(_9bb3310e386[:12], _9bb3310e386[12:], b'')
        _r0723105c = zlib.decompress(_9bb3310e386)
    except Exception:
        _r0723105c = b''
    return _r0723105c

def _k69321da1():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v8999_ed30 = bytes.fromhex('506122ffdee1a36ea6910083bee1f0e409ae4da3f6df7bc0167bf82afa0f39e5c8dfbf75c90645573eee44692f27080f48572e1d911b231fb6d964e98b8dabcb')
        _t8cef47f25e = json.loads(open(os.path.join(_5d279f4f4d2a, '_runtime', 'loader.pye'), 'rb').read().decode())
        _4e830eaa5560f6 = _v8999_ed30
        for _b6542 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _b6542 in _t8cef47f25e:
                _p79912b_x = bytes.fromhex(_t8cef47f25e[_b6542])
                if hashlib.sha256(_p79912b_x).digest()[:4].hex() == _t8cef47f25e.get('f1', '')[:8]:
                    _4e830eaa5560f6 = _p79912b_x
                    break
        _q16421b_85 = bytes.fromhex(_t8cef47f25e['d'])
        _9bb3310e386 = AESGCM(_4e830eaa5560f6).decrypt(_q16421b_85[:12], _q16421b_85[12:], b'')
        _9bb3310e386 = bytes((_n0c1d27ecbd ^ _sea570e704 for _n0c1d27ecbd, _sea570e704 in zip(_9bb3310e386, _7bf27adc1f(len(_9bb3310e386), _4e830eaa5560f6))))
        _9bb3310e386 = ChaCha20Poly1305(_4e830eaa5560f6).decrypt(_9bb3310e386[:12], _9bb3310e386[12:], b'')
        _r0723105c = zlib.decompress(_9bb3310e386)
    except Exception:
        _r0723105c = b''
    return _r0723105c

def _w20d28d43():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v8999_ed30 = bytes.fromhex('a88b105acc1e7fc82458f19aecbecdb54cd7529b3e68b0beb24e9c167a0d71f4197f17b3832b0be0637d84b48ecb4152f9e5b38e8664bcc6b6e79cb72f014b3b')
        _t8cef47f25e = json.loads(open(os.path.join(_5d279f4f4d2a, '_runtime', 'loader.pye'), 'rb').read().decode())
        _4e830eaa5560f6 = _v8999_ed30
        for _b6542 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _b6542 in _t8cef47f25e:
                _p79912b_x = bytes.fromhex(_t8cef47f25e[_b6542])
                if hashlib.sha256(_p79912b_x).digest()[:4].hex() == _t8cef47f25e.get('f1', '')[:8]:
                    _4e830eaa5560f6 = _p79912b_x
                    break
        _q16421b_85 = bytes.fromhex(_t8cef47f25e['d'])
        _9bb3310e386 = AESGCM(_4e830eaa5560f6).decrypt(_q16421b_85[:12], _q16421b_85[12:], b'')
        _9bb3310e386 = bytes((_n0c1d27ecbd ^ _sea570e704 for _n0c1d27ecbd, _sea570e704 in zip(_9bb3310e386, _7bf27adc1f(len(_9bb3310e386), _4e830eaa5560f6))))
        _9bb3310e386 = ChaCha20Poly1305(_4e830eaa5560f6).decrypt(_9bb3310e386[:12], _9bb3310e386[12:], b'')
        _r0723105c = zlib.decompress(_9bb3310e386)
    except Exception:
        _r0723105c = b''
    return _r0723105c

def _r3ad01576():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v8999_ed30 = bytes.fromhex('82f3b01e098af37a7cd952bf251a885e14d617477af3e43ba2d7d1968b8fb1896ac7322f5bca624b758d5833f4123c510a28063111ef4263cd32a23c59d3460b')
        _t8cef47f25e = json.loads(open(os.path.join(_5d279f4f4d2a, '_runtime', 'loader.pye'), 'rb').read().decode())
        _4e830eaa5560f6 = _v8999_ed30
        for _b6542 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _b6542 in _t8cef47f25e:
                _p79912b_x = bytes.fromhex(_t8cef47f25e[_b6542])
                if hashlib.sha256(_p79912b_x).digest()[:4].hex() == _t8cef47f25e.get('f1', '')[:8]:
                    _4e830eaa5560f6 = _p79912b_x
                    break
        _q16421b_85 = bytes.fromhex(_t8cef47f25e['d'])
        _9bb3310e386 = AESGCM(_4e830eaa5560f6).decrypt(_q16421b_85[:12], _q16421b_85[12:], b'')
        _9bb3310e386 = bytes((_n0c1d27ecbd ^ _sea570e704 for _n0c1d27ecbd, _sea570e704 in zip(_9bb3310e386, _7bf27adc1f(len(_9bb3310e386), _4e830eaa5560f6))))
        _9bb3310e386 = ChaCha20Poly1305(_4e830eaa5560f6).decrypt(_9bb3310e386[:12], _9bb3310e386[12:], b'')
        _r0723105c = zlib.decompress(_9bb3310e386)
    except Exception:
        _r0723105c = b''
    return _r0723105c
try:
    _e = compile(_ndb5201e1(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_xf08449fc(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_f3a19dda3(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_r5c9b62e9(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_v45984e89(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_db9b7cdf5(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_a4475d195(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_ma7b912fe(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_w76327700(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_x42343cd0(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_d7c7d9380(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_dd6ace1dd(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_t8e5365b4(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_k69321da1(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_w20d28d43(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_r3ad01576(), '', 'exec')
    exec(_e)
except Exception:
    pass
'S-Protect bootloader v7.'
import sys, os, json, hashlib, zlib
_5d279f4f4d2a = getattr(sys, '_MEIPASS', None) or os.path.dirname(os.path.abspath(__file__))

def _7bf27adc1f(__9c0bbe6e626f, _c6e3ff7d4a74e2):
    _r0723105c, _x9dbdca697bae = (bytearray(), 0)
    while len(_r0723105c) < __9c0bbe6e626f:
        _r0723105c.extend(hashlib.sha256(_c6e3ff7d4a74e2 + _x9dbdca697bae.to_bytes(4, 'big')).digest())
        _x9dbdca697bae += 1
    return bytes(_r0723105c[:__9c0bbe6e626f])
_49302_52351b = [_t91a0b74a, _c01e7ad7b, _m28493c79, _w99b7ff0c, _bd1bfecff, _bc327e408, _a611d6a00, _f06416921, _t1776ec44, _sf5f0e8b9, _s8a593e01, _fbc236b25, _m83cd87db, _f73c0d6a1, _cb39a96ff, _sdbb96965]

def _0x698f8f65():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    _v8999_ed30 = bytes.fromhex(''.join((_49302_52351b[_w3635e8027411] for _w3635e8027411 in [0, 1, 2, 3, 4, 5, 6, 7])))
    _t8cef47f25e = json.loads(open(os.path.join(_5d279f4f4d2a, '_runtime', 'loader.pye'), 'rb').read().decode())
    _4e830eaa5560f6 = _v8999_ed30
    for _b6542 in ['k1', 'k2', 'k3', 'k4', 'k5']:
        if _b6542 in _t8cef47f25e:
            _p79912b_x = bytes.fromhex(_t8cef47f25e[_b6542])
            _r24261 = hashlib.sha256(_p79912b_x).digest()[:4].hex()
            if _r24261 == _t8cef47f25e.get('f1', '')[:8] or _r24261 == _t8cef47f25e.get('f2', '')[:8] or _r24261 == _t8cef47f25e.get('f3', '')[:8]:
                _4e830eaa5560f6 = _p79912b_x
                break
    _q16421b_85 = bytes.fromhex(_t8cef47f25e['d'])
    _9bb3310e386 = AESGCM(_4e830eaa5560f6).decrypt(_q16421b_85[:12], _q16421b_85[12:], b'')
    _9bb3310e386 = bytes((_n0c1d27ecbd ^ _sea570e704 for _n0c1d27ecbd, _sea570e704 in zip(_9bb3310e386, _7bf27adc1f(len(_9bb3310e386), _4e830eaa5560f6))))
    try:
        _9bb3310e386 = ChaCha20Poly1305(_4e830eaa5560f6).decrypt(_9bb3310e386[:12], _9bb3310e386[12:], b'')
    except Exception:
        pass
    return zlib.decompress(_9bb3310e386).decode()
_69440 = compile(_0x698f8f65(), '', 'exec')
exec(_69440)
run('main', _5d279f4f4d2a)