# Architecture Documentation

## Overview

The sm-bc-test framework is designed to validate interoperability of SM cryptographic algorithm implementations across multiple programming languages.

## Design Principles

1. **Unified Interface**: All language wrappers expose the same CLI interface
2. **Language Independence**: Test runner doesn't depend on any specific wrapper implementation
3. **JSON Communication**: All data exchange uses JSON for language neutrality
4. **Modular Design**: Each wrapper is self-contained and can be developed/tested independently

## Components

### 1. Language Wrappers

Each wrapper is a CLI tool that:
- Accepts algorithm and operation as positional arguments
- Takes input data as JSON via `--input` flag
- Returns results as JSON to stdout
- Returns exit code 0 for success, non-zero for errors

**Interface Contract:**

```
wrapper <algorithm> <operation> --input '<json>'
```

**Input Format:**
```json
{
  "data": "...",           // For SM3 hash
  "plaintext": "...",      // For encryption
  "ciphertext": "...",     // For decryption
  "key": "...",            // For SM4
  "mode": "ECB|CBC",       // For SM4
  "iv": "...",             // For SM4 CBC
  "message": "...",        // For SM2 sign/verify
  "signature": "...",      // For SM2 verify
  "private_key": "...",    // For SM2 sign/decrypt
  "public_key": "..."      // For SM2 verify/encrypt
}
```

**Output Format:**
```json
{
  "status": "success|error",
  "output": "...",          // Result data (hex string)
  "message": "...",         // Error message if status=error
  "valid": true|false,      // For SM2 verify
  "signature": "...",       // For SM2 sign
  "private_key": "...",     // For SM2 sign (when generated)
  "public_key": "..."       // For SM2 sign (when generated)
}
```

### 2. Test Runner

The test runner (`runner/runner.py`) orchestrates cross-language tests:

**Test Flow:**

```
1. Detect Available Wrappers
   └─> Scan wrappers/ directory for executable scripts

2. SM3 Hash Consistency Test
   ├─> Hash same input with all languages
   └─> Verify all hashes match

3. SM4 Encrypt/Decrypt Cross-Language Test
   └─> For each language pair (A, B):
       ├─> A encrypts plaintext
       └─> B decrypts ciphertext
           └─> Verify plaintext matches

4. SM2 Sign/Verify Cross-Language Test
   └─> For each language pair (A, B):
       ├─> A generates keypair and signs message
       └─> B verifies signature with public key
           └─> Verify signature is valid
```

**Test Matrix:**

For N languages, the test matrix is:
- SM3: N tests (consistency check)
- SM4: N × N tests (all pairs)
- SM2 Sign/Verify: N × N tests (all pairs)

Total: N + 2N² tests

### 3. Dependency Management

Each wrapper manages its own dependencies:

- **Python**: `pip` with `requirements.txt`
- **JavaScript**: `npm` with `package.json`
- **PHP**: `composer` with `composer.json`
- **Go**: `go mod` with `go.mod`

All wrappers reference the corresponding SM library from GitHub.

## Test Results

Test results are saved to `test_results.json` with format:

```json
[
  {
    "test": "sm3_hash|sm4_encrypt_decrypt|sm2_sign_verify",
    "status": "passed|failed",
    "encryptor": "language_name",
    "decryptor": "language_name",
    "signer": "language_name",
    "verifier": "language_name",
    "error": "error message if failed"
  }
]
```

## Extension Points

### Adding New Operations

1. Update all wrappers to support the new operation
2. Add test method in `runner.py`
3. Update documentation

### Adding New Languages

1. Create new wrapper directory under `wrappers/`
2. Implement CLI interface following the contract
3. Add dependency management file
4. Test runner will auto-detect it

### Custom Test Vectors

Place test data in `fixtures/` directory and modify test runner to load and use them.

## Error Handling

### Wrapper Level
- Invalid input → JSON error response with exit code 1
- Library error → JSON error response with exit code 1
- Missing dependency → JSON error response with exit code 1

### Runner Level
- Wrapper not found → Skip language, log warning
- Wrapper timeout (30s) → Mark test as failed
- JSON parse error → Mark test as failed
- Verification failure → Mark test as failed

## Security Considerations

1. **Key Management**: Test keys are generated dynamically, not stored
2. **Input Validation**: Wrappers should validate input before processing
3. **Hex Encoding**: Binary data is hex-encoded for safe JSON transport
4. **Error Messages**: Should not leak sensitive information

## Performance

- Tests run sequentially to avoid resource conflicts
- Each wrapper operation has 30-second timeout
- No persistent state between tests
- Test runner uses subprocess for isolation

## Future Enhancements

1. **Parallel Execution**: Run independent tests concurrently
2. **Test Vectors**: Add official SM algorithm test vectors
3. **Performance Benchmarks**: Add timing measurements
4. **CI Integration**: GitHub Actions workflow
5. **Docker Support**: Containerized testing environment
6. **Web Dashboard**: Visual test results display
