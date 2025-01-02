# Installation Guide

This guide will help you install LumenQA and set up your testing environment.

## System Requirements

### Minimum Requirements
- **Python**: 3.9 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 500MB for LumenQA + dependencies
- **OS**: macOS, Linux, or Windows (with WSL2)

### Recommended for Optimal Performance
- **CPU**: Modern multi-core processor (Apple M1/M2 or AMD Ryzen 5/Intel i5+)
- **RAM**: 16GB for large test suites
- **GPU**: Optional, but provides 40% performance boost
  - macOS: Metal support (M1/M2/Intel)
  - Linux: NVIDIA GPU with CUDA 11.0+
  - Windows: DirectX 12 compatible GPU

## Installation

### Via pip (Recommended)

```bash
pip install lumenqa
```

### From Source

```bash
git clone https://github.com/lumenqa/lumenqa.git
cd lumenqa
pip install -e .
```

### Using Poetry

```bash
poetry add lumenqa
```

## Verify Installation

```bash
lumen --version
```

You should see:

```
   ██╗     ██╗   ██╗███╗   ███╗███████╗███╗   ██╗
   ...
LumenQA Framework v0.9.4
├─ LumenVM Runtime v2.1.3
├─ PyLux Language v1.0.0-beta.9
└─ Python 3.11.5
```

## Browser Setup

LumenQA automatically downloads and manages browser binaries. On first run:

```bash
lumen doctor
```

This will:
- Verify Python version
- Check LumenVM installation
- Download browser drivers (Chrome, Firefox, Safari)
- Test GPU acceleration
- Validate network connectivity

**Sample Output:**

```
🏥 LumenQA System Check

Component              Status  Version/Info
─────────────────────────────────────────────
Python version         ✓       3.11.5
LumenVM Runtime        ✓       2.1.3
GPU Acceleration       ✓       Metal (Apple M2)
Chrome browser         ✓       119.0.6045.105
Network connectivity   ✓       Connected
LumenCloud API         ✓       Authenticated

✓ All systems operational!
```

## GPU Acceleration Setup

### macOS
GPU acceleration works out of the box with Metal support.

### Linux (NVIDIA)

```bash
# Install CUDA toolkit
sudo apt install nvidia-cuda-toolkit

# Verify
nvidia-smi
```

### Linux (AMD)

```bash
# Install ROCm
sudo apt install rocm-dkms
```

### Windows

Ensure DirectX 12 is installed (comes with Windows 10+).

## IDE Integration

### VS Code Extension

```bash
code --install-extension lumenqa.pylux-syntax
```

Features:
- PyLux syntax highlighting
- Autocomplete for LumenQA commands
- Inline test execution
- Intent tree visualization

### JetBrains IDEs

Install the "PyLux Support" plugin from the marketplace.

## Environment Setup

### Create Configuration File

```bash
lumen init my-project
cd my-project
```

This creates:

```
my-project/
├── lumen.yml          # Main configuration
├── tests/             # Test files
│   └── example.lux
└── .lumenignore       # Files to ignore
```

### Configure lumen.yml

```yaml
framework: lumenqa
version: 0.9.4

parallelization: auto
browsers:
  - chrome
headless: true

lumenvm:
  gpu_acceleration: true
```

## LumenCloud (Optional)

For advanced analytics and parallel cloud execution:

```bash
lumen cloud login
```

Follow the prompts to authenticate.

## Troubleshooting

### Permission Denied Errors

```bash
# macOS/Linux
sudo chown -R $USER:$USER ~/.lumen

# Windows
# Run terminal as Administrator
```

### GPU Not Detected

```bash
lumen doctor --verbose
```

Check the GPU section for specific error messages.

### Import Errors

```bash
# Reinstall with all dependencies
pip install --force-reinstall lumenqa[all]
```

### Firewall Issues

LumenQA needs network access for:
- Browser driver downloads
- LumenCloud sync (optional)

Whitelist: `*.lumenqa.dev` in your firewall.

## Next Steps

- **[Quick Start Guide](quickstart.md)** - Write your first test
- **[PyLux Syntax](pylux-syntax.md)** - Learn the language
- **[Configuration Guide](guides/configuration.md)** - Advanced setup

## Updating LumenQA

```bash
pip install --upgrade lumenqa
```

Check the [CHANGELOG](../CHANGELOG.md) for breaking changes.

---

**Need help?** Join our [Discord](https://discord.gg/lumenqa) or email support@lumenqa.dev
