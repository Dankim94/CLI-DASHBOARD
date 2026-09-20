from rich import print
from rich.console import Console
console = Console()
print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
console.print("Hello World!", style="bold magenta", emoji=True)

