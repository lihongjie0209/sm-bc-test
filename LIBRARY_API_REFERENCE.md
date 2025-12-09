# Library API Reference

This document contains API references for all SM libraries used in the cross-language testing framework.

## JavaScript (sm-js-bc)

### Installation
```bash
npm install sm-js-bc
```

### SM3 Hash
```javascript
import { SM3Digest } from 'sm-js-bc';

const digest = new SM3Digest();
const data = new TextEncoder().encode('Hello, SM3!');
digest.update(data, 0, data.length);
const hash = new Uint8Array(digest.getDigestSize());
digest.doFinal(hash, 0);
console.log(Buffer.from(hash).toString('hex'));
```

### SM4 Encryption/Decryption
```javascript
import { SM4 } from 'sm-js-bc';

// Generate key
const key = SM4.generateKey(); // 16 bytes

// Encrypt (ECB mode with PKCS7 padding by default)
const plaintext = new TextEncoder().encode('Hello, SM4!');
const ciphertext = SM4.encrypt(plaintext, key);

// Decrypt
const decrypted = SM4.decrypt(ciphertext, key);
const text = new TextDecoder().decode(decrypted);
```

### SM2 Sign/Verify
```javascript
import { SM2 } from 'sm-js-bc';

// Generate key pair
const keyPair = SM2.generateKeyPair();
// Returns: { privateKey: BigInt, publicKey: { x: BigInt, y: BigInt } }

// Sign
const message = 'Hello, SM2!';
const signature = SM2.sign(message, keyPair.privateKey);

// Verify
const isValid = SM2.verify(message, signature, keyPair.publicKey);
```

### SM2 Encrypt/Decrypt
```javascript
import { SM2 } from 'sm-js-bc';

const keyPair = SM2.generateKeyPair();

// Encrypt
const plaintext = new TextEncoder().encode('Secret message');
const ciphertext = SM2.encrypt(plaintext, keyPair.publicKey);

// Decrypt
const decrypted = SM2.decrypt(ciphertext, keyPair.privateKey);
const text = new TextDecoder().decode(decrypted);
```

## PHP (sm-php-bc)

### Installation
```bash
composer require sm-php-bc/sm-php-bc
```

### SM3 Hash
```php
use SmBc\Crypto\SM3;

$hash = SM3::hash('Hello, SM3!');
echo bin2hex($hash);
```

### SM4 Encryption/Decryption
```php
use SmBc\Crypto\SM4;

// Generate key
$key = SM4::generateKey(); // 16 bytes

// Encrypt (ECB mode with PKCS7 padding by default)
$plaintext = 'Hello, SM4!';
$ciphertext = SM4::encrypt($plaintext, $key);

// Decrypt
$decrypted = SM4::decrypt($ciphertext, $key);
```

### SM2 Sign/Verify
```php
use SmBc\Crypto\SM2;

// Generate key pair
$keyPair = SM2::generateKeyPair();
// Returns: ['privateKey' => GMP, 'publicKey' => ['x' => GMP, 'y' => GMP]]

// Sign
$message = 'Hello, SM2!';
$signature = SM2::sign($message, $keyPair['privateKey']);

// Verify
$isValid = SM2::verify($message, $signature, $keyPair['publicKey']);
```

### SM2 Encrypt/Decrypt
```php
use SmBc\Crypto\SM2;

$keyPair = SM2::generateKeyPair();

// Encrypt
$plaintext = 'Secret message';
$ciphertext = SM2::encrypt($plaintext, $keyPair['publicKey']);

// Decrypt
$decrypted = SM2::decrypt($ciphertext, $keyPair['privateKey']);
```

## Go (sm-go-bc)

### Installation
```bash
go get github.com/lihongjie0209/sm-go-bc@latest
```

### SM3 Hash
```go
import (
    "github.com/lihongjie0209/sm-go-bc/crypto/digests"
)

digest := digests.NewSM3Digest()
data := []byte("Hello, SM3!")
digest.BlockUpdate(data, 0, len(data))
hash := make([]byte, digest.GetDigestSize())
digest.DoFinal(hash, 0)
fmt.Printf("%x\n", hash)
```

