import re
import os
from pathlib import Path

OUT_PREFIX = "out/"


def fill_tag_buffer(infile, tag_buffer):
    while not re.match("^---$", line := infile.readline().rstrip()):
        if re.match(r"^(?:([\w-]+):\s+(?:'([^']+(?:',\s*'[^']+)*)'|\[([^\]]+)\]))$", line):
            # format of line after --- matches tag format
            tag_buffer += line + "\n"
        else:
            # nahh ... was a normal line ... false alarm
            # line or tag_buffer should be empty in this case
            assert tag_buffer == "" or line == ""
            return line, tag_buffer
    return None, tag_buffer


def write_md_file(infile, tag_buffer):
    line, tag_buffer = fill_tag_buffer(infile, tag_buffer)
    if line and tag_buffer:
        print("error: mis-identified tag block")
        exit(1)
    if line:
        print(f"error line: {line}")

    tags = {}
    for line in tag_buffer.splitlines():
        line = line.rstrip()
        # split line with first ':' as separator
        key, value = line.split(": ", 1)
        tags[key] = value.lstrip("'").rstrip("'")
    print(tags)

    # write normal text to file
    filepath = (OUT_PREFIX + tags["title"]).rsplit('/', 1)
    filepath[0] = filepath[0]
    filepath[-1] += '.md'

    if len(filepath) > 1:
        print(f"creating directory {Path(filepath[0])}")
        os.makedirs(Path(filepath[0]), exist_ok=True)

    print(f"opening {Path('/'.join(filepath))}")
    with open(Path('/'.join(filepath)), 'w') as outfile:
        # write tags to file
        outfile.write(f"---\ntitle: '{tags['title']}'\n")
        tags.pop("title")
        for key, value in tags.items():
            if value.startswith("[") and value.endswith("]"):
                outfile.write(f"{key}: {value}\n")
            else:
                outfile.write(f"{key}: '{value}'\n")
        outfile.write('---\n')

        # write rest of markdown to file
        while True:
            while not re.match("^---$", line := infile.readline()):
                if line:
                    outfile.write(line)
                else:
                    print('done EOF')
                    return None

            assert line == "---\n"
            line, tag_buffer = fill_tag_buffer(infile, "")
            if line and tag_buffer:
                print(f"error: line {line} \ntag_buffer {tag_buffer}")
                exit(1)
            if line:
                outfile.write(line)
            if tag_buffer:
                print('done writing a md file - continue with next')
                return tag_buffer


if __name__ == "__main__":
    # open text file as input
    with open('tiddlers.md', 'r') as infile:
        line = infile.readline()
        if not re.match("^---$", line):
            print("error: file does not start with tag block")
            exit(1)
        tag_buffer = ""

        while True:
            tag_buffer = write_md_file(infile, tag_buffer)
            if not tag_buffer:
                print('done with whole input file')
                break

# match whole tag block
# ---\n(?:([\w-]+):\s+(?:'([^']+(?:',\s*'[^']+)*)'|\[([^\]]+)\])\n)+---
