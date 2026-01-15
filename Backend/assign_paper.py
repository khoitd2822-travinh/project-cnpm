import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import ctypes

# Fix độ nét High DPI cho Windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# ================= CONFIG & COLORS =================
COLORS = {
    "sidebar": "#1E293B",
    "sidebar_hover": "#334155",
    "bg_content": "#F8FAFC",
    "primary": "#2563EB",
    "success": "#10B981",
    "text_main": "#0F172A",
    "text_light": "#F8FAFC",
    "white": "#FFFFFF",
    "border": "#E2E8F0"
}

FONTS = {
    "title": ("Segoe UI", 24, "bold"),
    "header": ("Segoe UI", 14, "bold"),
    "normal": ("Segoe UI", 11),
    "btn": ("Segoe UI", 10, "bold"),
    "table": ("Segoe UI", 11)
}

history = [] # Cơ sở dữ liệu tạm thời

# ================= CUSTOM COMPONENTS =================
class SideButton(tk.Button):
    def __init__(self, master, text, command, icon="•", **kwargs):
        super().__init__(master, text=f"  {icon}  {text}", command=command,
                         anchor="w", fg=COLORS["text_light"], bg=COLORS["sidebar"],
                         activebackground=COLORS["sidebar_hover"], activeforeground="white",
                         font=FONTS["btn"], relief="flat", borderwidth=0, 
                         cursor="hand2", pady=15, padx=20, **kwargs)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hệ Thống Phân Công Bài Báo - No Login")
        self.state('zoomed') 
        self.geometry("1200x800")
        self.configure(bg=COLORS["bg_content"])

        # Layout chính: Sidebar (Trái) + Content (Phải)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. SIDEBAR
        self.sidebar = tk.Frame(self, bg=COLORS["sidebar"], width=280)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        tk.Label(self.sidebar, text="QUẢN TRỊ VIÊN", font=("Segoe UI", 16, "bold"),
                 bg=COLORS["sidebar"], fg=COLORS["success"], pady=30).pack()

        SideButton(self.sidebar, "Trang Chủ", lambda: self.show_frame("RoleFrame"), icon="🏠").pack(fill="x")
        SideButton(self.sidebar, "Admin Phân Công", lambda: self.show_frame("AdminFrame"), icon="📝").pack(fill="x")
        SideButton(self.sidebar, "Reviewer Portal", lambda: self.show_frame("ReviewerFrame"), icon="👤").pack(fill="x")
        SideButton(self.sidebar, "Lịch Sử Hệ Thống", lambda: self.show_frame("HistoryFrame"), icon="📊").pack(fill="x")
        
        tk.Label(self.sidebar, text="© 2024 Project CNPM", font=("Segoe UI", 8),
                 bg=COLORS["sidebar"], fg="#64748B").pack(side="bottom", pady=20)

        # 2. CONTENT AREA
        self.content_area = tk.Frame(self, bg=COLORS["bg_content"])
        self.content_area.grid(row=0, column=1, sticky="nsew")
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=FONTS["table"], rowheight=40, borderwidth=0)
        style.configure("Treeview.Heading", font=FONTS["header"], background="#F1F5F9", relief="flat")

        self.frames = {}
        for F in (RoleFrame, AdminFrame, ReviewerFrame, HistoryFrame, SuccessFrame):
            page_name = F.__name__
            frame = F(parent=self.content_area, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("RoleFrame")

    def show_frame(self, page_name, filter_id=None):
        frame = self.frames[page_name]
        if hasattr(frame, 'on_show'):
            frame.on_show(filter_id)
        frame.tkraise()

# ================= 1. TRANG CHỦ (CHỌN VAI TRÒ) =================
class RoleFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg_content"])
        
        container = tk.Frame(self, bg=COLORS["bg_content"])
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(container, text="HỆ THỐNG PHÂN CÔNG BÀI BÁO", font=FONTS["title"], 
                 bg=COLORS["bg_content"], fg=COLORS["text_main"]).pack(pady=10)
        
        cards = tk.Frame(container, bg=COLORS["bg_content"])
        cards.pack(pady=40)

        self.create_card(cards, "ADMIN", "Phân công bài báo", COLORS["primary"], 
                         lambda: controller.show_frame("AdminFrame")).grid(row=0, column=0, padx=20)
        self.create_card(cards, "REVIEWER", "Xem lịch sử cá nhân", COLORS["success"], 
                         lambda: controller.show_frame("ReviewerFrame")).grid(row=0, column=1, padx=20)
        self.create_card(cards, "CHAIR/AUTHOR", "Xem lịch sử chung", "#64748B", 
                         lambda: controller.show_frame("HistoryFrame")).grid(row=0, column=2, padx=20)

    def create_card(self, parent, title, desc, color, cmd):
        f = tk.Frame(parent, bg=COLORS["white"], width=280, height=200, highlightthickness=1, highlightbackground=COLORS["border"])
        f.pack_propagate(False)
        tk.Label(f, text=title, font=FONTS["header"], fg=color, bg="white").pack(pady=(30, 10))
        tk.Label(f, text=desc, font=FONTS["normal"], bg="white", fg="#64748B").pack()
        tk.Button(f, text="Truy cập →", font=FONTS["btn"], bg=color, fg="white", relief="flat", padx=20, pady=8, command=cmd).pack(side="bottom", pady=20)
        return f

# ================= 2. ADMIN (PHÂN CÔNG) =================
class AdminFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg_content"])
        self.controller = controller
        
        f = tk.Frame(self, bg=COLORS["white"], padx=60, pady=50, highlightthickness=1, highlightbackground=COLORS["border"])
        f.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(f, text="PHÂN CÔNG BÀI BÁO MỚI", font=FONTS["title"], bg="white").pack(pady=(0,30))

        self.inputs = {}
        fields = [("Mã bài báo (6 số)", "paper"), ("Mã Reviewer (6 số)", "rid"), 
                  ("Tên Reviewer", "rname"), ("Deadline (DD/MM/YYYY)", "deadline")]

        grid_form = tk.Frame(f, bg="white")
        grid_form.pack()

        for i, (lbl, key) in enumerate(fields):
            r, c = divmod(i, 2)
            cell = tk.Frame(grid_form, bg="white", padx=15, pady=10)
            cell.grid(row=r, column=c)
            tk.Label(cell, text=lbl, bg="white", font=FONTS["normal"]).pack(anchor="w")
            e = ttk.Entry(cell, width=35, font=FONTS["normal"])
            e.pack(ipady=8, pady=5)
            self.inputs[key] = e

        tk.Label(f, text="Lĩnh vực bài báo", bg="white", font=FONTS["normal"]).pack(anchor="w", padx=15)
        self.field_cb = ttk.Combobox(f, values=["AI", "Cyber Security", "Data Science", "Software"], state="readonly", font=FONTS["normal"])
        self.field_cb.pack(fill="x", padx=15, pady=10, ipady=5)

        tk.Button(f, text="XÁC NHẬN PHÂN CÔNG", bg=COLORS["primary"], fg="white", font=FONTS["btn"],
                  relief="flat", pady=15, cursor="hand2", command=self.submit).pack(fill="x", padx=15, pady=20)

    def submit(self):
        v = {k: e.get().strip() for k, e in self.inputs.items()}
        v["field"] = self.field_cb.get()

        if len(v["paper"]) == 6 and len(v["rid"]) == 6 and v["field"]:
            history.append({
                "paper": v["paper"], "rid": v["rid"], "name": v["rname"],
                "field": v["field"], "deadline": v["deadline"],
                "time": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            # Reset form
            for e in self.inputs.values(): e.delete(0, tk.END)
            self.field_cb.set('')
            self.controller.show_frame("SuccessFrame")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng Mã 6 số và đầy đủ thông tin!")

# ================= 3. REVIEWER (NHẬP ID XEM LỊCH SỬ) =================
class ReviewerFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg_content"])
        self.controller = controller

        f = tk.Frame(self, bg=COLORS["white"], padx=60, pady=60, highlightthickness=1, highlightbackground=COLORS["border"])
        f.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(f, text="REVIEWER PORTAL", font=FONTS["title"], bg="white").pack(pady=(0, 30))
        tk.Label(f, text="Nhập mã ID 6 chữ số để xem lịch sử của bạn", bg="white", fg="#64748B").pack(pady=(0,20))

        self.id_ent = ttk.Entry(f, width=40, font=FONTS["normal"], justify="center")
        self.id_ent.pack(ipady=10, pady=10)
        self.id_ent.bind("<Return>", lambda e: self.search())

        tk.Button(f, text="XEM LỊCH SỬ PHÂN CÔNG CỦA TÔI", bg=COLORS["success"], fg="white", 
                  font=FONTS["btn"], pady=12, width=35, relief="flat", command=self.search).pack(pady=20)

    def search(self):
        uid = self.id_ent.get().strip()
        if len(uid) == 6 and uid.isdigit():
            self.controller.show_frame("HistoryFrame", filter_id=uid)
        else:
            messagebox.showwarning("Lỗi", "Mã ID phải là 6 chữ số!")

# ================= 4. LỊCH SỬ (HISTORY TREEVIEW) =================
class HistoryFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg_content"])
        self.controller = controller

        header = tk.Frame(self, bg=COLORS["white"], height=80, highlightthickness=1, highlightbackground=COLORS["border"])
        header.pack(fill="x")
        self.title_lbl = tk.Label(header, text="📊 LỊCH SỬ PHÂN CÔNG", font=FONTS["header"], bg="white", padx=30)
        self.title_lbl.pack(side="left", fill="y")

        container = tk.Frame(self, bg=COLORS["bg_content"], padx=40, pady=40)
        container.pack(fill="both", expand=True)

        cols = ("STT", "Mã Bài", "Reviewer", "Mã Reviewer", "Lĩnh Vực", "Giờ Phân Công", "Hạn Deadline")
        self.tree = ttk.Treeview(container, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center", width=120)
        
        self.tree.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        sb.pack(side="right", fill="y")

    def on_show(self, filter_id=None):
        for i in self.tree.get_children(): self.tree.delete(i)
        
        data = history
        if filter_id:
            data = [h for h in history if h['rid'] == filter_id]
            self.title_lbl.config(text="👤 LỊCH SỬ PHÂN CÔNG CỦA BẠN")
        else:
            self.title_lbl.config(text="📊 LỊCH SỬ PHÂN CÔNG TỔNG QUÁT")

        for i, h in enumerate(data, 1):
            self.tree.insert("", "end", values=(i, h['paper'], h['name'], h['rid'], h['field'], h['time'], h['deadline']))

# ================= 5. THÀNH CÔNG (SUCCESS SCREEN) =================
class SuccessFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg_content"])
        f = tk.Frame(self, bg=COLORS["white"], padx=80, pady=80, highlightthickness=1, highlightbackground=COLORS["border"])
        f.place(relx=0.5, rely=0.5, anchor="center")

        canvas = tk.Canvas(f, width=100, height=100, bg="white", highlightthickness=0)
        canvas.pack()
        canvas.create_oval(5, 5, 95, 95, fill=COLORS["success"], outline="")
        canvas.create_text(50, 52, text="✔", fill="white", font=("Arial", 50, "bold"))

        tk.Label(f, text="THÀNH CÔNG!", font=FONTS["title"], fg=COLORS["success"], bg="white").pack(pady=20)
        tk.Button(f, text="TIẾP TỤC PHÂN CÔNG", bg=COLORS["primary"], fg="white", 
                  font=FONTS["btn"], pady=12, width=25, relief="flat",
                  command=lambda: controller.show_frame("AdminFrame")).pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()

