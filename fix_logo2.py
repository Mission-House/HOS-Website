from PIL import Image, ImageDraw

def perfect_crop(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size
    pixels = img.load()
    
    left, right, top, bottom = w, 0, h, 0
    
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            # strict threshold for white
            if r < 245 or g < 245 or b < 245:
                if x < left: left = x
                if x > right: right = x
                if y < top: top = y
                if y > bottom: bottom = y

    print(f"Non-white bounding box: left={left}, right={right}, top={top}, bottom={bottom}")
    
    # Calculate exact center
    cx = (left + right) / 2
    cy = (top + bottom) / 2
    
    # Radius is half the max dimension
    r = max(right - left + 1, bottom - top + 1) / 2
    
    new_left = int(cx - r)
    new_top = int(cy - r)
    new_right = int(cx + r)
    new_bottom = int(cy + r)
    
    cropped = img.crop((new_left, new_top, new_right, new_bottom))
    crop_w, crop_h = cropped.size
    
    out = Image.new("RGBA", (crop_w, crop_h), (0,0,0,0))
    mask = Image.new("L", (crop_w, crop_h), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, crop_w, crop_h), fill=255)
    
    out.paste(cropped, (0, 0), mask)
    out.save(output_path, "PNG")
    print(f"Saved perfect crop to {output_path}")

perfect_crop("images/logo.jpg", "images/logo_clean.png")
