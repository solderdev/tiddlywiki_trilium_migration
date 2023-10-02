import os
from pathlib import Path

# for each file in folder "./out/" and all subfolders create subfolder and execute shell command "pandoc .. 'filename'"
for root, dirs, files in os.walk("./out/"):
    for file in files:
        if file.endswith(".md"):
            print(f'root: {root} -- file: {file}')
            os.makedirs(Path("pandoc_out/" + root), exist_ok=True)
            # escape spaces in path
            filename = os.path.join(root, file).replace(" ", r"\ ")
            os.system(f"pandoc -f markdown -t commonmark -o ./pandoc_out/{filename} " + filename)

# zip all files in folder pandoc_out:
os.system("zip -r pandoc_out.zip pandoc_out")
