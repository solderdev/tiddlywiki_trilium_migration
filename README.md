# Move Tiddlywiki tiddlers via Markdown conversion to Trilium

## Prerequisites
* install `pandoc`
* Python (tested with 3.10 - should not really matter)


## Export Tiddlywiki to Markdown

Install **Markdown Export Plugin** from https://cdaven.github.io/tiddlywiki/#Markdown%20Export%20Plugin in your Tiddlywiki.

In Tiddlywiki: navigate to "Tools" -> "export all" -> "Markdown" and save the single markdown file to the same directory as the python scripts.


## Run Split Script

The exported markdown file contains all tiddlers in one file. **Make sure it's named "tiddlers.md".**

The script "mdsplit.py" splits the file into separate markdown files for each tiddler (to "out" directory).

```
python3 mdsplit.py
```

Make sure the script does not produce errors and reports "done with whole input file".


## Run Commonmark Conversion Script

This is needed, because Trilium accepts only Commonmark formatted markdown files:

The script "exec_pandoc.py" basically only runs the command `pandoc -f markdown -t commonmark -o OUTFILE INFILE for every .md file produced by the first script.

```
python3 exec_pandoc.py
```

## Import Zipped Markdown Files to Trilium

Right-click on a note, select "Import into note".

Select the "pandoc_out.zip" file and click "Import".

### Warning:
**as of Trilium Version 0.61.8-beta this does not correctly import embedded images. When uploading the single .md files one by one (instead of zipped) it works fine.**


## Future Work
Use API to batch-upload the markdown files to Trilium.
