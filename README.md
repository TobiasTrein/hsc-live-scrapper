# HelloStreetCat Live Scraper

This Python program captures screenshots of the **HelloStreetCat** YouTube livestream when a cat is detected on the camera. The program uses the **YOLO** object detection model to identify cats in the live stream.

## Features
- Detects cats in the **HelloStreetCat** livestream using YOLO.
- Captures a screenshot when a cat is detected.
- Simple and easy to set up with minimal dependencies.

---

## Requirements

The program requires Python and the dependencies listed in `requirements.txt`. You can install them with:
```bash
pip install -r requirements.txt
```

---

## Usage

Run the program with the following command:
```bash
python main.py <url>
```

### Positional Arguments:
- `<url>`: The URL of the HelloStreetCat livestream on YouTube.

---

## Troubleshooting Format Errors

If you encounter a format error, follow these steps:

1. Uncomment the `list_formats(live_url)` line in the code to list all available formats for the livestream.
2. Run the program to get the format codes:
   ```bash
   python main.py <url>
   ```
3. Note the format code of a valid video stream.
4. Update the `download_live_segment` function in the code to use the correct format.

---

## Example Workflow

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the program:
   ```bash
   python main.py https://www.youtube.com/watch?v=PbtBplkR35k
   ```

3. If a valid format is required:
   - Uncomment `list_formats(live_url)`.
   - Run the program to retrieve format codes.
   - Update `download_live_segment` function with a valid format code.

---

## Notes

- Screenshots are saved only when a cat is detected.
- The YOLO model is used for real-time object detection, ensuring reliable cat detection from the livestream.

Enjoy capturing your favorite street cats! 😺