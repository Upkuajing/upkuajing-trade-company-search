"""
跨境魔方API脚本公共工具
"""
import os
import json
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, Optional
import httpx

# API配置
API_BASE_URL = "https://openapi.upkuajing.com"
API_KEY_ENV = "UPKUAJING_API_KEY"
UPKUAJING_DIR = Path.home() / '.upkuajing'
UPKUAJING_ENV_FILE = UPKUAJING_DIR / '.env'

# 技能目录配置
SKILL_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASK_DATA_DIR = os.path.join(SKILL_BASE_DIR, 'task_data')


# API错误码定义
class APIErrorCode:
    """跨境魔方API错误码常量"""
    UNKNOWN_ERROR = 99  # 系统繁忙
    REQUEST_PARAM_ERROR = 98  # 请求参数错误
    REQUEST_METHOD_ERROR = 97  # 请求方式错误
    REQUEST_AUTH_ERROR = 96  # 认证错误
    SEARCH_BALANCE_NOT_ENOUGH = 95  # 余额不足


# API错误码映射表
API_ERROR_MESSAGES = {
    APIErrorCode.UNKNOWN_ERROR: "系统繁忙，请稍后重试",
    APIErrorCode.REQUEST_PARAM_ERROR: "请求参数错误，请检查参数名称和值",
    APIErrorCode.REQUEST_METHOD_ERROR: "请求方式错误，请使用正确的HTTP方法",
    APIErrorCode.REQUEST_AUTH_ERROR: "认证错误，请检查API密钥是否有效",
    APIErrorCode.SEARCH_BALANCE_NOT_ENOUGH: "余额不足，请充值后继续使用",
}

# API错误处理建议
API_ERROR_SUGGESTIONS = {
    APIErrorCode.REQUEST_AUTH_ERROR: f"请检查环境变量 {API_KEY_ENV} 或文件 {UPKUAJING_ENV_FILE} 中的API密钥是否正确",
    APIErrorCode.SEARCH_BALANCE_NOT_ENOUGH: "请运行 auth.py --new_rec_order 创建充值订单",
    APIErrorCode.REQUEST_PARAM_ERROR: "请参考 references/ 目录下的API文档检查参数格式",
}


