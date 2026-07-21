import platform, sys, os, shutil, subprocess, tempfile, hashlib, base64, json
import threading, queue, gzip, zlib, io, marshal, dis, zipfile, ssl, secrets
import socket, configparser, csv, re, string, xml.etree.ElementTree as ET
import collections, itertools, dataclasses, enum, functools, pathlib, glob
import importlib, ast, gc, weakref, inspect, timeit, mmap, atexit, asyncio
import concurrent.futures, contextlib, tarfile, codecs, ctypes, heapq
import logging, pickle, struct, hmac
from datetime import datetime
from urllib.parse import urlparse, urlencode
from tqdm import tqdm
from colorama import init, Fore, Style

init(autoreset=True)
WORKSPACE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_workspace")
os.makedirs(WORKSPACE, exist_ok=True)

CORE_STDLIB = ["os","sys","json","re","math","datetime","pathlib","hashlib",
    "base64","itertools","collections","typing","random","socket","csv","sqlite3",
    "threading","subprocess","zipfile","logging","enum","functools","decimal",
    "uuid","shutil","inspect","io","struct","array","ctypes","platform",
    "argparse","string","dataclasses","secrets","zlib","gzip","bz2","lzma",
    "ssl","asyncio","gc","ast"]
DEPRECATED = ["imp","formatter","pipes","distutils","cgi","telnetlib","crypt","imghdr"]
THIRD_PARTY = ["tqdm","colorama","cryptography","numpy","requests","rich"]

def _is_normal(r):
    ep = r.get("expect", "pass") == "pass"
    return r["status"] == ep

def _calc(cats):
    t = sum(len(c["r"]) for c in cats)
    n = sum(1 for c in cats for r in c["r"] if _is_normal(r))
    return t, n, t - n

def _abnormal(cats):
    return [(c["n"], r) for c in cats for r in c["r"] if not _is_normal(r)]

def basic():
    yield {"name":"Python 版本","status":True,"detail":sys.version.split()[0]}
    yield {"name":"Python 实现","status":True,"detail":platform.python_implementation()}
    yield {"name":"操作系统","status":True,"detail":f"{platform.system()} {platform.release()}"}
    yield {"name":"系统架构","status":True,"detail":platform.machine()}
    try:
        import psutil
        yield {"name":"物理内存","status":True,"detail":f"{psutil.virtual_memory().total/1073741824:.1f} GB"}
        yield {"name":"CPU 核心数","status":True,"detail":str(psutil.cpu_count(logical=True))}
    except ImportError:
        yield {"name":"物理内存","status":False,"detail":"psutil 未安装"}
        yield {"name":"CPU 核心数","status":False,"detail":"psutil 未安装"}
    yield {"name":"磁盘剩余空间","status":True,"detail":f"{shutil.disk_usage(os.path.abspath(os.sep)).free/1073741824:.1f} GB"}
    yield {"name":"64 位","status":sys.maxsize>2**32,"detail":"是" if sys.maxsize>2**32 else "否"}
    try:
        r = subprocess.run(["nvidia-smi","--query-gpu=name","--format=csv,noheader"],capture_output=True,text=True,timeout=5)
        yield {"name":"NVIDIA GPU","status":r.returncode==0,"detail":r.stdout.strip() if r.returncode==0 else "未检测到"}
    except: yield {"name":"NVIDIA GPU","status":False,"detail":"nvidia-smi 不可用"}
    yield {"name":"主机名","status":True,"detail":platform.node()}

def stdlib():
    for m in CORE_STDLIB:
        try: importlib.import_module(m); yield {"name":f"模块 {m}","status":True,"detail":"导入成功"}
        except: yield {"name":f"模块 {m}","status":False,"detail":"导入失败"}
    for m in DEPRECATED:
        try: importlib.import_module(m); yield {"name":f"已弃用 {m}","status":True,"detail":"仍存在","expect":"fail"}
        except: yield {"name":f"已弃用 {m}","status":False,"detail":"已移除","expect":"fail"}

