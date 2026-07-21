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
__0x8849614a63 = 'a50e1b125977b59c6593921bdfe6127ea8f01c5d034066dbe162248dba20a32045acd2053458e274ad00f1f1f34ac6c356071515f62566914a5e531f010d863e0a0121625ea0a80cdf9667d836cbdfe3f747e0ce6deea7313e95ac3744384efc95a213b6779c72c11d4ff0d2adc5a7ef9ae737e2bf7af8fbc313e379e480ee2d99d59d71698da6163d0af2f2f8e255961cd75d5a13a95b467dd26de05b14af463589dc7ca51cf5b08ea5d4d4a64328b56333021f83c2792bb0f7b6af8efae6122ae2a3a67ed5e9cc13d3ea00641490d038b45636e133d01a9319be6f6e9e67793b0f7079f076fd'
__zaa0153eb = 'b1cb75e63a7fe1a84447c313a00ebe7e429f8ebd343021d5005908bd48ab1b346e76f725c2de2db15628cf8d82d620087938a5a4fff3ad7a0ddf8fd345bd618c9e238f1b2b062de0a31b9fb1aa5dc41a2481531974fe6dbcf7916b6b3d928565e1990bbb61e4d3c446cfe06aa2'
__q2bd3fe1e = 'b5747b8d86dec641de1e2855b67258062fd90f3b095b6b9e8bb2dc4226dba1d76ab932061e6d5c2c5f328fbe9469c4a6c0bab3ec8e378e1e768b8766748db871441345ae4e927d508ffc730dd9894c7b63ee3ae5ae9356d3652fad07c01cf8d41936013ce4ce5ffca4f3589fe1bc6ab4f65dc7832b6e48bb40eaa226766d3ff30f312a0b7c87'
__sfacf353e = '0b6f196e93925b43aa83ea45e8fc57c62c95faedbb9ea0e0371677a519ce3fa7e81ec3ac9d3600f8e82258bd3f67420df6bfae73398b2a5f4de10511a29c89fb7ce17007aab117d1e0b72204211fa13c10fbbe2934335c1c650436e97bd542224ae54cb33cc0b73e420895c390728e4f0ca83111d1f986c740f046a0bb1eaa9285364d57f5cec1f3773cbb0c1ed6b533bd1ac57b81545d4ade0c084d38d05fd4665957ad8da6a7fc7ca21adf6eab4f9b5da26127cb5fa4b2a5b149e04a2b965cf67b1d395cc96f3dcd96d113adb3ce41364b5d1d38f8b286777d23c32ae42327581c73299fd210c995255fba3f1d8c0486a978ab00f2ddb13f61530371fa089d7dc96b97493b844973e9284d1dad8eedada0d1ed1ac82c13d6d544abd498cb'
__c870e13bc = 'e9bae936f4251d9285afc0673483d9287a4cbd5e720bb70a522ea9e3094d204803018514563da941ad189b8c2ddb6cf8c8e06959f18cdc062a98867830dfeea06b56e9450edb7e07ca9ba1c688420f1e6734400334f699f4ef0391b1a098b823c10963336ec97fe8234f2a3f060acca945f3417ac112a4460b5d4aa04f8c8fcd39afb19276e1a814f696aa4702e8551946f50c3ddc3c0dabc187a0a3caaf291fa42e7a3662ea2b8f6a982f5aca0ef45d1687e3e018bca7b58ddd156fcfb097a190ba8e155e805915fcbba2ad03139710cb981db3eff486ed6ffa9c4430ff7e16e550f0fcf742a2d8e017c0edc6dde0ee2998b29fd87bc52342306c567489b4457178f308baeb'
__x6e1a41d6 = 'cb01d1416411f0c1eea884768236c70168a89f5033dfbd6f5b42bee29b37fa115341c5a987370deb0efa4bd465cc04f1cd7154c99e01b0c67a9e884d27c78ba3914c0ab74e78585bc919d1d6bb2d50eea016ca20ae28ccbc9887c7a35609f03d3d0ecf04dd8ef20ff0b854894f86eea516c8ad879cd02360703995136673518d76e316a5a188c59bb03de090103d6b5b0ac96550e04d62dffc3142d5cf132cd46bc09c2fdec3bf43ba1157ae05fc5875284cc0942c52f50135d5eb4047cc4efbea9b3585b9512c167c0626fb93c7965468d514d45379feea614f2a206e12dc360274a9291f9029f4f371104cd9d67e4ce7f5a62137b74f8336819722bdfe75c027c556d4b03cd594c1a1f8d43ef1994b3f2c102258fe00cd7f10561787cb8d100107181a01e8543337'
__c9ff820e1 = '2d41573bc08759808c5d7e604aed9debfb094854bbf46ccf624b9f2d5c8f3b5e366aa29913f2a490087c69644fb18de37253d15aa5534c1a83323406f9238045b3d4cab4a8021e368711513c87e266a534f02f99e42041f2fdc13ea99c4e7baea98d357d9d89b7eb9698'
__na16d977f = '0941a6f61ef3df94f01f8867914ed29f150cf33960d4d68c8fe5a3576f8decd999f030e7d1923aa5d85f8f8b40281fd3a318dc233d7fc03718a25d98506675cc2080bb7b14ded2da9b4965ec3f65d62c432fd411a9a770012cfa62e3738450a4e9cce65d40b48268313ebf1f0f9366788fadf3fc9b291f1d1d6d5b14a9ec01dbefe01520198ebfc1197b6fb110d0cec6028a4729ca8f11b5daee367b3e928e163fcc651279ee1dfd525bd0d99f9e2ca6aef1a5968bdedadcee3287329875f39b7c41f0ab0b4ffeeb819f8c346675b4478858448545fdbb28d5e95da5a0c581d9d7643a5d4ca96d7c68d2cdf7c6567029fa6c025f089d54918cba36dd8c16ef6d1d9fafe46274acffb43a09a7ffd8fb58eaf22b8e7fba7e0e76ff2aef'
__ee8f0eb61 = '182b887857a715348e8cd9932c8f372b41260306dc15dce3c17ea2b27d4733ecd847d05924731395982cf05e3499b6d6be9373fbc1c90772d081090f9de121f7e84940af5979a6e3c86480026f180320ff38369ec142fdb32567e5440e1abe403b87a2526a907dba4900a3e3e2810faa975719ee12187b109b5c8d44db2ee2a41f7e6f4a5a147dd809a87c4d2a5224132052e4a0b5bd93f82733d5e72eea2299aca633f1aa8dd10ac5a3b3df0e632369dcb3fcd93e3383884bedd40ba1db62330c46170e0b515de62906a81e48e1f45a95772e0c58d5be91cc2c0d147114c34293ee886f1f5a30d40c980b8745b14612448229c55ed88325271339a821ea13262ca56533de'
__dc167b2c0 = 'feab7588ba28350628433ae71454d9881c96cc423c8a28a668a3cc3c869e111132f0a78ed5f56a5179a7c8a5e962bd85b26223c36b718a87c5e75e66d67a2c2917a5299cca1d152cf8e8ea15b0880b79b38fc5425db0dfca9870ac1708aafd755548d95b0e60b0bd515b971f6e0a02dd3b5e3e3bcedada367c67646e137e25a777'
__e2ccc4cba = '27d2f06f7568d9e4a7a3b43911a90527ae2eda52f3854f4a48fc73908ba6032330576fab1f9abfb735576195e5281197b823c560c8927c4117c8c63050dde00d00e1aedcce9307c7b6f848585cde0a567dcc1742c8b91e0aa19a3a5ddfef4c1390707b72d54a7efd3170a593767619aaaeff75a9ba53636ad84a0129b76fa79098e228a6480829a5598d659cd4'
__ac78f4a8e = '9c7de6a4bec99410e9a8c25d55d27c2bb2b8cd8c51f1c9d0809cbbafca18705cc790d94d48993a5bee298c41e0cdef62289c1e559cf90a7608121c4875085c9d81cd06eb789a44b23f8066702e2cee6498603ff10dc84af53378c984a6f5f1355e1b201051e4ffbb9f92f2fe43d54c39176552c2d30dfa1faea8390eacd56b989e1ac467449026a1fb7fec0eee541a81cbaf4b627fea08f4925577f46c127281462c8a5a055e2ac7e48129fbc6f7a2ef46bce4831596b72351f9cef55a659e45c2212c7ceba4ddfe6e9edaf4f46ef526e3438e48d07006c0cfe2defee1a3e8a25f739f24fca9cb39764abc2edff6afbe72b3c60fbf3c5c'
__qa3e10d6b = '7b2911e81714820fe10ff885b0afee449465a70d4d9def71952f21f5e4b3e7126d2f0624e6ba655ed6d5f701bcb71a19547b52ce5ee8f17ff45af7b428968ecbc65531a7c8b0e5063664eb8f7b90ecdf3515923d91634bf61ce968af95c2282c4da094b02a7d4acadc00678e0c150aea2fccaef442075c93e0bae19f4ffecae3b4e5b1436e1253d749710046635fe7ff2d9daa85266554'
__w023aa20d = '63f54fc7008d1d0ad1b0e2a12439fc430b3ae4f5cf8949562d2d95516a4921da974deb3592ed8bc18b500abc5971ee6dac3d51324be91eb33cf8589c6f53f87575790583d863d382fa256cdd079cee9bba4e3b3a29975f8f65c7cd02b8491a5af84e4dcf319b08011f1fe65e344e0509303177f21fc38d1949c32314837b3a8a4b91ff7b3f41f2b3b3c1eeecd4b4d440550c6f32693db3c0e4a08f2bd9fccb3480e83b78bb3976f5f640162d4f94cf77d9bff0e711b3a6906ee524a79f4692ee327f8abf4a090c0ce7693159eb6da9a807fa063b30ce18ed5eb65905c91ea67fe3469d2bd62be2d47d952988238c38164408b041cb9f6abf97bc6c3e4ceea5ecb27615fce2abecc8b727f2280bb64a9acc2eaed9'
__pb3b7754f = 'c1017205be8af402440ca8eeb9f015760f29cfa8d44c0e9a73510ac1a2770970b07573aaf917a267d1608c5b3a648e0b3b77966e4c1afd864ee0aabf84e4cafd0e1d9eedf9048012b300b64f1c701fb5210f0b3fa4fdbbc3889f04b1f6cb5e5461ce70a40eefbd32a92531430dff96d4283e68ef058fdb51bab884cdc202286345'
__vd2c90b0f = '34631adf375d1d7c49d3e3e5ed1dfa79d48518e6cfb6762a33cdcb333691d2043b2f4310289a0437e52fec6dec4b0a033de42c5cd1e748f3bb08398cf16e9919a135d6c7ab98b570f66ad1b6e402b71f1c4240e3ca8df79b28b96fd064793869f47508021f750e000b64f28f3bc889b037e3f97b89e98d89a839a35924162af1985323e230a54376be5e97260c099b5501b4503b4051cfd043014ccd433c1f7a2c662910c3d9c87796c1f4e02ae222b8a32c271ac2bd79c43f212415f8091b161a4ebcf28663e7140604dd8617e1d90a8a1ccff790bc8263d61fa7cd68471d677de0bc05cd0813aa7b4e0d868978694225f2dbc22f8511dba7201c0c27a647c8c0f21a97eeb8137fe1ca604dd2ba8a705f97839f7a1b'
__f53cfe254 = '801241899863f1536bd13f11ffffafff5b668360b8da96022b9dd1a6e4019facd61c782de519e3dc2d5a8debe76d1de7077efeaf71114dfdaf98e193b3cb19632f0f78fe06949476a9325f1972f704f900405e5f9c8a97a13eadc96c8830f8dfc8010e196f99725e17ba7290b7bd8939840d8af13ad269a091f120576d33ec37a79dfa15ba01eaa9b02f8b5e458c2e4462141e8fa79d2683cbf1d754e8a57c73798d2775315b5da7ca4df49d106c5e85546fa7683b7d308b5ad0ad09412a912a5dabcb0a06e731fb4451659f64464649409329c8d8b3ef2a2e253cab6e1807c7ca54c6e8e5a63feb0dd9d584450deb5755d91e3fc6f5e295cf6a31a60c7a6119643c51fdde823e'
__q2d82f6d4 = '6bcc4bbac5e3c39405dec5b3f31a04503647297804503731c4106629da74b1e7385d68ff22ef8156543d9abec93680d12459e8da1ece2abce417dac26180a70280e3db28723f3cba9205123d055ce02a27d412b08a87f42d3e5c078aa1eaf7e9bb08ce7daf3ec0b7103bc8fe62ebca8908ff14f24cf89046c98aa5b90f3cf1c186096a6a3c7174d2609688375ba905681bcbe88262d0c5c1e0ce66f4dce590b44f508571b5306ea96553d89c1a6fb86c1f2222a987cf04278abdd1794c70ad1eea66dd0e5596f9c519c4f6f0f11496cebe645c5fafbe92be6d9d7814f8563ad0185579d8edb9bccc3a71d126c8a46b8c04f2d0d5357f0d219214486788a3e89473ae5f5759d89eb4916d678d8627222961ff49a9'
__rb4cbdfa0 = '287da20b14293d1b51d1d3f0be8f580108a463089189af3ff142dd1d0a0e4587c9539303ba3440f16a4ee3a8c1df61f3d6130def94cfafa8b6a9c3c43a78ddf6a575bc17b5576ab86df4695ca5d89cd4dd867e885c8e55ef06c45e4e798f23d3d1179fd7c10c7242'
__a42b24f52 = 'be8a55bb8f7f8cdc6264d350ea7653b2423c838fdb8f5751f3af00b619946d0b4b2e310bc3349fddb47472f6788d42aba40dcff9989fe58b042389535186df4527312558ba43167711737bf71bff3aa705ad22abea0e67e6cdb782dc7c528c5a4415e4417daec9002cb0d62122f64d226788170c5af5f4cd0c4ed7e07be25ebfb1f4fa3d5e45dd039924d0'
__r8006921e = '1347194d73fa3436ef37363ae916d66706836c9ea2bab767d709593a4f4e0a2e857706b16f9402141afb758c1c2a5cd10a3315821f2c1595f6e9f6f4c80b945b5add4cceaa107d751d5b0fd7813a7062dbc1d997e88dc819efb5e8395ab7d46815f24f3d8667efccb9e4c2f2950a2f8dee5721295cbdf94bcbe54f4f78cb64d5c4ca67cd6c45d99440dc79f18a27e6df52bae4e57f0dc5a181c326e5d788c5a12bc2884d0e473317727762ffb01f3ca5dfa619bed69b16966c01b5e298ae9ccf81ddcebbc56e959cd269f200c68ee1d19d4199f453dfd92853a13ea71a08a0d59c1e54eaff'
__f8ae56a73 = '5bade37b5ba67db21035cb01c2407b6ee0e3ab8d825f73364a25e7dc1cf01b02b9c8e092704d690c2613d135ed89111b992dda9dcc87ed039c667427a90ccbe385a3d12b3f91ce7804b96dbcbc5444747e4dadc5b0f5ad9737b686456ada1762e25a3aeba67daa72ce2d9c1d59ec717e140032ddb01f2959e97e1ceae8b718638e6cc0925f4d10f7148fa6eea6f4c0c0c1d593860eeba7fb5ea0439445a24e7371e34272e0d0c388ba66871d28e48eae2bdf0c87e82ede2699599231f9306331751cd4'
__q1f048259 = '29edaec65afce7e20f7ff0bb8ed114ed1c51e03354e8e99fe255eb0beaa35e90481f206d2db91f8de9fa29e3ff56735b4d8cc5477591dbc24fb2c615819cd468aa48e9ce424e7fb3190720d60a8ab78228174ff863e424e9f6f56d67c69857f186353916d6731c54722317dac94797715df244029c44c3bd00bd14b935e96608b8a2d314ebdc7f82d6612aa609db32447265e2f86cd548fe23b20dd500d87f79f4f51e3c58cee5b0bec13f1a984495eb3868df0b7583e260e18056befed9e434dacf'
__r38fbb58c = '58e5794653bbdadfb72c9afe701ac6ad4605013ee00b053d38eb22141040d141745aea68277f87fb3e75499f97b68c7353f3d3765073e990f2a8c0074caaa72155e793fa92ba4c5df6df8483d7349487f1d84a894c224e3c29d23a91cfd41804cc6df76f06f38bb30259516e3fe090351d5c225c148f1e3722ff7c2861f50428646ef3042467255aba0e5d768db218ec03fe83eeec9633c2d1b01e797be6467c364443e94b76ce447ed58d673949c6b46fa92ab96d3abc9e2a2cbdd4438f3a096779bbe212a962bd24e0b425aecd04084287f70032b1febe2caa6c723ba372180116ede7f7f05540d48f4029addf70eae22a79f9c3c35135ec1d66bc93025cbfbf235369450a72cf2af90ef78e3590fb0c6756db685f77c1ffb3977710dc'
__e0453adc1 = '847191244c5a6238e10018554d1d61196e82fe5b9118e26c80846e206e03e8d585dab0c4495c50f70184829ad8d03100c9b1ef0d373e952b559f8fc8dbbb628e43a41591e370583a389acbf0defb46475153b7d54d7d6dbb5d281053f17be2ded42bb8ace45d245a4ec76ffd46428476ccfefaad569a74642dfb6629c93dfea1734548433b'
__b6e053bb7 = 'd5a81024ad8d9e4fb13526ddbb1cb6475d1e71b42a4ac6b3409d52e83817c1d6d0a3d64a2d5d821cd220c696c768b93f36fdd4838f27f42203af0277463dee81cff5e03bf82b405a43a0a868859da25e1d2f9cf964e6e4bb0b6c3954ed690637f4aa7e7c65d588eb56d4751e9c58331195a25a5e11d8ec574cce59'
__e5211bff8 = '47d01900afe198ecf3bed524c1947e0200b5890f172fb63f8f98edb68aa799c1c70f3b948950bb2a714b7b840651e26701286b3536a1ead1684fdda6c03092c54a6e73fc1785c1aea57376af9eb63acc0b3893544a1428d1ca0e443e5f4cf2e522744e8cbb299f8c5eb07936e5d3cac36064437dad6af42ab87a1cc8ea179ed61c043d3ab268d1420608887e103731effb786735debbd805f5456166c8b8b0cc1542ca6da3efdd9d4492fcaef9a82c872691119241ab38f6f54c99029d5c40ed0bca39ae22364a7c434f569e8fe0da1683aa7673229558d65759e55dc2b08641c9efeb3b511e7267223661be3b0f6fe8d5bc7ed24075cdea3f2c454ec61c1cc73a0df0a0abfdbefa7282fdc674d1b336f8bcd2d577e639297177fd2438f3c0ef2ba1'
__f190605d1 = 'aa147ad70b442649017ca84362551451f16dc33a044e97fb4231e5bcaeb3097f7d1672d56c56dfd246428f2b3fcb77ae78bb959d486ba7ae512114babdf120ada3b5e342972d35a5c5d2f658ba49e3cf341189ebd32bfb59025af4e93215c0862a3f6ec076fc6974206ab7e4017990944585a1d4f4d055c2baf04d9c2dae63f2c57017cffeff358cdead1abd330182ffea62e2d64daa44a9bcb12c661955cf5ffa562962f3399470784d63db7f9638afd9c8e1acd599c43861efa3bd0031097e5a62cbed8dbe641517d39e5901bb62dec0f92d5f70e85399eddd39d72578ecc3f1cd0031db4a1b3f'
__c5389a830 = '217b1d153f4d0299c67bb2c69659122b89df70ac12ff77738cb372bf16d1625cfec0ced1d8fa508f5085fa2a25de93c5cd964e763b2f198e9b434c4b4bb92c4b8fd1d1858f3234930e7ebc72fe3f5aa8d5b3ebb2992097da683500cf44ff3ac76e4cb6d03265bbbb90e19e9230522b1a7d22d67fc4eb3737a8528e21858be0fba898421c35086c2bbd8fb85972af467b76bbb934d6bd21b2a2073092e0f2673c779a68aeb030f769b7b64c5eb64d6664f58d6486eee1cd5734d6df7730afdc9651fae8d89bd17d9cf09bf53936828f56b13b'
__v862783b1 = '75609cc3cd7774cc8e09b6b3e598a2f641626e20760bf1d506e8b27e29711417a3132c0e666cad369f2c8afda9b77b54319085eb47ede430fc86deb58ab72a3b2555ad8ec157874cbde63462210621584d30145e4be0fa0ba634a2f557ca64842d30b30fbc9d694fdab0dfd1ad74352f27b2365946fa46bba1a78cf2e13faa730980066b8592169ddede5b7c0bb999f348052b635189ca062cb56bfeff820cc59e3468338b0cfd414f2152b8953beb21743ccc2537f66663ee8ef1afbb70bed6a30b5bb8e73609e20bcef6f69d05172743b8c5656a63f23ab6ea1beb7087f5538faa3c84bf60b138737908ac8a6d9a1ab6'
_w82456408 = 'e163770f'
_ye63e94d5 = 'b13a99c4'
_y74a0447f = '6968c3a4'
_xf54d62aa = '312c10a5'
_t0cf72434 = '2489c825'
_c737892e9 = '53e559c9'
_te72b1f87 = '29e556fb'
_0x62f96f446d = '805d8f20'
_dc43904eb = 'de246f1be6ae025d'
_ec62418b9 = '5e912835bc27ba45'
_c81c05eaf = 'a2d6e8dad44c88b6'
_af7c273f9 = 'f974521c787e9da7'
_bb9e9becd = 'e49ff15c84a89f3e'
_v880653cf = 'db30d6857c0cc91a'
_fdf66f150 = '3c15a10ae2b611c8'
_zac329b60 = '8c49350f6dcf1e0f'
_d1f12d935 = 'e163770f'
_vf11e2a74 = 'b13a99c4'
_q81f206c2 = '6968c3a4'
_0x354d81fbf6 = '312c10a5'
_ze71c1f59 = '2489c825'
_qe0ecc74a = '53e559c9'
_k97920be4 = '29e556fb'
_pc4910734 = '805d8f20'
_d669f5171 = 'de246f1be6ae025d'
_m83d99d39 = '5e912835bc27ba45'
_y1189f9b5 = 'a2d6e8dad44c88b6'
_r4214eddd = 'f974521c787e9da7'
_m2b0c5bb0 = 'e49ff15c84a89f3e'
_ve34f1e29 = 'db30d6857c0cc91a'
_e4a71034b = '3c15a10ae2b611c8'
_b63266f5d = '8c49350f6dcf1e0f'

