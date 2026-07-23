"""S-Protect-PY type definitions - full customization."""

# DATA LAYER: immutable config schema
# INTEGRITY: field order must not change

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from sprotect.keyvault.config import KeyVaultConfig


class ObfuscateLevel(Enum):
    L1 = 1; L2 = 2; L3 = 3; L4 = 4; L5 = 5

class InterdependencyMode(Enum):
    CHAIN = "chain"; FULL_MESH = "full-mesh"; HYBRID = "hybrid"

class NamingStyle(Enum):
    HEX = "hex"; CHINESE = "chinese"; INVISIBLE = "invisible"
    MATH_SYMBOLS = "math-symbols"; CUSTOM = "custom"

class AntiDebugAction(Enum):
    EXIT = "exit"; CORRUPT = "corrupt"; WARN = "warn"

class VirtualizationMode(Enum):
    PARTIAL = "partial"; FULL = "full"

class WatermarkLevel(Enum):
    FILE = "file"; CODE = "code"; RUNTIME = "runtime"

class EncryptAlgorithm(Enum):
    AES256GCM = "aes-256-gcm"
    X25519AES = "x25519-aes"
    CHACHA20 = "chacha20"
    HYBRID = "hybrid"


@dataclass
class RenameRules:
    """命名混淆规则"""
    style: NamingStyle = NamingStyle.HEX           # 命名风格
    reserved: list[str] = field(default_factory=lambda: ["__init__", "main"])  # 保留名称
    dictionary: Optional[dict] = None               # 自定义映射字典 {原名: 混淆名}
    prefix: str = "_0x"                             # 自定义前缀
    suffix: str = ""                                # 自定义后缀
    min_length: int = 6                             # 混淆名最小长度
    blacklist: list[str] = field(default_factory=list)  # 黑名单（强制不改名）

@dataclass
class ObfuscateConfig:
    """混淆配置"""
    level: ObfuscateLevel = ObfuscateLevel.L5
    rename_variables: bool = True
    rename_functions: bool = True
    rename_classes: bool = True
    rename_rules: RenameRules = field(default_factory=RenameRules)
    encrypt_strings: bool = True
    encrypt_numbers: bool = True
    string_min_length: int = 3                       # 字符串最小加密长度
    string_encrypt_ratio: float = 1.0                # 字符串加密比例 0-1
    control_flow_flattening: bool = True
    dead_code_injection: bool = True
    dead_code_density: float = 0.3                   # 死代码密度 0-1
    opaque_predicate_count: int = 2                  # 不透明谓词数量
    remove_docstrings: bool = True                   # 是否删除文档字符串
    remove_comments: bool = True                     # 是否删除注释
    strip_blank_lines: bool = True                   # 是否删除空行
    max_line_length: int = 0                         # 最大行长（0=不限制）
    string_split: bool = True                         # 字符串分割为碎片拼接
    string_cipher: str = "mixed"                      # 字符串加密方式: base64 | xor | mixed
    obfuscate_imports: bool = True                    # import 转为 __import__()
    obfuscate_calls: bool = True                      # 函数调用混淆
    obfuscate_arithmetic: bool = True                 # 算术表达式混淆
    obfuscate_booleans: bool = True                   # True/False 混淆

@dataclass
class HybridEncryptConfig:
    """混合加密配置"""
    enabled: bool = False
    algorithm: str = "RSA"
    key_size: int = 4096
    key_file: str = "key.pem"

@dataclass
class EncryptConfig:
    """加密配置"""
    algorithm: str = "aes-256-gcm"                   # 加密算法
    key_source: str = "auto"                         # 密钥来源 auto|file|env
    key_file: Optional[str] = None                   # 密钥文件路径
    key_env_var: Optional[str] = None                # 密钥环境变量名
    interdependency: InterdependencyMode = InterdependencyMode.CHAIN
    backup: bool = True
    backup_max_count: int = 5                        # 最大备份数
    replace_originals: bool = False
    shard_count: int = 3                             # 密钥分片数
    shard_min_files: int = 2                         # 最少分片文件数
    compress_level: int = 9                          # 压缩等级 0-9
    polymorphic_padding: bool = True                 # 多态填充
    polymorphic_padding_max: int = 512               # 最大填充字节
    aad_context: str = "S-Protect-PY"               # AAD 附加认证数据
    extra_layers: list[str] = field(default_factory=list)  # 额外加密层
    hybrid: HybridEncryptConfig = field(default_factory=HybridEncryptConfig)
    workers: int = 0                                  # 并行工作线程（0=自动=CPU核数）

@dataclass
class AntiDebugCheckConfig:
    """单个检测项配置"""
    check: str = "pdb"                               # 检测项名称
    enabled: bool = True                             # 是否启用
    action: Optional[str] = None                     # 覆盖全局动作

@dataclass
class AntiDebugConfig:
    """反调试/反VM/反沙箱配置"""
    enabled: bool = True
    action: AntiDebugAction = AntiDebugAction.EXIT
    checks: list[str] = field(default_factory=lambda: [
        "pdb", "ptrace", "debugger", "vm", "sandbox",
        "timing", "cuckoo", "ida", "procmon", "gpu",
    ])
    per_check_actions: list[AntiDebugCheckConfig] = field(default_factory=list)
    process_whitelist: list[str] = field(default_factory=list)  # 进程白名单
    block_tracing: bool = True                       # 阻断 settrace/setprofile
    timing_threshold: float = 2.0                    # 时序检测阈值（秒）
    exit_code: int = 1                               # 退出码
    wipe_memory: bool = True                         # 是否清空内存
    corrupt_on_exit: bool = False                    # 退出前是否破坏内存

