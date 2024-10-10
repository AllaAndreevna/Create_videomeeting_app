import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import textwrap 
# from create_video_meeting_screen import create_video_meeting_screen

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
            x1 = background.shape[1] - frame1.shape[1] - frame2.shape[1]
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

        result = background.copy()
        result[y1:y1+frame1.shape[0], x1:x1+frame1.shape[1]] = frame1
        result[y2:y2+frame2.shape[0], x2:x2+frame2.shape[1]] = frame2
        if layout == "center" or layout == "top_left" or layout == "top_right":
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
            margin = 10
            rect_width = text_width + 2 * margin
            rect_height = text_height + 2 * margin

            if text_width > frame1.shape[1]:
                # Split the text into multiple lines
                lines = textwrap.wrap(name2, width=10)  # adjust the width parameter as needed
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
                cv2.putText(result, name2, (x1, y1 + 1520), cv2.FONT_HERSHEY_SIMPLEX, 10.0, (0, 0, 0), 6)

        if layout == "bottom_left" or layout == "bottom_right":
            (text_width, text_height), _ = cv2.getTextSize(name1, cv2.FONT_HERSHEY_SIMPLEX, 10.0, 2)
            rect_width = text_width + 2 * margin
            rect_height = text_height + 2 * margin

            # Отображать текст над видео
            if text_width > frame1.shape[1]:
            # Split the text into multiple lines
                lines = textwrap.wrap(name1, width=10)  # adjust the width parameter as needed
                y_offset = 0
                for line in lines:
                    (line_width, line_height), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 10.0, 2)
                    rect_width = line_width + 2 * margin
                    rect_height = line_height + 2 * margin
                    cv2.rectangle(result, (x1 - margin, y1 + y_offset - rect_height - margin), (x1 + rect_width, y1 + y_offset - margin), (255, 255, 255), -1, cv2.LINE_AA)
                    cv2.putText(result, line, (x1, y1 + y_offset - margin), cv2.FONT_HERSHEY_SIMPLEX, 10.0, (0, 0, 0), 2)
                    y_offset -= line_height + 2 * margin

                cv2.rectangle(result, (x1 - margin, y1 - rect_height - margin), (x1 + rect_width, y1 - margin), (255, 255, 255), -1, cv2.LINE_AA)
                cv2.putText(result, name1, (x1, y1 - margin), cv2.FONT_HERSHEY_SIMPLEX, 10.0, (0, 0, 0), 6)
                

            (text_width, text_height), _ = cv2.getTextSize(name2, cv2.FONT_HERSHEY_SIMPLEX, 10.0, 2)
            rect_width = text_width + 2 * margin
            rect_height = text_height + 2 * margin

            # Отображать текст над видео
            if text_width > frame1.shape[1]:
            # Split the text into multiple lines
                lines = textwrap.wrap(name2, width=10)  # adjust the width parameter as needed
                y_offset = 0
                for line in lines:
                    (line_width, line_height), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 10.0, 2)
                    rect_width = line_width + 2 * margin
                    rect_height = line_height + 2 * margin
                    cv2.rectangle(result, (x1 - margin, y1 + y_offset - rect_height - margin), (x1 + rect_width, y1 + y_offset - margin), (255, 255, 255), -1, cv2.LINE_AA)
                    cv2.putText(result, line, (x1, y1 + y_offset - margin), cv2.FONT_HERSHEY_SIMPLEX, 10.0, (0, 0, 0), 2)
                    y_offset -= line_height + 2 * margin
            else:
                cv2.rectangle(result, (x2 - margin, y2 - rect_height - margin), (x2 + rect_width, y2 - margin), (255, 255, 255), -1, cv2.LINE_AA)
                cv2.putText(result, name2, (x2, y2 - margin), cv2.FONT_HERSHEY_SIMPLEX, 10.0, (0, 0, 0), 6)



            
        elif layout == "left_side" or layout == "right_side":
            # Отображать текст над видео
            cv2.rectangle(result, (x1 - margin, y1 - rect_height - margin), (x1 + rect_width, y1 - margin), (255, 255, 255), -1, cv2.LINE_AA)
            cv2.putText(result, name1, (x1, y1 - margin), cv2.FONT_HERSHEY_SIMPLEX, 10.0, (0, 0, 0), 6)
            cv2.rectangle(result, (x2 - margin, y2 - rect_height - margin), (x2 + rect_width, y2 - margin), (255, 255, 255), -1, cv2.LINE_AA)
            cv2.putText(result, name2, (x2, y2 - margin), cv2.FONT_HERSHEY_SIMPLEX, 10.0, (0, 0, 0), 6)
        else:
            # Отображать текст под видео
            cv2.rectangle(result, (x1 - margin, y1 + frame1.shape[0] + margin), (x1 + rect_width, y1 + frame1.shape[0] + rect_height + margin), (255, 255, 255), -1, cv2.LINE_AA)
            cv2.putText(result, name1, (x1, y1 + frame1.shape[0] + margin), cv2.FONT_HERSHEY_SIMPLEX, 10.0, (0, 0, 0), 6)
            cv2.rectangle(result, (x2 - margin, y2 + frame2.shape[0] + margin), (x2 + rect_width, y2 + frame2.shape[0] + rect_height + margin), (255, 255, 255), -1, cv2.LINE_AA)
            cv2.putText(result, name2, (x2, y2 + frame2.shape[0] + margin), cv2.FONT_HERSHEY_SIMPLEX, 10.0, (0, 0, 0), 6)

        cv2.imshow("Video Meeting Screen", result)
      
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cv2.destroyAllWindows()
    cap1.release()
    cap2.release()

