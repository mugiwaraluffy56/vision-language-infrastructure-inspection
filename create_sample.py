from PIL import Image, ImageDraw

def create_sample_image():
    img = Image.new('RGB', (640, 640), color='gray')
    draw = ImageDraw.Draw(img)
    # Draw a "crack"
    draw.line((100, 100, 200, 300), fill='black', width=3)
    img.save('data/sample.jpg')
    print("Created data/sample.jpg")

if __name__ == "__main__":
    create_sample_image()
