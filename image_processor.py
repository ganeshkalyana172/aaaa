"""Resize, grayscale, rotate, or convert an image using Pillow."""
from pathlib import Path
try: from PIL import Image, ImageOps, UnidentifiedImageError
except ImportError:
    print("Install dependency: python -m pip install pillow"); raise SystemExit(1)
def main():
    src = Path(input("Image path: ").strip().strip('"')).expanduser()
    if not src.is_file(): print("File not found."); return
    try:
        with Image.open(src) as im: image = ImageOps.exif_transpose(im).copy()
    except (OSError, UnidentifiedImageError) as e: print("Cannot open image:", e); return
    print(f"Size: {image.width} x {image.height}\n1 Resize\n2 Grayscale\n3 Rotate\n4 Convert format")
    choice = input("Choose operation: ").strip(); result = image
    if choice == "1":
        try:
            w, h = int(input("Width: ")), int(input("Height: "))
            if w < 1 or h < 1: raise ValueError
            result = image.resize((w, h))
        except ValueError: print("Dimensions must be positive integers."); return
    elif choice == "2": result = ImageOps.grayscale(image)
    elif choice == "3":
        try: angle = float(input("Rotation angle in degrees: "))
        except ValueError: print("Invalid angle."); return
        result = image.rotate(angle, expand=True)
    elif choice != "4": print("Invalid operation."); return
    ext = input(f"Output format [png]: ").strip().lower() or "png"
    if ext not in {"png", "jpg", "jpeg", "webp", "bmp", "tiff"}: print("Use png, jpg, jpeg, webp, bmp, or tiff."); return
    out = src.with_name(src.stem + "_processed." + ext)
    if ext in ("jpg", "jpeg") and result.mode not in ("RGB", "L"): result = result.convert("RGB")
    try: result.save(out, format="JPEG" if ext in ("jpg", "jpeg") else ext.upper()); print("Saved:", out.resolve())
    except OSError as e: print("Could not save:", e)
if __name__ == "__main__": main()
