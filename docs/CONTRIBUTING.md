# Contributing Guide

Thank you for your interest in contributing to sm-bc-test!

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/sm-bc-test.git
   cd sm-bc-test
   ```
3. Run the setup script:
   ```bash
   ./setup.sh
   ```
4. Run tests to verify setup:
   ```bash
   cd runner
   python3 runner.py
   ```

## Development Workflow

### Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Test your changes:
   ```bash
   cd runner
   python3 runner.py
   ```

4. Commit with descriptive message:
   ```bash
   git add .
   git commit -m "Add: description of your changes"
   ```

5. Push and create pull request

### Testing Individual Wrappers

Before submitting changes to a wrapper, test it independently:

```bash
# Python
cd wrappers/py
python3 wrapper.py sm3 hash --input '{"data": "test"}'

# JavaScript
cd wrappers/js
node wrapper.js sm3 hash --input '{"data": "test"}'

# PHP
cd wrappers/php
php wrapper.php sm3 hash --input '{"data": "test"}'

# Go
cd wrappers/go
./wrapper sm3 hash --input '{"data": "test"}'
```

## Adding Support for New Operations

To add a new cryptographic operation:

1. **Update all wrappers** to implement the operation:
   - Add handler function in each wrapper
   - Register handler in the routing table
   - Follow existing code patterns

2. **Update test runner**:
   - Add test method in `runner/runner.py`
   - Follow naming convention: `test_<algorithm>_<operation>`
   - Add to `run_all_tests()` method

3. **Update documentation**:
   - Update README.md with new operation
   - Update ARCHITECTURE.md if interface changes
   - Add examples in documentation

## Adding Support for New Languages

To add support for a new programming language:

1. **Create wrapper directory**:
   ```bash
   mkdir wrappers/newlang
   ```

2. **Implement CLI wrapper** following the interface:
   ```
   wrapper <algorithm> <operation> --input '<json>'
   ```

3. **Add dependency management**:
   - Create appropriate dependency file (requirements.txt, package.json, etc.)
   - Reference the SM library for your language

4. **Test the wrapper**:
   ```bash
   cd wrappers/newlang
   ./wrapper sm3 hash --input '{"data": "test"}'
   ```

5. **Update documentation**:
   - Add language to README.md
   - Update setup.sh with installation steps
   - Document any special requirements

### Wrapper Implementation Checklist

- [ ] Implements all required operations (SM2, SM3, SM4)
- [ ] Follows unified CLI interface
- [ ] Returns valid JSON output
- [ ] Handles errors gracefully
- [ ] Uses exit code 0 for success, non-zero for errors
- [ ] Includes dependency management file
- [ ] Is executable (chmod +x)
- [ ] Has shebang line (#!/usr/bin/env ...)

## Code Style

### Python
- Follow PEP 8
- Use type hints where appropriate
- Add docstrings for functions

### JavaScript
- Use ES6+ features
- Use const/let (not var)
- Handle promises properly

### PHP
- Follow PSR-12 coding standard
- Use type declarations
- Handle exceptions properly

### Go
- Follow official Go style guide
- Use gofmt for formatting
- Handle errors explicitly

## Testing Guidelines

### Unit Testing
- Test each operation individually
- Test error handling
- Test edge cases

### Integration Testing
- Test cross-language compatibility
- Test all language pairs
- Verify data consistency

### Test Data
- Use realistic test data
- Test with various input sizes
- Test boundary conditions

## Documentation

When adding new features, update:

- [ ] README.md - User-facing documentation
- [ ] ARCHITECTURE.md - Technical details
- [ ] CONTRIBUTING.md - Development guidelines
- [ ] Inline code comments - For complex logic

## Pull Request Guidelines

### Before Submitting

- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No debugging code left in

### PR Description

Include:
- What changes were made
- Why the changes were needed
- How to test the changes
- Any breaking changes
- Related issues (if any)

### Example PR Template

```markdown
## Summary
Brief description of changes

## Changes
- Added support for SM2 key generation
- Updated test runner to validate keys
- Added documentation for new feature

## Testing
1. Run setup.sh
2. Execute runner/runner.py
3. Verify all tests pass

## Checklist
- [x] Tests pass
- [x] Documentation updated
- [x] No breaking changes
```

## Questions or Issues?

- Open an issue on GitHub
- Check existing issues first
- Provide clear reproduction steps
- Include error messages and logs

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on the code, not the person

Thank you for contributing to sm-bc-test!
