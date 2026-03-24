# upkuajing-trade-company-search

An AI Agent Skill for querying customs trade data through the UpKuajing Open Platform to discover potential customers and business partners.

![upkuajing](upkuajing.png)

## Features

- **Trade Order Search**: Query import/export records, transaction amounts, and trade routes
- **Company Discovery**: Reverse search for potential customers and suppliers through trade data
- **Company Details**: Get corporate business information and background data
- **Contact Information**: Query emails, phones, social media, and other contact details

Use cases: Foreign trade customer development, competitive supply chain analysis, logistics industry customer discovery, import/export market research.

## Skill Installation

### OpenClaw Installation

1. Copy the entire skill directory to OpenClaw's skills directory:
```bash
cp -r upkuajing-trade-company-search ~/.openclaw/workspace/skills/
```

2. Or create a symbolic link:
```bash
ln -s /path/to/upkuajing-trade-company-search ~/.openclaw/workspace/skills/
```

3. Restart OpenClaw to activate the skill

### Claude Code Installation

1. Copy the entire skill directory to Claude Code's skills directory:
```bash
cp -r upkuajing-trade-company-search ~/.claude/skills/
```

2. Or configure the skills path in Claude Code settings to point to this directory

### Directory Structure Requirements

Ensure the skill directory contains the following structure:
```
upkuajing-trade-company-search/
├── SKILL.md              # Skill description file (required)
├── requirements.txt      # Python dependencies
├── scripts/              # Python scripts directory (required)
│   ├── auth.py
│   ├── common.py
│   ├── trade_list_search.py
│   ├── company_list_search.py
│   ├── company_get_details.py
│   └── company_get_contact.py
└── references/           # API reference documentation
    ├── trade-list-api.md
    ├── company-list-api.md
    ├── company-detail-api.md
    └── contact-fetch-api.md
```

## Environment Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set API Key

**Method 1: Using Environment Variables**
```bash
export UPKUAJING_API_KEY=your_api_key_here
```

**Method 2: Using .env File**
```bash
cp .env.example .env
# Edit .env file and fill in your API key
```

### 3. Apply for API Key

If you don't have an API key, you can apply through:
```bash
python scripts/auth.py --new_key
```

## Quick Start

### Using in AI Agent

After installation, you can use it directly in supported AI Agent tools:

**Search Trade Orders**
```
Help me find US import records of LED products from China
```

**Discover Potential Customers**
```
Find US companies that import electronics
```

**Get Company Details**
```
Get detailed information for this trading company: [Company ID]
```

### Command Line Usage

You can also call Python scripts directly:

```bash
# Trade list search
python scripts/trade_list_search.py \
  --params '{"importCountries": ["US"], "exportCountries": ["CN"], "products": ["LED"]}' \
  --query_count 20

# Company list search
python scripts/company_list_search.py \
  --params '{"importCountries": ["US"]}' \
  --query_count 20

# Get company details
python scripts/company_get_details.py --pid [Company ID]

# Get contact information
python scripts/company_get_contact.py --pid [Company ID]
```

## Usage Examples

### Scenario 1: Foreign Trade Customer Development

Discover potential customers importing specific products:
```bash
python scripts/company_list_search.py \
  --params '{"importCountries": ["US"], "products": ["electronics"]}' \
  --query_count 50
```

### Scenario 2: Competitive Analysis

Analyze competitors' supply chains:
```bash
# Find competitors' suppliers
python scripts/trade_list_search.py \
  --params '{"importCountries": ["US"], "exportCountries": ["CN"]}' \
  --query_count 100
```

### Scenario 3: Market Research

Research trade flows for specific products:
```bash
python scripts/trade_list_search.py \
  --params '{"products": ["solar panels"], "year": 2025}' \
  --query_count 200
```

## API Reference

For detailed API parameter descriptions, please refer to the documentation in the `references/` directory:
- [Trade List Search](references/trade-list-api.md)
- [Company List Search](references/company-list-api.md)
- [Company Details](references/company-detail-api.md)
- [Contact Information](references/contact-fetch-api.md)

## Data-Driven Approach

Unlike `upkuajing-company-people-search`, this skill is based on customs trade data.

## Pricing

All API calls incur fees. For latest pricing, please visit: https://www.upkuajing.com/openapi/pricing

**Account Recharge:**
```bash
python scripts/auth.py --new_rec_order
```

**Account Info Query:**
```bash
python scripts/auth.py --account_info
```

## Troubleshooting

### Invalid API Key
Check if the API key in environment variables or .env file is correctly set.

### Insufficient Balance
Run `python scripts/auth.py --account_info` to check account balance and recharge if needed.

### Permission Error
Confirm that your API key has access to the relevant API endpoints.

### No Data Returned
- Adjust search criteria and use more general keywords
- Check if country codes are correct (use ISO 3166-1 alpha-2 format)
- Try reducing filter conditions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Support

For questions or suggestions, please submit an Issue or Pull Request.
