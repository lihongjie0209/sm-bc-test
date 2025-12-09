# Usage Examples

This document provides practical examples of using the sm-bc-test framework.

## Running the Test Suite

### Full Test Suite

Run all cross-language tests:

```bash
cd runner
python3 runner.py
```

Output:
```
SM Cross-Language Test Runner
Project root: /path/to/sm-bc-test
Detected wrappers: python, javascript, php, go

=== Testing SM3 Hash Consistency ===
Testing python... ✓ Hash: 66c7f0f462ee...
Testing javascript... ✓ Hash: 66c7f0f462ee...
Testing php... ✓ Hash: 66c7f0f462ee...
Testing go... ✓ Hash: 66c7f0f462ee...
✓ All hashes match!

=== Testing SM4 Encrypt/Decrypt Cross-Language ===
...

=== Testing SM2 Sign/Verify Cross-Language ===
...

============================================================
TEST SUMMARY
============================================================
Total tests: 24
Passed: 24
Failed: 0

Detailed results saved to: /path/to/sm-bc-test/test_results.json
```

## Using Individual Wrappers

### Python Wrapper

#### SM3 Hash
```bash
cd wrappers/py
python3 wrapper.py sm3 hash --input '{"data": "Hello World"}'
```

Output:
```json
{
  "status": "success",
  "output": "44f0061e69fa6fdfc290c494654a05dc0c053da7e5c52b84ef93a9d67d3fff88"
}
```

#### SM4 Encryption (ECB)
```bash
python3 wrapper.py sm4 encrypt --input '{
  "plaintext": "Hello SM4",
  "key": "0123456789abcdef0123456789abcdef",
  "mode": "ECB"
}'
```

Output:
```json
{
  "status": "success",
  "output": "a1b2c3d4e5f6..."
}
```

#### SM4 Decryption (CBC with IV)
```bash
python3 wrapper.py sm4 decrypt --input '{
  "ciphertext": "a1b2c3d4e5f6...",
  "key": "0123456789abcdef0123456789abcdef",
  "mode": "CBC",
  "iv": "fedcba9876543210fedcba9876543210"
}'
```

#### SM2 Sign (Generate New Keypair)
```bash
python3 wrapper.py sm2 sign --input '{
  "message": "Sign this message"
}'
```

Output:
```json
{
  "status": "success",
  "signature": "3046022100...",
  "private_key": "private_key_here",
  "public_key": "public_key_here"
}
```

#### SM2 Verify
```bash
python3 wrapper.py sm2 verify --input '{
  "message": "Sign this message",
  "signature": "3046022100...",
  "public_key": "public_key_here"
}'
```

Output:
```json
{
  "status": "success",
  "valid": true
}
```

### JavaScript Wrapper

#### SM3 Hash
```bash
cd wrappers/js
node wrapper.js sm3 hash --input '{"data": "Hello World"}'
```

#### SM4 Encryption
```bash
node wrapper.js sm4 encrypt --input '{
  "plaintext": "Hello SM4",
  "key": "0123456789abcdef0123456789abcdef",
  "mode": "ECB"
}'
```

#### SM2 Sign and Verify
```bash
# Sign
node wrapper.js sm2 sign --input '{"message": "Test message"}'

# Verify (use public_key from sign output)
node wrapper.js sm2 verify --input '{
  "message": "Test message",
  "signature": "...",
  "public_key": "..."
}'
```

### PHP Wrapper

#### SM3 Hash
```bash
cd wrappers/php
php wrapper.php sm3 hash --input '{"data": "Hello World"}'
```

#### SM4 Operations
```bash
# Encrypt
php wrapper.php sm4 encrypt --input '{
  "plaintext": "Hello SM4",
  "key": "0123456789abcdef0123456789abcdef"
}'

# Decrypt
php wrapper.php sm4 decrypt --input '{
  "ciphertext": "...",
  "key": "0123456789abcdef0123456789abcdef"
}'
```

### Go Wrapper

#### SM3 Hash
```bash
cd wrappers/go
./wrapper sm3 hash --input '{"data": "Hello World"}'
```

#### SM2 Encryption/Decryption
```bash
# First, generate a keypair (via sign operation)
./wrapper sm2 sign --input '{"message": "test"}' > keys.json

# Extract public key from keys.json for encryption
./wrapper sm2 encrypt --input '{
  "plaintext": "Secret message",
  "public_key": "04..."
}'

# Extract private key for decryption
./wrapper sm2 decrypt --input '{
  "ciphertext": "...",
  "private_key": "..."
}'
```

## Cross-Language Test Examples

### Example 1: Python Encrypts, Go Decrypts

```bash
# Step 1: Encrypt with Python
cd wrappers/py
ENCRYPTED=$(python3 wrapper.py sm4 encrypt --input '{
  "plaintext": "Cross-language test",
  "key": "0123456789abcdef0123456789abcdef"
}' | jq -r '.output')

echo "Encrypted: $ENCRYPTED"

# Step 2: Decrypt with Go
cd ../go
./wrapper sm4 decrypt --input "{
  \"ciphertext\": \"$ENCRYPTED\",
  \"key\": \"0123456789abcdef0123456789abcdef\"
}"
```

Expected output:
```json
{
  "status": "success",
  "output": "Cross-language test"
}
```

### Example 2: JavaScript Signs, PHP Verifies

```bash
# Step 1: Sign with JavaScript
cd wrappers/js
node wrapper.js sm2 sign --input '{"message": "Cross-language signature"}' > sig.json

SIGNATURE=$(jq -r '.signature' sig.json)
PUBLIC_KEY=$(jq -r '.public_key' sig.json)

# Step 2: Verify with PHP
cd ../php
php wrapper.php sm2 verify --input "{
  \"message\": \"Cross-language signature\",
  \"signature\": \"$SIGNATURE\",
  \"public_key\": \"$PUBLIC_KEY\"
}"
```

