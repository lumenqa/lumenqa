# Running LumenQA in Docker

This guide shows how to run LumenQA tests in a Docker container.

## Quick Start

### Option 1: Using the run script

```bash
# Build and run in one command
docker-compose up --build

# Or use the convenience script
./run-tests.sh
```

### Option 2: Docker commands directly

```bash
# Build the image
docker build -t lumenqa:latest .

# Run tests
docker run --rm -it lumenqa:latest lumen test

# Run with options
docker run --rm -it lumenqa:latest lumen test --browser chrome
```

### Option 3: Interactive mode

```bash
# Start interactive shell
docker run --rm -it lumenqa:latest /bin/bash

# Inside container, run any lumen commands:
lumen --version
lumen doctor
lumen test
```

## Available Commands

### Run full test suite
```bash
docker run --rm -it lumenqa:latest lumen test
```

### Run with parallel execution
```bash
docker run --rm -it lumenqa:latest lumen test --parallel 4
```

### Check system status
```bash
docker run --rm -it lumenqa:latest lumen doctor
```

### Show version
```bash
docker run --rm -it lumenqa:latest lumen --version
```

## Docker Compose

The `docker-compose.yml` provides a complete setup:

```bash
# Build and start
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Mounting Test Files

To run your own test files:

```bash
docker run --rm -it \
  -v $(pwd)/tests:/app/tests \
  -v $(pwd)/results:/app/results \
  lumenqa:latest lumen test
```

## Environment Variables

```bash
docker run --rm -it \
  -e LUMEN_ENV=production \
  -e APP_URL=https://staging.example.com \
  -e GPU_ACCELERATION=true \
  lumenqa:latest lumen test
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Run LumenQA tests
  run: |
    docker build -t lumenqa:latest .
    docker run --rm lumenqa:latest lumen test
```

### Jenkins

```groovy
stage('Test') {
    steps {
        sh 'docker build -t lumenqa:latest .'
        sh 'docker run --rm lumenqa:latest lumen test'
    }
}
```

## Troubleshooting

### Container exits immediately

Make sure you're using the `-it` flags for interactive mode:
```bash
docker run --rm -it lumenqa:latest lumen test
```

### GPU acceleration not working

GPU passthrough requires additional Docker configuration. The framework will automatically fall back to CPU mode.

### Permission issues

If you have permission issues with mounted volumes:
```bash
docker run --rm -it --user $(id -u):$(id -g) \
  -v $(pwd)/tests:/app/tests \
  lumenqa:latest lumen test
```

## Performance

Docker adds minimal overhead (~2-3%) to LumenQA's execution time. For maximum performance, use native installation.

---

For more information, see the [main README](README.md).
