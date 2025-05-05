import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
from gtts import gTTS
import os


class Audio_Converter(tk.Tk):
    def __init__(self):
        super().__init__()
        # main tkinter window
        self.title("PDF to Audio Converter")
        self.geometry("720x680")
        self.configure(bg="#ccc")

        # class variables
        self.pdf_file_path = ""
        self.output_file_path = ""

        # labels/widgets and buttons
        self.header_label = tk.Label(
            self,
            text="PDF to Audio Converter",
            font=("Arial", 28),
            bg="#ccc",
            fg="#000",
        )
        self.header_label.pack(pady=20)

        self.info_label = tk.Label(
            self,
            text="Select a PDF file and output directory",
            bg="#ccc",
            fg="#000",
            font=("Arial", 20),
        )
        self.info_label.pack(pady=20)

        self.upload_button = tk.Button(
            self,
            text="Upload PDF",
            command=self.upload_pdf,
            bg="lightgreen",
            fg="#000",
            width=30,
            padx=10,
            pady=10,
            font=("Arial", 16),
        )
        self.upload_button.pack(pady=10)
        self.pdf_label = tk.Label(
            self,
            text="",
            font=("Arial", 10),
            wraplength=550,
            justify="left",
            bg="#ccc",
            padx=5,
            pady=5,
            fg="#000",
        )
        self.pdf_label.pack(pady=5)

        self.choose_output_folder_button = tk.Button(
            self,
            text="Choose Output Folder",
            command=self.choose_output_folder,
            bg="lightgreen",
            fg="#000",
            width=30,
            padx=10,
            pady=10,
            font=("Arial", 16),
        )
        self.choose_output_folder_button.pack(pady=10)
        self.output_label = tk.Label(
            self,
            text="",
            font=("Arial", 10),
            wraplength=550,
            justify="left",
            bg="#ccc",
            padx=5,
            pady=5,
            fg="#000",
        )
        self.output_label.pack(pady=5)

        self.convert_button = tk.Button(
            self,
            text="Convert to Audio",
            command=self.convert_to_audio,
            state="disabled",
            bg="lightgreen",
            fg="#000",
            width=30,
            padx=10,
            pady=10,
            font=("Arial", 16),
        )
        self.convert_button.pack(pady=10)

    # methods
    def upload_pdf(self):
        self.pdf_file_path = filedialog.askopenfilename(
            title="Select PDF File", filetypes=[("PDF Files", "*.pdf")]
        )
        if self.pdf_file_path:
            self.check_ready()
            self.pdf_label.config(text=f"PDF Path:\n{self.pdf_file_path}")

    def choose_output_folder(self):
        self.output_file_path = filedialog.askdirectory(title="Select Output Folder")
        if self.output_file_path:
            self.check_ready()
            self.output_label.config(text=f"Output Folder:\n{self.output_file_path}")

    def convert_to_audio(self):
        try:
            text = self.extract_text_from_pdf(self.pdf_file_path)
            if not text.strip():
                raise ValueError("The PDF file is empty or could not be read.")
            filename = (
                os.path.splitext(os.path.basename(self.pdf_file_path))[0] + ".mp3"
            )
            output_path = os.path.join(self.output_file_path, filename)
            self.save_audio(text, output_path)
            messagebox.showinfo("Success", f"Audio file saved as {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        else:
            print("Audio conversion completed successfully.")

    def check_ready(self):
        if self.pdf_file_path and self.output_file_path:
            self.convert_button.config(state="normal")

    def extract_text_from_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        return "\n".join([page.get_text() for page in doc])

    def save_audio(self, text, output_path):
        tts = gTTS(text=text, lang="en")
        tts.save(output_path)
