import os
import subprocess

def compile_batch(batch_filename: str) -> bool:
    """Compiles a batch file (batch.cmd or batch.bat) to a C executable."""
    if not os.path.exists(batch_filename):
        return False

    try:
        with open(batch_filename, "r") as bat:
            batch_lines = bat.readlines()
    except IOError:
        return False

    with open("test.c", "w") as test_file:
        test_file.write("#include <stdlib.h>\n")
        test_file.write("int main() {\n")
        for line in batch_lines:
            clean_line = line.strip().replace('"', r'\"')
            if clean_line:
                test_file.write(f'    system("{clean_line}");\n')
        test_file.write("    return 0;\n")
        test_file.write("}\n")

    try:
        subprocess.run(["gcc", "test.c", "-o", "compiled.exe"], check=True, capture_output=True, text=True)
        os.remove("test.c")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Compilation error: {e.stderr}")
        if os.path.exists("test.c"):
            os.remove("test.c")
        return False
