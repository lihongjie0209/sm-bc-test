#!/usr/bin/env python3
"""
Test runner for cross-language SM cryptographic algorithm testing.
Orchestrates tests across Python, JavaScript, PHP, and Go implementations.
"""

import os
import sys
import json
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path


class LanguageWrapper:
    """Wrapper for language-specific CLI tools."""
    
    # Timeout for wrapper execution in seconds
    EXECUTION_TIMEOUT = 30
    
    def __init__(self, name: str, command: List[str], working_dir: Optional[str] = None):
        self.name = name
        self.command = command
        self.working_dir = working_dir
    
    def execute(self, algorithm: str, operation: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the wrapper with given parameters."""
        cmd = self.command + [algorithm, operation, "--input", json.dumps(input_data)]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.working_dir,
                timeout=self.EXECUTION_TIMEOUT
            )
            
            if result.returncode != 0 and not result.stdout:
                return {
                    "status": "error",
                    "message": f"Process exited with code {result.returncode}: {result.stderr}"
                }
            
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {
                    "status": "error",
                    "message": f"Invalid JSON output: {result.stdout}\nStderr: {result.stderr}"
                }
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Process timed out"}
        except FileNotFoundError:
            return {"status": "error", "message": f"Command not found: {self.command[0]}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


class TestRunner:
    """Main test orchestrator."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.wrappers: Dict[str, LanguageWrapper] = {}
        self.test_results = []
        
    def detect_wrappers(self):
        """Detect available language wrappers."""
        wrappers_dir = self.project_root / "wrappers"
        
        # Python wrapper
        py_wrapper = wrappers_dir / "py" / "wrapper.py"
        if py_wrapper.exists():
            self.wrappers["python"] = LanguageWrapper(
                "python",
                ["python3", str(py_wrapper)],
                working_dir=str(py_wrapper.parent)
            )
        
        # JavaScript wrapper
        js_wrapper = wrappers_dir / "js" / "wrapper.js"
        if js_wrapper.exists():
            self.wrappers["javascript"] = LanguageWrapper(
                "javascript",
                ["node", str(js_wrapper)],
                working_dir=str(js_wrapper.parent)
            )
        
        # PHP wrapper
        php_wrapper = wrappers_dir / "php" / "wrapper.php"
        if php_wrapper.exists():
            self.wrappers["php"] = LanguageWrapper(
                "php",
                ["php", str(php_wrapper)],
                working_dir=str(php_wrapper.parent)
            )
        
        # Go wrapper (assuming it's compiled to "wrapper" binary)
        go_wrapper = wrappers_dir / "go" / "wrapper"
        if go_wrapper.exists():
            self.wrappers["go"] = LanguageWrapper(
                "go",
                [str(go_wrapper)],
                working_dir=str(go_wrapper.parent)
            )
        
        print(f"Detected wrappers: {', '.join(self.wrappers.keys())}")
        return len(self.wrappers) > 0
    
    def test_sm3_hash(self):
        """Test SM3 hash consistency across all languages."""
        print("\n=== Testing SM3 Hash Consistency ===")
        
        test_data = "Hello, SM3!"
        hashes = {}
        
        for lang_name, wrapper in self.wrappers.items():
            print(f"Testing {lang_name}...", end=" ")
            result = wrapper.execute("sm3", "hash", {"data": test_data})
            
            if result["status"] == "success":
                hashes[lang_name] = result["output"]
                print(f"✓ Hash: {result['output'][:16]}...")
            else:
                print(f"✗ Error: {result.get('message', 'Unknown error')}")
                self.test_results.append({
                    "test": "sm3_hash",
                    "language": lang_name,
                    "status": "failed",
                    "error": result.get("message")
                })
                continue
        
        # Check consistency
        if len(set(hashes.values())) == 1:
            print("✓ All hashes match!")
            self.test_results.append({
                "test": "sm3_hash",
                "status": "passed",
                "languages": list(hashes.keys())
            })
        else:
            print("✗ Hash mismatch detected!")
            for lang, hash_val in hashes.items():
                print(f"  {lang}: {hash_val}")
            self.test_results.append({
                "test": "sm3_hash",
                "status": "failed",
                "error": "Hash values do not match",
                "hashes": hashes
            })
    
    def test_sm4_encrypt_decrypt(self):
        """Test SM4 encryption/decryption across all language pairs."""
        print("\n=== Testing SM4 Encrypt/Decrypt Cross-Language ===")
        
        plaintext = "Test message for SM4"
        key = "0123456789abcdef0123456789abcdef"  # 32 hex chars = 16 bytes
        
        languages = list(self.wrappers.keys())
        
        for encryptor_name in languages:
            encryptor = self.wrappers[encryptor_name]
            
            # Encrypt with language A
            print(f"\nEncrypting with {encryptor_name}...", end=" ")
            encrypt_result = encryptor.execute("sm4", "encrypt", {
                "plaintext": plaintext,
                "key": key,
                "mode": "ECB"
            })
            
            if encrypt_result["status"] != "success":
                print(f"✗ Error: {encrypt_result.get('message', 'Unknown error')}")
                continue
            
            ciphertext = encrypt_result["output"]
            print(f"✓ Ciphertext: {ciphertext[:16]}...")
            
            # Try to decrypt with all languages
            for decryptor_name in languages:
                decryptor = self.wrappers[decryptor_name]
                
                print(f"  Decrypting with {decryptor_name}...", end=" ")
                decrypt_result = decryptor.execute("sm4", "decrypt", {
                    "ciphertext": ciphertext,
                    "key": key,
                    "mode": "ECB"
                })
                
                if decrypt_result["status"] != "success":
                    print(f"✗ Error: {decrypt_result.get('message', 'Unknown error')}")
                    self.test_results.append({
                        "test": "sm4_encrypt_decrypt",
                        "encryptor": encryptor_name,
                        "decryptor": decryptor_name,
                        "status": "failed",
                        "error": decrypt_result.get("message")
                    })
                    continue
                
                decrypted_plaintext = decrypt_result["output"]
                
                if decrypted_plaintext == plaintext:
                    print("✓ Match")
                    self.test_results.append({
                        "test": "sm4_encrypt_decrypt",
                        "encryptor": encryptor_name,
                        "decryptor": decryptor_name,
                        "status": "passed"
                    })
                else:
                    print(f"✗ Mismatch (got: {decrypted_plaintext})")
                    self.test_results.append({
                        "test": "sm4_encrypt_decrypt",
                        "encryptor": encryptor_name,
                        "decryptor": decryptor_name,
                        "status": "failed",
                        "error": f"Plaintext mismatch: expected '{plaintext}', got '{decrypted_plaintext}'"
                    })
    
    def test_sm2_sign_verify(self):
        """Test SM2 signature/verification across all language pairs."""
        print("\n=== Testing SM2 Sign/Verify Cross-Language ===")
        
        message = "Test message for SM2 signing"
        languages = list(self.wrappers.keys())
        
        for signer_name in languages:
            signer = self.wrappers[signer_name]
            
            # Sign with language A (generate new keypair)
            print(f"\nSigning with {signer_name}...", end=" ")
            sign_result = signer.execute("sm2", "sign", {"message": message})
            
            if sign_result["status"] != "success":
                print(f"✗ Error: {sign_result.get('message', 'Unknown error')}")
                continue
            
            signature = sign_result["signature"]
            public_key = sign_result.get("public_key")
            
            if not public_key:
                print("✗ Error: No public key returned")
                continue
            
            print(f"✓ Signature: {signature[:16]}...")
            
            # Try to verify with all languages
            for verifier_name in languages:
                verifier = self.wrappers[verifier_name]
                
                print(f"  Verifying with {verifier_name}...", end=" ")
                verify_result = verifier.execute("sm2", "verify", {
                    "message": message,
                    "signature": signature,
                    "public_key": public_key
                })
                
                if verify_result["status"] != "success":
                    print(f"✗ Error: {verify_result.get('message', 'Unknown error')}")
                    self.test_results.append({
                        "test": "sm2_sign_verify",
                        "signer": signer_name,
                        "verifier": verifier_name,
                        "status": "failed",
                        "error": verify_result.get("message")
                    })
                    continue
                
                is_valid = verify_result.get("valid", False)
                
                if is_valid:
                    print("✓ Valid")
                    self.test_results.append({
                        "test": "sm2_sign_verify",
                        "signer": signer_name,
                        "verifier": verifier_name,
                        "status": "passed"
                    })
                else:
                    print("✗ Invalid")
                    self.test_results.append({
                        "test": "sm2_sign_verify",
                        "signer": signer_name,
                        "verifier": verifier_name,
                        "status": "failed",
                        "error": "Signature verification failed"
                    })
    
    def run_all_tests(self):
        """Run all cross-language tests."""
        if not self.detect_wrappers():
            print("Error: No wrappers detected!")
            return False
        
        if len(self.wrappers) < 2:
            print("Warning: Need at least 2 language wrappers for cross-language testing")
            print("Running available tests anyway...")
        
        self.test_sm3_hash()
        self.test_sm4_encrypt_decrypt()
        self.test_sm2_sign_verify()
        
        return self.print_summary()
    
    def print_summary(self):
        """Print test results summary."""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in self.test_results if r["status"] == "passed")
        failed = sum(1 for r in self.test_results if r["status"] == "failed")
        total = passed + failed
        
        print(f"Total tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        
        if failed > 0:
            print("\nFailed tests:")
            for result in self.test_results:
                if result["status"] == "failed":
                    print(f"  - {result['test']}: {result.get('error', 'Unknown error')}")
        
        # Save detailed results
        results_file = self.project_root / "test_results.json"
        with open(results_file, "w") as f:
            json.dump(self.test_results, f, indent=2)
        print(f"\nDetailed results saved to: {results_file}")
        
        return failed == 0


def main():
    # Determine project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    print("SM Cross-Language Test Runner")
    print(f"Project root: {project_root}")
    
    runner = TestRunner(str(project_root))
    success = runner.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
