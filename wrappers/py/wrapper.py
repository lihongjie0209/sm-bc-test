#!/usr/bin/env python3
"""
Python wrapper for SM cryptographic algorithms.
Provides a unified CLI interface for cross-language testing.
"""

import sys
import json
import argparse
from typing import Dict, Any

try:
    from sm_py_bc import SM2, SM3, SM4
except ImportError:
    print(json.dumps({"status": "error", "message": "sm-py-bc library not installed"}), file=sys.stderr)
    sys.exit(1)


def sm3_hash(data: Dict[str, Any]) -> Dict[str, Any]:
    """Compute SM3 hash of input data."""
    try:
        input_data = data.get("data", "")
        if isinstance(input_data, str):
            input_data = input_data.encode()
        
        sm3 = SM3()
        result = sm3.hash(input_data)
        
        return {
            "status": "success",
            "output": result.hex() if isinstance(result, bytes) else result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def sm4_encrypt(data: Dict[str, Any]) -> Dict[str, Any]:
    """Encrypt data using SM4."""
    try:
        plaintext = data.get("plaintext", "")
        key = data.get("key", "")
        mode = data.get("mode", "ECB")
        iv = data.get("iv", "")
        
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()
        if isinstance(key, str):
            key = bytes.fromhex(key)
        if isinstance(iv, str) and iv:
            iv = bytes.fromhex(iv)
        
        sm4 = SM4(key, mode=mode, iv=iv if iv else None)
        ciphertext = sm4.encrypt(plaintext)
        
        return {
            "status": "success",
            "output": ciphertext.hex() if isinstance(ciphertext, bytes) else ciphertext
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def sm4_decrypt(data: Dict[str, Any]) -> Dict[str, Any]:
    """Decrypt data using SM4."""
    try:
        ciphertext = data.get("ciphertext", "")
        key = data.get("key", "")
        mode = data.get("mode", "ECB")
        iv = data.get("iv", "")
        
        if isinstance(ciphertext, str):
            ciphertext = bytes.fromhex(ciphertext)
        if isinstance(key, str):
            key = bytes.fromhex(key)
        if isinstance(iv, str) and iv:
            iv = bytes.fromhex(iv)
        
        sm4 = SM4(key, mode=mode, iv=iv if iv else None)
        plaintext = sm4.decrypt(ciphertext)
        
        return {
            "status": "success",
            "output": plaintext.decode() if isinstance(plaintext, bytes) else plaintext
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def sm2_sign(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sign data using SM2."""
    try:
        message = data.get("message", "")
        private_key = data.get("private_key", "")
        
        if isinstance(message, str):
            message = message.encode()
        
        sm2 = SM2()
        if private_key:
            sm2.set_private_key(private_key)
        else:
            # Generate new key pair if not provided
            private_key, public_key = sm2.generate_keypair()
            
        signature = sm2.sign(message)
        
        result = {
            "status": "success",
            "signature": signature.hex() if isinstance(signature, bytes) else signature
        }
        
        # Include keys if generated
        if not data.get("private_key"):
            result["private_key"] = private_key
            result["public_key"] = public_key
        
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


def sm2_verify(data: Dict[str, Any]) -> Dict[str, Any]:
    """Verify SM2 signature."""
    try:
        message = data.get("message", "")
        signature = data.get("signature", "")
        public_key = data.get("public_key", "")
        
        if isinstance(message, str):
            message = message.encode()
        if isinstance(signature, str):
            signature = bytes.fromhex(signature)
        
        sm2 = SM2()
        sm2.set_public_key(public_key)
        
        is_valid = sm2.verify(message, signature)
        
        return {
            "status": "success",
            "valid": bool(is_valid)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def sm2_encrypt(data: Dict[str, Any]) -> Dict[str, Any]:
    """Encrypt data using SM2."""
    try:
        plaintext = data.get("plaintext", "")
        public_key = data.get("public_key", "")
        
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()
        
        sm2 = SM2()
        sm2.set_public_key(public_key)
        
        ciphertext = sm2.encrypt(plaintext)
        
        return {
            "status": "success",
            "output": ciphertext.hex() if isinstance(ciphertext, bytes) else ciphertext
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def sm2_decrypt(data: Dict[str, Any]) -> Dict[str, Any]:
    """Decrypt data using SM2."""
    try:
        ciphertext = data.get("ciphertext", "")
        private_key = data.get("private_key", "")
        
        if isinstance(ciphertext, str):
            ciphertext = bytes.fromhex(ciphertext)
        
        sm2 = SM2()
        sm2.set_private_key(private_key)
        
        plaintext = sm2.decrypt(ciphertext)
        
        return {
            "status": "success",
            "output": plaintext.decode() if isinstance(plaintext, bytes) else plaintext
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Python SM cryptography CLI wrapper")
    parser.add_argument("algorithm", choices=["sm2", "sm3", "sm4"], help="Algorithm to use")
    parser.add_argument("operation", help="Operation to perform")
    parser.add_argument("--input", required=True, help="JSON input data")
    
    args = parser.parse_args()
    
    try:
        input_data = json.loads(args.input)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "message": f"Invalid JSON input: {e}"}))
        sys.exit(1)
    
    # Route to appropriate handler
    handlers = {
        ("sm3", "hash"): sm3_hash,
        ("sm4", "encrypt"): sm4_encrypt,
        ("sm4", "decrypt"): sm4_decrypt,
        ("sm2", "sign"): sm2_sign,
        ("sm2", "verify"): sm2_verify,
        ("sm2", "encrypt"): sm2_encrypt,
        ("sm2", "decrypt"): sm2_decrypt,
    }
    
    key = (args.algorithm.lower(), args.operation.lower())
    handler = handlers.get(key)
    
    if not handler:
        print(json.dumps({
            "status": "error",
            "message": f"Unsupported operation: {args.algorithm} {args.operation}"
        }))
        sys.exit(1)
    
    result = handler(input_data)
    print(json.dumps(result))
    
    sys.exit(0 if result["status"] == "success" else 1)


if __name__ == "__main__":
    main()
