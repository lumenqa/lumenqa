# Contributing to LumenQA

Thank you for your interest in contributing to LumenQA! This document provides guidelines for contributing to the project.

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before submitting a bug report:
- Check existing issues to avoid duplicates
- Collect relevant information (OS, Python version, LumenQA version)
- Create a minimal reproduction case

**Submit via:** https://github.com/lumenqa/lumenqa/issues

### Suggesting Features

We love feature suggestions! Please:
- Check if it's already been suggested
- Provide clear use cases
- Explain why it would benefit the community

### Pull Requests

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests
5. Run the test suite (`lumen run tests/`)
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/lumenqa.git
cd lumenqa

# Install in development mode
pip install -e ".[dev]"

# Run tests
lumen run tests/
```

## Coding Standards

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write docstrings for public APIs
- Keep functions focused and small
- Write tests for new features

## Testing

```bash
# Run unit tests
pytest tests/

# Run integration tests
lumen run integration-tests/

# Run benchmarks
python benchmarks/run.py
```

## Documentation

- Update documentation for new features
- Use clear, concise language
- Include code examples
- Update CHANGELOG.md

## Commit Messages

Follow conventional commits:

```
feat: add visual regression testing
fix: correct intent tree caching bug
docs: update installation guide
perf: optimize DOM hashing algorithm
test: add tests for parallel execution
```

## Review Process

1. Maintainers will review your PR
2. Address feedback
3. Once approved, maintainer will merge

## Questions?

- Discord: https://discord.gg/lumenqa
- Email: contribute@lumenqa.dev

Thank you for contributing! 🚀
