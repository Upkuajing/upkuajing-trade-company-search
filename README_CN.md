# upkuajing-trade-company-search

通过跨境魔方开放平台查询海关贸易数据的 AI Agent Skill，用于发现潜在客户和商业合作伙伴。

![upkuajing](upkuajing.png)

## 功能特性

- **贸易订单搜索**：查询进口/出口记录、交易金额、贸易路线
- **公司发现**：通过贸易数据反向查找潜在客户和供应商
- **公司详情**：获取公司工商信息和背景资料
- **联系方式**：查询邮箱、电话、社交媒体等联系信息

适用场景：外贸客户开发、竞品供应链分析、物流行业客户挖掘、进出口市场调研。

## Skill 安装

### 让Agent自动安装

### OpenClaw 安装

1. 复制整个 skill 目录到 OpenClaw 的 skills 目录：
```bash
cp -r upkuajing-trade-company-search ~/.openclaw/workspace/skills/
```

2. 或者创建符号链接：
```bash
ln -s /path/to/upkuajing-trade-company-search ~/.openclaw/workspace/skills/
```

3. 重启 OpenClaw 使 skill 生效

### Claude Code 安装

1. 复制整个 skill 目录到 Claude Code 的 skills 目录：
```bash
cp -r upkuajing-trade-company-search ~/.claude/skills/
```

2. 或者在 Claude Code 设置中配置 skills 路径指向此目录

### 目录结构要求

确保 skill 目录包含以下结构：
```
upkuajing-trade-company-search/
├── SKILL.md              # Skill 描述文件（必需）
├── requirements.txt      # Python 依赖
├── scripts/              # Python 脚本目录（必需）
│   ├── auth.py
│   ├── common.py
│   ├── trade_list_search.py
│   ├── company_list_search.py
│   ├── company_get_details.py
│   └── company_get_contact.py
└── references/           # API 参考文档
    ├── trade-list-api.md
    ├── company-list-api.md
    ├── company-detail-api.md
    └── contact-fetch-api.md
```

## 环境配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 设置 API 密钥

**方式1：使用环境变量**
```bash
export UPKUAJING_API_KEY=your_api_key_here
```

**方式2：使用 .env 文件**
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API 密钥
```

### 3. 申请 API 密钥

如果没有 API 密钥，可以通过以下方式申请：
```bash
python scripts/auth.py --new_key
```

## 快速开始

### 在 AI Agent 中使用

安装完成后，可以直接在支持的 AI Agent 工具中使用：

**搜索贸易订单**
```
帮我查找美国从中国进口LED产品的贸易记录
```

**发现潜在客户**
```
找进口电子产品的美国公司
```

**获取公司详情**
```
获取这个贸易公司的详细信息：[公司ID]
```

### 命令行使用

也可以直接调用 Python 脚本：

```bash
# 贸易列表搜索
python scripts/trade_list_search.py \
  --params '{"importCountries": ["US"], "exportCountries": ["CN"], "products": ["LED"]}' \
  --query_count 20

# 公司列表搜索
python scripts/company_list_search.py \
  --params '{"importCountries": ["US"]}' \
  --query_count 20

# 获取公司详情
python scripts/company_get_details.py --pid [公司ID]

# 获取联系方式
python scripts/company_get_contact.py --pid [公司ID]
```

## 使用示例

### 场景1：外贸客户开发

发现进口特定产品的潜在客户：
```bash
python scripts/company_list_search.py \
  --params '{"importCountries": ["US"], "products": ["electronics"]}' \
  --query_count 50
```

### 场景2：竞品分析

分析竞争对手的供应链：
```bash
# 查找竞争对手的供应商
python scripts/trade_list_search.py \
  --params '{"importCountries": ["US"], "exportCountries": ["CN"]}' \
  --query_count 100
```

### 场景3：市场调研

研究特定产品的贸易流向：
```bash
python scripts/trade_list_search.py \
  --params '{"products": ["solar panels"], "year": 2025}' \
  --query_count 200
```

## API 参考

详细的 API 参数说明请查看 `references/` 目录下的文档：
- [贸易列表搜索](references/trade-list-api.md)
- [公司列表搜索](references/company-list-api.md)
- [公司详情](references/company-detail-api.md)
- [联系方式](references/contact-fetch-api.md)

## 数据驱动特点

与 `upkuajing-company-people-search` 不同，本 skill 基于海关贸易数据

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 支持

如有问题或建议，请提交 Issue 或 Pull Request。
