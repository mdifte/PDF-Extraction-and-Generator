import os
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import List
import tkinter as tk
from tkinter import filedialog, ttk
from data_extractor import PDFExtractor
from document_generator_updated import DocumentGenerator
from data_extractor import ExtractedData

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('pdf_processor.log', mode='a'),
                        logging.StreamHandler()
                    ])

class BatchProcessor:
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        logging.info("BatchProcessor initialized with max_workers=%d", max_workers)
        
    def process_files(self, input_files: List[str], output_dir: str, 
                     progress_callback=None):
        logging.info("Starting to process %d files", len(input_files))
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for input_file in input_files:
                logging.info("Submitting file for processing: %s", input_file)
                future = executor.submit(self._process_single_file,
                                      input_file, output_dir)
                futures.append(future)
                
            for i, future in enumerate(futures):
                try:
                    future.result()
                    logging.info("Successfully processed file: %s", input_files[i])
                    if progress_callback:
                        progress_callback((i + 1) / len(input_files) * 100)
                except Exception as e:
                    logging.error("Error processing %s: %s", input_files[i], str(e))
                    print(f"Error processing {input_files[i]}: {str(e)}")
                    
    def _process_single_file(self, input_file: str, output_dir: str):
        try:
            logging.info("Processing single file: %s", input_file)
            extractor = PDFExtractor(input_file)
            extracted_data_list = extractor.extract_data()            
            generator = DocumentGenerator(output_dir, input_file)
            generator.generate_pdf(extracted_data_list)
            logging.info("Generated output for file %s: ", input_file)
                
        except Exception as e:
            logging.error("Failed to process %s: %s", input_file, str(e))
            raise Exception(f"Failed to process {input_file}: {str(e)}")

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("PDF Processor v2.0 - Document Generator")
        self.geometry("600x700")  # Increased height from 500 to 700
        self.resizable(True, True)
        
        # Configure the main window
        self.configure(bg="#f0f0f0")
        
        # Configure modern styling
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f0f0')
        style.configure('Subtitle.TLabel', font=('Arial', 10), background='#f0f0f0', foreground='#666666')
        style.configure('Custom.TButton', font=('Arial', 10, 'bold'), padding=10)
        style.configure('Status.TLabel', font=('Arial', 9), background='#f0f0f0')
        
        # Initialize variables
        self.selected_files = []
        self.output_directory = ""
        
        logging.info("Application initialized")
        self.setup_ui()
        logging.info("UI setup complete!")
        
    def setup_ui(self):
        # Create main container with padding
        main_frame = ttk.Frame(self, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title section
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_label = ttk.Label(title_frame, text="PDF Document Processor", style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, 
                                 text="Select PDF files to process and choose output directory", 
                                 style='Subtitle.TLabel')
        subtitle_label.pack(pady=(5, 0))
        
        # Input files section
        input_frame = ttk.LabelFrame(main_frame, text="Input Files", padding="15")
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # File selection area
        file_selection_frame = ttk.Frame(input_frame)
        file_selection_frame.pack(fill=tk.X)
        
        self.select_files_btn = ttk.Button(file_selection_frame, 
                                         text="📄 Select PDF Files", 
                                         command=self.select_files,
                                         style='Custom.TButton')
        self.select_files_btn.pack(side=tk.LEFT)
        
        self.files_count_label = ttk.Label(file_selection_frame, 
                                         text="No files selected", 
                                         style='Status.TLabel')
        self.files_count_label.pack(side=tk.LEFT, padx=(15, 0))
        
        # Selected files listbox
        self.files_listbox_frame = ttk.Frame(input_frame)
        self.files_listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Scrollable listbox for selected files
        self.files_listbox = tk.Listbox(self.files_listbox_frame, 
                                      height=6, 
                                      font=('Arial', 9),
                                      bg='white',
                                      selectbackground='#0078d4',
                                      relief='solid',
                                      borderwidth=1)
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        files_scrollbar = ttk.Scrollbar(self.files_listbox_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        files_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_listbox.config(yscrollcommand=files_scrollbar.set)
        
        # Output directory section
        output_frame = ttk.LabelFrame(main_frame, text="Output Directory", padding="15")
        output_frame.pack(fill=tk.X, pady=(0, 20))
        
        output_selection_frame = ttk.Frame(output_frame)
        output_selection_frame.pack(fill=tk.X)
        
        self.select_output_btn = ttk.Button(output_selection_frame, 
                                          text="📁 Select Output Directory", 
                                          command=self.select_output_directory,
                                          style='Custom.TButton')
        self.select_output_btn.pack(side=tk.LEFT)
        
        self.output_path_label = ttk.Label(output_selection_frame, 
                                         text="No directory selected", 
                                         style='Status.TLabel')
        self.output_path_label.pack(side=tk.LEFT, padx=(15, 0))
        
        # Process section
        process_frame = ttk.Frame(main_frame)
        process_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.process_btn = ttk.Button(process_frame, 
                                    text="🚀 Process Files", 
                                    command=self.start_processing,
                                    style='Custom.TButton',
                                    state='disabled')
        self.process_btn.pack()
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="15")
        progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress.pack(pady=(0, 10))
        
        self.status_label = ttk.Label(progress_frame, text="Ready to process files", style='Status.TLabel')
        self.status_label.pack()
        
    
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select PDF Files to Process",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        
        if files:
            self.selected_files = list(files)
            logging.info("Files selected: %s", files)
            
            # Update UI
            self.files_count_label.config(text=f"{len(files)} file(s) selected")
            
            # Clear and populate listbox
            self.files_listbox.delete(0, tk.END)
            for file in files:
                filename = os.path.basename(file)
                self.files_listbox.insert(tk.END, filename)
            
            # Automatically open output directory selection after files are selected
            self.status_label.config(text="Now select the output directory...")
            self.after(100, self.select_output_directory)  # Small delay for better UX
            
            self.update_process_button_state()
    
    def select_output_directory(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        
        if directory:
            self.output_directory = directory
            logging.info("Output directory selected: %s", directory)
            
            # Update UI - show truncated path if too long
            display_path = directory
            if len(display_path) > 50:
                display_path = "..." + display_path[-47:]
            
            self.output_path_label.config(text=display_path)
            self.status_label.config(text="Ready to process files!")
            self.update_process_button_state()
        else:
            # User cancelled directory selection
            if self.selected_files:
                self.status_label.config(text="Please select an output directory to continue")
            else:
                self.status_label.config(text="Ready to process files")
    
    def update_process_button_state(self):
        """Enable process button only when both files and output directory are selected"""
        if self.selected_files and self.output_directory:
            self.process_btn.config(state='normal')
        else:
            self.process_btn.config(state='disabled')
    
    def start_processing(self):
        if not self.selected_files or not self.output_directory:
            self.status_label.config(text="Please select files and output directory first")
            return
        
        # Reset progress
        self.progress['value'] = 0
        self.status_label.config(text="Starting processing...")
        self.process_btn.config(state='disabled')
        
        # Start processing in a separate thread to keep UI responsive
        import threading
        thread = threading.Thread(target=self.process_files_thread)
        thread.daemon = True
        thread.start()
    
    def process_files_thread(self):
        """Process files in a separate thread"""
        processor = BatchProcessor()
        try:
            processor.process_files(
                self.selected_files,
                self.output_directory,
                self.update_progress
            )
            self.after(0, lambda: self.status_label.config(text="✅ Processing completed successfully!"))
            self.after(0, lambda: self.process_btn.config(state='normal'))
            logging.info("All files processed successfully")
        except Exception as e:
            self.after(0, lambda: self.status_label.config(text=f"❌ Error: {str(e)}"))
            self.after(0, lambda: self.process_btn.config(state='normal'))
            logging.error("Error during file processing: %s", str(e))

        
    def update_progress(self, value):
        """Update progress bar from any thread"""
        self.after(0, lambda: self.progress.config(value=value))
        self.after(0, lambda: self.status_label.config(text=f"Processing... {value:.1f}% complete"))
        logging.info("Progress updated to %.2f%%", value)

if __name__ == "__main__":
    logging.info("Application started")
    app = Application()
    app.mainloop()
    logging.info("Application exited")


