import os
def compile_batch() -> bool:
    """File name must be batch.cmd or batch.bat"""
    if os.path.exists("test.cmd"):
        with open("batch.cmd", "r") as bat:
            batch = bat.readlines()
    elif os.path.exists("batch.bat"):
        with open("test.bat", "r") as bat:
            batch = bat.readlines()
    else:
        return False
    with open("test.c", "w") as test:
        test.write("#include <stdlib.h>\n")
        test.write("int main() {\n")
        for i in batch:
            clean_line = i.strip().replace('"', r'\"')  # Remove \n and escape quotes
            if clean_line:  # Skip empty lines
                test.write(f'    system("{clean_line}");\n')
        test.write("    return 0;\n")
        test.write("}\n")

    os.system("gcc test.c -o compiled.exe")
    os.remove("test.c")
    return True