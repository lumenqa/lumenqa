# LumenVM Architecture

LumenVM is the Rust-based bytecode runtime that powers LumenQA, delivering unprecedented performance through GPU acceleration, parallel execution, and just-in-time optimization.

## Overview

**LumenVM** (Lumen Virtual Machine) is a custom runtime environment specifically designed for browser automation. Unlike traditional frameworks that run directly on V8/Node.js or Python interpreters, LumenVM compiles PyLux code to optimized bytecode.

```
PyLux Source (.lux)
  ↓
Parser → AST
  ↓
Intent Tree Generator
  ↓
Bytecode Compiler
  ↓
LumenVM Runtime (Rust)
  ↓
GPU-Accelerated Execution
```

## Architecture Components

### 1. Bytecode Compiler

Converts PyLux to platform-optimized bytecode:

```
# PyLux
click "Submit"

# Bytecode (simplified)
LOAD_INTENT "Submit"
BUILD_TREE strategies=[text, css, aria, visual]
EXECUTE_CLICK gpu_accel=true
ASSERT_SUCCESS
```

**Optimization passes:**
- Dead code elimination
- Constant folding
- Selector caching
- Parallel operation detection

### 2. Just-In-Time (JIT) Optimization

LumenVM includes a JIT compiler that optimizes hot paths:

```rust
// Pseudo-code
if execution_count > JIT_THRESHOLD {
    compile_to_native_code(bytecode);
    // 40-60% performance boost for repeated operations
}
```

Frequently-run tests get compiled to native machine code.

### 3. GPU Acceleration Layer

**Why GPU?**
- DOM querying involves massive parallel searches
- Visual AI requires matrix operations (perfect for GPU)
- Screenshot diffing benefits from parallel pixel comparison

**What runs on GPU:**
- CSS selector matching across thousands of elements
- Visual pattern recognition
- Screenshot comparison
- Image processing for visual regression

**Performance:**
- 10,000 element DOM search: 4ms (GPU) vs 45ms (CPU)
- Visual diff (1920x1080): 8ms (GPU) vs 180ms (CPU)

### 4. Parallel Execution Engine

LumenVM detects parallelizable operations automatically:

```pylux
# PyLux automatically parallelizes this:
async test "Homepage check":
    await navigate "https://example.com"

    await all:
        - expect element ".header" visible
        - expect element ".footer" visible
        - screenshot "page"
```

Compiled to:

```
NAVIGATE url="https://example.com"
FORK 3  # Create 3 parallel execution threads
  THREAD_1: CHECK_VISIBLE ".header"
  THREAD_2: CHECK_VISIBLE ".footer"
  THREAD_3: SCREENSHOT "page"
JOIN  # Wait for all threads
```

**Network-Layer Parallelization:**

Unlike other frameworks that parallelize at the test level, LumenVM parallelizes at the network layer:

```
Traditional: Test 1 ────▶ Complete ────▶ Test 2 ────▶ Complete
            |                          |
            └─ Wait for response       └─ Wait for response

LumenVM:    Test 1 ────┐
            Test 2 ────┼──▶ All network requests in parallel
            Test 3 ────┘
            (Shared connection pool, HTTP/2 multiplexing)
```

**Result:** 6-10x faster test execution.

### 5. Memory Management

Rust's ownership model + custom allocator:

```rust
pub struct TestContext {
    dom_cache: LRUCache<DOMSnapshot>,
    selector_cache: HashMap<String, Element>,
    intent_trees: Vec<IntentTree>,
}

impl Drop for TestContext {
    fn drop(&mut self) {
        // Automatic cleanup - no memory leaks!
    }
}
```

**Memory usage:** 70-80% less than Node.js/Python equivalents.

## Execution Pipeline

### Stage 1: Initialization

```
1. Load bytecode from compiled .lux files
2. Initialize GPU context (Metal/CUDA/Vulkan)
3. Create browser connection pool
4. Load cached DOM snapshots (if available)
5. Warm up JIT compiler
```

**Time:** ~600ms

### Stage 2: Test Execution

```
FOR EACH test:
  1. Parse test bytecode
  2. Build execution graph (detect parallelism)
  3. Schedule operations on worker threads
  4. Execute with GPU acceleration
  5. Collect results
  6. Update caches
```

### Stage 3: Reporting

```
1. Aggregate results from all threads
2. Generate performance metrics
3. Compare with baseline (Playwright/Selenium)
4. Upload to LumenCloud (optional)
```

## Performance Optimizations

### 1. Differential DOM Caching

```rust
struct DOMCache {
    snapshots: HashMap<PageHash, DOMSnapshot>,
}

fn check_element(selector: &str) -> Result<Element> {
    let current_hash = hash_dom();

    if let Some(snapshot) = cache.get(&current_hash) {
        // DOM unchanged - use cached result
        return snapshot.find(selector);
    }

    // DOM changed - full search
    let element = search_dom(selector);
    cache.insert(current_hash, create_snapshot());
    element
}
```

