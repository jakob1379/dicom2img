# dicom2img

A command-line tool to convert DICOM files into a series of image slices (PNG or JPG). It reads
DICOM files, sorts them by slice location, normalizes pixel data, and saves each slice as an
individual image file.

## Usage

```bash
$ dicom2img [OPTIONS] FILES...
```

**Arguments**:

*   `FILES...`: Path(s) to DICOM files [required]

**Options**:

*   `-o, --out PATH`: Folder to output files in. [default: out/]
*   `--ext [png|jpg]`: Extension for outputted images [default: png]
*   `-d, --dry-run`: Do not save anything
*   `--help`: Show this message and exit.

## Example

Convert all DICOM files in the `scans/` directory to PNG images in `output_pngs/`:

```bash
dicom2img scans/*.dcm -o output_pngs/
```

Convert specific files to JPG format in the default `out/` directory:

```bash
dicom2img scan1.dcm scan2.dcm --ext jpg
```