def _r42dc564d():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('617f29ec45f452e6dcce880e02c45c5d91227e10e1dac0fe84f8955984b9052bb75c9fe424878d0f78ad36e0be3b4a834ff6ab52785662057116e91da22832f6')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _e670123d6():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('25e85093179dd49d611c72df7ca3f71d2d40f9f5164bed2af81d43349171a356e7eb5a6a05df7891e3388a10b94f76cf782f33ce2065e955eb14f1ddb6fd8f17')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _dc9b92109():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('bb2d902a6e267019c73a7176b58f09c7e9c8b3041f4db151a20a470e63e869c61338290a81515281692d70dc9ba3bf352231d0da18abbcbe867a72a3784ccdf6')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _fccb81ebd():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('e1588dfa3e959714e817ea1b38fb71b663e056b4867956b5a9072176214bd0bac5bc9593f10b8887ffd6ae5f888283fd1725cdefbdc2f0ec2f7072d415d4ca96')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _t9835f0c1():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('38653b0a716cc98d848626051651645860b458f7cbe69f4080592d88faf935457c4932443203c8aa5266a1a8f1467384fc1dd96e9c089d520016421064be8c2f')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _e87c66252():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('d4fb712cf1512b453d91c43d789c23f32f6e635d41ce63d94fb4d141e8c6b5e2c6c98fd00352c479dc326186e2128466b6eb66280885a7a706a778f7aec36e62')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _k65cbb260():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('25a6a6a6d89f3d2f465625f8be11cd7a4897fc705cf37cc2c7f66aef1177b22927f9bf592acda981a9cd15c9d9b92267b404e5ce1106e6eb3bf8a337955ed6e0')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _y8629fe01():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('54279849a8ca3e8ec0a78671ebf1af3d3fa3c165d3cee395aa0a1eab4f80f8f99876eab663dc03a618392a480276ce3aafe34850f68b8cb6afa3f3574c02890e')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _d88ed50cc():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('f24aca5c28ac5b7462ad6cf38cfea877fe6fcfb79465cb3be668a6418797d596edc047b4d12ab96d163094102df62623c9705a84ce1328af62939578376c82ba')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _se57bf9fc():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('5b48a147b344557a873bb632308ff3bccc1c02925cfc5cd23ab3cd6479cb7b80c3d11ba5fd9ce822c89eb77d076d4f39312c81039ae32d0d6e75a7613bccf466')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _c37fabb6f():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('80c759e127fec9d7d098211affa1333ee4803133e7f27dda0112f93bc2274af045c771a4a5ac20823940edafda7feeb8f9ea2f80ddc29ff579324f821a0bca16')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _q9b6fb8e2():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('126ce0545e6737dec8dde1a3df7c625b483ed42e7009be8629b9f0272a016a16dc3a228783410ad02a2dfb6ce6978fd7cfc415ea4d21a003f997c983e537da08')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _b362c9a97():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('2fb7068dc4225c6558a1939d9b93f36dd0a3a4fbb55bfef3c25e4c0ed145df702f798979c57434ddbe39af4c44a3f8dac02bdedc9299a0a3a3159c923886fb7e')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _v6fa81aad():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('d3653e3134680fd5019e154916d8951ef70ad16e90fa2b23f3462b2189b1e515d61fb2b55ac073512ce97356db94c9e589ad83351603a47895e11b40f142f181')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _r03317d0d():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('7404f413322132aac18ec766a2324453e085917d3f6b6d6ce039d146c1c15221bdf6a60a7bc8c02c6f4d7d68fe2088f7201cbf0de89a26cb8d0055c7c4d574ec')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _f156406aa():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('5f88fe5c342040f705c2df4c5535e440ea9adeca583e800c64b977ff2b6b02bfd799e7b3ddc0535c4c4a10b9f7e6483461ba769680a4840cd5131254f80c40d4')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _p001c6033():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('56385a5b6411a5257c05c660455312de619f9fa9b7dce1e2f0071fd995b29d8b9e9e2dd27331f0fdf100772673e03640855f7321173030578e52e7c1b9ebf173')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _y23003af6():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('f0a5aac10545000723d02f7f45638871fcaa220293e4c7e5d24b06065eb5d906c7f3bc9427658f6b6d5c9296fafed6b3cb56fb387d146896efbedfdfefb4f5c9')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _ya6e3f917():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('89dbc50de93633e7dc3a18c69a0dd4574f21c3c3d3118bbaf5ad5745566e45a24b2f75bc027594281afa7588653fba8e60bea9f5a11bdcd19fe73b7e1d99188a')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa

