from enum import Enum
from pathlib import Path

import typer
from rich import print  # noqa: A004
from typing_extensions import Annotated

from dicom2img import read_slices, save_as_png

app = typer.Typer()


class Extension(str, Enum):
    png = "png"
    jpg = "jpg"


@app.command()
def main(
    files: Annotated[list[Path], typer.Argument(help="Path(s) to DICOM files")],
    output_dir: Annotated[
        Path,
        typer.Option("--out", "-o", help="Folder to output files in. Defaults to datapath"),
    ] = Path("out/"),
    ext: Annotated[Extension, typer.Option(help="Extension for outputted images")] = Extension.png,
    dry_run: Annotated[bool, typer.Option("--dry-run", "-d", help="Do not save anything")] = False,
):
    """Read and convert DICOM files to slices"""

    slices = read_slices(files)

    if slices:
        print(f"[green]Found {len(slices)} valid DICOM slices[/green]")
        print(f"Slice thickness: {slices[0].SliceThickness}")
        print(f"Image dimensions: {slices[0].Rows} x {slices[0].Columns} x {len(slices)}")

        if not dry_run:
            output_dir.mkdir(exist_ok=True, parents=True)
            save_as_png(slices, output_dir, ext.value)
    else:
        print("[red]No valid DICOM slices found. Check input paths.[/red]")
