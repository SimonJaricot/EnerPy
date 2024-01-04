from pathlib import Path

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

colors = {
    'purple': "#5930F2",
    'green': "#16E4CA",
}
