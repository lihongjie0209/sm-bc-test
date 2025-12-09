package main

import (
	"encoding/hex"
	"encoding/json"
	"flag"
	"fmt"
	"os"

	sm "github.com/lihongjie0209/sm-go-bc"
)

type Result struct {
	Status  string `json:"status"`
	Message string `json:"message,omitempty"`
	Output  string `json:"output,omitempty"`
	Valid   *bool  `json:"valid,omitempty"`

	// For SM2 sign operation
	Signature  string `json:"signature,omitempty"`
	PrivateKey string `json:"private_key,omitempty"`
	PublicKey  string `json:"public_key,omitempty"`
}

func sm3Hash(input map[string]interface{}) Result {
	data, ok := input["data"].(string)
	if !ok {
		return Result{Status: "error", Message: "missing or invalid 'data' field"}
	}

	sm3 := sm.NewSM3()
	hash := sm3.Hash([]byte(data))

	return Result{
		Status: "success",
		Output: hex.EncodeToString(hash),
	}
}

func sm4Encrypt(input map[string]interface{}) Result {
	plaintext, ok := input["plaintext"].(string)
	if !ok {
		return Result{Status: "error", Message: "missing or invalid 'plaintext' field"}
	}

	keyHex, ok := input["key"].(string)
	if !ok {
		return Result{Status: "error", Message: "missing or invalid 'key' field"}
	}

	key, err := hex.DecodeString(keyHex)
	if err != nil {
		return Result{Status: "error", Message: fmt.Sprintf("invalid key hex: %v", err)}
	}

	mode := "ECB"
	if m, ok := input["mode"].(string); ok {
		mode = m
	}

	var iv []byte
	if ivHex, ok := input["iv"].(string); ok && ivHex != "" {
		iv, err = hex.DecodeString(ivHex)
		if err != nil {
			return Result{Status: "error", Message: fmt.Sprintf("invalid iv hex: %v", err)}
		}
	}

	sm4, err := sm.NewSM4(key, mode, iv)
	if err != nil {
		return Result{Status: "error", Message: fmt.Sprintf("failed to create SM4: %v", err)}
	}

	ciphertext, err := sm4.Encrypt([]byte(plaintext))
	if err != nil {
		return Result{Status: "error", Message: fmt.Sprintf("encryption failed: %v", err)}
	}

	return Result{
		Status: "success",
		Output: hex.EncodeToString(ciphertext),
	}
}

func sm4Decrypt(input map[string]interface{}) Result {
	ciphertextHex, ok := input["ciphertext"].(string)
	if !ok {
		return Result{Status: "error", Message: "missing or invalid 'ciphertext' field"}
	}

	ciphertext, err := hex.DecodeString(ciphertextHex)
	if err != nil {
		return Result{Status: "error", Message: fmt.Sprintf("invalid ciphertext hex: %v", err)}
	}

	keyHex, ok := input["key"].(string)
	if !ok {
		return Result{Status: "error", Message: "missing or invalid 'key' field"}
	}

	key, err := hex.DecodeString(keyHex)
	if err != nil {
		return Result{Status: "error", Message: fmt.Sprintf("invalid key hex: %v", err)}
	}

	mode := "ECB"
	if m, ok := input["mode"].(string); ok {
		mode = m
	}

	var iv []byte
	if ivHex, ok := input["iv"].(string); ok && ivHex != "" {
		iv, err = hex.DecodeString(ivHex)
		if err != nil {
			return Result{Status: "error", Message: fmt.Sprintf("invalid iv hex: %v", err)}
		}
	}

	sm4, err := sm.NewSM4(key, mode, iv)
	if err != nil {
		return Result{Status: "error", Message: fmt.Sprintf("failed to create SM4: %v", err)}
	}

	plaintext, err := sm4.Decrypt(ciphertext)
	if err != nil {
		return Result{Status: "error", Message: fmt.Sprintf("decryption failed: %v", err)}
	}

	return Result{
		Status: "success",
		Output: string(plaintext),
	}
}

func sm2Sign(input map[string]interface{}) Result {
	message, ok := input["message"].(string)
	if !ok {
		return Result{Status: "error", Message: "missing or invalid 'message' field"}
	}

	sm2 := sm.NewSM2()

	privateKey, hasPrivateKey := input["private_key"].(string)
	if !hasPrivateKey || privateKey == "" {
		// Generate new key pair
		priv, pub, err := sm2.GenerateKeypair()
		if err != nil {
			return Result{Status: "error", Message: fmt.Sprintf("failed to generate keypair: %v", err)}
		}

		signature, err := sm2.Sign([]byte(message), priv)
		if err != nil {
			return Result{Status: "error", Message: fmt.Sprintf("signing failed: %v", err)}
		}

		return Result{
			Status:     "success",
			Signature:  hex.EncodeToString(signature),
			PrivateKey: priv,
			PublicKey:  pub,
		}
	}

	signature, err := sm2.Sign([]byte(message), privateKey)
	if err != nil {
		return Result{Status: "error", Message: fmt.Sprintf("signing failed: %v", err)}
	}

	return Result{
		Status:    "success",
		Signature: hex.EncodeToString(signature),
	}
}

