import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from io import BytesIO
import base64

class ImageFetcher:
    def __init__(self, root):
        self.root = root
        self.root.title('Image Fetcher')
        self.root.geometry('500x400')
        self.root.configure(bg='#FFFFFF')

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#FFFFFF')
        self.style.configure('TButton', font=('Arial', 14), foreground='black')
        self.style.configure('TLabel', background='#FFFFFF', font=('Arial', 14))
        self.style.configure('Header.TLabel', font=('Arial', 18, 'bold'))

        self.header_frame = ttk.Frame(root)
        self.header_frame.pack(fill='x')

        self.header_label = ttk.Label(self.header_frame, text='QLDT Image Fetcher', style='Header.TLabel')
        self.header_label.pack(pady=10)

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(pady=10)

        self.id_label = ttk.Label(self.main_frame, text='Student ID:')
        self.id_label.grid(row=0, column=0, sticky='w')

        self.id_entry = ttk.Entry(self.main_frame)
        self.id_entry.grid(row=0, column=1, sticky='w')

        self.fetch_button = ttk.Button(self.main_frame, text='Fetch Image', command=self.fetch_image)
        self.fetch_button.grid(row=0, column=2, padx=10)

        self.image_label = ttk.Label(root)
        self.image_label.pack(pady=10)

    def fetch_image(self):
        student_id = self.id_entry.get()
        if not student_id:
            messagebox.showwarning('Warning', 'Please enter a student ID.')
            return

        headers = {
            'Content-Length': '0',
            'Accept': 'application/json, text/plain, */*',
            'idpc': '',  # fill in if necessary
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.88 Safari/537.36',
            'Content-Type': 'text/plain',
            'Origin': 'http://qldt.hanu.vn',
            'Referer': 'http://qldt.hanu.vn/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cookie': 'ASP.NET_SessionId=gmh3t5xnr5snnggebvktlgoi',
            'Connection': 'close'
        }

        response = requests.post('http://qldt.hanu.vn/api/sms/w-locthongtinimagesinhvien', headers=headers, params={'MaSV': student_id})

        if response.status_code == 200:
            data = response.json()
            if data.get('result') == True:
                img_base64 = data.get('data', {}).get('thong_tin_sinh_vien', {}).get('image', '')
                if img_base64:
                    image_data = base64.b64decode(img_base64)
                    image = Image.open(BytesIO(image_data))
                    photo = ImageTk.PhotoImage(image)
                    self.image_label.config(image=photo)
                    self.image_label.image = photo
                else:
                    messagebox.showinfo('Info', 'Image not found for the provided ID.')
            else:
                messagebox.showerror('Error', 'An error occurred while fetching the image or no image found for the provided ID.')
        else:
            messagebox.showerror('Error', f'Request failed with status code {response.status_code}.')

root = tk.Tk()
app = ImageFetcher(root)
root.mainloop()
