#!/bin/bash

# LumenQA Test Runner Script
# This script runs the test suite using LumenQA

set -e

# Colors for output
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
cat << "EOF"
   ██╗     ██╗   ██╗███╗   ███╗███████╗███╗   ██╗
   ██║     ██║   ██║████╗ ████║██╔════╝████╗  ██║
   ██║     ██║   ██║██╔████╔██║█████╗  ██╔██╗ ██║
   ██║     ██║   ██║██║╚██╔╝██║██╔══╝  ██║╚██╗██║
   ███████╗╚██████╔╝██║ ╚═╝ ██║███████╗██║ ╚████║
   ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝
EOF
echo -e "${NC}"

echo -e "${GREEN}LumenQA Test Runner${NC}"
echo ""

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo -e "${CYAN}Running in Docker container${NC}"
fi

# Run the tests
echo -e "${YELLOW}Starting test suite...${NC}"
echo ""

# Execute LumenQA test command
lumen test --browser chrome

# Capture exit code
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Test suite completed successfully!${NC}"
else
    echo -e "${YELLOW}⚠️  Some tests failed. Check output above for details.${NC}"
fi

exit $EXIT_CODE
