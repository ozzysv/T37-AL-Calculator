import tkinter as tk
from tkinter import ttk, messagebox
import locale
import math
import webbrowser

REPO_URL = "https://github.com/ozzysv/T37-AL-Calculator"

RINGS = {
    "T37-2": 4.0,  # nH/turn²
    "T37-6": 3.0,  # nH/turn²
}

TEXTS = {
    "uk": {
        "window_title": "T37 AL Calculator",
        "title": "T37 AL Calculator",
        "subtitle": "Розрахунок AL і порівняння з T37-2 та T37-6",
        "measure_note": "Вимірювання індуктивності бажано проводити на частоті 1 МГц або 100 кГц",
        "turns": "Кількість витків",
        "inductance": "Індуктивність",
        "calculate": "Розрахувати",
        "result": "Результат",
        "closest": "Найближче до {ring}  •  відхилення {err:.1f}%",
        "expected": "Для {n} витків: T37-2 ≈ {l2:.0f} nH, T37-6 ≈ {l6:.0f} nH",
        "target_title": "Розрахунок кількості витків",
        "target_inductance": "Необхідна індуктивність",
        "turns_result": "Потрібно: {n} витків",
        "turns_exact": "Розрахунково: {exact:.2f} витка  •  AL = {al:.3f} nH/вит²",
        "target_button": "Розрахувати витки",
        "error_title": "Помилка",
        "error_text": "Введи додатне число витків і додатне значення індуктивності.",
        "target_error": "Спочатку розрахуй AL, потім введи необхідну індуктивність.",
        "lang_uk": "Українська",
        "lang_en": "English",
        "lang_de": "Deutsch",
    },
    "en": {
        "window_title": "T37 AL Calculator",
        "title": "T37 AL Calculator",
        "subtitle": "AL calculation and comparison with T37-2 and T37-6",
        "measure_note": "Inductance should preferably be measured at 1 MHz or 100 kHz",
        "turns": "Number of turns",
        "inductance": "Inductance",
        "calculate": "Calculate",
        "result": "Result",
        "closest": "Closest to {ring}  •  deviation {err:.1f}%",
        "expected": "For {n} turns: T37-2 ≈ {l2:.0f} nH, T37-6 ≈ {l6:.0f} nH",
        "target_title": "Turns calculation",
        "target_inductance": "Required inductance",
        "turns_result": "Required: {n} turns",
        "turns_exact": "Calculated: {exact:.2f} turns  •  AL = {al:.3f} nH/turn²",
        "target_button": "Calculate turns",
        "error_title": "Error",
        "error_text": "Enter a positive number of turns and a positive inductance value.",
        "target_error": "Calculate AL first, then enter the required inductance.",
        "lang_uk": "Українська",
        "lang_en": "English",
        "lang_de": "Deutsch",
    },
    "de": {
        "window_title": "T37 AL Rechner",
        "title": "T37 AL Rechner",
        "subtitle": "AL-Berechnung und Vergleich mit T37-2 und T37-6",
        "measure_note": "Die Induktivität sollte vorzugsweise bei 1 MHz oder 100 kHz gemessen werden",
        "turns": "Windungszahl",
        "inductance": "Induktivität",
        "calculate": "Berechnen",
        "result": "Ergebnis",
        "closest": "Am nächsten an {ring}  •  Abweichung {err:.1f}%",
        "expected": "Bei {n} Windungen: T37-2 ≈ {l2:.0f} nH, T37-6 ≈ {l6:.0f} nH",
        "target_title": "Windungszahl berechnen",
        "target_inductance": "Benötigte Induktivität",
        "turns_result": "Benötigt: {n} Windungen",
        "turns_exact": "Berechnet: {exact:.2f} Windungen  •  AL = {al:.3f} nH/Wdg²",
        "target_button": "Windungen berechnen",
        "error_title": "Fehler",
        "error_text": "Bitte eine positive Windungszahl und einen positiven Induktivitätswert eingeben.",
        "target_error": "Zuerst AL berechnen und danach die benötigte Induktivität eingeben.",
        "lang_uk": "Українська",
        "lang_en": "English",
        "lang_de": "Deutsch",
    },
}


