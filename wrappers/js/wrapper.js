#!/usr/bin/env node
/**
 * JavaScript wrapper for SM cryptographic algorithms.
 * Provides a unified CLI interface for cross-language testing.
 */

const { Command } = require('commander');

let SM2, SM3, SM4;
try {
    const smLib = require('sm-js-bc');
    SM2 = smLib.SM2;
    SM3 = smLib.SM3;
    SM4 = smLib.SM4;
} catch (error) {
    console.error(JSON.stringify({
        status: 'error',
        message: 'sm-js-bc library not installed'
    }));
    process.exit(1);
}

function sm3Hash(data) {
    try {
        const inputData = data.data || '';
        const sm3 = new SM3();
        const result = sm3.hash(inputData);
        
        return {
            status: 'success',
            output: result
        };
    } catch (error) {
        return {
            status: 'error',
            message: error.message
        };
    }
}

function sm4Encrypt(data) {
    try {
        const plaintext = data.plaintext || '';
        const key = data.key || '';
        const mode = data.mode || 'ECB';
        const iv = data.iv || '';
        
        const sm4 = new SM4(key, mode, iv || undefined);
        const ciphertext = sm4.encrypt(plaintext);
        
        return {
            status: 'success',
            output: ciphertext
        };
    } catch (error) {
        return {
            status: 'error',
            message: error.message
        };
    }
}

function sm4Decrypt(data) {
    try {
        const ciphertext = data.ciphertext || '';
        const key = data.key || '';
        const mode = data.mode || 'ECB';
        const iv = data.iv || '';
        
        const sm4 = new SM4(key, mode, iv || undefined);
        const plaintext = sm4.decrypt(ciphertext);
        
        return {
            status: 'success',
            output: plaintext
        };
    } catch (error) {
        return {
            status: 'error',
            message: error.message
        };
    }
}

function sm2Sign(data) {
    try {
        const message = data.message || '';
        let privateKey = data.private_key || '';
        
        const sm2 = new SM2();
        
        if (!privateKey) {
            // Generate new key pair if not provided
            const keypair = sm2.generateKeypair();
            privateKey = keypair.privateKey;
            const publicKey = keypair.publicKey;
            
            const signature = sm2.sign(message, privateKey);
            
            return {
                status: 'success',
                signature: signature,
                private_key: privateKey,
                public_key: publicKey
            };
        } else {
            const signature = sm2.sign(message, privateKey);
            
            return {
                status: 'success',
                signature: signature
            };
        }
    } catch (error) {
        return {
            status: 'error',
            message: error.message
        };
    }
}

function sm2Verify(data) {
    try {
        const message = data.message || '';
        const signature = data.signature || '';
        const publicKey = data.public_key || '';
        
        const sm2 = new SM2();
        const isValid = sm2.verify(message, signature, publicKey);
        
        return {
            status: 'success',
            valid: Boolean(isValid)
        };
    } catch (error) {
        return {
            status: 'error',
            message: error.message
        };
    }
}

function sm2Encrypt(data) {
    try {
        const plaintext = data.plaintext || '';
        const publicKey = data.public_key || '';
        
        const sm2 = new SM2();
        const ciphertext = sm2.encrypt(plaintext, publicKey);
        
        return {
            status: 'success',
            output: ciphertext
        };
    } catch (error) {
        return {
            status: 'error',
            message: error.message
        };
    }
}

function sm2Decrypt(data) {
    try {
        const ciphertext = data.ciphertext || '';
        const privateKey = data.private_key || '';
        
        const sm2 = new SM2();
        const plaintext = sm2.decrypt(ciphertext, privateKey);
        
        return {
            status: 'success',
            output: plaintext
        };
    } catch (error) {
        return {
            status: 'error',
            message: error.message
        };
    }
}

const handlers = {
    'sm3-hash': sm3Hash,
    'sm4-encrypt': sm4Encrypt,
    'sm4-decrypt': sm4Decrypt,
    'sm2-sign': sm2Sign,
    'sm2-verify': sm2Verify,
    'sm2-encrypt': sm2Encrypt,
    'sm2-decrypt': sm2Decrypt,
};

function main() {
    const program = new Command();
    
    program
        .name('wrapper')
        .description('JavaScript SM cryptography CLI wrapper')
        .argument('<algorithm>', 'Algorithm to use (sm2, sm3, sm4)')
        .argument('<operation>', 'Operation to perform')
        .requiredOption('--input <json>', 'JSON input data')
        .action((algorithm, operation, options) => {
            let inputData;
            try {
                inputData = JSON.parse(options.input);
            } catch (error) {
                console.log(JSON.stringify({
                    status: 'error',
                    message: `Invalid JSON input: ${error.message}`
                }));
                process.exit(1);
            }
            
            const key = `${algorithm.toLowerCase()}-${operation.toLowerCase()}`;
            const handler = handlers[key];
            
            if (!handler) {
                console.log(JSON.stringify({
                    status: 'error',
                    message: `Unsupported operation: ${algorithm} ${operation}`
                }));
                process.exit(1);
            }
            
            const result = handler(inputData);
            console.log(JSON.stringify(result));
            
            process.exit(result.status === 'success' ? 0 : 1);
        });
    
    program.parse();
}

if (require.main === module) {
    main();
}
