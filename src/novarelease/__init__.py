import subprocess

import typer

app = typer.Typer(no_args_is_help=True)


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True, check=False)
    if result.returncode:
        raise typer.BadParameter(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


@app.command()
def version() -> None:
    tags = git("tag", "--sort=-version:refname").splitlines()
    typer.echo(tags[0] if tags else "No version tags")


@app.command()
def changelog() -> None:
    tag = git("describe", "--tags", "--abbrev=0")
    print(git("log", f"{tag}..HEAD", "--pretty=format:- %s"))