Expected output:
```json
{
  "status": "success",
  "valid": true
}
```

### Example 3: SM3 Consistency Check

```bash
# Hash the same data with all languages
MESSAGE="Consistency test"

cd wrappers/py
HASH_PY=$(python3 wrapper.py sm3 hash --input "{\"data\": \"$MESSAGE\"}" | jq -r '.output')

cd ../js
HASH_JS=$(node wrapper.js sm3 hash --input "{\"data\": \"$MESSAGE\"}" | jq -r '.output')

cd ../php
HASH_PHP=$(php wrapper.php sm3 hash --input "{\"data\": \"$MESSAGE\"}" | jq -r '.output')

cd ../go
HASH_GO=$(./wrapper sm3 hash --input "{\"data\": \"$MESSAGE\"}" | jq -r '.output')

# Compare
echo "Python:     $HASH_PY"
echo "JavaScript: $HASH_JS"
echo "PHP:        $HASH_PHP"
echo "Go:         $HASH_GO"

if [ "$HASH_PY" = "$HASH_JS" ] && [ "$HASH_JS" = "$HASH_PHP" ] && [ "$HASH_PHP" = "$HASH_GO" ]; then
    echo "✓ All hashes match!"
else
    echo "✗ Hash mismatch detected!"
fi
```

## Error Handling Examples

### Invalid Input
```bash
python3 wrapper.py sm3 hash --input '{"invalid": "json"}'
```

Output:
```json
{
  "status": "error",
  "message": "missing or invalid 'data' field"
}
```

### Unsupported Operation
```bash
python3 wrapper.py sm3 invalid --input '{"data": "test"}'
```

Output:
```json
{
  "status": "error",
  "message": "Unsupported operation: sm3 invalid"
}
```

### Invalid Signature Verification
```bash
python3 wrapper.py sm2 verify --input '{
  "message": "Original message",
  "signature": "invalid_signature",
  "public_key": "..."
}'
```

Output:
```json
{
  "status": "success",
  "valid": false
}
```

## Integration with Scripts

### Bash Script Example

```bash
#!/bin/bash
# test_sm4.sh - Test SM4 encryption/decryption

KEY="0123456789abcdef0123456789abcdef"
PLAINTEXT="Secret message"

# Encrypt
RESULT=$(python3 wrappers/py/wrapper.py sm4 encrypt --input "{
  \"plaintext\": \"$PLAINTEXT\",
  \"key\": \"$KEY\"
}")

STATUS=$(echo $RESULT | jq -r '.status')
if [ "$STATUS" != "success" ]; then
    echo "Encryption failed"
    exit 1
fi

CIPHERTEXT=$(echo $RESULT | jq -r '.output')
echo "Encrypted: $CIPHERTEXT"

# Decrypt
RESULT=$(node wrappers/js/wrapper.js sm4 decrypt --input "{
  \"ciphertext\": \"$CIPHERTEXT\",
  \"key\": \"$KEY\"
}")

DECRYPTED=$(echo $RESULT | jq -r '.output')
echo "Decrypted: $DECRYPTED"

if [ "$DECRYPTED" = "$PLAINTEXT" ]; then
    echo "✓ Test passed"
else
    echo "✗ Test failed"
    exit 1
fi
```

### Python Script Example

```python
#!/usr/bin/env python3
import json
import subprocess

def call_wrapper(lang, algorithm, operation, input_data):
    wrapper_paths = {
        'py': 'wrappers/py/wrapper.py',
        'js': 'wrappers/js/wrapper.js',
        'php': 'wrappers/php/wrapper.php',
        'go': 'wrappers/go/wrapper'
    }
    
    cmd = [
        'python3' if lang == 'py' else 'node' if lang == 'js' else 'php' if lang == 'php' else '',
        wrapper_paths[lang],
        algorithm,
        operation,
        '--input',
        json.dumps(input_data)
    ]
    
    if lang == 'go':
        cmd = [wrapper_paths[lang], algorithm, operation, '--input', json.dumps(input_data)]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

# Test cross-language compatibility
plaintext = "Test message"
key = "0123456789abcdef0123456789abcdef"

# Python encrypts
encrypted = call_wrapper('py', 'sm4', 'encrypt', {
    'plaintext': plaintext,
    'key': key
})

print(f"Encrypted: {encrypted['output']}")

# JavaScript decrypts
decrypted = call_wrapper('js', 'sm4', 'decrypt', {
    'ciphertext': encrypted['output'],
    'key': key
})

print(f"Decrypted: {decrypted['output']}")
print(f"Match: {decrypted['output'] == plaintext}")
```

## Troubleshooting

### Wrapper Not Found
If you get "wrapper not found" errors:

```bash
# Make scripts executable
chmod +x wrappers/*/wrapper.*
chmod +x runner/runner.py

# For Go, rebuild the binary
cd wrappers/go
go build -o wrapper wrapper.go
```

### Dependency Issues
If you get import errors:

```bash
# Reinstall dependencies
./setup.sh

# Or manually for each language
cd wrappers/py && pip install -r requirements.txt
cd wrappers/js && npm install
cd wrappers/php && composer install
cd wrappers/go && go mod tidy
```

### JSON Parse Errors
Make sure to properly escape quotes in shell commands:

```bash
# Bad
wrapper.py sm3 hash --input {"data": "test"}

# Good
wrapper.py sm3 hash --input '{"data": "test"}'
```
