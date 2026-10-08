import pathlib
import sys

if len(sys.argv) != 2:
    exit(1)

source = pathlib.Path(sys.argv[1])

SUMMARY = ""

for path, _, filenames in source.walk():
    title = path.name
    nested = len(str(path).split("/")) - len(str(source).split("/"))
    line = "  "*nested + f"- [{title}]({path}/index.md)\n"
    SUMMARY += line
    for file in filenames:
        line = "  "*nested + f"  - [{file}]({path}/{file})\n"
        SUMMARY += line

print(SUMMARY)