def thirdparty():
    for p in THIRD_PARTY:
        try: importlib.import_module(p); yield {"name":f"第三方 {p}","status":True,"detail":"导入成功"}
        except: yield {"name":f"第三方 {p}","status":False,"detail":"导入失败"}

def runtime():
    tmp = None
    try:
        tmp = os.path.join(tempfile.gettempdir(),"_envtest.tmp")
        with open(tmp,"w",encoding="utf-8") as f: f.write("test")
        with open(tmp,"r",encoding="utf-8") as f: ok = f.read()=="test"
        yield {"name":"文件读写","status":ok,"detail":"成功" if ok else "失败"}
    except Exception as e: yield {"name":"文件读写","status":False,"detail":str(e)}
    finally:
        if tmp and os.path.exists(tmp): os.remove(tmp)
    try: yield {"name":"SHA256","status":True,"detail":hashlib.sha256(b"test").hexdigest()[:16]+"..."}
    except Exception as e: yield {"name":"SHA256","status":False,"detail":str(e)}
    try:
        e=base64.b64encode(b"data").decode(); d=base64.b64decode(e).decode()
        yield {"name":"Base64","status":d=="data","detail":"成功" if d=="data" else "失败"}
    except Exception as e: yield {"name":"Base64","status":False,"detail":str(e)}
    try:
        ok=json.loads(json.dumps({"k":"v","n":42}))=={"k":"v","n":42}
        yield {"name":"JSON","status":ok,"detail":"成功" if ok else "失败"}
    except Exception as e: yield {"name":"JSON","status":False,"detail":str(e)}
    try:
        q=queue.Queue()
        t=threading.Thread(target=lambda q:q.put("ok"),args=(q,),daemon=True)
        t.start(); t.join(5); ok=q.get_nowait()=="ok"
        yield {"name":"多线程","status":ok,"detail":"成功" if ok else "失败"}
    except Exception as e: yield {"name":"多线程","status":False,"detail":str(e)}
    try: yield {"name":"Socket","status":True,"detail":socket.gethostname()}
    except Exception as e: yield {"name":"Socket","status":False,"detail":str(e)}
    try:
        o=b"x"*1000; c=gzip.compress(o); d=gzip.decompress(c)
        yield {"name":"GZip","status":o==d,"detail":f"压缩比 {len(c)/len(o):.1%}"}
    except Exception as e: yield {"name":"GZip","status":False,"detail":str(e)}
    try:
        import requests
        r=requests.get("https://httpbin.org/get",timeout=5)
        yield {"name":"HTTP 请求","status":r.status_code==200,"detail":f"状态码 {r.status_code}"}
    except ImportError: yield {"name":"HTTP 请求","status":False,"detail":"requests 未安装"}
    except Exception as e: yield {"name":"HTTP 请求","status":False,"detail":str(e)}
    try:
        ok=pickle.loads(pickle.dumps({"k":"v"}))=={"k":"v"}
        yield {"name":"pickle","status":ok,"detail":"成功" if ok else "失败"}
    except Exception as e: yield {"name":"pickle","status":False,"detail":str(e)}
    try:
        v=(42,3.14,b"\x01"); p=struct.pack("!I d s",*v); ok=struct.unpack("!I d s",p)==v
        yield {"name":"struct","status":ok,"detail":f"packed {len(p)} bytes"}
    except Exception as e: yield {"name":"struct","status":False,"detail":str(e)}
    try:
        lock=threading.Lock(); ok1=lock.acquire(0.1); lock.release()
        rlock=threading.RLock(); ok2=rlock.acquire(0.1); rlock.release()
        yield {"name":"Lock/RLock","status":ok1 and ok2,"detail":"成功"}
    except Exception as e: yield {"name":"Lock/RLock","status":False,"detail":str(e)}
    try:
        ok=io.BytesIO(b"buf").read()==b"buf"
        yield {"name":"BytesIO","status":ok,"detail":"成功" if ok else "失败"}
    except Exception as e: yield {"name":"BytesIO","status":False,"detail":str(e)}
    try:
        yield {"name":"CRC32/ADLER32","status":zlib.crc32(b"hello")!=0 and zlib.adler32(b"hello")!=0,"detail":"成功"}
    except Exception as e: yield {"name":"CRC32/ADLER32","status":False,"detail":str(e)}

