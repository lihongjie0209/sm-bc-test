#!/usr/bin/env php
<?php
/**
 * PHP wrapper for SM cryptographic algorithms.
 * Provides a unified CLI interface for cross-language testing.
 */

require_once __DIR__ . '/vendor/autoload.php';

use SmPhpBc\SM2;
use SmPhpBc\SM3;
use SmPhpBc\SM4;

function sm3Hash($data) {
    try {
        $inputData = $data['data'] ?? '';
        $sm3 = new SM3();
        $result = $sm3->hash($inputData);
        
        return [
            'status' => 'success',
            'output' => $result
        ];
    } catch (Exception $e) {
        return [
            'status' => 'error',
            'message' => $e->getMessage()
        ];
    }
}

function sm4Encrypt($data) {
    try {
        $plaintext = $data['plaintext'] ?? '';
        $key = $data['key'] ?? '';
        $mode = $data['mode'] ?? 'ECB';
        $iv = $data['iv'] ?? '';
        
        $sm4 = new SM4($key, $mode, $iv ?: null);
        $ciphertext = $sm4->encrypt($plaintext);
        
        return [
            'status' => 'success',
            'output' => $ciphertext
        ];
    } catch (Exception $e) {
        return [
            'status' => 'error',
            'message' => $e->getMessage()
        ];
    }
}

function sm4Decrypt($data) {
    try {
        $ciphertext = $data['ciphertext'] ?? '';
        $key = $data['key'] ?? '';
        $mode = $data['mode'] ?? 'ECB';
        $iv = $data['iv'] ?? '';
        
        $sm4 = new SM4($key, $mode, $iv ?: null);
        $plaintext = $sm4->decrypt($ciphertext);
        
        return [
            'status' => 'success',
            'output' => $plaintext
        ];
    } catch (Exception $e) {
        return [
            'status' => 'error',
            'message' => $e->getMessage()
        ];
    }
}

function sm2Sign($data) {
    try {
        $message = $data['message'] ?? '';
        $privateKey = $data['private_key'] ?? '';
        
        $sm2 = new SM2();
        
        if (empty($privateKey)) {
            // Generate new key pair if not provided
            $keypair = $sm2->generateKeypair();
            $privateKey = $keypair['privateKey'];
            $publicKey = $keypair['publicKey'];
            
            $signature = $sm2->sign($message, $privateKey);
            
            return [
                'status' => 'success',
                'signature' => $signature,
                'private_key' => $privateKey,
                'public_key' => $publicKey
            ];
        } else {
            $signature = $sm2->sign($message, $privateKey);
            
            return [
                'status' => 'success',
                'signature' => $signature
            ];
        }
    } catch (Exception $e) {
        return [
            'status' => 'error',
            'message' => $e->getMessage()
        ];
    }
}

function sm2Verify($data) {
    try {
        $message = $data['message'] ?? '';
        $signature = $data['signature'] ?? '';
        $publicKey = $data['public_key'] ?? '';
        
        $sm2 = new SM2();
        $isValid = $sm2->verify($message, $signature, $publicKey);
        
        return [
            'status' => 'success',
            'valid' => (bool)$isValid
        ];
    } catch (Exception $e) {
        return [
            'status' => 'error',
            'message' => $e->getMessage()
        ];
    }
}

function sm2Encrypt($data) {
    try {
        $plaintext = $data['plaintext'] ?? '';
        $publicKey = $data['public_key'] ?? '';
        
        $sm2 = new SM2();
        $ciphertext = $sm2->encrypt($plaintext, $publicKey);
        
        return [
            'status' => 'success',
            'output' => $ciphertext
        ];
    } catch (Exception $e) {
        return [
            'status' => 'error',
            'message' => $e->getMessage()
        ];
    }
}

function sm2Decrypt($data) {
    try {
        $ciphertext = $data['ciphertext'] ?? '';
        $privateKey = $data['private_key'] ?? '';
        
        $sm2 = new SM2();
        $plaintext = $sm2->decrypt($ciphertext, $privateKey);
        
        return [
            'status' => 'success',
            'output' => $plaintext
        ];
    } catch (Exception $e) {
        return [
            'status' => 'error',
            'message' => $e->getMessage()
        ];
    }
}

$handlers = [
    'sm3-hash' => 'sm3Hash',
    'sm4-encrypt' => 'sm4Encrypt',
    'sm4-decrypt' => 'sm4Decrypt',
    'sm2-sign' => 'sm2Sign',
    'sm2-verify' => 'sm2Verify',
    'sm2-encrypt' => 'sm2Encrypt',
    'sm2-decrypt' => 'sm2Decrypt',
];

function main($argc, $argv) {
    global $handlers;
    
    if ($argc < 3) {
        echo json_encode([
            'status' => 'error',
            'message' => 'Usage: wrapper.php <algorithm> <operation> --input <json>'
        ]);
        exit(1);
    }
    
    $algorithm = strtolower($argv[1]);
    $operation = strtolower($argv[2]);
    
    // Parse --input flag
    $input = null;
    for ($i = 3; $i < $argc; $i++) {
        if ($argv[$i] === '--input' && isset($argv[$i + 1])) {
            $input = $argv[$i + 1];
            break;
        }
    }
    
    if ($input === null) {
        echo json_encode([
            'status' => 'error',
            'message' => '--input parameter is required'
        ]);
        exit(1);
    }
    
    $inputData = json_decode($input, true);
    if ($inputData === null && json_last_error() !== JSON_ERROR_NONE) {
        echo json_encode([
            'status' => 'error',
            'message' => 'Invalid JSON input: ' . json_last_error_msg()
        ]);
        exit(1);
    }
    
    $key = "$algorithm-$operation";
    if (!isset($handlers[$key])) {
        echo json_encode([
            'status' => 'error',
            'message' => "Unsupported operation: $algorithm $operation"
        ]);
        exit(1);
    }
    
    $handler = $handlers[$key];
    $result = $handler($inputData);
    echo json_encode($result);
    
    exit($result['status'] === 'success' ? 0 : 1);
}

main($argc, $argv);
