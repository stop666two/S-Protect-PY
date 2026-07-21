from tqdm import tqdm
from config import TEST_CATEGORIES
from tests.basic import run_basic_checks
from tests.stdlib import run_stdlib_checks
from tests.thirdparty import run_thirdparty_checks
from tests.runtime import run_runtime_checks
from tests.pip_test import run_pip_tests
from tests.realworld import run_realworld_checks
from tests.compile_crypto import run_compile_crypto_checks
from tests.advanced import run_advanced_checks
from tests.stress import run_stress_checks
from tests.special import run_special_checks


def _count_items(gen_fn):
    return sum(1 for _ in gen_fn())


def run_all_tests():
    test_funcs = [
        ("basic", run_basic_checks),
        ("stdlib", run_stdlib_checks),
        ("thirdparty", run_thirdparty_checks),
        ("runtime", run_runtime_checks),
        ("compile_crypto", run_compile_crypto_checks),
        ("advanced", run_advanced_checks),
        ("stress", run_stress_checks),
        ("special", run_special_checks),
        ("pip_test", run_pip_tests),
        ("realworld", run_realworld_checks),
    ]

    cat_sizes = []
    total_steps = 0
    for name, func in test_funcs:
        size = _count_items(func)
        cat_sizes.append((name, func, size))
        total_steps += size

    cat_steps = []
    with tqdm(total=total_steps, desc="环境测试中", unit="项", ncols=80) as pbar:
        for name, func, _ in cat_sizes:
            cat_name = TEST_CATEGORIES.get(name, name)
            results = []
            for r in func():
                r.setdefault("expect", "pass")
                results.append(r)
                pbar.set_postfix_str(r["name"][:30])
                pbar.update(1)
            pbar.set_postfix_str("")
            cat_steps.append({"name": cat_name, "results": results})

    return cat_steps