def compile_crypto():
    try: yield {"name":"compile()","status":eval(compile("1+2*3","","eval"))==7,"detail":"成功"}
    except Exception as e: yield {"name":"compile()","status":False,"detail":str(e)}
    try:
        ns={}; exec(compile("r=21+21","","exec"),ns)
        yield {"name":"exec()","status":ns["r"]==42,"detail":"成功"}
    except Exception as e: yield {"name":"exec()","status":False,"detail":str(e)}
    try:
        c=compile("lambda x:x*2","","eval"); d=marshal.dumps(c); f=eval(marshal.loads(d))
        yield {"name":"marshal","status":f(5)==10,"detail":f"f(5)={f(5)}"}
    except Exception as e: yield {"name":"marshal","status":False,"detail":str(e)}
    try:
        ins=list(dis.get_instructions(compile("a+b","","eval")))
        yield {"name":"dis 反汇编","status":len(ins)>0,"detail":f"{len(ins)} 条"}
    except Exception as e: yield {"name":"dis 反汇编","status":False,"detail":str(e)}
    tmp=None
    try:
        tmp=os.path.join(tempfile.gettempdir(),"_py_zipimporter.zip")
        with zipfile.ZipFile(tmp,"w",zipfile.ZIP_DEFLATED) as z: z.writestr("m.py","def f():return 42")
        import zipimport; mod=zipimport.zipimporter(tmp).load_module("m")
        yield {"name":"zipimporter","status":mod.f()==42,"detail":"成功"}
    except Exception as e: yield {"name":"zipimporter","status":False,"detail":str(e)}
    finally:
        if tmp and os.path.exists(tmp): os.remove(tmp); sys.modules.pop("m",None)
    try:
        for a in ["md5","sha1","sha256","sha512","sha3_256","blake2b"]: hashlib.new(a,b"data")
        yield {"name":"hashlib 多算法","status":True,"detail":"6/6"}
    except Exception as e: yield {"name":"hashlib 多算法","status":False,"detail":str(e)}
    try: yield {"name":"PBKDF2","status":len(hashlib.pbkdf2_hmac("sha256",b"p",b"s",1000))==32,"detail":"成功"}
    except Exception as e: yield {"name":"PBKDF2","status":False,"detail":str(e)}
    try: yield {"name":"HMAC","status":len(hmac.new(b"k",b"m","sha256").hexdigest())==64,"detail":"成功"}
    except Exception as e: yield {"name":"HMAC","status":False,"detail":str(e)}
    try:
        from cryptography.fernet import Fernet
        f=Fernet(Fernet.generate_key()); ok=f.decrypt(f.encrypt(b"data"))==b"data"
        yield {"name":"AES 加解密","status":ok,"detail":"成功"}
    except ImportError: yield {"name":"AES 加解密","status":False,"detail":"cryptography 未安装"}
    except Exception as e: yield {"name":"AES 加解密","status":False,"detail":str(e)}

def advanced():
    try:
        async def a(): await asyncio.sleep(0.01); return "ok"
        yield {"name":"asyncio","status":asyncio.run(a())=="ok","detail":"成功"}
    except Exception as e: yield {"name":"asyncio","status":False,"detail":str(e)}
    try:
        with concurrent.futures.ThreadPoolExecutor() as ex:
            f=ex.submit(lambda:7*7); yield {"name":"线程池","status":f.result()==49,"detail":"成功"}
    except Exception as e: yield {"name":"线程池","status":False,"detail":str(e)}
    try:
        r=subprocess.run([sys.executable,"-c","print(42)"],capture_output=True,text=True,timeout=5)
        yield {"name":"子进程","status":r.stdout.strip()=="42","detail":f"输出={r.stdout.strip()}"}
    except Exception as e: yield {"name":"子进程","status":False,"detail":str(e)}
    try: yield {"name":"timeit","status":timeit.timeit("sum(range(100))",number=1000)>0,"detail":"成功"}
    except Exception as e: yield {"name":"timeit","status":False,"detail":str(e)}
    try:
        with tempfile.NamedTemporaryFile(suffix=".bin",delete=True) as f:
            f.write(b"mmap"); f.flush()
            with mmap.mmap(f.fileno(),0) as m: ok=m[:4]==b"mmap"
        yield {"name":"mmap","status":ok,"detail":"成功" if ok else "失败"}
    except Exception as e: yield {"name":"mmap","status":False,"detail":str(e)}
    try: yield {"name":"importlib.metadata","status":len(importlib.metadata.version("tqdm"))>0,"detail":f"v{importlib.metadata.version('tqdm')}"}
    except Exception as e: yield {"name":"importlib.metadata","status":False,"detail":str(e)}
    try: yield {"name":"os.urandom/pid","status":len(os.urandom(16))==16 and os.getpid()>0,"detail":f"PID={os.getpid()}"}
    except Exception as e: yield {"name":"os.urandom/pid","status":False,"detail":str(e)}

