from PIL import Image, ImageDraw
import sys

def crop_logo(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size
    
    # We want to crop out the white part. Let's find the bounding box of the non-white area.
    # Alternatively, just create a circular mask, but we need to know the offset.
    
    # Let's inspect the pixels along the horizontal center line
    pixels = img.load()
    left_edge = 0
    right_edge = w - 1
    
    # Find first non-white pixel from left (white might be 255,255,255 or close)
    for x in range(w):
        r, g, b, a = pixels[x, h//2]
        if r < 240 or g < 240 or b < 240:
            left_edge = x
            break
            
    for x in range(w-1, -1, -1):
        r, g, b, a = pixels[x, h//2]
        if r < 240 or g < 240 or b < 240:
            right_edge = x
            break

    top_edge = 0
    bottom_edge = h - 1
    for y in range(h):
        r, g, b, a = pixels[w//2, y]
        if r < 240 or g < 240 or b < 240:
            top_edge = y
            break
            
    for y in range(h-1, -1, -1):
        r, g, b, a = pixels[w//2, y]
        if r < 240 or g < 240 or b < 240:
            bottom_edge = y
            break

    print(f"Edges: {left_edge}, {right_edge}, {top_edge}, {bottom_edge}")
    
    # Calculate the center and radius of the actual logo
    center_x = (left_edge + right_edge) // 2
    center_y = (top_edge + bottom_edge) // 2
    radius = min(right_edge - center_x, bottom_edge - center_y)
    
    print(f"Center: ({center_x}, {center_y}), Radius: {radius}")
    
    # Create a new blank image with a transparent background
    size = radius * 2
    out_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    
    # Create a circular mask
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    
    # Crop the original image to the bounding box of the circle
    bbox = (center_x - radius, center_y - radius, center_x + radius, center_y + radius)
    cropped_img = img.crop(bbox)
    
    # Apply the mask
    out_img.paste(cropped_img, (0, 0), mask)
    out_img.save(output_path, "PNG")
    print(f"Saved {output_path}")

try:
    crop_logo("images/logo.jpg", "images/logo_clean.png")
except Exception as e:
    print(f"Error: {e}")

