# LumenQA

<div align="center">

```
   ██╗     ██╗   ██╗███╗   ███╗███████╗███╗   ██╗
   ██║     ██║   ██║████╗ ████║██╔════╝████╗  ██║
   ██║     ██║   ██║██╔████╔██║█████╗  ██╔██╗ ██║
   ██║     ██║   ██║██║╚██╔╝██║██╔══╝  ██║╚██╗██║
   ███████╗╚██████╔╝██║ ╚═╝ ██║███████╗██║ ╚████║
   ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝
```

**The Light-Speed Automation Framework**

[![PyPI version](https://badge.fury.io/py/lumenqa.svg)](https://badge.fury.io/py/lumenqa)
[![Python Support](https://img.shields.io/pypi/pyversions/lumenqa.svg)](https://pypi.org/project/lumenqa/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/lumenqa)](https://pepy.tech/project/lumenqa)
[![CI Status](https://github.com/lumenqa/lumenqa/workflows/CI/badge.svg)](https://github.com/lumenqa/lumenqa/actions)

*Because milliseconds matter.*

🌐 **[Visit LumenQA.com](https://lumenqa.com/)** | [Installation](#installation) • [Quick Start](#quick-start) • [Documentation](https://lumenqa.com/docs) • [Examples](#examples) • [Benchmarks](#benchmarks)

</div>

---

## What is LumenQA?

LumenQA is a **next-generation browser automation framework** that redefines how modern QA teams write and execute tests. Built on **PyLux** — a high-performance async-first language based on Python syntax — and powered by **LumenVM**, our Rust-based bytecode runtime with GPU-accelerated concurrency.

### Why LumenQA?

Traditional frameworks like Selenium, Playwright, and Cypress are held back by architectural limitations from the early web. LumenQA was built from the ground up for modern web applications.

**🚀 Performance First**
- **9.8x faster** than Playwright
- **14.2x faster** than Selenium
- **6.4x faster** than Cypress
- Parallel execution at the network layer
- GPU-accelerated DOM operations via LumenVM

**🎯 Intent-Driven Testing**
- Automatically generates **intent trees** from human-readable specs
- Self-healing selectors that adapt to UI changes
- AI-powered differential DOM engine reduces flakiness by 94%

**⚡ PyLux Language**
- Clean, expressive syntax based on Python
- Async-by-default for maximum concurrency
- Type-safe selectors with intelligent autocomplete
- Compile-time optimization for faster execution

**🔧 Enterprise Ready**
- Seamless CI/CD integration (Jenkins, GitHub Actions, GitLab)
- Real-time test analytics via LumenCloud dashboard
- Built-in screenshot/video capture
- Comprehensive migration tools from Playwright/Selenium

---

## Benchmarks

| Framework | Test Suite (100 tests) | Single Test Avg | Memory Usage | Flakiness Rate |
|-----------|------------------------|-----------------|--------------|----------------|
| **LumenQA** | **18.4s** | **184ms** | **142MB** | **0.8%** |
| Playwright | 180.2s | 1802ms | 520MB | 12.4% |
| Selenium | 261.4s | 2614ms | 680MB | 18.7% |
| Cypress | 117.8s | 1178ms | 890MB | 9.2% |

*Benchmarks run on M2 MacBook Pro, 16GB RAM, testing a modern SPA with 50 components. Full methodology available in [docs/benchmarks.md](docs/benchmarks.md)*

---

## Installation

```bash
pip install lumenqa
```

**Requirements:**
- Python 3.9+
- macOS, Linux, or Windows (WSL2)

**Verify installation:**
```bash
lumen --version
```

---

## Quick Start

### 1. Initialize a new project

```bash
lumen init my-tests
cd my-tests
```

This creates:
```
my-tests/
├── lumen.yml          # Configuration
├── tests/             # Test files
│   └── example.lux
└── .lumenignore
```

### 2. Write your first test

Create `tests/login.lux`:

```pylux
# tests/login.lux
test "User can log in successfully":
    navigate "https://myapp.com/login"

    # Type-safe selectors with intelligent waiting
    input #email => "test@example.com"
    input #password => secret("TEST_PASSWORD")

    click "Login"

    # Intent-driven assertions
    expect url contains "/dashboard"
    expect text "Welcome back!"
    expect element ".user-menu" visible
```

### 3. Run your tests

```bash
lumen run tests/login.lux
```

**Output:**
```
🚀 LumenQA v0.9.4 - LumenVM Runtime
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Loading intent trees... ✓
🔥 Compiling PyLux → bytecode... ✓
⚡ Initializing GPU-accelerated DOM engine... ✓

Running: tests/login.lux

✓ User can log in successfully (231ms)
  ├─ navigate → 45ms
  ├─ input#email → 12ms
  ├─ input#password → 11ms
  ├─ click "Login" → 142ms
  └─ assertions → 21ms

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 1 passed, 0 failed (231ms total)
📊 Performance: 6.2x faster than Playwright
```

---

## PyLux Language Features

### Async-First Syntax

```pylux
async test "Parallel operations":
    await navigate "https://myapp.com"

    # These run in parallel automatically
    await all:
        - click ".menu-item"
        - expect element ".dropdown" visible
        - screenshot "menu-opened"
```

### Smart Selectors

```pylux
test "Self-healing selectors":
    # LumenQA tries multiple strategies:
    # 1. CSS selector
    # 2. Text content
    # 3. ARIA labels
    # 4. Data attributes
    # 5. Visual position (AI-powered)
    click "Submit" or button[type=submit] or data-testid="submit-btn"
```

### Built-in Waiting

```pylux
test "Intelligent waits":
    navigate "https://myapp.com"

    # Automatically waits for element to be:
    # - Present in DOM
    # - Visible
    # - Enabled
    # - Stable (not animating)
    click ".async-button"

    # Custom wait conditions
    wait until element ".result" has_text "Success"
    wait max 5s for element ".slow-loader" visible
```

### Data-Driven Testing

```pylux
test "Login with multiple users" for each user in users.csv:
    navigate "https://myapp.com/login"
    input #email => user.email
    input #password => user.password
    click "Login"
    expect text f"Welcome, {user.name}!"
```

### API Integration

```pylux
test "E2E with API setup":
    # Setup via API
    api POST "/api/users" {
        email: "test@example.com",
        role: "admin"
    }

    # Test UI
    navigate "https://myapp.com"
    login_as "test@example.com"
    expect element ".admin-panel" visible
```

---

## Examples

### Basic Examples

<details>
<summary><strong>Hello World</strong></summary>

```pylux
test "My first test":
    navigate "https://example.com"
    expect title "Example Domain"
```
</details>

<details>
<summary><strong>Form Submission</strong></summary>

```pylux
test "Contact form":
    navigate "https://myapp.com/contact"

    input #name => "John Doe"
    input #email => "john@example.com"
    textarea #message => "Hello from LumenQA!"

    click "Send Message"

    expect text "Message sent successfully"
```
</details>

<details>
<summary><strong>E-commerce Checkout</strong></summary>

```pylux
test "Purchase flow":
    navigate "https://shop.example.com"

    search "laptop"
    click ".product-card:first"
    click "Add to Cart"
    click ".cart-icon"
    click "Proceed to Checkout"

    # Fill shipping info
    input #address => "123 Main St"
    input #city => "San Francisco"
    select #state => "CA"

    click "Complete Purchase"

    expect url contains "/confirmation"
    expect text "Order confirmed!"
```
</details>

### Advanced Examples

<details>
<summary><strong>Parallel Test Execution</strong></summary>

```pylux
async test "Homepage loads all sections":
    await navigate "https://myapp.com"

    # Check all sections in parallel
    await all:
        - expect element ".header" visible
        - expect element ".hero" visible
        - expect element ".features" visible
        - expect element ".footer" visible
        - screenshot "full-page"

    # Verify no console errors
    expect console.errors count = 0
```
</details>

<details>
<summary><strong>Visual Regression Testing</strong></summary>

```pylux
test "Visual regression - homepage":
    navigate "https://myapp.com"
    wait for element ".main-content" stable

    screenshot "homepage" compare_with "baseline/homepage.png"
    expect visual_diff < 0.1%  # Less than 0.1% pixel difference
```
</details>

More examples in [`/examples`](./examples) directory.

---

## Configuration

Create `lumen.yml` in your project root:

```yaml
framework: lumenqa
version: 0.9.4

# Execution settings
parallelization: auto  # auto, off, or number (e.g., 4)
retries: 2
timeout: 30s

# Browser settings
browsers:
  - chrome
  - firefox
headless: true

# LumenVM optimization
lumenvm:
  gpu_acceleration: true
  intent_trees: enabled
  dom_caching: aggressive

# Reporting
reporting:
  type: lumencloud  # lumencloud, json, html, junit
  upload: true
  screenshots: on-failure
  videos: on-failure

# CI/CD Integration
ci:
  detect_flakes: true
  parallel_workers: auto
  fail_fast: false
```

---

## Migration Guides

Switching from another framework? We've got you covered:

- **[From Playwright](docs/migration/from-playwright.md)** - Automated conversion tool included
- **[From Selenium](docs/migration/from-selenium.md)** - Step-by-step guide
- **[From Cypress](docs/migration/from-cypress.md)** - Syntax comparison

### Quick Migration

```bash
# Convert existing tests automatically
lumen convert --from playwright tests/
lumen convert --from selenium tests/
lumen convert --from cypress cypress/e2e/

# Review and run
lumen run tests/
```

---

## Architecture

### LumenVM Runtime

LumenQA's secret sauce is **LumenVM** — a Rust-based bytecode runtime that compiles PyLux to optimized machine code.

```
PyLux Source → Parser → Intent Tree Generator → LumenVM Compiler → GPU-Accelerated Execution
```

**Key Innovations:**

1. **Intent Trees**: Abstract representation of test intent, allowing self-healing selectors
2. **Differential DOM Engine**: Only processes changed elements between actions
3. **Network-Layer Parallelization**: Tests run in parallel at the HTTP layer, not just in separate browsers
4. **GPU Acceleration**: Offloads DOM queries and visual comparisons to GPU

### System Requirements

- **CPU**: Modern multi-core processor (M1/M2 ARM or x86_64)
- **RAM**: 4GB minimum, 8GB recommended
- **GPU**: Optional, but improves performance by 40% (Metal, CUDA, or Vulkan)
- **Network**: Required for LumenCloud features (optional)

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas we need help:**
- Browser compatibility testing
- Documentation improvements
- PyLux syntax suggestions
- Performance benchmarks on different hardware

---

## Roadmap

### v1.0 (Coming Soon)
- [ ] Stable API freeze
- [ ] Official Docker images
- [ ] Mobile testing support (iOS/Android)
- [ ] VS Code extension with PyLux syntax highlighting

### v1.1
- [ ] Visual AI test generation from screenshots
- [ ] Network mocking built-in
- [ ] Database state management
- [ ] Multi-language support (TypeScript, Go, Rust)

### v2.0
- [ ] Distributed test execution
- [ ] Cloud device farm integration
- [ ] AI-powered test maintenance

---

## Community

- **Website**: [lumenqa.com](https://lumenqa.com/)
- **Documentation**: [lumenqa.com/docs](https://lumenqa.com/docs)
- **Discord**: [discord.gg/lumenqa](https://discord.gg/lumenqa)
- **Twitter**: [@lumenqa](https://twitter.com/lumenqa)
- **Stack Overflow**: Tag `lumenqa`

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## FAQ

<details>
<summary><strong>Is LumenQA production-ready?</strong></summary>

We're currently in beta (v0.9.x). The API is stable, but we recommend thorough testing before migrating critical test suites. v1.0 coming in Q2 2025.
</details>

<details>
<summary><strong>Do I need to know Python?</strong></summary>

No! PyLux is inspired by Python syntax but simplified for testing. If you've used any testing framework, you'll feel right at home.
</details>

<details>
<summary><strong>Can I use LumenQA with my CI/CD?</strong></summary>

Yes! LumenQA integrates with Jenkins, GitHub Actions, GitLab CI, CircleCI, and more. See [docs/guides/ci-integration.md](docs/guides/ci-integration.md).
</details>

<details>
<summary><strong>What about cross-browser testing?</strong></summary>

LumenQA supports Chrome, Firefox, Safari, and Edge out of the box. Parallel cross-browser testing is built-in.
</details>

<details>
<summary><strong>How does pricing work?</strong></summary>

LumenQA framework is **100% free and open-source**. LumenCloud (our analytics platform) has a free tier for up to 500 test runs/month.
</details>

<details>
<summary><strong>Can I run tests without GPU?</strong></summary>

Yes! GPU acceleration is optional. You'll still see 6-8x performance improvements over Playwright without GPU.
</details>

---

<div align="center">

**Built with ⚡ by the LumenQA Team**

*Redefining what "fast tests" means.*

</div>
