import os
import datetime
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()

CONTENT_DIR = "content"
LOGS_DIR = os.path.join(CONTENT_DIR, "logs")
VIDEOS_DIR = os.path.join(CONTENT_DIR, "videos")
PODCASTS_DIR = os.path.join(CONTENT_DIR, "podcasts")

def ensure_dirs():
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    os.makedirs(PODCASTS_DIR, exist_ok=True)

def create_entry(category, title, content_type):
    ensure_dirs()
    today = datetime.date.today().isoformat()
    safe_title = title.lower().replace(" ", "-")
    filename = f"{today}-{safe_title}.md"
    
    if category == "log":
        path = os.path.join(LOGS_DIR, filename)
        content = f"---\ndate: {today}\ntype: log\ntags: []\n---\n\n# {title}\n\n"
    elif category == "video":
        path = os.path.join(VIDEOS_DIR, filename)
        content = f"---\ndate: {today}\ntype: video\nstatus: planning\nplatform: youtube\ntags: []\n---\n\n# Video Project: {title}\n\n## Concept\n## Script Outline\n## Production Notes\n"
    elif category == "podcast":
        path = os.path.join(PODCASTS_DIR, filename)
        content = f"---\ndate: {today}\ntype: podcast\nstatus: planning\nepisode: \ntags: []\n---\n\n# Podcast Episode: {title}\n\n## Topic\n## Key Points\n## Guest (if any)\n"
    else:
        console.print(f"[bold red]Unknown category: {category}[/bold red]")
        return

    if os.path.exists(path):
        console.print(f"[bold yellow]File already exists: {path}[/bold yellow]")
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        console.print(f"[bold green]Created new {category}: {path}[/bold green]")

@app.command()
def log(title: str = typer.Argument(..., help="Title of the log entry")):
    """Create a new daily log entry."""
    create_entry("log", title, "log")

@app.command()
def video(title: str = typer.Argument(..., help="Title of the video project")):
    """Create a new video project entry."""
    create_entry("video", title, "video")

@app.command()
def podcast(title: str = typer.Argument(..., help="Title of the podcast episode")):
    """Create a new podcast episode entry."""
    create_entry("podcast", title, "podcast")

@app.command()
def list():
    """List all entries."""
    ensure_dirs()
    table = Table(title="Content Entries")
    table.add_column("Date", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Filename", style="green")

    for category, directory in [("Log", LOGS_DIR), ("Video", VIDEOS_DIR), ("Podcast", PODCASTS_DIR)]:
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                if filename.endswith(".md"):
                    date_part = filename.split("-", 3)[:3]
                    if len(date_part) == 3 and all(p.isdigit() for p in date_part):
                         date_str = "-".join(date_part)
                    else:
                         date_str = "Unknown"
                    table.add_row(date_str, category, filename)
    
    console.print(table)

if __name__ == "__main__":
    app()