def detect_language():
    lang_code = ""
    try:
        loc = locale.getdefaultlocale()[0]
        if loc:
            lang_code = loc.lower()
    except Exception:
        pass

    if not lang_code:
        try:
            loc = locale.getlocale()[0]
            if loc:
                lang_code = loc.lower()
        except Exception:
            pass

    if lang_code.startswith(("ru", "uk")):
        return "uk"
    if lang_code.startswith("de"):
        return "de"
    if lang_code.startswith("en"):
        return "en"
    return "en"


class ALCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.lang = detect_language()
        self.current_al = None

        window_w = 720
        window_h = 560
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        pos_x = (screen_w - window_w) // 2
        pos_y = (screen_h - window_h) // 2

        self.geometry(f"{window_w}x{window_h}+{pos_x}+{pos_y}")
        self.resizable(False, False)
        self.configure(bg="#111827")

        self._setup_styles()
        self._build_ui()
        self.apply_language()

    def _setup_styles(self):
        s = ttk.Style(self)
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass

        s.configure("Root.TFrame", background="#111827")
        s.configure("Card.TFrame", background="#1F2937")
        s.configure("Title.TLabel", background="#111827", foreground="#F9FAFB",
                    font=("Segoe UI", 21, "bold"))
        s.configure("Sub.TLabel", background="#111827", foreground="#9CA3AF",
                    font=("Segoe UI", 9))
        s.configure("Input.TLabel", background="#111827", foreground="#E5E7EB",
                    font=("Segoe UI", 10, "bold"))
        s.configure("CardTitle.TLabel", background="#1F2937", foreground="#F9FAFB",
                    font=("Segoe UI", 11, "bold"))
        s.configure("Big.TLabel", background="#1F2937", foreground="#60A5FA",
                    font=("Segoe UI", 23, "bold"))
        s.configure("Result.TLabel", background="#1F2937", foreground="#F9FAFB",
                    font=("Segoe UI", 10, "bold"))
        s.configure("CardText.TLabel", background="#1F2937", foreground="#D1D5DB",
                    font=("Segoe UI", 9))
        s.configure("TurnsBig.TLabel", background="#1F2937", foreground="#60A5FA",
                    font=("Segoe UI", 20, "bold"))
        s.configure("Calc.TButton", font=("Segoe UI", 10, "bold"), padding=(12, 8))

    def _build_ui(self):
        self.root_frame = ttk.Frame(self, style="Root.TFrame", padding=14)
        self.root_frame.pack(fill="both", expand=True)

        top_row = ttk.Frame(self.root_frame, style="Root.TFrame")
        top_row.pack(fill="x")

        self.title_label = ttk.Label(top_row, style="Title.TLabel")
        self.title_label.pack(side="left", anchor="w")

        self.subtitle_label = ttk.Label(self.root_frame, style="Sub.TLabel")
        self.subtitle_label.pack(anchor="w", pady=(1, 1))

        self.measure_note_label = ttk.Label(self.root_frame, style="Sub.TLabel")
        self.measure_note_label.pack(anchor="w", pady=(0, 9))

        # First input row
        inputs = ttk.Frame(self.root_frame, style="Root.TFrame")
        inputs.pack(fill="x")

        left = ttk.Frame(inputs, style="Root.TFrame")
        left.pack(side="left", fill="x", expand=True, padx=(0, 8))
        right = ttk.Frame(inputs, style="Root.TFrame")
        right.pack(side="left", fill="x", expand=True, padx=(8, 0))

        self.turns_label = ttk.Label(left, style="Input.TLabel")
        self.turns_label.pack(anchor="w")
        self.turns = tk.StringVar(value="12")
        self.turns_entry = ttk.Entry(left, textvariable=self.turns, font=("Segoe UI", 12))
        self.turns_entry.pack(fill="x", pady=(4, 0))

        self.inductance_label = ttk.Label(right, style="Input.TLabel")
        self.inductance_label.pack(anchor="w")

        row = ttk.Frame(right, style="Root.TFrame")
        row.pack(fill="x", pady=(4, 0))

        self.ind = tk.StringVar(value="570")
        self.ind_entry = ttk.Entry(row, textvariable=self.ind, font=("Segoe UI", 12))
        self.ind_entry.pack(side="left", fill="x", expand=True)

        self.unit = tk.StringVar(value="nH")
        self.unit_combo = ttk.Combobox(
            row, textvariable=self.unit, values=("nH", "µH"),
            width=5, state="readonly", font=("Segoe UI", 10)
        )
        self.unit_combo.pack(side="left", padx=(6, 0))

        self.calc_button = ttk.Button(
            self.root_frame, command=self.calculate, style="Calc.TButton"
        )
        self.calc_button.pack(fill="x", pady=9)

        # Result card: text on left, compact graphic on right
        self.result_frame = ttk.Frame(self.root_frame, style="Card.TFrame", padding=10)
        self.result_frame.pack(fill="x")

        result_left = ttk.Frame(self.result_frame, style="Card.TFrame")
        result_left.pack(side="left", fill="both", expand=True)

        self.result_title = ttk.Label(result_left, style="CardTitle.TLabel")
        self.result_title.pack(anchor="w")

        self.al_label = ttk.Label(result_left, text="—", style="Big.TLabel")
        self.al_label.pack(anchor="w", pady=(3, 1))

        self.closest_label = ttk.Label(result_left, text="", style="Result.TLabel")
        self.closest_label.pack(anchor="w")

        self.detail_label = ttk.Label(result_left, text="", style="CardText.TLabel")
        self.detail_label.pack(anchor="w", pady=(3, 0))

        self.canvas = tk.Canvas(
            self.result_frame,
            width=260, height=118,
            bg="#1F2937",
            highlightthickness=0
        )
        self.canvas.pack(side="right", padx=(10, 0))

        # Second calculator occupies the old graphic area
        self.target_frame = ttk.Frame(self.root_frame, style="Card.TFrame", padding=10)
        self.target_frame.pack(fill="both", expand=True, pady=(9, 0))

        self.target_title = ttk.Label(self.target_frame, style="CardTitle.TLabel")
        self.target_title.pack(anchor="w")

        target_row = ttk.Frame(self.target_frame, style="Card.TFrame")
        target_row.pack(fill="x", pady=(8, 6))

        self.target_inductance_label = ttk.Label(target_row, style="CardText.TLabel")
        self.target_inductance_label.pack(side="left")

        self.target_ind = tk.StringVar(value="580")
        self.target_entry = ttk.Entry(
            target_row, textvariable=self.target_ind,
            font=("Segoe UI", 12), width=18
        )
        self.target_entry.pack(side="left", padx=(12, 6))

        self.target_unit = tk.StringVar(value="nH")
        self.target_unit_combo = ttk.Combobox(
            target_row, textvariable=self.target_unit,
            values=("nH", "µH"), width=5,
            state="readonly", font=("Segoe UI", 10)
        )
        self.target_unit_combo.pack(side="left")

        self.target_button = ttk.Button(
            target_row, command=self.calculate_turns, style="Calc.TButton"
        )
        self.target_button.pack(side="right")

        self.turns_result_label = ttk.Label(
            self.target_frame, text="—", style="TurnsBig.TLabel"
        )
        self.turns_result_label.pack(anchor="w", pady=(8, 2))

        self.turns_exact_label = ttk.Label(
            self.target_frame, text="", style="CardText.TLabel"
        )
        self.turns_exact_label.pack(anchor="w")

        # Repository link at the bottom-right
        self.repo_link = tk.Label(
            self.root_frame,
            text="github.com/ozzysv/T37-AL-Calculator",
            bg="#111827",
            fg="#60A5FA",
            activeforeground="#93C5FD",
            activebackground="#111827",
            cursor="hand2",
            font=("Segoe UI", 8, "underline")
        )
        self.repo_link.pack(side="bottom", anchor="e", pady=(7, 0))
        self.repo_link.bind("<Button-1>", lambda event: webbrowser.open(REPO_URL))

        for w in (self.turns_entry, self.ind_entry):
            w.bind("<Return>", lambda event: self.calculate())
        self.target_entry.bind("<Return>", lambda event: self.calculate_turns())

        self.after(150, self.calculate)

    def apply_language(self):
        t = TEXTS[self.lang]

        self.title(t["window_title"])
        self.title_label.config(text=t["title"])
        self.subtitle_label.config(text=t["subtitle"])
        self.measure_note_label.config(text=t["measure_note"])
        self.turns_label.config(text=t["turns"])
        self.inductance_label.config(text=t["inductance"])
        self.calc_button.config(text=t["calculate"])
        self.result_title.config(text=t["result"])
        self.target_title.config(text=t["target_title"])
        self.target_inductance_label.config(text=t["target_inductance"])
        self.target_button.config(text=t["target_button"])

        self.calculate()
        if self.target_ind.get().strip():
            self.calculate_turns(show_error=False)

    def calculate(self):
        try:
            n = int(self.turns.get().strip())
            l = float(self.ind.get().replace(",", ".").strip())

            if n <= 0 or l <= 0:
                raise ValueError

            l_nh = l * 1000.0 if self.unit.get() == "µH" else l
            al = l_nh / (n ** 2)
            self.current_al = al

            errors = {
                name: abs(al - ref) / ref * 100.0
                for name, ref in RINGS.items()
            }
            closest = min(errors, key=errors.get)

            expected = {
                name: ref * (n ** 2)
                for name, ref in RINGS.items()
            }

            t = TEXTS[self.lang]

            self.al_label.config(text=f"{al:.3f} nH/вит²")
            self.closest_label.config(
                text=t["closest"].format(ring=closest, err=errors[closest])
            )
            self.detail_label.config(
                text=t["expected"].format(
                    n=n,
                    l2=expected["T37-2"],
                    l6=expected["T37-6"]
                )
            )

            self.draw_comparison(al)
            self.calculate_turns(show_error=False)

        except ValueError:
            t = TEXTS[self.lang]
            messagebox.showerror(t["error_title"], t["error_text"])

    def calculate_turns(self, show_error=True):
        try:
            if not self.current_al or self.current_al <= 0:
                raise ValueError

            l = float(self.target_ind.get().replace(",", ".").strip())
            if l <= 0:
                raise ValueError

            l_nh = l * 1000.0 if self.target_unit.get() == "µH" else l

            exact_turns = math.sqrt(l_nh / self.current_al)

            # Normal nearest-integer rounding for positive values:
            turns = int(math.floor(exact_turns + 0.5))
            turns = max(1, turns)

            t = TEXTS[self.lang]
            self.turns_result_label.config(
                text=t["turns_result"].format(n=turns)
            )
            self.turns_exact_label.config(
                text=t["turns_exact"].format(
                    exact=exact_turns,
                    al=self.current_al
                )
            )

        except ValueError:
            if show_error:
                t = TEXTS[self.lang]
                messagebox.showerror(t["error_title"], t["target_error"])

    def draw_comparison(self, al):
        c = self.canvas
        c.delete("all")

        width = 260
        height = 118
        center_x = width / 2
        y = 70

        left_x = 37
        right_x = width - 37
        outer_r = 22
        inner_r = 10

        # Labels above rings
        c.create_text(
            left_x, 20, text="T37-2",
            fill="#FFFFFF", font=("Segoe UI", 8, "bold")
        )
        c.create_text(
            right_x, 20, text="T37-6",
            fill="#FFFFFF", font=("Segoe UI", 8, "bold")
        )

        # T37-2 ring
        c.create_oval(
            left_x-outer_r, y-outer_r,
            left_x+outer_r, y+outer_r,
            fill="#9A3E32", outline="#D26755", width=2
        )
        c.create_oval(
            left_x-inner_r, y-inner_r,
            left_x+inner_r, y+inner_r,
            fill="#1F2937", outline="#5C241F", width=1
        )

        # T37-6 ring
        c.create_oval(
            right_x-outer_r, y-outer_r,
            right_x+outer_r, y+outer_r,
            fill="#F0C91B", outline="#FFE45A", width=2
        )
        c.create_oval(
            right_x-inner_r, y-inner_r,
            right_x+inner_r, y+inner_r,
            fill="#1F2937", outline="#8A7100", width=1
        )

        # Hidden logical zero in center.
        d2 = abs(al - RINGS["T37-2"])
        d6 = abs(al - RINGS["T37-6"])
        denom = d2 + d6

        if denom == 0:
            preference = 0.0
        else:
            preference = (d2 - d6) / denom

        preference = max(-1.0, min(1.0, preference))

        track_left = left_x + outer_r + 9
        track_right = right_x - outer_r - 9
        bar_y1 = y - 6
        bar_y2 = y + 6

        c.create_rectangle(
            track_left, bar_y1, track_right, bar_y2,
            fill="#374151", outline=""
        )

        bar_half = (track_right - track_left) / 2
        end_x = center_x + preference * bar_half

        if preference < 0:
            c.create_rectangle(
                end_x, bar_y1, center_x, bar_y2,
                fill="#B64D3D", outline=""
            )
        elif preference > 0:
            c.create_rectangle(
                center_x, bar_y1, end_x, bar_y2,
                fill="#F0C91B", outline=""
            )


if __name__ == "__main__":
    ALCalculator().mainloop()
