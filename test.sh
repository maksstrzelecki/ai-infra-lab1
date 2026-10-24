#!/bin/bash

passed=0
failed=0

assert() {
	local actual
	actual=$(python3 inference.py "$1")
	local expected="$2"

	if [[ "$actual" != "$expected" ]]; then
		echo "❌ FAIL: $1 | Expected: $expected | Got: $actual"
		((failed++))
	else
		echo "✅ PASS: $1 | Expected: $expected | Got: $actual"
		((passed++))
	fi
}

assert "images/two.png" 2
assert "images/three.png" 3
assert "images/four.png" 4
assert "images/five.png" 5

echo ""
echo "Tests passed: $passed"
echo "Tests failed: $failed"

if (( failed > 0 )); then
	exit 1
fi