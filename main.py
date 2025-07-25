import pyttsx3
import fitz  # PyMuPDF
import threading
from tkinter import filedialog, Tk, Button, Label, Canvas, Scrollbar, VERTICAL, RIGHT, Y, Frame, StringVar, OptionMenu
from PIL import Image, ImageTk
import io
import time

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 140)  # Teaching mode: slower
engine.setProperty('volume', 1.0)

# Voice selection
voices = engine.getProperty('voices')
voice_options = {v.name: v.id for v in voices}

# GUI setup
root = Tk()
root.title("🧑‍🏫 PDF Teacher Narrator")
root.configure(bg="#23272e")  # Dark background

selected_voice = StringVar()
selected_voice.set(voices[0].name)

def set_voice(name):
    engine.setProperty('voice', voice_options[name])

is_paused = False
stop_reading = False
canvas = None
canvas_image = None
image_ref = None
scale = 2.0
current_pdf_path = None
current_page_number = 0
total_pages = 0

def extract_words_and_image(pdf_path, page_number=0):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number)
    words = page.get_text("words")
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
    img_data = pix.tobytes("ppm")
    img = Image.open(io.BytesIO(img_data))
    doc.close()
    return words, img

def highlight_word(box):
    x0, y0, x1, y1 = [coord * scale for coord in box]
    return canvas.create_rectangle(x0, y0, x1, y1, outline='#FF1744', width=3, tag="highlight")

def clear_highlight():
    canvas.delete("highlight")

def read_words(file_path, words):
    global is_paused, stop_reading
    sentence = ""
    sentence_boxes = []
    for word_data in words:
        if stop_reading:
            break
        while is_paused:
            time.sleep(0.1)
        x0, y0, x1, y1, word, *_ = word_data
        sentence += word + " "
        sentence_boxes.append((x0, y0, x1, y1))
        # If word ends with punctuation, treat as sentence end
        if word.endswith(('.', '!', '?')):
            clear_highlight()
            for box in sentence_boxes:
                highlight_word(box)
                root.update()
                time.sleep(0.02)
            current_sentence.set(sentence.strip())
            engine.say(sentence.strip())
            engine.runAndWait()
            sentence = ""
            sentence_boxes = []
    # Read any remaining words
    if sentence:
        clear_highlight()
        for box in sentence_boxes:
            highlight_word(box)
            root.update()
            time.sleep(0.02)
        current_sentence.set(sentence.strip())
        engine.say(sentence.strip())
        engine.runAndWait()
    current_sentence.set("")

def show_page(pdf_path, page_number):
    global canvas, image_ref, total_pages, stop_reading
    stop_reading = True
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count
    doc.close()
    words, img = extract_words_and_image(pdf_path, page_number)
    photo = ImageTk.PhotoImage(img)
    canvas.config(scrollregion=(0, 0, photo.width(), photo.height()))
    canvas.delete("all")
    canvas.create_image(0, 0, anchor='nw', image=photo)
    image_ref = photo
    stop_reading = False
    threading.Thread(target=read_words, args=(pdf_path, words), daemon=True).start()

def choose_pdf():
    global current_pdf_path, current_page_number
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not file_path:
        return
    current_pdf_path = file_path
    current_page_number = 0
    show_page(current_pdf_path, current_page_number)

def on_scroll(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def pause():
    global is_paused
    is_paused = True

def resume():
    global is_paused
    is_paused = False

def stop():
    global stop_reading
    stop_reading = True
    engine.stop()
    current_sentence.set("")

Label(
    root,
    text="🧑‍🏫 PDF Teacher Narrator",
    font=("Segoe UI", 22, "bold"),
    bg="#23272e",
    fg="#f8f8f2"
).pack(pady=(18, 6))

Label(root, text="Choose Voice:", font=("Segoe UI", 12), bg="#23272e", fg="#f8f8f2").pack()
voice_menu = OptionMenu(root, selected_voice, *voice_options.keys(), command=set_voice)
voice_menu.config(font=("Segoe UI", 12), bg="#282c34", fg="#f8f8f2", bd=0, highlightthickness=0)
voice_menu.pack(pady=4)

def style_button(btn, bg, fg, hover_bg):
    btn.configure(
        font=("Segoe UI", 13, "bold"),
        bg=bg,
        fg=fg,
        activebackground=hover_bg,
        activeforeground=fg,
        relief="flat",
        bd=0,
        padx=18,
        pady=8,
        cursor="hand2"
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))

btn_choose = Button(root, text="📂 Choose PDF & Start", command=choose_pdf)
style_button(btn_choose, "#4CAF50", "#23272e", "#388E3C")
btn_choose.pack(pady=7)

btn_pause = Button(root, text="⏸️ Pause", command=pause)
style_button(btn_pause, "#FF9800", "#23272e", "#F57C00")
btn_pause.pack(pady=7)

btn_resume = Button(root, text="▶️ Resume", command=resume)
style_button(btn_resume, "#2196F3", "#23272e", "#1976D2")
btn_resume.pack(pady=7)

btn_stop = Button(root, text="🛑 Stop", command=stop)
style_button(btn_stop, "#f44336", "#23272e", "#d32f2f")
btn_stop.pack(pady=7)

# Frame for canvas and scrollbar
canvas_frame = Frame(root, bg="#282c34")
canvas_frame.pack(padx=16, pady=(16, 8), fill="both", expand=True)

canvas = Canvas(canvas_frame, bg="#1e2127", highlightthickness=0, yscrollincrement=10)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = Scrollbar(canvas_frame, orient=VERTICAL, command=canvas.yview, bg="#282c34", troughcolor="#23272e")
scrollbar.pack(side=RIGHT, fill=Y)
canvas.config(yscrollcommand=scrollbar.set)

canvas.bind_all("<MouseWheel>", on_scroll)

current_sentence = StringVar()
Label(
    root,
    textvariable=current_sentence,
    font=("Segoe UI", 14, "italic"),
    bg="#23272e",
    fg="#50fa7b",
    wraplength=600,
    justify="center"
).pack(pady=(10, 0))

Label(
    root,
    text="© 2025 PDF Teacher Narrator | Made with Python & Tkinter",
    font=("Segoe UI", 10),
    bg="#23272e",
    fg="#888"
).pack(side="bottom", pady=(0, 10))

root.mainloop()
