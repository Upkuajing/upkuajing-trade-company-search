#!/usr/bin/env python3
"""
跨境魔方公司联系方式
获取公司的联系信息（邮箱、电话、社交媒体、网站）。
"""
import argparse
import sys
from common import make_request, print_json_output


def get_contact_info(company_id: int) -> dict:
    """
    获取公司的联系信息。

    Args:
        company_id: 公司ID（整数）

    Returns:
        包含联系信息的API响应
    """
    params = {
        'companyId': company_id
    }
    response = make_request('/customs/company/contact', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台获取公司联系信息'
    )
    parser.add_argument(
        '--companyId',
        type=int,
        required=True,
        help='公司ID（整数）'
    )

    args = parser.parse_args()

    # 获取联系信息
    response = get_contact_info(args.companyId)

    # 从响应中提取数据
    if response.get('code') == 0:
        data = response.get('data', {})
        # 提取费用信息 金额单位 分钱
        api_cost = response.get('fee', {}).get("apiCost", 0)
        print_json_output({"data": data, "apiCost": f"{api_cost}分钱"})
    else:
        print(f"错误：{response.get('msg', '未知错误')}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
