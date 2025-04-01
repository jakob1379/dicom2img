from pathlib import Path

import numpy as np
from PIL import Image
from pydicom import dcmread
from pydicom.dataset import FileDataset
from rich import print  # noqa: A004
from rich.progress import track


def read_slices(paths: list[Path]) -> list[FileDataset]:
    """Read DICOM files from a list of paths."""
    slices = []
    for file_path in paths:
        try:
            ds = dcmread(file_path)
            if hasattr(ds, "SliceLocation"):
                slices.append(ds)
            else:
                print(f"[yellow]Skipped DICOM file without SliceLocation: {file_path}[/yellow]")
        except Exception as e:
            print(f"[red]Skipped non-DICOM file or invalid DICOM: {file_path} - {e}[/red]")

    # Sort slices by SliceLocation
    if slices:
        try:
            slices = sorted(slices, key=lambda sli: sli.SliceLocation)
        except AttributeError as e:
            print(
                f"[red]Failed to sort slices by SliceLocation. Ensure all slices have this attribute. Error: {e}[/red]"
            )
            return []  # Or raise the exception, depending on desired behavior
    else:
        print("[yellow]No valid DICOM slices found.[/yellow]")

    return slices


def normalize(image):
    """Normalize the image to a range of 0-255."""
    # TODO: consider using z-normalization https://www.datature.io/blog/a-comprehensive-guide-to-3d-models-for-medical-image-segmentation
    return (np.maximum(image, 0) / image.max()) * 255


def save_as_png(slices: list[FileDataset], output_dir: Path, ext: str = ".png"):
    """Save DICOM slices as PNG images in the output directory."""
    output_dir.mkdir(exist_ok=True)  # Ensure output directory exists
    for sli in track(slices, description="Saving slices..."):
        # Use the filename without extension for the output name
        out_name = Path(sli.filename).stem + f".{ext}"
        out_path = output_dir / out_name

        image = sli.pixel_array.astype(float)
        normalized_image = normalize(image)
        final_image = Image.fromarray(np.uint8(normalized_image))

        final_image.save(out_path)