def _xe3f53c27():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib
    try:
        _v6822_b89c = bytes.fromhex('ce24e820509f1f4e5e411c11f0e2df93a2a4e9979fe313e2857183098a564ea4ee06add26828d11b114bfa585b92a6d2edc8e99c14d4274161e6966231935d69')
        _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
        _b3c379ae5a8c82 = _v6822_b89c
        for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
            if _g1382 in _t4510755878:
                _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
                if hashlib.sha256(_p0fff4f_b).digest()[:4].hex() == _t4510755878.get('f1', '')[:8]:
                    _b3c379ae5a8c82 = _p0fff4f_b
                    break
        _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
        _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
        _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
        _xb32affaa = zlib.decompress(_dc35148f377)
    except Exception:
        _xb32affaa = b''
    return _xb32affaa
try:
    _e = compile(_r42dc564d(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_e670123d6(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_dc9b92109(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_fccb81ebd(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_t9835f0c1(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_e87c66252(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_k65cbb260(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_y8629fe01(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_d88ed50cc(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_se57bf9fc(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_c37fabb6f(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_q9b6fb8e2(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_b362c9a97(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_v6fa81aad(), '', 'exec')
    exec(_e)
# Import order matters
# XXX: known issue
# monkey patch for compatibility
# pylint: disable=unused-variable

except Exception:
    pass
try:
    _e = compile(_r03317d0d(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_f156406aa(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_p001c6033(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_y23003af6(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_ya6e3f917(), '', 'exec')
    exec(_e)
except Exception:
    pass
try:
    _e = compile(_xe3f53c27(), '', 'exec')
    exec(_e)
except Exception:
    pass
'S-Protect bootloader v7.'
import sys, os, json, hashlib, zlib
_fc7981a92422 = getattr(sys, '_MEIPASS', None) or os.path.dirname(os.path.abspath(__file__))

def _8ee69f5f20(__2996f58668b0, _724c8a95b19958):
    _xb32affaa, _x42d57a231a0b = (bytearray(), 0)
    while len(_xb32affaa) < __2996f58668b0:
        _xb32affaa.extend(hashlib.sha256(_724c8a95b19958 + _x42d57a231a0b.to_bytes(4, 'big')).digest())
        _x42d57a231a0b += 1
    return bytes(_xb32affaa[:__2996f58668b0])
_1467_3ed7b3 = [_w82456408, _ye63e94d5, _y74a0447f, _xf54d62aa, _t0cf72434, _c737892e9, _te72b1f87, _0x62f96f446d, _dc43904eb, _ec62418b9, _c81c05eaf, _af7c273f9, _bb9e9becd, _v880653cf, _fdf66f150, _zac329b60]

def _0x0dfd011c():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    _v6822_b89c = bytes.fromhex(''.join((_1467_3ed7b3[_w1be73c697df4] for _w1be73c697df4 in [0, 1, 2, 3, 4, 5, 6, 7])))
    _t4510755878 = json.loads(open(os.path.join(_fc7981a92422, '_runtime', 'loader.pye'), 'rb').read().decode())
    _b3c379ae5a8c82 = _v6822_b89c
    for _g1382 in ['k1', 'k2', 'k3', 'k4', 'k5']:
        if _g1382 in _t4510755878:
            _p0fff4f_b = bytes.fromhex(_t4510755878[_g1382])
            _r20920 = hashlib.sha256(_p0fff4f_b).digest()[:4].hex()
            if _r20920 == _t4510755878.get('f1', '')[:8] or _r20920 == _t4510755878.get('f2', '')[:8] or _r20920 == _t4510755878.get('f3', '')[:8]:
                _b3c379ae5a8c82 = _p0fff4f_b
                break
    _q1ae44a_14 = bytes.fromhex(_t4510755878['d'])
    _dc35148f377 = AESGCM(_b3c379ae5a8c82).decrypt(_q1ae44a_14[:12], _q1ae44a_14[12:], b'')
    _dc35148f377 = bytes((_n413ad7cc7c ^ _s7c775f827 for _n413ad7cc7c, _s7c775f827 in zip(_dc35148f377, _8ee69f5f20(len(_dc35148f377), _b3c379ae5a8c82))))
    try:
        _dc35148f377 = ChaCha20Poly1305(_b3c379ae5a8c82).decrypt(_dc35148f377[:12], _dc35148f377[12:], b'')
    except Exception:
        pass
    return zlib.decompress(_dc35148f377).decode()
_77579 = compile(_0x0dfd011c(), '', 'exec')
exec(_77579)
run('main', _fc7981a92422)