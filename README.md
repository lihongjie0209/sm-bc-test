# sm-bc-test

Cross-language interoperability testing framework for SM (ShangMi) cryptographic algorithms.

## Overview

This project provides a comprehensive testing framework to validate cross-language compatibility of SM2, SM3, and SM4 cryptographic algorithm implementations across Python, JavaScript, PHP, and Go.

## Project Structure

```
sm-bc-test/
├── wrappers/           # Language-specific CLI wrappers
│   ├── py/            # Python wrapper
│   │   ├── wrapper.py
│   │   └── requirements.txt
│   ├── js/            # JavaScript wrapper
│   │   ├── wrapper.js
│   │   └── package.json
│   ├── php/           # PHP wrapper
│   │   ├── wrapper.php
│   │   └── composer.json
│   └── go/            # Go wrapper
│       ├── wrapper.go
│       └── go.mod
├── runner/            # Test orchestration
│   ├── runner.py
│   └── requirements.txt
├── fixtures/          # Test data (optional)
└── docs/             # Documentation
    └── prd.md
```

## Quick Start

### Prerequisites

- Python 3.7+
- Node.js 14+
- PHP 7.4+
- Go 1.21+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/lihongjie0209/sm-bc-test.git
cd sm-bc-test
```

2. Install dependencies for each wrapper:

**Python:**
```bash
cd wrappers/py
pip install -r requirements.txt
```

**JavaScript:**
```bash
cd wrappers/js
npm install
```

**PHP:**
```bash
cd wrappers/php
composer install
```

**Go:**
```bash
cd wrappers/go
go mod tidy
go build -o wrapper wrapper.go
```

### Running Tests

```bash
cd runner
python3 runner.py
```

## Wrapper CLI Interface

All wrappers follow a unified CLI interface:

```bash
./wrapper <algorithm> <operation> --input '{"key": "value"}'
```

### Supported Operations

**SM3:**
- `hash`: Compute hash digest

**SM4:**
- `encrypt`: Encrypt data (ECB/CBC mode)
- `decrypt`: Decrypt data (ECB/CBC mode)

**SM2:**
- `sign`: Generate signature
- `verify`: Verify signature
- `encrypt`: Encrypt data
- `decrypt`: Decrypt data

### Output Format

All wrappers output JSON:
```json
{
  "status": "success",
  "output": "..."
}
```

Or on error:
```json
{
  "status": "error",
  "message": "error description"
}
```

## Test Coverage

The test runner validates:

1. **SM3 Hash Consistency**: All languages produce identical hash values for the same input
2. **SM4 Cross-Encryption**: Data encrypted by language A can be decrypted by language B
3. **SM2 Cross-Signing**: Signatures created by language A can be verified by language B

## Dependencies

Each wrapper uses the corresponding SM cryptographic library:

- Python: [sm-py-bc](https://github.com/lihongjie0209/sm-py-bc)
- JavaScript: [sm-js-bc](https://github.com/lihongjie0209/sm-js-bc)
- PHP: [sm-php-bc](https://github.com/lihongjie0209/sm-php-bc)
- Go: [sm-go-bc](https://github.com/lihongjie0209/sm-go-bc)

## Development

### Adding New Tests

Edit `runner/runner.py` and add test methods following the existing pattern.

### Testing Individual Wrappers

Each wrapper can be tested independently:

```bash
# Python
cd wrappers/py
python3 wrapper.py sm3 hash --input '{"data": "test"}'

# JavaScript
cd wrappers/js
node wrapper.js sm3 hash --input '{"data": "test"}'

# PHP
cd wrappers/php
php wrapper.php sm3 hash --input '{"data": "test"}'

# Go
cd wrappers/go
./wrapper sm3 hash --input '{"data": "test"}'
```

## Contributing

Contributions are welcome! Please ensure:
1. All wrappers maintain the unified interface
2. New operations are implemented across all languages
3. Tests are updated to cover new functionality

## License

See individual library repositories for licensing information.