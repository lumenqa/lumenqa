# LumenQA Documentation

Welcome to the official LumenQA documentation! LumenQA is a next-generation browser automation framework that delivers unparalleled performance through our PyLux language and LumenVM runtime.

## Getting Started

New to LumenQA? Start here:

1. **[Installation](installation.md)** - Get LumenQA up and running
2. **[Quick Start](quickstart.md)** - Your first test in 5 minutes
3. **[PyLux Syntax](pylux-syntax.md)** - Learn the PyLux language

## Core Documentation

### Language & Syntax
- **[PyLux Language Reference](pylux-syntax.md)** - Complete language guide
- **[API Reference](api-reference.md)** - All commands and methods

### Concepts
- **[Intent Trees](concepts/intent-trees.md)** - Understanding self-healing tests
- **[LumenVM Architecture](concepts/lumenvm.md)** - The runtime engine
- **[Differential DOM Engine](concepts/dom-engine.md)** - Performance secrets

### Guides
- **[Best Practices](guides/best-practices.md)** - Write maintainable tests
- **[Parallel Execution](guides/parallel-execution.md)** - Scale your test suite
- **[CI/CD Integration](guides/ci-integration.md)** - Automate everything
- **[Troubleshooting](guides/troubleshooting.md)** - Common issues & solutions

### Migration
- **[From Playwright](migration/from-playwright.md)**
- **[From Selenium](migration/from-selenium.md)**
- **[From Cypress](migration/from-cypress.md)**

## Performance

**[Benchmarks](benchmarks.md)** - See how LumenQA compares to other frameworks

## Additional Resources

- **[Examples](../examples/)** - Sample test suites
- **[GitHub Repository](https://github.com/lumenqa/lumenqa)**
- **[Discord Community](https://discord.gg/lumenqa)**
- **[Blog](https://lumenqa.dev/blog)**

## Version

This documentation is for **LumenQA v0.9.4**.

---

## Quick Example

```pylux
test "User login flow":
    navigate "https://myapp.com/login"
    input #email => "user@example.com"
    input #password => secret("PASSWORD")
    click "Login"
    expect text "Welcome back!"
```

**Result:** 9.8x faster than Playwright, self-healing selectors, GPU-accelerated.

---

## Need Help?

- 💬 Join our [Discord](https://discord.gg/lumenqa)
- 📧 Email: support@lumenqa.dev
- 🐛 Report bugs: [GitHub Issues](https://github.com/lumenqa/lumenqa/issues)
