import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF for PDF text extraction
from gtts import gTTS  # Google Text-to-Speech for audio conversion
import os
import threading


class Audio_Converter(tk.Tk):
    def __init__(self):
        super().__init__()
        # Initialize the main tkinter window
        self.title("PDF to Audio Converter")
        self.geometry("720x680")
        self.configure(bg="#ccc")

        # Class variables to hold file paths
        self.pdf_file_path = ""
        self.output_file_path = ""

        # Create and pack the header label (Title)
        self.header_label = tk.Label(
            self,
            text="PDF to Audio Converter",
            font=("Arial", 28),
            bg="#ccc",
            fg="#000",
        )
        self.header_label.pack(pady=20)

        # Create and pack the information label (Instructions)
        self.info_label = tk.Label(
            self,
            text="Select a PDF file and output directory",
            bg="#ccc",
            fg="#000",
            font=("Arial", 20),
        )
        self.info_label.pack(pady=20)

        # Create and pack the button to upload PDF file
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

        # Create and pack label to display selected PDF file path
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

        # Create and pack the button to choose the output folder
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

        # Create and pack label to display selected output folder path
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

        # Create and pack the button to trigger the conversion to audio
        self.convert_button = tk.Button(
            self,
            text="Convert to Audio",
            command=self.convert_to_audio,
            state="disabled",  # Initially disabled until both PDF and output folder are selected
            bg="lightgreen",
            fg="#000",
            width=30,
            padx=10,
            pady=10,
            font=("Arial", 16),
        )
        self.convert_button.pack(pady=10)

    # Method to upload PDF file
    def upload_pdf(self):
        # Open file dialog to choose PDF
        self.pdf_file_path = filedialog.askopenfilename(
            title="Select PDF File", filetypes=[("PDF Files", "*.pdf")]
        )
        if self.pdf_file_path:
            self.check_ready()  # Check if both PDF and output folder are selected
            # Display the selected PDF path on the GUI
            self.pdf_label.config(text=f"PDF Path:\n{self.pdf_file_path}")

    # Method to choose output folder for saving audio file
    def choose_output_folder(self):
        # Open folder dialog to choose output directory
        self.output_file_path = filedialog.askdirectory(title="Select Output Folder")
        if self.output_file_path:
            self.check_ready()  # Check if both PDF and output folder are selected
            # Display the selected output folder path on the GUI
            self.output_label.config(text=f"Output Folder:\n{self.output_file_path}")

    # Method to convert PDF to audio
    def convert_to_audio(self):
        self.show_loading_screen()  # Show loading screen during conversion
        # Run the conversion in a separate thread to keep the GUI responsive
        threading.Thread(target=self._convert_and_notify).start()

    # Method to extract text from the PDF and save it as audio
    def _convert_and_notify(self):
        try:
            # Extract text from the PDF
            text = self.extract_text_from_pdf(self.pdf_file_path)
            if not text.strip():  # Check if the PDF is empty or unreadable
                raise ValueError("The PDF file is empty or could not be read.")

            # Create output file name and path
            filename = (
                os.path.splitext(os.path.basename(self.pdf_file_path))[0] + ".mp3"
            )
            output_path = os.path.join(self.output_file_path, filename)
            # Convert the extracted text to audio and save it
            self.save_audio(text, output_path)

            # Notify the user with a success message
            self.after(
                0,
                lambda: messagebox.showinfo(
                    "Success", f"Audio file saved as {output_path}"
                ),
            )
        except Exception as e:
            # Notify the user with an error message if something goes wrong
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            # Hide the loading screen once the process is complete
            self.after(0, self.hide_loading_screen)

    # Method to enable the "Convert to Audio" button when both PDF and output folder are selected
    def check_ready(self):
        if self.pdf_file_path and self.output_file_path:
            self.convert_button.config(state="normal")

    # Method to extract text from the selected PDF file
    def extract_text_from_pdf(self, pdf_path):
        # Open the PDF file using PyMuPDF (fitz)
        doc = fitz.open(pdf_path)
        # Extract text from all pages and return it as a string
        return "\n".join([page.get_text() for page in doc])

    # Method to save the extracted text as an audio file (MP3)
    def save_audio(self, text, output_path):
        # Convert the extracted text to speech using gTTS and save it as an MP3 file
        tts = gTTS(text=text, lang="en")
        tts.save(output_path)

    # Method to display a loading screen while the conversion is in progress
    def show_loading_screen(self):
        # Create a top-level window for the loading screen
        self.loading_window = tk.Toplevel(self)
        self.loading_window.title("Converting...")
        self.loading_window.geometry("300x100")
        self.loading_window.configure(bg="#eee")
        self.loading_window.transient(self)  # Keep it on top
        self.loading_window.grab_set()  # Make it modal

        # Center the loading window on the screen
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        loading_width = 300
        loading_height = 100
        x = (screen_width // 2) - (loading_width // 2)
        y = (screen_height // 2) - (loading_height // 2)
        self.loading_window.geometry(f"{loading_width}x{loading_height}+{x}+{y}")

        # Add a label to display "Converting to audio..." inside the loading window
        label = tk.Label(
            self.loading_window,
            text="Converting to audio...",
            font=("Arial", 14),
            bg="#eee",
        )
        label.pack(expand=True, pady=20)

        # Disable the close button for the loading window
        self.loading_window.protocol("WM_DELETE_WINDOW", lambda: None)

    # Method to hide the loading screen once the conversion is complete
    def hide_loading_screen(self):
        # Destroy the loading window if it exists
        if hasattr(self, "loading_window") and self.loading_window:
            self.loading_window.destroy()
