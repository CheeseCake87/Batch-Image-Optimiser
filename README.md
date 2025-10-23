# Batch-Image-Optimiser

A command-line tool for batch image optimisation and conversion.

## Usage

Load the `images` folder with images you'd like to optimise. 
They will be optimised and saved in the `optimised` folder.

- `to-webp`: Convert images to webp format
  - `--dpi`: Set DPI for the output images, defaults to 72
  - `--max-vector`: Set the highest value of width or height to this
- `to-jpg`: Convert images to jpg format
  - ...
- `to-png`: Convert images to png format
  - ...

```bash
python3 -m bio to-webp --max-vector 800
```