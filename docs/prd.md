# Role
你是一个精通密码学（特别是国密 SM2/SM3/SM4 标准）和 DevOps 的高级软件工程师。

# Context
我开发了四个不同语言版本的国密算法库（Python, JavaScript, PHP, Go），现在需要创建一个新的 Git 仓库 `sm-cross-test`，用于进行跨语言的互操作性测试。
目标是：A语言生成数据（加密/签名），B语言验证数据（解密/验签），以确保所有实现的完备性和一致性。

现有的库地址如下（作为依赖参考）：
- Python: https://github.com/lihongjie0209/sm-py-bc
- JS: https://github.com/lihongjie0209/sm-js-bc
- PHP: https://github.com/lihongjie0209/sm-php-bc
- Go: https://github.com/lihongjie0209/sm-go-bc

# Goal
请帮我从零构建这个测试框架的脚手架代码。

# Requirements

## 1. 目录结构设计
请按以下结构组织代码：
- `wrappers/`: 存放各语言的适配器代码。
  - `go/`: 封装 Go 库的 CLI 工具。
  - `py/`: 封装 Python 库的 CLI 工具。
  - `js/`: 封装 JS 库的 CLI 工具。
  - `php/`: 封装 PHP 库的 CLI 工具。
- `runner/`: 测试调度逻辑（建议用 Python 或 Node.js 编写）。
- `fixtures/`: 存放测试用例数据（如果需要）。

## 2. 统一接口规范 (CLI Wrapper)
为了方便调度，每个语言的 wrapper 必须编译/封装为可执行命令，并接受统一的 JSON 参数。
请为每种语言编写一个 CLI 脚本，支持以下模式：

**命令格式:** `./wrapper [algorithm] [operation] --input '{"data": "..."}'`

**支持的操作:**
- SM3: hash
- SM4: encrypt, decrypt (支持 ECB/CBC 模式)
- SM2: sign, verify, encrypt, decrypt

**输出格式:**
必须输出纯 JSON 字符串，例如：`{"status": "success", "output": "..."}` 或 `{"status": "error", "message": "..."}`

## 3. 测试调度器 (Test Runner)
编写一个主控脚本（Test Runner），逻辑如下：
1. **生成矩阵**: 自动识别所有可用语言。
2. **SM2 签名/验签测试**: 
   - 遍历语言 A (作为 Signer)。
   - 遍历所有其他语言 B (作为 Verifier)。
   - A 生成公私钥和签名 -> B 使用 A 的公钥验签 -> 断言成功。
3. **SM4 加密/解密测试**:
   - 遍历语言 A (作为 Encryptor)。
   - 遍历所有其他语言 B (作为 Decryptor)。
   - A 加密 -> B 解密 -> 断言明文一致。
4. **SM3 哈希测试**:
   - 确保所有语言对同一输入的哈希值一致。

## 4. 依赖管理
为每个 wrapper 目录生成对应的依赖文件（go.mod, package.json, requirements.txt, composer.json），并正确引用上述 Context 中的 git 仓库地址。

## 5. 输出交付
请先生成目录结构和 Interface 定义，然后为我编写 `wrappers/py` 和 `runner` 的核心代码作为示例。