def load_env_file() -> Dict[str, str]:
    """
    从 ~/.upkuajing/.env 文件加载环境变量。

    Returns:
        环境变量字典
    """
    env_vars = {}
    if UPKUAJING_ENV_FILE.exists():
        with open(UPKUAJING_ENV_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释
                if not line or line.startswith('#'):
                    continue
                # 解析 KEY=VALUE 格式
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars


def get_api_key() -> str:
    """
    获取API密钥，优先从环境变量，其次从 ~/.upkuajing/.env 文件。
    """
    # 优先从环境变量获取
    api_key = os.environ.get(API_KEY_ENV)

    # 如果环境变量没有，尝试从 ~/.upkuajing/.env 读取
    if not api_key:
        env_vars = load_env_file()
        api_key = env_vars.get(API_KEY_ENV)

    if not api_key:
        print(
            f"错误：未找到API密钥。\n"
            f"请设置环境变量 {API_KEY_ENV}，\n"
            f"或在 {UPKUAJING_ENV_FILE} 文件中添加：{API_KEY_ENV}=your_api_key_here",
            file=sys.stderr
        )
        sys.exit(1)
    return api_key


def make_request(
        endpoint: str,
        params: Dict[str, Any],
        api_key: Optional[str] = None,
        require_auth: bool = True
) -> Dict[str, Any]:
    """
    向跨境魔方API发起HTTP请求。

    Args:
        endpoint: API端点路径
        params: 请求参数字典
        api_key: API密钥（如果为None且require_auth=True，将从环境变量获取）
        require_auth: 是否需要Bearer令牌认证，默认为True
    """
    if require_auth and api_key is None:
        api_key = get_api_key()

    url = f"{API_BASE_URL}{endpoint}"
    headers = {
        "Content-Type": "application/json"
    }

    # 只有在需要认证时才添加 Authorization 头
    if require_auth:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(url, json=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            # 检查API级别的错误  0表示成功，非0代表错误
            if data.get("code") != 0:
                # 不再自动退出，返回错误响应让调用者处理
                return data

            return data

    except httpx.HTTPStatusError as e:
        print(f"HTTP错误：{e.response.status_code}", file=sys.stderr)
        print(f"响应：{e.response.text}", file=sys.stderr)
        sys.exit(1)
    except httpx.RequestError as e:
        print(f"网络错误：无法连接到API服务器", file=sys.stderr)
        print(f"详细信息：{str(e)}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("错误：API返回的JSON无效", file=sys.stderr)
        sys.exit(1)


def handle_api_error(response_data: Dict[str, Any], exit_on_error: bool = True) -> None:
    """
    处理API错误响应，提供详细的错误消息。

    Args:
        response_data: API响应数据
        exit_on_error: 是否在遇到错误时退出程序（默认True）

    Returns:
        None（如果exit_on_error=True会退出程序）

    Raises:
        SystemExit: 如果exit_on_error=True且遇到错误
    """
    error_code = response_data.get("code")
    server_msg = response_data.get("msg", "")

    # 获取标准错误消息
    if error_code in API_ERROR_MESSAGES:
        standard_msg = API_ERROR_MESSAGES[error_code]
    else:
        standard_msg = server_msg or "未知错误"

    # 输出错误信息
    print(f"API错误（代码：{error_code}）：{standard_msg}", file=sys.stderr)

    # 如果服务器返回了额外的消息，也显示出来
    if server_msg and server_msg != standard_msg:
        print(f"服务器消息：{server_msg}", file=sys.stderr)

    # 提供处理建议
    if error_code in API_ERROR_SUGGESTIONS:
        print(f"建议：{API_ERROR_SUGGESTIONS[error_code]}", file=sys.stderr)

    if exit_on_error:
        sys.exit(1)


def save_to_file(data: Any, filepath: str) -> None:
    """
    将数据保存到文件，使用JSONL格式（每行一个JSON对象）。

    Args:
        data: 要保存的数据（可以是字典或列表）
        filepath: 输出文件路径
    """
    try:
        # 如果数据是列表，将每个项目写入单独的行
        if isinstance(data, list):
            with open(filepath, 'a', encoding='utf-8') as f:
                for item in data:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
        else:
            # 如果数据是单个字典，将其写入一行
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
    except IOError as e:
        print(f"写入文件错误 {filepath}：{str(e)}", file=sys.stderr)
        sys.exit(1)


def parse_params(params_str: str) -> Dict[str, Any]:
    """
    解析JSON字符串参数。

    Args:
        params_str: 包含参数的JSON字符串

    Returns:
        解析后的参数字典

    Raises:
        SystemExit: 如果JSON解析失败
    """
    try:
        params = json.loads(params_str)
        if not isinstance(params, dict):
            print("错误：参数必须是JSON对象", file=sys.stderr)
            sys.exit(1)
        return params
    except json.JSONDecodeError as e:
        print(f"错误：参数中的JSON无效：{str(e)}", file=sys.stderr)
        sys.exit(1)


def print_json_output(data: Any) -> None:
    """
    将数据以格式化的JSON打印到标准输出。

    Args:
        data: 要打印的数据
    """
    print(json.dumps(data, ensure_ascii=False, indent=2))


# ============ 任务管理函数 ============

def generate_task_id() -> str:
    """
    生成新的任务ID（UUID4格式）。

    Returns:
        任务ID字符串
    """
    return str(uuid.uuid4())


def get_task_dir(task_id: str) -> str:
    """
    获取任务目录路径（带安全验证）。

    Args:
        task_id: 任务ID（必须是有效的UUID格式）

    Returns:
        任务目录的完整路径

    Raises:
        ValueError: 如果 task_id 不是有效的UUID或包含路径遍历字符
    """
    # 验证 UUID 格式，防止路径遍历攻击
    try:
        uuid.UUID(task_id)
    except ValueError:
        raise ValueError(f"无效的 task_id 格式：{task_id}")

    task_dir = os.path.join(TASK_DATA_DIR, task_id)

    # 确保路径在 TASK_DATA_DIR 内（防止路径遍历）
    task_dir = os.path.abspath(task_dir)
    data_dir = os.path.abspath(TASK_DATA_DIR)
    if not task_dir.startswith(data_dir):
        raise ValueError("task_id 包含非法路径字符")

    return task_dir


def ensure_task_dir(task_id: str) -> str:
    """
    确保任务目录存在，如果不存在则创建。

    Args:
        task_id: 任务ID

    Returns:
        任务目录的完整路径
    """
    task_dir = get_task_dir(task_id)
    os.makedirs(task_dir, exist_ok=True)
    return task_dir


def get_task_meta_file(task_id: str) -> str:
    """
    获取任务元数据文件路径。

    Args:
        task_id: 任务ID

    Returns:
        元数据文件的完整路径
    """
    return os.path.join(get_task_dir(task_id), 'meta.json')


def get_task_result_file(task_id: str) -> str:
    """
    获取任务结果文件路径。

    Args:
        task_id: 任务ID

    Returns:
        结果文件的完整路径
    """
    return os.path.join(get_task_dir(task_id), 'result.jsonl')


def save_task_meta(task_id: str, meta: Dict[str, Any]) -> None:
    """
    保存任务元数据到文件。

    Args:
        task_id: 任务ID
        meta: 元数据字典
    """
    meta_file = get_task_meta_file(task_id)
    ensure_task_dir(task_id)
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def load_task_meta(task_id: str) -> Optional[Dict[str, Any]]:
    """
    从文件加载任务元数据。

    Args:
        task_id: 任务ID

    Returns:
        元数据字典，如果文件不存在则返回None
    """
    meta_file = get_task_meta_file(task_id)
    if not os.path.exists(meta_file):
        return None
    with open(meta_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def append_result_data(task_id: str, data_list: list) -> None:
    """
    追加结果数据到任务结果文件。

    Args:
        task_id: 任务ID
        data_list: 要追加的数据列表
    """
    result_file = get_task_result_file(task_id)
    ensure_task_dir(task_id)
    with open(result_file, 'a', encoding='utf-8') as f:
        for item in data_list:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def cover_fee_info(fee: dict) -> dict:
    """
    将Api响应的费用信息 转为利于Ai理解的格式
    """
    if not fee:
        return {}
    api_cost = fee.get("apiCost", 0)
    balance = fee.get("accountBalance", 0)
    return {
        "apiCost": f"{api_cost}分钱",
        "balance": f"{balance}分钱"
    }