### SM4 Encryption/Decryption
```go
import (
    "github.com/lihongjie0209/sm-go-bc/crypto/engines"
    "github.com/lihongjie0209/sm-go-bc/crypto/modes"
    "github.com/lihongjie0209/sm-go-bc/crypto/paddings"
    "github.com/lihongjie0209/sm-go-bc/crypto/params"
)

// Create engine
engine := engines.NewSM4Engine()
cipher := paddings.NewPaddedBufferedBlockCipher(
    modes.NewECBBlockCipher(engine),
    paddings.NewPKCS7Padding(),
)

// Encrypt
key := []byte{...} // 16 bytes
cipher.Init(true, params.NewKeyParameter(key))
plaintext := []byte("Hello, SM4!")
out := make([]byte, cipher.GetOutputSize(len(plaintext)))
n := cipher.ProcessBytes(plaintext, 0, len(plaintext), out, 0)
n, _ = cipher.DoFinal(out, n)
ciphertext := out[:n]

// Decrypt
cipher.Init(false, params.NewKeyParameter(key))
out = make([]byte, cipher.GetOutputSize(len(ciphertext)))
n = cipher.ProcessBytes(ciphertext, 0, len(ciphertext), out, 0)
n, _ = cipher.DoFinal(out, n)
decrypted := out[:n]
```

### SM2 Sign/Verify
```go
import (
    "crypto/rand"
    "math/big"
    "github.com/lihongjie0209/sm-go-bc/crypto/sm2"
    "github.com/lihongjie0209/sm-go-bc/crypto/signers"
    "github.com/lihongjie0209/sm-go-bc/crypto/params"
)

// Generate key pair
curve := sm2.GetCurve()
G := sm2.GetG()
d, _ := rand.Int(rand.Reader, sm2.GetN())
Q := G.Multiply(d)

// Sign
message := []byte("Hello, SM2!")
signer := signers.NewSM2Signer()
privParams := params.NewECPrivateKeyParameters(d, sm2.NewDomainParameters(curve, G, sm2.GetN(), 1))
signer.Init(true, privParams)
signer.Update(message)
signature, _ := signer.GenerateSignature()

// Verify
pubParams := params.NewECPublicKeyParameters(Q, sm2.NewDomainParameters(curve, G, sm2.GetN(), 1))
signer.Init(false, pubParams)
signer.Update(message)
isValid := signer.VerifySignature(signature)
```

### SM2 Encrypt/Decrypt
```go
import (
    "github.com/lihongjie0209/sm-go-bc/crypto/sm2"
    "github.com/lihongjie0209/sm-go-bc/crypto/params"
)

// Generate key pair (same as above)
curve := sm2.GetCurve()
G := sm2.GetG()
d, _ := rand.Int(rand.Reader, sm2.GetN())
Q := G.Multiply(d)

// Encrypt
engine := sm2.NewEngine()
pubParams := params.NewECPublicKeyParameters(Q, sm2.NewDomainParameters(curve, G, sm2.GetN(), 1))
engine.Init(true, pubParams)
plaintext := []byte("Secret message")
ciphertext, _ := engine.ProcessBlock(plaintext, 0, len(plaintext))

// Decrypt
privParams := params.NewECPrivateKeyParameters(d, sm2.NewDomainParameters(curve, G, sm2.GetN(), 1))
engine.Init(false, privParams)
decrypted, _ := engine.ProcessBlock(ciphertext, 0, len(ciphertext))
```

## Key Differences

### Data Types
- **JavaScript**: Uses `Uint8Array`, `BigInt` for keys
- **PHP**: Uses strings for data, `GMP` objects for big integers
- **Go**: Uses `[]byte` slices, `*big.Int` for big integers
- **Python**: Uses `bytes`, integers

### Key Formats
- **SM2 Private Key**: BigInt/GMP/big.Int representing the scalar d
- **SM2 Public Key**: Struct/dict with x, y coordinates (BigInt/GMP/big.Int)
- **SM4 Key**: 16 bytes raw binary
- **Signature**: Raw bytes (r || s format, typically 64 bytes)

### API Patterns
- **JavaScript & PHP**: High-level static methods (SM2.sign, SM4.encrypt)
- **Go & Python**: Lower-level with explicit initialization and parameter objects