def stress():
    try:
        libc=ctypes.CDLL("msvcrt.dll"); libc.sqrt.argtypes=[ctypes.c_double]; libc.sqrt.restype=ctypes.c_double
        v=libc.sqrt(ctypes.c_double(100.0))
        yield {"name":"ctypes C 调用","status":abs(v-10.0)<0.001,"detail":f"sqrt(100)={v:.4f}"}
    except Exception as e: yield {"name":"ctypes C 调用","status":False,"detail":str(e)}
    try:
        k32=ctypes.WinDLL("kernel32.dll",use_last_error=True)
        class SI(ctypes.Structure):
            _fields_=[("a",ctypes.c_uint16),("b",ctypes.c_uint16),("c",ctypes.c_uint32),
                      ("d",ctypes.c_void_p),("e",ctypes.c_void_p),("f",ctypes.c_size_t),
                      ("n",ctypes.c_uint32),("h",ctypes.c_uint32),("i",ctypes.c_uint32),
                      ("j",ctypes.c_uint16),("k",ctypes.c_uint16)]
        si=SI(); k32.GetSystemInfo(ctypes.byref(si))
        yield {"name":"Windows API","status":si.n>0,"detail":f"{si.n} 核"}
    except Exception as e: yield {"name":"Windows API","status":False,"detail":str(e)}
    try: yield {"name":"ssl 上下文","status":ssl.create_default_context().protocol>=ssl.PROTOCOL_TLS_CLIENT,"detail":"成功"}
    except Exception as e: yield {"name":"ssl 上下文","status":False,"detail":str(e)}
    try: yield {"name":"secrets","status":len(secrets.token_hex(16))==32,"detail":secrets.token_hex(16)[:16]+"..."}
    except Exception as e: yield {"name":"secrets","status":False,"detail":str(e)}
    d=0
    def _recurse(n):
        nonlocal d
        d=n
        return _recurse(n-1) if n>0 else "done"
    try: yield {"name":"递归 50 层","status":_recurse(50)=="done" and d==0,"detail":"成功"}
    except Exception as e: yield {"name":"递归 50 层","status":False,"detail":str(e)}
    try: atexit.register(lambda:None); yield {"name":"atexit","status":True,"detail":"已注册"}
    except Exception as e: yield {"name":"atexit","status":False,"detail":str(e)}