func sm2Verify(input map[string]interface{}) Result {
	message, ok := input["message"].(string)
	if !ok {
		return Result{Status: "error", Message: "missing or invalid 'message' field"}
	}

	signatureHex, ok := input["signature"].(string)
	if !ok {
		return Result{Status: "error", Message: "missing or invalid 'signature' field"}
	}

	signature, err := hex.DecodeString(signatureHex)
	if err != nil {
		return Result{Status: "error", Message: fmt.Sprintf("invalid signature hex: %v", err)}
	}

	publicKey, ok := input["public_key"].(string)
	if !ok {
		return Result{Status: "error", Message: "missing or invalid 'public_key' field"}
	}

	sm2 := sm.NewSM2()
	valid := sm2.Verify([]byte(message), signature, publicKey)

	return Result{
		Status: "success",
		Valid:  &valid,
	}
}

func sm2Encrypt(input map[string]interface{}) Result {
	plaintext, ok := input["plaintext"].(string)
	if !ok {
		return Result{Status: "error", Message: "missing or invalid 'plaintext' field"}
	}

	publicKey, ok := input["public_key"].(string)
	if !ok {
		return Result{Status: "error", Message: "missing or invalid 'public_key' field"}
	}

	sm2 := sm.NewSM2()
	ciphertext, err := sm2.Encrypt([]byte(plaintext), publicKey)
	if err != nil {
		return Result{Status: "error", Message: fmt.Sprintf("encryption failed: %v", err)}
	}

	return Result{
		Status: "success",
		Output: hex.EncodeToString(ciphertext),
	}
}

func sm2Decrypt(input map[string]interface{}) Result {
	ciphertextHex, ok := input["ciphertext"].(string)
	if !ok {
		return Result{Status: "error", Message: "missing or invalid 'ciphertext' field"}
	}

	ciphertext, err := hex.DecodeString(ciphertextHex)
	if err != nil {
		return Result{Status: "error", Message: fmt.Sprintf("invalid ciphertext hex: %v", err)}
	}

	privateKey, ok := input["private_key"].(string)
	if !ok {
		return Result{Status: "error", Message: "missing or invalid 'private_key' field"}
	}

	sm2 := sm.NewSM2()
	plaintext, err := sm2.Decrypt(ciphertext, privateKey)
	if err != nil {
		return Result{Status: "error", Message: fmt.Sprintf("decryption failed: %v", err)}
	}

	return Result{
		Status: "success",
		Output: string(plaintext),
	}
}

func main() {
	if len(os.Args) < 3 {
		result := Result{
			Status:  "error",
			Message: "Usage: wrapper <algorithm> <operation> --input <json>",
		}
		json.NewEncoder(os.Stdout).Encode(result)
		os.Exit(1)
	}

	algorithm := os.Args[1]
	operation := os.Args[2]

	// Parse flags
	fs := flag.NewFlagSet("wrapper", flag.ContinueOnError)
	inputJSON := fs.String("input", "", "JSON input data")
	fs.Parse(os.Args[3:])

	if *inputJSON == "" {
		result := Result{
			Status:  "error",
			Message: "--input parameter is required",
		}
		json.NewEncoder(os.Stdout).Encode(result)
		os.Exit(1)
	}

	var input map[string]interface{}
	if err := json.Unmarshal([]byte(*inputJSON), &input); err != nil {
		result := Result{
			Status:  "error",
			Message: fmt.Sprintf("Invalid JSON input: %v", err),
		}
		json.NewEncoder(os.Stdout).Encode(result)
		os.Exit(1)
	}

	handlers := map[string]func(map[string]interface{}) Result{
		"sm3-hash":      sm3Hash,
		"sm4-encrypt":   sm4Encrypt,
		"sm4-decrypt":   sm4Decrypt,
		"sm2-sign":      sm2Sign,
		"sm2-verify":    sm2Verify,
		"sm2-encrypt":   sm2Encrypt,
		"sm2-decrypt":   sm2Decrypt,
	}

	key := fmt.Sprintf("%s-%s", algorithm, operation)
	handler, ok := handlers[key]
	if !ok {
		result := Result{
			Status:  "error",
			Message: fmt.Sprintf("Unsupported operation: %s %s", algorithm, operation),
		}
		json.NewEncoder(os.Stdout).Encode(result)
		os.Exit(1)
	}

	result := handler(input)
	json.NewEncoder(os.Stdout).Encode(result)

	if result.Status != "success" {
		os.Exit(1)
	}
}
