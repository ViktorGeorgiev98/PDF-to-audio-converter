import tkinter as tk


class Audio_Converter(tk.Tk):
    def __init__(self):
        super().__init__()
        # main tkinter window
        self.title("PDF to Audio Converter")
        self.geometry("720x480")
        self.configure(bg="#ccc")

        # class variables
        self.pdf_file_path = ""
        self.output_file_path = ""

        # labels/widgets and buttons
        self.header_label = tk.Label(
            self,
            text="PDF to Audio Converter",
            font=("Arial", 24),
            bg="#ccc",
            fg="#000",
        )
        self.header_label.pack(pady=20)

        self.info_label = tk.Label(
            self,
            text="Select a PDF file and output directory",
            bg="#ccc",
            fg="#000",
            font=("Arial", 18),
        )
        self.info_label.pack(pady=20)

        self.upload_button = tk.Button(self, text="Upload PDF", command=self.upload_pdf)
        self.upload_button.pack(pady=10)

        self.choose_output_folder_button = tk.Button(
            self, text="Choose Output Folder", command=self.choose_output_folder
        )
        self.choose_output_folder_button.pack(pady=10)

        self.convert_button = tk.Button(
            self, text="Convert to Audio", command=self.convert_to_audio
        )
        self.convert_button.pack(pady=10)

    # methods
    def upload_pdf(self):
        pass

    def choose_output_folder(self):
        pass

    def convert_to_audio(self):
        pass