def special():
    try: yield {"name":"inspect.getsource","status":"def special" in inspect.getsource(special),"detail":"成功"}
    except: yield {"name":"inspect.getsource","status":False,"detail":"失败"}
    try: yield {"name":"repr+eval","status":eval(repr({"a":1,"b":2}))=={"a":1,"b":2},"detail":"成功"}
    except: yield {"name":"repr+eval","status":False,"detail":"失败"}
    try: yield {"name":"ast.literal_eval","status":ast.literal_eval("[1,2,3]")==[1,2,3],"detail":"成功"}
    except: yield {"name":"ast.literal_eval","status":False,"detail":"失败"}
    try: yield {"name":"type() 动态类","status":type("C",(),{"x":42})().x==42,"detail":"成功"}
    except: yield {"name":"type() 动态类","status":False,"detail":"失败"}
    try:
        class D:
            @property
            def v(self): return 42
        yield {"name":"@property","status":D().v==42,"detail":"成功"}
    except: yield {"name":"@property","status":False,"detail":"失败"}
    try:
        class T:
            @staticmethod
            def s(): return "ok"
            @classmethod
            def c(cls): return "ok"
        yield {"name":"@static/@classmethod","status":T.s()=="ok" and T.c()=="ok","detail":"成功"}
    except: yield {"name":"@static/@classmethod","status":False,"detail":"失败"}
    try:
        class _W: pass
        gc.collect(); o=_W(); r=weakref.ref(o); del o; gc.collect()
        yield {"name":"weakref","status":r() is None,"detail":"成功"}
    except: yield {"name":"weakref","status":False,"detail":"失败"}
    try:
        h=[]; heapq.heappush(h,3); heapq.heappush(h,1); heapq.heappush(h,2)
        ok=[heapq.heappop(h) for _ in range(3)]==[1,2,3]
        yield {"name":"heapq","status":ok,"detail":"成功"}
    except: yield {"name":"heapq","status":False,"detail":"失败"}
    try: yield {"name":"sys.getsizeof","status":sys.getsizeof({"a":1})>0,"detail":f"{sys.getsizeof({'a':1})} bytes"}
    except: yield {"name":"sys.getsizeof","status":False,"detail":"失败"}

def realworld():
    try:
        c=configparser.ConfigParser(); c.read_string("[a]\nb=1")
        yield {"name":"ConfigParser","status":c.get("a","b")=="1","detail":"成功"}
    except Exception as e: yield {"name":"ConfigParser","status":False,"detail":str(e)}
    try: yield {"name":"URL 解析","status":urlparse("https://example.com/p?q=1").scheme=="https","detail":"成功"}
    except Exception as e: yield {"name":"URL 解析","status":False,"detail":str(e)}
    try:
        os.environ["_T"]="v"; ok=os.environ.get("_T")=="v"; del os.environ["_T"]
        yield {"name":"环境变量","status":ok,"detail":"成功" if ok else "失败"}
    except Exception as e: yield {"name":"环境变量","status":False,"detail":str(e)}
    try: yield {"name":"正则匹配","status":re.match(r"^\w+@\w+\.\w+$","a@b.co") is not None,"detail":"成功"}
    except Exception as e: yield {"name":"正则匹配","status":False,"detail":str(e)}
    try: yield {"name":"string.Template","status":string.Template("Hello $n!").safe_substitute(n="world")=="Hello world!","detail":"成功"}
    except Exception as e: yield {"name":"string.Template","status":False,"detail":str(e)}
    try: yield {"name":"XML 解析","status":ET.fromstring("<r><i>v</i></r>").find("i").text=="v","detail":"成功"}
    except Exception as e: yield {"name":"XML 解析","status":False,"detail":str(e)}
    try: dq=collections.deque([1,2]); dq.append(3); yield {"name":"deque","status":list(dq)==[1,2,3],"detail":"成功"}
    except Exception as e: yield {"name":"deque","status":False,"detail":str(e)}
    try: yield {"name":"itertools.chain","status":list(itertools.chain([1],[2]))==[1,2],"detail":"成功"}
    except Exception as e: yield {"name":"itertools.chain","status":False,"detail":str(e)}
    try:
        p=pathlib.Path(WORKSPACE)/"_p.txt"; p.write_text("ok",encoding="utf-8"); c=p.read_text(encoding="utf-8"); p.unlink()
        yield {"name":"pathlib","status":c=="ok","detail":"成功"}
    except Exception as e: yield {"name":"pathlib","status":False,"detail":str(e)}
    try:
        @dataclasses.dataclass
        class U:
            n: str
            a: int
        yield {"name":"dataclasses","status":dataclasses.asdict(U("t",1))=={"n":"t","a":1},"detail":"成功"}
    except Exception as e: yield {"name":"dataclasses","status":False,"detail":str(e)}
    try:
        class C(enum.Enum): A=1; B=2
        yield {"name":"enum","status":C.A.value==1 and C.B.name=="B","detail":"成功"}
    except Exception as e: yield {"name":"enum","status":False,"detail":str(e)}
    except Exception as e: yield {"name":"enum","status":False,"detail":str(e)}
    try:
        @functools.lru_cache(maxsize=10)
        def _fib(n): return n if n<2 else _fib(n-1)+_fib(n-2)
        yield {"name":"lru_cache","status":_fib(10)==55,"detail":"成功"}
    except Exception as e: yield {"name":"lru_cache","status":False,"detail":str(e)}
    try: yield {"name":"partial","status":functools.partial(lambda a,b:a+b,5)(3)==8,"detail":"成功"}
    except Exception as e: yield {"name":"partial","status":False,"detail":str(e)}
    try:
        l=logging.getLogger("_t"); l.setLevel(logging.INFO)
        yield {"name":"logging","status":l.level==logging.INFO,"detail":"成功"}
    except Exception as e: yield {"name":"logging","status":False,"detail":str(e)}
    except Exception as e: yield {"name":"logging","status":False,"detail":str(e)}
    try: yield {"name":"re.sub","status":re.sub(r"\d","X","a1b2")=="aXbX","detail":"成功"}
    except Exception as e: yield {"name":"re.sub","status":False,"detail":str(e)}
    try:
        @contextlib.contextmanager
        def ctx(): yield "ok"
        with ctx() as v: ok=v=="ok"
        yield {"name":"contextmanager","status":ok,"detail":"成功"}
    except Exception as e: yield {"name":"contextmanager","status":False,"detail":str(e)}

