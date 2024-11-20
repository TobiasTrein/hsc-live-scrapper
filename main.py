import yt_dlp
import ffmpeg
import os
import time
import argparse
from datetime import datetime
import cv2
from ultralytics import YOLO

# Loads YOLO pre-trained model
model = YOLO("./yolov8n-cls.pt")

# Download live segment
def download_live_segment(live_url, duration, output_segment):
    ydl_opts = {
        'format': '312', # Specify the format
        'outtmpl': output_segment,
        'noplaylist': True,
        'quiet': True,
        'external_downloader': 'ffmpeg',
        'external_downloader_args': ['-t', str(duration), '-loglevel', 'error']  
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([live_url])

# Identify cats on image
def detect_cat(image_path):

    results = model(image_path) 
    
    #plt = results[0].plot()
    #cv2.imshow("Bounding Boxes", plt)
    #cv2.waitKey(0)  
    #print(results[0])
    
    # Verify if detection returned
    if results[0] is None:
        print("Nenhum resultado retornado pela detecção ou atributos ausentes.")
        return False
    
    top5 = results[0].probs.top5

    print(top5)

    return any(item in range(281, 286) for item in top5)

# Function to capture 1 second of video, get an image and verify the presence of a cat
def capture_one_second_and_screenshot(live_url, segment_filename):

    download_live_segment(live_url, 1, segment_filename)
    
    if os.path.exists(segment_filename):
        current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        screenshot_dir = 'screenshots'
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_filename = os.path.join(screenshot_dir, f'sc-{current_time}.png')
        
        # Get an image from the video
        (
            ffmpeg
            .input(segment_filename, ss=0.5)
            .output(screenshot_filename, vframes=1)
            .run(overwrite_output=True, quiet=True) 
        )

        # Load thee image
        img = cv2.imread(screenshot_filename)
        height, width, _ = img.shape

        half_width = width // 2
        half_height = height // 2
        bottom_right_quadrant = img[half_height:height, half_width:width]
        quadrant_filename = os.path.join(screenshot_dir, f'quadrant-{current_time}.png')
        # Save a cropped image only for the front camera
        cv2.imwrite(quadrant_filename, bottom_right_quadrant)

        # Verifies if the front camera has a cat
        if detect_cat(quadrant_filename):
            print("Gato encontrado no quadrante inferior direito!")
            os.remove(quadrant_filename)
        else:
            print("Nenhum gato encontrado no quadrante inferior direito.")
            os.remove(screenshot_filename)
            os.remove(quadrant_filename)

        # Delete the video file
        os.remove(segment_filename)
    else:
        print('O arquivo de segmento não foi gerado.')

def main_routine(live_url):
    segment_filename = 'live_segment.mp4'

    while True:
        capture_one_second_and_screenshot(live_url, segment_filename)
        time.sleep(5)  # Repeats the routine every 5 seconds

def list_formats(live_url):
    with yt_dlp.YoutubeDL({'listformats': True}) as ydl:
        ydl.extract_info(live_url, download=False)

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process a YouTube live URL.")
    parser.add_argument("live_url", type=str, help="The URL of the YouTube live video.")
    
    # Parse the arguments
    args = parser.parse_args()
    live_url = args.live_url  # Retrieve the live URL from arguments

    # Call the function to list formats
    # list_formats(live_url)

    # Start the main routine
    main_routine(live_url)