**Benefit:** Repeated checks on stable pages are near-instant.

### 2. Smart Waiting

Traditional tools poll every N milliseconds:

```javascript
// Playwright-style
while (timeout_not_reached) {
    if (element_visible) return;
    await sleep(polling_interval);  // Wastes CPU
}
```

LumenVM uses event-driven waiting:

```rust
// LumenVM approach
async fn wait_for_visible(selector: &str) -> Result<()> {
    let (tx, rx) = channel();

    // Register observer for DOM mutations
    dom.observe_mutations(move |mutation| {
        if matches_selector(&mutation, selector) {
            tx.send(());
        }
    });

    // Wait for signal OR timeout
    tokio::select! {
        _ = rx.recv() => Ok(()),
        _ = sleep(timeout) => Err(TimeoutError)
    }
}
```

**Benefit:** No CPU wasted on polling. Instant response to changes.

### 3. Batch Operations

```rust
// Instead of:
for selector in selectors {
    check_visible(selector);  // N separate DOM queries
}

// LumenVM does:
batch_check_visible(selectors);  // 1 DOM query with GPU parallelization
```

**Speedup:** 10-50x for bulk operations.

## GPU Acceleration Deep Dive

### Selector Matching on GPU

```rust
// Simplified CUDA kernel for CSS selector matching
__global__ void match_selectors(
    Element* elements,
    char* selector,
    bool* results,
    int n
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        results[idx] = matches(elements[idx], selector);
    }
}

// 10,000 elements checked in parallel in ~4ms
```

### Visual Regression on GPU

```glsl
// GLSL shader for pixel-perfect diffing
void main() {
    vec4 baseline = texture(baselineTexture, texCoord);
    vec4 current = texture(currentTexture, texCoord);

    float diff = length(baseline - current);

    if (diff > threshold) {
        fragmentColor = vec4(1.0, 0.0, 0.0, 1.0);  // Red = different
    } else {
        fragmentColor = vec4(0.0, 1.0, 0.0, 1.0);  // Green = same
    }
}

// 1920x1080 screenshot compared in 8ms
```

## Platform Support

### macOS (Metal)
- **Best performance** on Apple Silicon (M1/M2)
- Native Metal API integration
- 40-50% faster than x86 Intel Macs

### Linux (CUDA/Vulkan)
- **NVIDIA GPUs**: CUDA acceleration
- **AMD GPUs**: Vulkan compute shaders
- **CPU fallback**: Still 6-8x faster than competitors

### Windows (DirectX 12)
- DirectX Compute Shaders
- Good performance on modern GPUs
- WSL2 supported

### CPU-Only Mode
- GPU acceleration optional
- Still benefits from Rust performance
- 6-8x faster than Playwright (CPU-only)

## Configuration

```yaml
# lumen.yml
lumenvm:
  gpu_acceleration: true
  gpu_backend: auto  # auto, metal, cuda, vulkan, dx12, cpu

  # Parallelization
  worker_threads: auto  # auto = CPU cores
  network_parallelization: true

  # Caching
  dom_cache_size: 100MB
  selector_cache: true

  # JIT
  jit_compilation: true
  jit_threshold: 3  # Compile after 3 executions

  # Debug
  verbose_logging: false
  profiling: false
```

## Benchmarking

Enable profiling to see where time is spent:

```bash
lumen run tests/ --profile
```

Output:
```
LumenVM Performance Profile
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Stage                   Time      % Total
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Initialization          0.6s      3.2%
Bytecode compilation    0.3s      1.6%
Test execution          14.2s     77.2%
  ├─ DOM operations     2.1s      11.4%
  ├─ Network requests   8.4s      45.7%
  ├─ Assertions         1.2s      6.5%
  └─ Screenshots        2.5s      13.6%
Result aggregation      0.2s      1.1%
Reporting               3.1s      16.9%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total                   18.4s     100%

GPU Utilization: 43%
Cache Hit Rate: 87%
JIT Compiled Tests: 23/100
```

## Future Roadmap

**LumenVM 3.0** (Q2 2025):
- WebAssembly compilation target
- Distributed execution across multiple machines
- ARM-specific optimizations
- AI-powered auto-tuning

---

## Next Steps

- **[Intent Trees](intent-trees.md)** - How LumenVM uses intent trees
- **[Differential DOM Engine](dom-engine.md)** - DOM optimization strategies
- **[Benchmarks](../benchmarks.md)** - Performance comparisons

---

LumenVM is the secret sauce behind LumenQA's performance. Rust + GPU + clever caching = 6-14x faster tests.