def print_report(cats):
    t,n,a=_calc(cats)
    print(); print(Fore.CYAN+Style.BRIGHT+"="*60)
    print(Fore.CYAN+Style.BRIGHT+"      Python 环境测试报告 (精简版)")
    print(Fore.CYAN+Style.BRIGHT+"="*60); print()
    for c in cats:
        print(Fore.YELLOW+Style.BRIGHT+f"【{c['n']}】"); print(Fore.YELLOW+"-"*45)
        for r in c["r"]:
            ep=r.get("expect","pass")=="pass"
            if _is_normal(r):
                ic=Fore.GREEN+"PASS"; st=Fore.GREEN+"通过"
            elif ep: ic=Fore.RED+"FAIL"; st=Fore.RED+"异常失败"
            else: ic=Fore.WHITE+"SKIP"; st=Fore.WHITE+"预期失败"
            print(f"  {ic} {r['name']:<28} {st}")
            print(f"    {Fore.WHITE}{r['detail']}")
        print()
    print(Fore.CYAN+Style.BRIGHT+"="*60)
    print(f"  总计: {t}  |  正常: {n}  |  异常: {a}")
    c=Fore.GREEN if a==0 else Fore.RED
    print(c+Style.BRIGHT+f"  判定: {'正常' if a==0 else '异常'}")
    print(Fore.CYAN+Style.BRIGHT+"="*60)
    if a>0:
        print(); print(Fore.RED+Style.BRIGHT+"异常明细:")
        for cn,r in _abnormal(cats):
            lb="预期失败但通过" if r.get("expect","pass")!="pass" else "预期通过但失败"
            print(f"  [{lb}] {cn}>{r['name']}: {r['detail']}")

def main():
    print("="*60); print("       Python 环境测试工具 (精简版)")
    print("  github.com/stop666two/py-running-text"); print("="*60); print()
    tests=[("基础信息",basic),("标准库",stdlib),("第三方包",thirdparty),
           ("运行时",runtime),("编译加密",compile_crypto),("高级",advanced),
           ("压力测试",stress),("特殊功能",special),("实际项目",realworld)]
    cats=[]
    with tqdm(total=200,desc="测试中",unit="项",ncols=80) as pb:
        for n,f in tests:
            rs=[]
            for r in f():
                r.setdefault("expect","pass"); rs.append(r); pb.set_postfix_str(r["name"][:28]); pb.update(1)
            pb.set_postfix_str("")
            cats.append({"n":n,"r":rs})
    print_report(cats)

if __name__=="__main__":
    main()
