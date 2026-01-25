"""Minimal Sphinx build test."""
import subprocess
import sys
import os

os.chdir('docs/api')

# Run sphinx-build and capture output
result = subprocess.run(
    [sys.executable, '-m', 'sphinx', '-b', 'html', '.', '_build'],
    capture_output=True,
    text=True
)

print("STDOUT:")
print(result.stdout)
print("\nSTDERR:")
print(result.stderr)
print(f"\nReturn code: {result.returncode}")

# Save to file
with open('../../sphinx_build_output.txt', 'w') as f:
    f.write("STDOUT:\n")
    f.write(result.stdout)
    f.write("\n\nSTDERR:\n")
    f.write(result.stderr)
    f.write(f"\n\nReturn code: {result.returncode}")

print("\nOutput saved to sphinx_build_output.txt")
