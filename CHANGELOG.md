# Changelog

All notable changes to LumenQA will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.9.4] - 2025-01-10

### Added
- GPU acceleration for Safari on macOS (Metal backend)
- New `wait until` command for custom conditions
- Screenshot comparison with visual diff highlighting
- LumenCloud analytics integration

### Changed
- Intent tree generation 25% faster with improved caching
- Reduced memory usage by 15% through better DOM snapshot management
- Improved PyLux syntax error messages

### Fixed
- Fixed race condition in parallel test execution
- Corrected screenshot timestamps in test reports
- Fixed issue with Shadow DOM traversal in complex SPAs

## [0.9.3] - 2024-12-18

### Added
- Support for Firefox on Linux ARM64
- New `mock api` command for API response mocking
- GraphQL query support with `gql` command
- Video recording for test sessions

### Changed
- LumenVM 2.1 with 40% faster bytecode compilation
- Intent trees now support 6 fallback strategies (was 4)
- Improved error messages with suggestions

### Fixed
- Fixed WebSocket connection handling in CI environments
- Corrected issue with nested selectors in PyLux
- Fixed memory leak in long-running test sessions

## [0.9.2] - 2024-11-28

### Added
- Automatic retry for flaky tests
- CI/CD integration guides for major platforms
- New `lumen doctor` command for system diagnostics

### Changed
- Reduced startup time by 50% with lazy loading
- Improved parallel execution efficiency
- Better error reporting with stack traces

### Fixed
- Fixed issue with HTTPS certificate validation
- Corrected screenshot capture on Retina displays
- Fixed DOM cache invalidation edge cases

## [0.9.1] - 2024-11-05

### Added
- Migration tools from Playwright, Selenium, Cypress
- Self-healing selectors with visual AI fallback
- GPU-accelerated DOM hashing

### Changed
- LumenVM 2.0 released with major performance improvements
- Intent trees now learn from historical test runs
- Reduced false positives in flakiness detection

### Fixed
- Fixed race condition in parallel element queries
- Corrected timezone handling in test reports
- Fixed issue with file uploads in headless mode

## [0.9.0] - 2024-10-12

### Added
- Initial beta release
- PyLux language support
- LumenVM runtime with GPU acceleration
- Intent trees for self-healing selectors
- Differential DOM engine
- Support for Chrome, Firefox, Safari, Edge
- Parallel test execution
- API testing capabilities

### Changed
- N/A (initial release)

### Fixed
- N/A (initial release)

---

## Upgrade Guide

### 0.9.3 → 0.9.4

No breaking changes. Update:

```bash
pip install --upgrade lumenqa
```

### 0.9.2 → 0.9.3

**Breaking:** `mock_network` command renamed to `mock api`

```pylux
# Old
mock_network "/api/users" returns {...}

# New
mock api "/api/users" returns {...}
```

---

For detailed documentation, visit [lumenqa.com/docs](https://lumenqa.com/docs)
