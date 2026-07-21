import marshal
import dis
import py_compile
import tempfile
import os
import zipfile
import sys


def run_compile_crypto_checks():
    try:
        code = compile("1 + 2 * 3", "<test>", "eval")
        val = eval(code)
        ok = val == 7
        yield {
            "name": "compile() 编译代码",
            "status": ok,
            "detail": f"1+2*3={val}" if ok else f"结果异常: {val}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "compile() 编译代码",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        src = "def f(x): return x * 2"
        code = compile(src, "<exec>", "exec")
        ns = {}
        exec(code, ns)
        result = ns["f"](21)
        ok = result == 42
        yield {
            "name": "exec() 动态执行",
            "status": ok,
            "detail": f"f(21)={result}" if ok else f"结果异常: {result}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "exec() 动态执行",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        code_obj = compile("lambda x: x ** 2", "<test>", "eval")
        data = marshal.dumps(code_obj)
        restored = marshal.loads(data)
        f = eval(restored)
        val = f(5)
        ok = val == 25
        yield {
            "name": "marshal 序列化/反序列化",
            "status": ok,
            "detail": f"marshal {len(data)} bytes, f(5)={val}" if ok else f"结果异常: {val}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "marshal 序列化/反序列化",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    tmp_pyc = None
    try:
        tmp_src = os.path.join(tempfile.gettempdir(), "_py_compile_test.py")
        with open(tmp_src, "w", encoding="utf-8") as f:
            f.write("x = 42")
        tmp_pyc = tmp_src + "c"
        py_compile.compile(tmp_src, cfile=tmp_pyc)
        ok = os.path.exists(tmp_pyc)
        yield {
            "name": "py_compile 字节码编译",
            "status": ok,
            "detail": f".pyc 文件 {'已生成' if ok else '未生成'}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "py_compile 字节码编译",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }
    finally:
        for p in [tmp_src, tmp_pyc]:
            if p and os.path.exists(p):
                os.remove(p)

    try:
        code_obj = compile("a + b", "<test>", "eval")
        instructions = list(dis.get_instructions(code_obj))
        has_load = any("LOAD" in i.opname for i in instructions)
        yield {
            "name": "dis 反汇编",
            "status": has_load,
            "detail": f"{len(instructions)} 条指令, 含 LOAD={has_load}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "dis 反汇编",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    tmp_zip = None
    try:
        tmp_zip = os.path.join(tempfile.gettempdir(), "_py_zipimporter_test.zip")
        module_code = "def greet(name): return f'Hello, {name}!'"
        with zipfile.ZipFile(tmp_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("greeter.py", module_code)
        import zipimport
        importer = zipimport.zipimporter(tmp_zip)
        mod = importer.load_module("greeter")
        result = mod.greet("测试")
        ok = result == "Hello, 测试!"
        yield {
            "name": "zipimporter 从 ZIP 导入",
            "status": ok,
            "detail": f"greeter.greet('测试')={result}" if ok else f"结果异常: {result}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "zipimporter 从 ZIP 导入",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }
    finally:
        if tmp_zip and os.path.exists(tmp_zip):
            os.remove(tmp_zip)
        if "greeter" in sys.modules:
            del sys.modules["greeter"]

    try:
        import hashlib
        algos = hashlib.algorithms_available
        data = b"test data for hashing"
        results_list = []
        for algo in ["md5", "sha1", "sha256", "sha512", "sha3_256", "blake2b", "blake2s"]:
            if algo in algos:
                h = hashlib.new(algo, data).hexdigest()
                results_list.append(f"{algo}={h[:8]}")
                ok = True
            else:
                results_list.append(f"{algo}=不支持")
                ok = False
        all_ok = all(algo in algos for algo in ["md5", "sha1", "sha256", "sha512"])
        yield {
            "name": "hashlib 多算法",
            "status": all_ok,
            "detail": ", ".join(results_list),
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "hashlib 多算法",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        import hashlib
        dk = hashlib.pbkdf2_hmac("sha256", b"password", b"salt", 1000)
        ok = len(dk) == 32
        yield {
            "name": "hashlib PBKDF2 密钥派生",
            "status": ok,
            "detail": f"派生密钥 {len(dk)} bytes" if ok else "派生失败",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "hashlib PBKDF2 密钥派生",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        import hashlib
        dk = hashlib.scrypt(b"password", salt=b"salt1234", n=1024, r=8, p=1)
        ok = len(dk) == 64
        yield {
            "name": "hashlib scrypt 密钥派生",
            "status": ok,
            "detail": f"派生密钥 {len(dk)} bytes" if ok else "派生失败",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "hashlib scrypt 密钥派生",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        import hmac
        key = b"secret-key"
        msg = b"authenticate me"
        sig = hmac.new(key, msg, "sha256").hexdigest()
        expected = hmac.new(key, msg, "sha256").hexdigest()
        ok = sig == expected
        yield {
            "name": "hmac 签名验证",
            "status": ok,
            "detail": f"SHA256 HMAC={sig[:16]}..." if ok else "签名不一致",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "hmac 签名验证",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        from cryptography.fernet import Fernet
        key = Fernet.generate_key()
        cipher = Fernet(key)
        original = b"sensitive data for encryption test"
        token = cipher.encrypt(original)
        decrypted = cipher.decrypt(token)
        ok = decrypted == original
        yield {
            "name": "cryptography AES 加解密",
            "status": ok,
            "detail": f"{len(original)} bytes -> {len(token)} bytes, 解密{'成功' if ok else '失败'}",
            "expect": "pass",
        }
    except ImportError:
        yield {
            "name": "cryptography AES 加解密",
            "status": False,
            "detail": "cryptography 未安装，跳过",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "cryptography AES 加解密",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }
