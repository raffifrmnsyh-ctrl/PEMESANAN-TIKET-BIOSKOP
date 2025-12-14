import tkinter as tk
from tkinter import messagebox
from typing import List
import ttkbootstrap as tb
from ttkbootstrap.constants import *

# ==============================
# MODEL OOP
# ==============================
# KELAS FILM (ENCAPSULATION)
class Film:
    HARGA_DASAR = 35000

    def __init__(self, judul, durasi):
        self.__judul = judul
        self.__durasi = durasi
        self._jenis = "2D Regular"

    def get_judul(self):
        return self.__judul

    def hitung_harga(self):
        return self.HARGA_DASAR

    def get_info(self):
        return f"{self.__judul} ({self._jenis})"

# KELAS FILM 3D (INHERITANCE + POLYMORPHISM)
class Film3D(Film):
    def __init__(self, judul, durasi):
        super().__init__(judul, durasi)
        self._jenis = "3D Premium"

    def hitung_harga(self):
        return super().hitung_harga() + 15000


# ==============================
# APLIKASI UTAMA
# ==============================

class BioskopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Absolute Cinematic")
        self.root.geometry("800x600")

        self.container = tb.Frame(root)
        self.container.pack(fill="both", expand=True)

        self.show_intro()

    # ---------- INTRO ----------
    def show_intro(self):
        self.clear()

        intro = tb.Frame(self.container, bootstyle="dark")
        intro.pack(fill="both", expand=True)

        tb.Label(
            intro,
            text="🎬 ABSOLUTE CINEMATIC",
            font=("Helvetica", 24, "bold"),
            bootstyle="inverse-dark"
        ).pack(pady=100)

        tb.Label(
            intro,
            text="Experience The Movie Like Never Before",
            font=("Helvetica", 12),
            bootstyle="secondary"
        ).pack()

        self.root.after(2500, self.show_main)

    # ---------- MAIN APP ----------
    def show_main(self):
        self.clear()

        self.film_list: List[Film] = [
            Film("Avatar Fire And Rush", 100),
            Film3D("Guna Guna Istri Muda", 140),
            Film("Penjara Kematian", 120)
        ]

        self.kursi_status = [False] * 25
        self.kursi_pilih = []
        self.film_aktif = self.film_list[0]

        header = tb.Frame(self.container, bootstyle="primary")
        header.pack(fill="x")

        tb.Label(
            header,
            text="🎟️ PEMESANAN TIKET BIOSKOP",
            font=("Helvetica", 18, "bold"),
            bootstyle="inverse-primary"
        ).pack(pady=10)

        film_frame = tb.Labelframe(
            self.container,
            text="Pilih Film",
            padding=15,
            bootstyle="info"
        )
        film_frame.pack(fill="x", padx=20, pady=10)

        self.film_var = tk.StringVar(value=self.film_aktif.get_judul())
        opsi = [f.get_judul() for f in self.film_list]

        tb.OptionMenu(
            film_frame,
            self.film_var,
            opsi[0],
            *opsi,
            command=self.ganti_film
        ).pack(anchor="w")

        self.label_info = tb.Label(
            film_frame,
            font=("Helvetica", 11, "bold"),
            bootstyle="danger"
        )
        self.label_info.pack(pady=5)

        kursi_frame = tb.Labelframe(
            self.container,
            text="Pilih Kursi",
            padding=15,
            bootstyle="success"
        )
        kursi_frame.pack(padx=20, pady=10)

        tb.Label(
            kursi_frame,
            text="LAYAR BIOSKOP",
            bootstyle="inverse-dark"
        ).pack(fill="x", pady=5)

        self.grid = tb.Frame(kursi_frame)
        self.grid.pack()

        tb.Button(
            self.container,
            text="🎫 PESAN TIKET",
            bootstyle="danger",
            command=self.pesan
        ).pack(pady=15)

        self.update_info()
        self.render_kursi()

    # ---------- LOGIC ----------
    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    def ganti_film(self, judul):
        for f in self.film_list:
            if f.get_judul() == judul:
                self.film_aktif = f
        self.kursi_pilih.clear()
        self.update_info()
        self.render_kursi()

    def update_info(self):
        harga = self.film_aktif.hitung_harga()
        self.label_info.config(
            text=f"{self.film_aktif.get_info()} | Rp{harga:,}"
        )

    def render_kursi(self):
        for w in self.grid.winfo_children():
            w.destroy()

        for i in range(25):
            style = "success"
            if self.kursi_status[i]:
                style = "danger"
            elif i in self.kursi_pilih:
                style = "warning"

            tb.Button(
                self.grid,
                text=f"K{i+1}",
                width=6,
                bootstyle=style,
                command=lambda x=i: self.toggle_kursi(x)
            ).grid(row=i//5, column=i%5, padx=5, pady=5)

    def toggle_kursi(self, i):
        if self.kursi_status[i]:
            messagebox.showwarning("Peringatan", "Kursi sudah terisi")
            return
        if i in self.kursi_pilih:
            self.kursi_pilih.remove(i)
        else:
            self.kursi_pilih.append(i)
        self.render_kursi()

    def pesan(self):
        if not self.kursi_pilih:
            messagebox.showwarning("Error", "Pilih kursi dulu!")
            return

        total = len(self.kursi_pilih) * self.film_aktif.hitung_harga()
        kursi = ", ".join(f"K{i+1}" for i in self.kursi_pilih)

        if messagebox.askyesno(
            "Konfirmasi",
            f"Film: {self.film_aktif.get_judul()}\n"
            f"Kursi: {kursi}\n"
            f"Total: Rp{total:,}"
        ):
            for i in self.kursi_pilih:
                self.kursi_status[i] = True
            self.kursi_pilih.clear()
            self.render_kursi()
            messagebox.showinfo("Sukses", "Pemesanan berhasil 🎉")


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    BioskopApp(root)
    root.mainloop()