def select_files():
    # Select background image
    background_image = filedialog.askopenfilename(title="Select background image", filetypes=[("Image Files", ".jpg .jpeg .png")])
    
    # Select videos
    video1 = filedialog.askopenfilename(title="Select first video", filetypes=[("Video Files", ".mp4 .avi .mov")])
    video2 = filedialog.askopenfilename(title="Select second video", filetypes=[("Video Files", ".mp4 .avi .mov")])

    # Input names
    name1 = input_name1.get()
    name2 = input_name2.get()

    # Create video meeting screen
    create_video_meeting_screen(background_image, video1, video2, name1, name2, layout_var.get())



# Create window
root = tk.Tk()
root.title("Video Meeting Screen")
root.geometry("1000x400")

# Create a frame for the title
title_frame = tk.Frame(root)
title_frame.pack(pady=20)

# Create a label for the title
title_label = tk.Label(title_frame, text="Video Meeting Screen", font=("Arial", 24))
title_label.pack()

# Create a frame for the input fields
input_frame = tk.Frame(root)
input_frame.pack(pady=20)

# Create labels and input fields for the speaker names
speaker_label = tk.Label(input_frame, text="Запишите имена спикеров:", font=("Arial", 18))
speaker_label.pack()

input_name1_label = tk.Label(input_frame, text="Спикер 1:", font=("Arial", 16))
input_name1_label.pack()
input_name1 = tk.Entry(input_frame, font=("Arial", 16))
input_name1.pack()

input_name2_label = tk.Label(input_frame, text="Спикер 2:", font=("Arial", 16))
input_name2_label.pack()
input_name2 = tk.Entry(input_frame, font=("Arial", 16))
input_name2.pack()

# Create a frame for the layout options
layout_frame = tk.Frame(root)
layout_frame.pack(pady=20)

# Create a label for the layout options
layout_label = tk.Label(layout_frame, text="Выберите расположение видео:", font=("Arial", 18))
layout_label.pack()

# Create a variable for the layout option
layout_var = tk.StringVar()
layout_var.set("center")

# Create radio buttons for the layout options
layout_center = tk.Radiobutton(layout_frame, text="Центр", variable=layout_var, value="center", font=("Arial", 16))
layout_center.pack(side=tk.LEFT)
layout_top_left = tk.Radiobutton(layout_frame, text="Верхний левый угол", variable=layout_var, value="top_left", font=("Arial", 16))
layout_top_left.pack(side=tk.LEFT)
layout_top_right = tk.Radiobutton(layout_frame, text="Верхний правый угол", variable=layout_var, value="top_right", font=("Arial", 16))
layout_top_right.pack(side=tk.LEFT)
layout_bottom_left = tk.Radiobutton(layout_frame, text="Нижний левый угол", variable=layout_var, value="bottom_left", font=("Arial", 16))
layout_bottom_left.pack(side=tk.LEFT)
layout_bottom_right = tk.Radiobutton(layout_frame, text="Нижний правый угол", variable=layout_var, value="bottom_right", font=("Arial", 16))
layout_bottom_right.pack(side=tk.LEFT)
layout_left_side = tk.Radiobutton(layout_frame, text="Левая сторона", variable=layout_var, value="left_side", font=("Arial", 16))
layout_left_side.pack(side=tk.LEFT)
layout_right_side = tk.Radiobutton(layout_frame, text="Правая сторона", variable=layout_var, value="right_side", font=("Arial", 16))
layout_right_side.pack(side=tk.LEFT)

# Create a button to select files
button_select_files = tk.Button(root, text="Select files", command=select_files, font=("Arial", 16))
button_select_files.pack(pady=20)

# Run GUI
root.mainloop()


