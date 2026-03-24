---
name: upkuajing-trade-company-search
description: 通过跨境魔方开放平台查询海关贸易数据。支持：查询贸易订单明细（进口/出口记录、交易金额、贸易路线）；发现潜在客户和商业合作伙伴（买家开发、供应商调查、客户挖掘）；获取公司详情和联系方式（邮箱、电话、社交媒体）。适用场景：外贸客户开发、竞品供应链分析、物流行业客户挖掘、进出口市场调研。
homepage: https://www.upkuajing.com
metadata: {"clawdbot":{"emoji":"🏢","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# 跨境魔方海关贸易公司搜索

使用跨境魔方开放平台API通过海关贸易数据搜索公司。本技能采用**数据驱动方式**：通过分析贸易记录和交易模式来查找公司。

## 概述

本技能通过四个脚本提供对跨境魔方海关贸易数据API的访问：两种搜索方式（贸易列表、公司列表）和两个增强接口（公司详情、联系信息）; 
通过`auth.py`脚本提供 API密钥生成、充值；

## 脚本运行

### 环境准备

1. **检查 Python**：`python --version`
2. **检查并创建虚拟环境**（如果需要）
3. **安装依赖**：`pip install -r requirements.txt`

脚本目录：`scripts/*.py`
运行示例：`python scripts/*.py`

### 两种搜索方式

**贸易列表搜索** (`trade_list_search.py`)
- **返回粒度**：每条贸易订单为一行记录
- **适用场景**：关心的是"发生了什么交易"
- **示例**：
   - "显示A公司采购LED的所有订单"
   - "找进/出口到美国的大豆贸易记录"
   - "查看某段时间内的具体交易明细"
- **参数**：查看参数说明 [贸易列表](references/trade-list-api.md)


**公司列表搜索** (`company_list_search.py`)
- **返回粒度**：对贸易订单按公司聚合后，每家公司为一行
- **适用场景**：关心的是"有哪些公司"
- **示例**：
  - "找采购过LED的公司有哪些"
  - "找与中国有电子产品进出口往来的美国公司"
  - "找有中美贸易往来的公司"（物流行业客户开发）
- **参数**：查看参数说明 [公司列表](references/company-list-api.md)


### 两个增强功能

在获取到贸易列表或公司列表后，如有必要，可通过以下接口对结果中的公司ID进行信息增强：
**公司详情** (`company_get_details.py --companyId *`) 
- 获取公司信息（不包括联系方式）
- **API业务参数**：[公司详情](references/company-detail-api.md)

**联系信息** (`company_get_contact.py --companyId *`)
- 获取联系方式详情 邮箱、电话、社交媒体、网站
- **API业务参数**：[获取联系方式](references/contact-fetch-api.md)

## API密钥与充值
使用此技能需要API密钥。API密钥应设置在 `UPKUAJING_API_KEY` 环境变量中：
```bash
export UPKUAJING_API_KEY=your_api_key_here
```
### **未设置API密钥**
如果未设置UPKUAJING_API_KEY API密钥，请提示并让用户选择：
1. 用户有，由用户提供(让用户设置到环境变量)
2. 用户没有，你可使用接口进行申请（`auth.py --new_key`），申请到新密钥后，需告知用户妥善保存
等待用户选择；

### **账户充值**
如果调用接口响应账户余额不足时，需说明并引导用户进行账户充值：
1. 创建充值订单（`auth.py --new_rec_order`）
2. 根据订单响应，发送支付页面URL给用户，引导用户打开地址付款，付款成功后告诉你；

### **获取账户信息**
可通过此脚本，获取UPKUAJING_API_KEY对应的账户信息 `auth.py --account_info`
  
## 费用

**所有API调用都会产生费用** API调用按请求次数计费。
**最新价格信息**：用户可访问 [详细价格说明](https://www.upkuajing.com/web/openapi/price.html)

在进行多次API调用之前，请告知用户预计费用并获得确认。
**确认规则：只要 query_count > 20，无论请求多少条，执行前必须：**
1. 计算所需调用次数：`ceil(query_count / 20)` 次
2. 告知用户预计消耗次数
3. 等待用户确认后再执行脚本


## 工作流程
根据用户意图选择合适的API
### 决策指南

| 用户意图 | 使用API |
|-------------|---------|
| "分析贸易模式/订单数据" | 贸易列表 |
| "找采购XXX的公司" | 公司列表 |
| "找XXX的供应商，有邮箱" | 公司列表 existEmail=1 |
| "获取公司详细信息" | 公司详情 |
| "获取联系方式" | 联系信息 |

## 使用示例

### 场景1: 小量查询 — 贸易数据分析

**用户请求**："显示2024年出口到美国的LED灯具贸易数据"
```bash
python scripts/trade_list_search.py \
  --params '{"products": ["LED lights"], "buyerCountryCodes": ["US"], "dateStart": 1704067200000, "dateEnd": 1735689599999}' \
  --query_count 20
```

如需进一步获取供应商详情：
```bash
python scripts/company_get_details.py --companyId 123456
```

### 场景 2: 大量查询 — 大数据集分析

**用户请求**："分析2024年的100条大豆贸易数据"
**执行前**告知用户：ceil(100/20) = 5 次API调用，确认后再执行；
```bash
python scripts/trade_list_search.py --params '{"products": ["soybean"], "dateStart": 1704067200000, "dateEnd": 1735689599999}' --query_count 100
```

### 场景 3: 超大量查询 - 需要多次调用脚本

**用户请求**："找从中国进口电子产品的2000家公司，要有邮箱"
**执行前**告知用户：ceil(2000/20) = 100 次API调用，确认后再执行；
```bash
python scripts/company_list_search.py --params '{"companyType": 2, "sellerCountryCodes": ["CN"], "existEmail": 1}' --query_count 1000
```
**执行结束**：脚本响应 {"task_id":"a1b2-c3d4", "file_url": "xxxxx", ……}
**继续执行，追加数据**：指定task_id，让脚本从上次的cursor处继续查询并追加到文件
```bash
python scripts/company_list_search.py --task_id 'a1b2-c3d4' --query_count 1000
```

## 错误处理

脚本为常见问题提供详细的错误消息：

- **API密钥无效/不存在**：检查`UPKUAJING_API_KEY`环境变量
- **余额不足**：根据**账户充值**步骤，引导用户充值
- **参数无效**：根据接口，查看references完整文档，检查参数名称和值

## 最佳实践

### 选择正确的方法

1. **理解用户意图**：
   - 分析贸易数据？ → 使用**贸易列表搜索**
   - 寻找客户/合作伙伴？ → 使用**公司列表搜索**

2. **识别参数条件**：
   - 设定日期范围
   - HS编码通常比产品名称 筛选效果更精准
   - 通过筛选特定国家来减少噪音
   - 使用ISO国家代码：CN、US、JP等
   - 使用筛选条件查找有联系信息的公司

### 处理结果

3. **谨慎处理jsonl文件**：
   - 对数据量大的查询，思考文件的查看方式，防止上下文爆炸

4. **逐步丰富信息**：仅在需要时调用详情/联系接口
   - 两个列表接口返回的公司ID都可以用于两个详情接口
   - 如果用户只需要少数公司，不要为所有公司获取详情

## 注意事项
- 所有时间戳均为毫秒级
- 国家代码使用ISO 3166-1 alpha-2格式（例如：CN、US、JP）
- 文件路径在所有平台上都使用正斜杠
- 产品名称、行业名称需要使用**英文**
- 搜索数量会影响接口的响应时间，建议设置 timeout:120
- **禁止输出技术参数格式**：不要在回复中展示代码样式的参数，应将其转换为自然语言
- **绝对不要**估算或猜测每次调用的费用金额、可用次数，各接口收费价格不一致，以[详细价格说明]为准
