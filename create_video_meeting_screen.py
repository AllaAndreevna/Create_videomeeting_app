import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import textwrap 

def create_video_meeting_screen(background_image, video1, video2, name1, name2, layout):
     # Load background image
    background = cv2.imread(background_image)
    if background is None:
        print("Ошибка: не удалось прочитать изображение фона.")
        return
    height, width, _ = background.shape
    cv2.namedWindow("Video Meeting Screen", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Video Meeting Screen", width, height)
    # Load videos
    cap1 = cv2.VideoCapture(video1)
    cap2 = cv2.VideoCapture(video2)

    # Create window for output
    cv2.namedWindow("Video Meeting Screen")
    # cv2.resizeWindow("Video Meeting Screen",  background.shape[1], background.shape[0])

    # Handle WM_CLOSE event
    def on_closing():
        cv2.destroyAllWindows()
        root.destroy()

    # Create window
    root = tk.Tk()
    root.title("Video Meeting Screen")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        scale_percent = 100
        width = int(frame1.shape[1] * scale_percent / 100)
        height = int(frame1.shape[0] * scale_percent / 100)
        dim = (width, height)
        frame1 = cv2.resize(frame1, dim, interpolation=cv2.INTER_AREA)

        width = int(frame2.shape[1] * scale_percent / 100)
        height = int(frame2.shape[0] * scale_percent / 100)
        dim = (width, height)
        frame2 = cv2.resize(frame2, dim, interpolation=cv2.INTER_AREA)

       
        frame = np.zeros((background.shape[0], background.shape[1], 3), dtype=np.uint8)
   
        layout = layout_var.get()
        if layout == "center":
            x1 = (background.shape[1] - frame1.shape[1]) // 2 - frame2.shape[1] // 2
            y1 = (background.shape[0] - frame1.shape[0]) // 2
            x2 = (background.shape[1] - frame2.shape[1]) // 2 + frame1.shape[1] // 2
            y2 = (background.shape[0] - frame2.shape[0]) // 2
        elif layout == "top_left":
            x1 = 0
            y1 = 0
            x2 = frame1.shape[1]
            y2 = 0
        elif layout == "top_right":
            x1 = background.shape[1] - frame1.shape[1] - frame2.shape[1]
            y1 = 0
            x2 = background.shape[1] - frame2.shape[1]
            y2 = 0
        elif layout == "bottom_left":
            x1 = 0
            y1 = background.shape[0] - frame1.shape[0] - 50
            x2 = frame1.shape[1]
            y2 = background.shape[0] - frame2.shape[0] - 50
        elif layout == "bottom_right":
            x1 = background.shape[1] - frame1.shape[1]
            y1 = background.shape[0] - frame1.shape[0] - 50
            x2 = background.shape[1] - frame2.shape[1]
            y2 = background.shape[0] - frame2.shape[0] - 50
        elif layout == "left_side":
            x1 = 0
            y1 = (background.shape[0] - frame1.shape[0]) // 2
            x2 = 0
            y2 = (background.shape[0] - frame2.shape[0]) // 2 + frame1.shape[0]
        elif layout == "right_side":
            x1 = background.shape[1] - frame1.shape[1]
            y1 = (background.shape[0] - frame1.shape[0]) // 2
            x2 = background.shape[1] - frame2.shape[1]
            y2 = (background.shape[0] - frame2.shape[0]) // 2 + frame1.shape[0]
        # x1 = (background.shape[1] - frame1.shape[1]) // 2 - frame2.shape[1] // 2
        # y1 = (background.shape[0] - frame1.shape[0]) // 2
        # frame[y1:y1+frame1.shape[0], x1:x1+frame1.shape[1]] = frame1

        # x2 = (background.shape[1] - frame2.shape[1]) // 2 + frame1.shape[1] // 2
        # y2 = (background.shape[0] - frame2.shape[0]) // 2
        # frame[y2:y2+frame2.shape[0], x2:x2+frame2.shape[1]] = frame2


        result = background.copy()
        result[y1:y1+frame1.shape[0], x1:x1+frame1.shape[1]] = frame1
        result[y2:y2+frame2.shape[0], x2:x2+frame2.shape[1]] = frame2

        (text_width, text_height), _ = cv2.getTextSize(name1, cv2.FONT_HERSHEY_SIMPLEX, 10.0, 2)
        margin = 10
        rect_width = text_width + 2 * margin
        rect_height = text_height + 2 * margin

        if text_width > frame1.shape[1]:
            # Split the text into multiple lines
            lines = textwrap.wrap(name1, width=10)  # adjust the width parameter as needed
            y_offset = 0
            for line in lines:
                (line_width, line_height), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 10.0, 2)
                rect_width = line_width + 2 * margin
                rect_height = line_height + 2 * margin
                cv2.rectangle(result, (x1 - margin, y1 + y_offset - rect_height + margin + 1520), (x1 + rect_width, y1 + y_offset + 1520), (255, 255, 255), -1, cv2.LINE_AA)
                cv2.putText(result, line, (x1, y1 + y_offset + 1520), cv2.FONT_HERSHEY_SIMPLEX, 10.0, (0, 0, 0), 2)
                y_offset += line_height + 2 * margin
        else:
            cv2.rectangle(result, (x1 - margin, y1 + 1520 - rect_height + margin), (x1 + rect_width, y1 + 1520), (255, 255, 255), -1, cv2.LINE_AA)
            cv2.putText(result, name1, (x1, y1 + 1520), cv2.FONT_HERSHEY_SIMPLEX, 10.0, (0, 0, 0), 6)

        (text_width, text_height), _ = cv2.getTextSize(name2, cv2.FONT_HERSHEY_SIMPLEX, 10.0, 2)
        rect_width = text_width + 2 * margin
        rect_height = text_height + 2 * margin

        if text_width > frame2.shape[1]:
            # Split the text into multiple lines
            lines = textwrap.wrap(name2, width=10)  # adjust the width parameter as needed
            y_offset = 0
            for line in lines:
                (line_width, line_height), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 10.0, 2)
                rect_width = line_width + 2 * margin
                rect_height = line_height + 2 * margin
                cv2.rectangle(result, (x2 - margin, y2 + y_offset - rect_height + margin + 1520), (x2 + rect_width, y2 + y_offset + 1520), (255, 255, 255), -1, cv2.LINE_AA)
                cv2.putText(result, line, (x2, y2 + y_offset + 1520), cv2.FONT_HERSHEY_SIMPLEX, 10.0, (0, 0, 0), 2)
                y_offset += line_height + 2 * margin
        else:

            cv2.rectangle(result, (x2 - margin, y2 + 1520 - rect_height + margin), (x2 + rect_width, y2 + 1520), (255, 255, 255), -1, cv2.LINE_AA)
            cv2.putText(result, name2, (x2, y2 + 1520), cv2.FONT_HERSHEY_SIMPLEX, 10.0, (0, 0, 0), 6)

        cv2.imshow("Video Meeting Screen", result)
      
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cv2.destroyAllWindows()
    cap1.release()
    cap2.release()