@dataclass
class VirtualizationConfig:
    """代码虚拟化配置"""
    enabled: bool = False
    mode: VirtualizationMode = VirtualizationMode.PARTIAL
    functions: list[str] = field(default_factory=list)
    glob_patterns: list[str] = field(default_factory=list)
    exclude_functions: list[str] = field(default_factory=list)  # 排除函数
    inline_threshold: int = 50                       # 内联阈值（行数）
    interpreter_obfuscate: bool = True               # 混淆解释器代码

@dataclass
class WatermarkConfig:
    """水印配置"""
    enabled: bool = True
    levels: list[WatermarkLevel] = field(default_factory=lambda: [
        WatermarkLevel.FILE, WatermarkLevel.CODE, WatermarkLevel.RUNTIME,
    ])
    batch_id: str = ""                               # 批次ID
    custom_template: Optional[str] = None            # 自定义水印模板
    multi_batch: list[str] = field(default_factory=list)  # 多批次ID
    visible: bool = False                            # 是否可见水印
    watermark_key: str = ""                          # 水印密钥（用于校验）

@dataclass
class ExpirationConfig:
    """过期时间配置"""
    enabled: bool = False
    expires_at: Optional[str] = None                 # 过期时间
    encrypted_at: Optional[str] = None               # 加密时间
    grace_period_hours: int = 0                      # 宽限期（小时）
    ntp_check: bool = True
    ntp_servers: list[str] = field(default_factory=lambda: [  # 5 个内置 NTP
        "pool.ntp.org",
        "time.google.com",
        "time.cloudflare.com",
        "time.windows.com",
        "time.apple.com",
    ])
    ntp_timeout: float = 3.0                         # NTP 超时（秒）
    on_network_fail: str = "reject"                  # 网络不通: reject|allow|grace
    check_interval_hours: int = 24                   # 运行时检查间隔
    max_drift_seconds: int = 3600                    # 最大时间偏差（秒）

@dataclass
class EnvironmentConfig:
    """环境指纹配置"""
    enabled: bool = False
    bind_directory: Optional[str] = None             # 绑定目录
    bind_username: Optional[str] = None              # 绑定用户名
    bind_env_vars: list[str] = field(default_factory=list)  # 绑定环境变量
    bind_file_hash: Optional[str] = None             # 绑定文件哈希
    bind_mac_address: Optional[str] = None           # 绑定 MAC 地址
    bind_hardware_id: Optional[str] = None           # 绑定硬件ID
    strict_mode: bool = False                        # 严格模式
    fingerprint_algorithm: str = "sha256"            # 指纹算法

@dataclass
class SandboxConfig:
    """沙箱检测配置"""
    enabled: bool = True
    detect_cuckoo: bool = True
    detect_sandboxie: bool = True
    detect_docker: bool = False
    detect_ci: bool = False                          # 检测 CI 环境

@dataclass
class FilesConfig:
    """文件过滤配置"""
    include: list[str] = field(default_factory=lambda: ["**/*.py"])
    exclude: list[str] = field(default_factory=list)
    exclude_dirs: list[str] = field(default_factory=lambda: [
        "_runtime", "_backup", "_meta", "_workspace",
        "output", "dist", "build",
        "__pycache__", ".git", ".idea", ".vscode",
        "venv", ".venv", "env", ".env",
        "node_modules", "__pypackages__",
        ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ])

@dataclass
class BootloaderConfig:
    """启动器配置"""
    name: str = "main.py"                            # 启动器文件名
    include_runtime_loader: bool = True              # 是否内嵌 runtime
    minimal_boot: bool = False                       # 极简启动模式
    custom_banner: Optional[str] = None              # 自定义启动横幅
    hide_python_windows: bool = False                # 隐藏控制台窗口
    anti_dump: bool = True                           # 反内存 Dump
    periodic_check_interval: float = 5.0             # 周期检查间隔（秒）

@dataclass
class ProjectConfig:
    """项目元信息"""
    name: str = "unnamed"
    version: str = "1.0.0"
    entry: str = "main.py"
    description: str = ""                            # 项目描述
    author: str = ""                                 # 作者

@dataclass
class PackConfig:
    """打包配置 - 将加密输出打包为单文件 exe（需 PyInstaller）"""
    enabled: bool = False                              # 是否启用打包
    onefile: bool = True                               # 单文件模式
    console: bool = True                                # 是否显示控制台窗口
    icon: Optional[str] = None                         # 图标文件路径
    extra_args: list[str] = field(default_factory=list) # 额外 PyInstaller 参数

@dataclass
class OutputConfig:
    """输出配置"""
    dir: str = "./output"
    keep_source_map: bool = False
    runtime_dir_name: str = "_runtime"               # runtime 目录名
    preserve_non_py: bool = True                     # 保留非 py 文件
    verbose: bool = False                            # 详细输出

@dataclass
class Config:
    """顶层配置 - 聚合所有子配置"""
    files: FilesConfig = field(default_factory=FilesConfig)
    obfuscate: ObfuscateConfig = field(default_factory=ObfuscateConfig)
    encrypt: EncryptConfig = field(default_factory=EncryptConfig)
    anti_debug: AntiDebugConfig = field(default_factory=AntiDebugConfig)
    virtualization: VirtualizationConfig = field(default_factory=VirtualizationConfig)
    watermark: WatermarkConfig = field(default_factory=WatermarkConfig)
    expiration: ExpirationConfig = field(default_factory=ExpirationConfig)
    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)
    sandbox: SandboxConfig = field(default_factory=SandboxConfig)
    bootloader: BootloaderConfig = field(default_factory=BootloaderConfig)
    pack: PackConfig = field(default_factory=PackConfig)
    project: ProjectConfig = field(default_factory=ProjectConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    keyvault: KeyVaultConfig = field(default_factory=KeyVaultConfig)
