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
    from sm_bc.crypto.digests import SM3Digest
    from sm_bc.crypto.SM2 import SM2
    from sm_bc.crypto.cipher import create_sm4_cipher
except ImportError as e:
    print(json.dumps({"status": "error", "message": f"sm-py-bc library not installed: {e}"}), file=sys.stderr)
    sys.exit(1)


def sm3_hash(data: Dict[str, Any]) -> Dict[str, Any]:
    """Compute SM3 hash of input data."""
    try:
        input_data = data.get("data", "")
        if isinstance(input_data, str):
            input_data = input_data.encode()
        
        digest = SM3Digest()
        digest.update_bytes(input_data, 0, len(input_data))
        result = bytearray(digest.get_digest_size())
        digest.do_final(result, 0)
        
        return {
            "status": "success",
            "output": result.hex()
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
        
        # Create cipher
        cipher = create_sm4_cipher(mode=mode.upper(), padding="PKCS7")
        
        # Initialize with key (and IV for CBC)
        if mode.upper() == "CBC" and iv:
            cipher.init(True, key, iv)
        else:
            cipher.init(True, key, None)
        
        # Encrypt
        ciphertext = cipher.encrypt(plaintext)
        
        return {
            "status": "success",
            "output": ciphertext.hex()
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
        
        # Create cipher
        cipher = create_sm4_cipher(mode=mode.upper(), padding="PKCS7")
        
        # Initialize with key (and IV for CBC)
        if mode.upper() == "CBC" and iv:
            cipher.init(False, key, iv)
        else:
            cipher.init(False, key, None)
        
        # Decrypt
        plaintext = cipher.decrypt(ciphertext)
        
        return {
            "status": "success",
            "output": plaintext.decode()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def sm2_sign(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sign data using SM2."""
    try:
        message = data.get("message", "")
        private_key_hex = data.get("private_key", "")
        
        # Generate or use provided private key
        if private_key_hex:
            d = int(private_key_hex, 16)
            # Calculate public key
            G = SM2.get_G()
            Q = G.multiply(d)
            public_key_hex = "04" + hex(Q.get_affine_x_coord().to_big_integer())[2:].zfill(64) + \
                             hex(Q.get_affine_y_coord().to_big_integer())[2:].zfill(64)
        else:
            # Generate new key pair
            keypair = SM2.generate_key_pair()
            d = keypair['private_key']
            private_key_hex = hex(d)[2:].zfill(64)
            public_key_hex = "04" + hex(keypair['public_key']['x'])[2:].zfill(64) + \
                             hex(keypair['public_key']['y'])[2:].zfill(64)
        
        # Sign
        signature = SM2.sign(message, d)
        
        result = {
            "status": "success",
            "signature": signature.hex()
        }
        
        # Include keys if generated
        if not data.get("private_key"):
            result["private_key"] = private_key_hex
            result["public_key"] = public_key_hex
        
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}


def sm2_verify(data: Dict[str, Any]) -> Dict[str, Any]:
    """Verify SM2 signature."""
    try:
        message = data.get("message", "")
        signature_hex = data.get("signature", "")
        public_key_hex = data.get("public_key", "")
        
        # Parse signature
        signature = bytes.fromhex(signature_hex)
        
        # Parse public key
        if public_key_hex.startswith("04"):
            public_key_hex = public_key_hex[2:]
        x = int(public_key_hex[:64], 16)
        y = int(public_key_hex[64:128], 16)
        
        # Verify
        is_valid = SM2.verify(message, signature, {'x': x, 'y': y})
        
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
        public_key_hex = data.get("public_key", "")
        
        # Parse public key
        if public_key_hex.startswith("04"):
            public_key_hex = public_key_hex[2:]
        x = int(public_key_hex[:64], 16)
        y = int(public_key_hex[64:128], 16)
        
        # Encrypt
        ciphertext = SM2.encrypt(plaintext, {'x': x, 'y': y})
        
        return {
            "status": "success",
            "output": ciphertext.hex()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def sm2_decrypt(data: Dict[str, Any]) -> Dict[str, Any]:
    """Decrypt data using SM2."""
    try:
        ciphertext = data.get("ciphertext", "")
        private_key_hex = data.get("private_key", "")
        
        if isinstance(ciphertext, str):
            ciphertext = bytes.fromhex(ciphertext)
        
        # Parse private key
        d = int(private_key_hex, 16)
        
        # Decrypt
        plaintext = SM2.decrypt(ciphertext, d)
        
        return {
            "status": "success",
            "output": plaintext.decode()
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
