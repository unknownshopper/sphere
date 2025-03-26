# 360° Gallery Creator

A web application that creates 360° photos from four regular images. The generated images are compatible with Facebook's 360° photo feature.

## Upload Page
[Create your 360° photo](http://localhost:5001)

## Features

- Upload 4 images (front, back, left, right)
- Automatic image adjustment and optimization
- Facebook-compatible 360° photo generation
- Real-time image preview
- Mobile-friendly interface

## Installation

1. Clone the repository
2. Install dependencies:
```pip install -r requirements.txt```
3. Install exiftool:
```brew install exiftool```
4. Run the application:
```python src/app.py```

## Usage

1. Open http://localhost:5001 in your browser
2. Upload your four images (recommended size: 1500x1500 pixels each)
3. Click "Create 360° Gallery"
4. Upload the generated image to Facebook

## Image Requirements
- Format: PNG or JPG
- Recommended size: 1500x1500 pixels per image
- Orientation: Square aspect ratio recommended
- Quality: Clear, well-lit images for best results

## License

MIT License