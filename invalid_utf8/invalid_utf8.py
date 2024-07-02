import os
import re
import codecs
import shutil

path = './invalid_files/'

files = os.listdir(path)
# print(files)

# Find errors - Run this part first to see if errors or after on valid_files/. to check if errors
# _surrogates = re.compile(r"[\uDC80-\uDCFF]")
#
# def detect_decoding_errors_line(l, _s=_surrogates.finditer):
#     """Return decoding errors in a line of text
#
#     Works with text lines decoded with the surrogateescape
#     error handler.
#
#     Returns a list of (pos, byte) tuples
#
#     """
#     # DC80 - DCFF encode bad bytes 80-FF
#     return [(m.start(), bytes([ord(m.group()) - 0xDC00]))
#             for m in _s(l)]
#
# for fi in files:
#     if fi[0] != '.':
#         with open('./invalid_files/' + fi, encoding="utf8", errors="surrogateescape") as f:
#             for i, line in enumerate(f, 1):
#                 errors = detect_decoding_errors_line(line)
#                 if errors:
#                     print(fi)
#                     print(f"Found errors on line {i}:")
#                     # for (col, b) in errors:
#                     #     print(f" {col + 1:2d}: {b[0]:02x}")

# Correct Errors
for fi in files:
    if fi[0] != '.':
    # with open(path + fi, "w", encoding="utf-8") as f:
    #     f.write('�')
        try:
            f = codecs.open(path + fi, encoding='utf-8', errors='replace')
            nf = open('./valid_files/' + fi, "w")
            nf.write(f.read())
            nf.close()
            # codecs.getwriter('utf-8')(open('./valid_files/' + fi,'w')).write(f)
            # for line in f:
            #     pass
            # print("Valid utf-8")


        except UnicodeDecodeError:
            print("invalid utf-8")

# Copy only files that have been altered to corrected folder
_surrogates = re.compile(r"[\uDC80-\uDCFF]")

def detect_decoding_errors_line(l, _s=_surrogates.finditer):
    """Return decoding errors in a line of text

    Works with text lines decoded with the surrogateescape
    error handler.

    Returns a list of (pos, byte) tuples

    """
    # DC80 - DCFF encode bad bytes 80-FF
    return [(m.start(), bytes([ord(m.group()) - 0xDC00]))
            for m in _s(l)]

for fi in files:
    if fi[0] != '.':
        invalid_path = './invalid_files/' + fi
        corrected_path = './corrected/' + fi

        with open(invalid_path, encoding="utf8", errors="surrogateescape") as f:
            for i, line in enumerate(f, 1):
                errors = detect_decoding_errors_line(line)
                if errors:
                    print(fi)
                    print(f"Found errors on line {i}:")
                    if not os.path.exists(corrected_path):
                       shutil.copy(invalid_path, corrected_path)
                    for (col, b) in errors:
                        print(f" {col + 1:2d}: {b[0]:02x}")
