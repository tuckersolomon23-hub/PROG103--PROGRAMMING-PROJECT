"""
============================================================
  PROG103 - Principle of Structured Programming
  Final Project: Student Results Management System
  Institution:   Limkokwing University of Creative Technology
  SDG Alignment: SDG 4 - Quality Education
  GUI Library:   Tkinter (Python Standard Library)
============================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# ─────────────────────────────────────────
#  DATA STORE  (in-memory list of dicts)
# ─────────────────────────────────────────
students = []          # Each entry: {id, name, math, english, science, ict, avg, grade, status}

# ─────────────────────────────────────────
#  UTILITY / LOGIC FUNCTIONS
# ─────────────────────────────────────────

def calculate_average(scores: list) -> float:
    """Return the arithmetic mean of a list of scores."""
    return sum(scores) / len(scores)


def determine_grade(average: float) -> str:
    """Return letter grade based on average score."""
    if average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


def determine_status(average: float) -> str:
    """Return pass/fail status."""
    return "PASS" if average >= 50 else "FAIL"


def generate_student_id() -> str:
    """Auto-generate a simple student ID."""
    return f"SL{str(len(students) + 1).zfill(3)}"


def find_student_by_id(student_id: str):
    """Search students list and return matching record or None."""
    for student in students:
        if student["id"] == student_id:
            return student
    return None


def validate_score(value: str, field_name: str) -> float:
    """Validate that a score is a number between 0 and 100."""
    try:
        score = float(value)
    except ValueError:
        raise ValueError(f"{field_name} must be a number.")
    if not (0 <= score <= 100):
        raise ValueError(f"{field_name} must be between 0 and 100.")
    return score


def validate_name(name: str) -> str:
    """Validate that student name is not empty."""
    name = name.strip()
    if not name:
        raise ValueError("Student name cannot be empty.")
    if len(name) < 2:
        raise ValueError("Student name is too short.")
    return name


def add_student(name, math, english, science, ict):
    """Create and store a new student record. Returns the record."""
    name     = validate_name(name)
    math     = validate_score(math,    "Mathematics")
    english  = validate_score(english, "English")
    science  = validate_score(science, "Science")
    ict      = validate_score(ict,     "ICT")

    avg    = calculate_average([math, english, science, ict])
    grade  = determine_grade(avg)
    status = determine_status(avg)

    record = {
        "id":      generate_student_id(),
        "name":    name,
        "math":    math,
        "english": english,
        "science": science,
        "ict":     ict,
        "avg":     round(avg, 2),
        "grade":   grade,
        "status":  status,
    }
    students.append(record)
    return record


def delete_student(student_id: str) -> bool:
    """Remove a student from the list by ID. Returns True if found."""
    global students
    before = len(students)
    students = [s for s in students if s["id"] != student_id]
    return len(students) < before


def get_statistics():
    """Compute class-wide statistics."""
    if not students:
        return None
    averages = [s["avg"] for s in students]
    passes   = [s for s in students if s["status"] == "PASS"]
    return {
        "total":      len(students),
        "highest":    max(averages),
        "lowest":     min(averages),
        "class_avg":  round(sum(averages) / len(averages), 2),
        "pass_count": len(passes),
        "fail_count": len(students) - len(passes),
    }


# ─────────────────────────────────────────
#  GUI APPLICATION CLASS
# ─────────────────────────────────────────

class StudentResultsApp:
    """Main GUI application using Tkinter."""

    # ── Colour palette ──────────────────
    C_BG       = "#F0F4F8"   # Light grey-blue background
    C_HEADER   = "#1A3C5E"   # Deep navy – header bar
    C_ACCENT   = "#2E7D32"   # Sierra Leone green
    C_ACCENT2  = "#C62828"   # Sierra Leone red
    C_WHITE    = "#FFFFFF"
    C_ROW_ODD  = "#E8F5E9"
    C_ROW_EVEN = "#FFFFFF"
    C_PASS     = "#2E7D32"
    C_FAIL     = "#C62828"
    C_TEXT     = "#1C1C1C"
    C_MUTED    = "#607D8B"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Student Results Management System – Limkokwing SL")
        self.root.geometry("1050x700")
        self.root.resizable(True, True)
        self.root.configure(bg=self.C_BG)

        self._build_header()
        self._build_main_area()
        self._build_status_bar()
        self._refresh_table()

    # ── Layout builders ──────────────────

    def _build_header(self):
        """Top banner with title."""
        hdr = tk.Frame(self.root, bg=self.C_HEADER, height=70)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)

        tk.Label(
            hdr,
            text="🎓  Student Results Management System",
            font=("Helvetica", 18, "bold"),
            bg=self.C_HEADER, fg=self.C_WHITE
        ).pack(side=tk.LEFT, padx=20, pady=15)

        tk.Label(
            hdr,
            text="SDG 4 – Quality Education  |  Limkokwing University SL",
            font=("Helvetica", 9),
            bg=self.C_HEADER, fg="#90CAF9"
        ).pack(side=tk.RIGHT, padx=20, pady=15)

    def _build_main_area(self):
        """Two-column layout: left = form, right = table."""
        body = tk.Frame(self.root, bg=self.C_BG)
        body.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        self._build_form_panel(body)
        self._build_table_panel(body)

    def _build_form_panel(self, parent):
        """Left panel: add student form + stats."""
        left = tk.Frame(parent, bg=self.C_WHITE, bd=1, relief=tk.SOLID, width=310)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        left.pack_propagate(False)

        # ── Section heading ──
        tk.Label(
            left, text="Add New Student",
            font=("Helvetica", 13, "bold"),
            bg=self.C_ACCENT, fg=self.C_WHITE,
            pady=8
        ).pack(fill=tk.X)

        form = tk.Frame(left, bg=self.C_WHITE, padx=14, pady=10)
        form.pack(fill=tk.X)

        # ── Fields ──
        fields = [
            ("Student Name", "name"),
            ("Mathematics  (0–100)", "math"),
            ("English       (0–100)", "english"),
            ("Science       (0–100)", "science"),
            ("ICT            (0–100)", "ict"),
        ]
        self.entries = {}
        for label_text, key in fields:
            tk.Label(
                form, text=label_text,
                font=("Helvetica", 9, "bold"),
                bg=self.C_WHITE, fg=self.C_TEXT, anchor="w"
            ).pack(fill=tk.X, pady=(6, 1))

            entry = tk.Entry(
                form, font=("Helvetica", 10),
                relief=tk.SOLID, bd=1, bg="#FAFAFA"
            )
            entry.pack(fill=tk.X, ipady=4)
            self.entries[key] = entry

        # ── Buttons ──
        btn_frame = tk.Frame(left, bg=self.C_WHITE, padx=14)
        btn_frame.pack(fill=tk.X, pady=8)

        tk.Button(
            btn_frame, text="➕  Add Student",
            font=("Helvetica", 10, "bold"),
            bg=self.C_ACCENT, fg=self.C_WHITE,
            relief=tk.FLAT, cursor="hand2",
            command=self._on_add_student, pady=7
        ).pack(fill=tk.X, pady=(0, 5))

        tk.Button(
            btn_frame, text="🗑  Delete Selected",
            font=("Helvetica", 10),
            bg=self.C_ACCENT2, fg=self.C_WHITE,
            relief=tk.FLAT, cursor="hand2",
            command=self._on_delete_student, pady=7
        ).pack(fill=tk.X, pady=(0, 5))

        tk.Button(
            btn_frame, text="🔄  Clear Form",
            font=("Helvetica", 10),
            bg="#546E7A", fg=self.C_WHITE,
            relief=tk.FLAT, cursor="hand2",
            command=self._clear_form, pady=7
        ).pack(fill=tk.X)

        # ── Statistics panel ──
        tk.Label(
            left, text="Class Statistics",
            font=("Helvetica", 12, "bold"),
            bg=self.C_HEADER, fg=self.C_WHITE,
            pady=6
        ).pack(fill=tk.X, pady=(16, 0))

        self.stats_frame = tk.Frame(left, bg=self.C_WHITE, padx=14, pady=8)
        self.stats_frame.pack(fill=tk.X)

        self.stat_labels = {}
        stat_keys = [
            ("Total Students",  "total"),
            ("Highest Average", "highest"),
            ("Lowest Average",  "lowest"),
            ("Class Average",   "class_avg"),
            ("Passed",          "pass_count"),
            ("Failed",          "fail_count"),
        ]
        for display, key in stat_keys:
            row = tk.Frame(self.stats_frame, bg=self.C_WHITE)
            row.pack(fill=tk.X, pady=2)
            tk.Label(
                row, text=display + ":",
                font=("Helvetica", 9), bg=self.C_WHITE,
                fg=self.C_MUTED, width=16, anchor="w"
            ).pack(side=tk.LEFT)
            lbl = tk.Label(
                row, text="—",
                font=("Helvetica", 9, "bold"),
                bg=self.C_WHITE, fg=self.C_TEXT
            )
            lbl.pack(side=tk.LEFT)
            self.stat_labels[key] = lbl

    def _build_table_panel(self, parent):
        """Right panel: results table."""
        right = tk.Frame(parent, bg=self.C_WHITE, bd=1, relief=tk.SOLID)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # heading + search row
        top = tk.Frame(right, bg=self.C_HEADER)
        top.pack(fill=tk.X)

        tk.Label(
            top, text="Student Records",
            font=("Helvetica", 12, "bold"),
            bg=self.C_HEADER, fg=self.C_WHITE, pady=8, padx=12
        ).pack(side=tk.LEFT)

        # Search box
        tk.Label(
            top, text="Search:", bg=self.C_HEADER,
            fg=self.C_WHITE, font=("Helvetica", 9)
        ).pack(side=tk.RIGHT, padx=(0, 4), pady=8)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self._refresh_table())
        tk.Entry(
            top, textvariable=self.search_var,
            font=("Helvetica", 9), width=18,
            relief=tk.FLAT, bd=2
        ).pack(side=tk.RIGHT, pady=8, padx=(0, 12))

        # Treeview
        cols = ("ID", "Name", "Math", "English", "Science", "ICT", "Average", "Grade", "Status")
        self.tree = ttk.Treeview(right, columns=cols, show="headings", selectmode="browse")

        col_widths = [55, 160, 60, 70, 65, 50, 70, 55, 65]
        for col, w in zip(cols, col_widths):
            self.tree.heading(col, text=col, command=lambda c=col: self._sort_by(c))
            self.tree.column(col, width=w, anchor=tk.CENTER)

        # Colour tags
        self.tree.tag_configure("pass",     foreground=self.C_PASS)
        self.tree.tag_configure("fail",     foreground=self.C_FAIL)
        self.tree.tag_configure("row_odd",  background=self.C_ROW_ODD)
        self.tree.tag_configure("row_even", background=self.C_ROW_EVEN)

        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                         font=("Helvetica", 9),
                         rowheight=24,
                         background=self.C_WHITE,
                         fieldbackground=self.C_WHITE)
        style.configure("Treeview.Heading",
                         font=("Helvetica", 9, "bold"),
                         background=self.C_BG,
                         foreground=self.C_HEADER)
        style.map("Treeview", background=[("selected", "#BBDEFB")])

        # Scrollbars
        v_scroll = ttk.Scrollbar(right, orient=tk.VERTICAL,   command=self.tree.yview)
        h_scroll = ttk.Scrollbar(right, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self._sort_col   = None
        self._sort_asc   = True

    def _build_status_bar(self):
        """Bottom status bar."""
        bar = tk.Frame(self.root, bg=self.C_HEADER, height=24)
        bar.pack(fill=tk.X, side=tk.BOTTOM)
        bar.pack_propagate(False)

        self.status_var = tk.StringVar(value="Ready  •  No students yet.")
        tk.Label(
            bar, textvariable=self.status_var,
            font=("Helvetica", 8), bg=self.C_HEADER,
            fg="#90CAF9", anchor="w", padx=10
        ).pack(side=tk.LEFT, fill=tk.Y)

        now = datetime.datetime.now().strftime("%d %B %Y  %H:%M")
        tk.Label(
            bar, text=now,
            font=("Helvetica", 8), bg=self.C_HEADER,
            fg="#90CAF9", padx=10
        ).pack(side=tk.RIGHT, fill=tk.Y)

    # ── Event handlers ───────────────────

    def _on_add_student(self):
        """Read form, validate, add student, refresh."""
        try:
            record = add_student(
                name    = self.entries["name"].get(),
                math    = self.entries["math"].get(),
                english = self.entries["english"].get(),
                science = self.entries["science"].get(),
                ict     = self.entries["ict"].get(),
            )
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return

        self._clear_form()
        self._refresh_table()
        self._set_status(f"✔  Student '{record['name']}' added  –  ID: {record['id']}")

    def _on_delete_student(self):
        """Delete the currently selected row."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a student to delete.")
            return

        item   = self.tree.item(selected[0])
        sid    = item["values"][0]
        name   = item["values"][1]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete student {name} ({sid})?\nThis cannot be undone."
        )
        if not confirm:
            return

        delete_student(sid)
        self._refresh_table()
        self._set_status(f"🗑  Student '{name}' ({sid}) deleted.")

    def _clear_form(self):
        """Clear all input fields."""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.entries["name"].focus()

    # ── Display helpers ──────────────────

    def _refresh_table(self):
        """Re-populate the Treeview from the students list."""
        query = self.search_var.get().lower() if hasattr(self, "search_var") else ""

        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        filtered = [
            s for s in students
            if query in s["name"].lower() or query in s["id"].lower()
        ] if query else students[:]

        for idx, s in enumerate(filtered):
            tags = []
            tags.append("row_odd" if idx % 2 == 0 else "row_even")
            tags.append("pass" if s["status"] == "PASS" else "fail")

            self.tree.insert("", tk.END, values=(
                s["id"], s["name"],
                s["math"], s["english"], s["science"], s["ict"],
                s["avg"], s["grade"], s["status"]
            ), tags=tags)

        self._update_stats()

    def _update_stats(self):
        """Refresh the statistics labels."""
        stats = get_statistics()
        if stats is None:
            for lbl in self.stat_labels.values():
                lbl.config(text="—", fg=self.C_TEXT)
            self._set_status("Ready  •  No students yet.")
            return

        mapping = {
            "total":      str(stats["total"]),
            "highest":    f"{stats['highest']}%",
            "lowest":     f"{stats['lowest']}%",
            "class_avg":  f"{stats['class_avg']}%",
            "pass_count": str(stats["pass_count"]),
            "fail_count": str(stats["fail_count"]),
        }
        for key, val in mapping.items():
            color = (self.C_PASS if key == "pass_count"
                     else self.C_FAIL if key == "fail_count"
                     else self.C_TEXT)
            self.stat_labels[key].config(text=val, fg=color)

        self._set_status(
            f"Total: {stats['total']}  |  "
            f"Class Avg: {stats['class_avg']}%  |  "
            f"Pass: {stats['pass_count']}  Fail: {stats['fail_count']}"
        )

    def _set_status(self, message: str):
        """Update the bottom status bar."""
        self.status_var.set(message)

    def _sort_by(self, col: str):
        """Sort table by clicked column header."""
        col_map = {
            "ID": "id", "Name": "name", "Math": "math",
            "English": "english", "Science": "science", "ICT": "ict",
            "Average": "avg", "Grade": "grade", "Status": "status"
        }
        key = col_map.get(col, "id")

        if self._sort_col == col:
            self._sort_asc = not self._sort_asc
        else:
            self._sort_col = col
            self._sort_asc = True

        students.sort(key=lambda s: s[key], reverse=not self._sort_asc)
        self._refresh_table()


# ─────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────

def main():
    """Launch the application."""
    root = tk.Tk()
    app  = StudentResultsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()