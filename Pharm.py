import tkinter as tk
from tkinter import messagebox
import mysql.connector as mysql
from mysql.connector import Error
from datetime import datetime
from pathlib import Path

THEME = {
    "main_bg": "#0b0f14",
    "header_bg": "#ffb000",
    "header_fg": "#111111",

    "window_bg": "#e9f7e9",

    "label_bg": "#1f2937",
    "label_fg": "#ffffff",

    "main_tile_bg": "#5b0d12",
    "main_tile_fg": "#ffffff",
    "main_tile_hover": "#3a070a",
    "main_tile_press": "#2a0507",

    "btn_bg": "#ffffff",
    "btn_fg": "#111111",
    "btn_active_bg": "#e6e6e6",
    "btn_active_fg": "#111111",

    "entry_bg": "#ffffff",
    "entry_fg": "#111111",
    "entry_insert": "#111111",

    "text_bg": "#0f172a",
    "text_fg": "#e8eef5",
    "text_insert": "#e8eef5",
}

DB_CONFIG = {"host": "localhost", "user": "root", "password": "Ishumysql123#", "database": "pharmacy"}
DELIVERY_FEE = 100
ORDER_TXT = Path("Order.txt")

# d[name] = [price, box_no, shelf_no, batch_no]
d = {
  "COMBIFLAM":[50,1,1,1234],"DIGENE":[100,1,1,1235],"DOLO":[75,1,1,1236],"PANTOP":[100,1,1,1237],
  "RAMISEV":[50,1,1,1238],"SELOKEN":[70,1,2,1239],"TAZLOC":[50,1,2,1240],"BETADINE":[150,1,2,1241],
  "DRISHTI":[70,1,2,1242],"SOFRAMYCIN":[100,1,2,1243],"RABESEC":[50,1,3,1244],"CALPOL":[50,1,3,1245],
  "CITREZENE":[100,1,3,1246],"AZETHRAL":[100,1,3,1247],"IBUPROFEN":[150,1,3,1248],"AMPOXIN":[100,1,4,1249],
  "ATARAX":[70,1,4,1250],"CROCIN":[100,1,4,1251],"ARISTOZYME":[70,1,4,1252],"TACODERM":[50,1,4,1253],
  "TUSQ-D":[150,2,1,1254],"OMNIGEL":[100,2,1,1255],"VOLINI":[100,2,1,1256],"AVOMINE":[75,2,1,1257],
  "SAVLON":[150,2,1,1258],"BEVON":[100,2,2,1259],"ENO":[50,2,2,1260],"BETNOVATE":[100,2,2,1261],
  "CREMAFFIN":[70,2,2,1262],"THROMBOPHOB":[50,2,2,1263],"OCUPOL":[70,2,3,1264],"ORACLEAR-S":[100,2,3,1265],
  "MAHACEF":[50,2,3,1266],"CLAMPKID":[75,2,3,1267],"MOBIZOX":[50,2,3,1268],"LANOXIN":[100,2,4,1269],
  "TEARDROPS":[100,2,4,1270],"ZINASE-D":[70,2,4,1271],"PHENERGAN":[100,2,4,1272],"SINAREST":[75,2,4,1273],
  "STODAL":[150,3,1,1274],"PICLIN":[55,3,1,1275],"KUFRAKSHAK":[70,3,1,1276],"JOSHINA":[60,3,1,1277],
  "IBUGESIC":[100,3,1,1278],"APTIMUST":[75,3,2,1279],"SPARACID":[55,3,2,1280],"RHEUMA-SAJ":[100,3,2,1281],
  "SCABOIL":[79,3,2,1282],"TIKLIK":[100,3,2,1283],"MEFTAL-P":[77,3,3,1284],"PARACIP":[95,3,3,1285],
  "EMESET":[50,3,3,1286],"KUKA":[100,3,3,1287],"NIMSIM":[70,3,3,1288],"CAVMOXKID":[120,3,4,1289],
  "NAZOCLEAR":[55,3,4,1290],"SULPHUR-OINTMENT":[100,3,4,1291],"HALOVATE":[95,3,4,1292],"ORA-SORE":[100,3,4,1293],
  "NEOSPORIN":[75,4,1,1294],"PARACETAMOL":[100,4,1,1295],"SUPRADYN":[77,4,1,1296],"ALLEGRA":[40,4,1,1297],
  "CALCITAS":[94,4,1,1299],"DUOLIN":[120,4,2,1300],"PROTERA-D":[90,4,2,1301],"ULTRACET":[81,4,2,1302],
  "ULTRANURON":[66,4,2,1303],"FLEXON":[120,4,2,1304],"NEBICARD":[150,4,3,1305],"BICOSUL":[120,4,3,1306],
  "DISPRIN":[100,4,3,1307],"SEPTRA":[60,4,3,1308],"ALDACTONE":[160,4,3,1309],"NUCOXIA":[200,4,4,1310],
  "BUDECORT":[100,4,4,1311],"OMNACORTIL":[55,4,4,1312],"AMBRODIL":[80,4,4,1313],"CALOSOFT LOTION":[89,4,4,1314],
  "METROGYL":[122,5,1,1315],"VOVERAN":[100,5,1,1316],"REFID PLUS":[111,5,1,1317],"CHESTON":[110,5,1,1318],
  "LEVOLIN":[66,5,1,1319],"COLIMEX":[122,5,2,1320],"ROCLAV":[55,5,2,1321],"VENTRYL":[78,5,2,1322],
  "ZEAL SYRUP":[56,5,2,1323],"MAXTRA":[89,5,2,1324],"HICET":[130,5,3,1325],"MEFAST 100":[100,5,3,1326],
  "COLISPAS":[90,5,3,1327],"CIPROFLOXACIN":[112,5,3,1328],"OFLOXACIN":[89,5,3,1329],"AUGEMENTIN":[132,5,4,1330],
  "ZYTEE":[44,5,4,1331],"OTRIVIN":[88,5,4,1332],"SENSUR":[90,5,4,1333],"VICKS":[133,5,4,1334]
}

# ---------- DB ----------
def connect_no_db():
    cfg = dict(DB_CONFIG)
    cfg.pop("database", None)
    return mysql.connect(**cfg)

def connect_db():
    return mysql.connect(**DB_CONFIG)

def _column_exists(cur, table_name: str, col_name: str) -> bool:
    cur.execute(
        """
        SELECT 1
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s
        LIMIT 1
        """,
        (DB_CONFIG["database"], table_name, col_name),
    )
    return cur.fetchone() is not None

def ensure_database_and_tables():
    try:
        cn = connect_no_db()
        cur = cn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}`")
        cur.close()
        cn.close()

        cn = connect_db()
        cur = cn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS medicines (
                name VARCHAR(64) PRIMARY KEY,
                price INT NOT NULL,
                box_no INT NOT NULL,
                shelf_no INT NOT NULL,
                batch_no INT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                created_at DATETIME NOT NULL,
                patient_name VARCHAR(64) NOT NULL,
                mobile VARCHAR(20) NOT NULL,
                address VARCHAR(128) NOT NULL,
                city VARCHAR(64) NOT NULL,
                state VARCHAR(64) NOT NULL,
                pincode VARCHAR(12) NOT NULL,
                delivery_fee INT NOT NULL,
                total_medicines INT NOT NULL,
                grand_total INT NOT NULL
            )
        """)
        # create minimal (old) + migrate forward
        cur.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                medicine_name VARCHAR(64) NOT NULL,
                batch_no INT NOT NULL,
                price INT NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
            )
        """)

        if not _column_exists(cur, "order_items", "qty"):
            cur.execute("ALTER TABLE order_items ADD COLUMN qty INT NOT NULL DEFAULT 1")
        if not _column_exists(cur, "order_items", "line_total"):
            cur.execute("ALTER TABLE order_items ADD COLUMN line_total INT NOT NULL DEFAULT 0")

        cur.execute("UPDATE order_items SET line_total = price * qty WHERE line_total = 0")

        seed_sql = """
            INSERT INTO medicines (name, price, box_no, shelf_no, batch_no)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                price = VALUES(price),
                box_no = VALUES(box_no),
                shelf_no = VALUES(shelf_no),
                batch_no = VALUES(batch_no)
        """
        for name, vals in d.items():
            price, box_no, shelf_no, batch_no = vals
            cur.execute(seed_sql, (name, int(price), int(box_no), int(shelf_no), int(batch_no)))

        cn.commit()
        cur.close()
        cn.close()

    except Error as e:
        messagebox.showerror("Database Error", f"{e}")

# ---------- UI HELPERS ----------
def label(parent, text):
    return tk.Label(parent, text=text, font=("Arial Black", 11),
                    bg=THEME["label_bg"], fg=THEME["label_fg"], padx=10, pady=7)

def entry(parent):
    return tk.Entry(parent, font=("Arial", 13), bd=3, relief="sunken",
                    bg=THEME["entry_bg"], fg=THEME["entry_fg"],
                    insertbackground=THEME["entry_insert"])

def output_text(parent, height=14, width=70):
    t = tk.Text(parent, height=height, width=width, bd=3, relief="sunken", wrap="word",
                bg=THEME["text_bg"], fg=THEME["text_fg"],
                insertbackground=THEME["text_insert"])
    t.configure(state="disabled")
    return t

def set_text(widget: tk.Text, msg: str):
    widget.configure(state="normal")
    widget.delete("1.0", tk.END)
    widget.insert(tk.END, msg)
    widget.configure(state="disabled")

def sub_button(parent, text, command, width=12):
    return tk.Button(
        parent, text=text, command=command,
        bg=THEME["btn_bg"], fg=THEME["btn_fg"],
        activebackground=THEME["btn_active_bg"],
        activeforeground=THEME["btn_active_fg"],
        font=("Arial Black", 11), bd=4, relief="raised",
        width=width, pady=10
    )

def menu_tile(parent, text, command, width_px=520, height_px=70):
    tile = tk.Frame(parent, bg=THEME["main_tile_bg"], highlightthickness=2,
                    highlightbackground="#000000")
    tile.pack_propagate(False)
    tile.configure(width=width_px, height=height_px)

    lbl = tk.Label(tile, text=text, bg=THEME["main_tile_bg"], fg=THEME["main_tile_fg"],
                   font=("Arial Black", 14))
    lbl.pack(expand=True, fill="both")

    def set_bg(color):
        tile.configure(bg=color)
        lbl.configure(bg=color)

    def on_enter(_): set_bg(THEME["main_tile_hover"])
    def on_leave(_): set_bg(THEME["main_tile_bg"])
    def on_press(_): set_bg(THEME["main_tile_press"])
    def on_release(_):
        set_bg(THEME["main_tile_hover"])
        command()

    for w in (tile, lbl):
        w.bind("<Enter>", on_enter)
        w.bind("<Leave>", on_leave)
        w.bind("<ButtonPress-1>", on_press)
        w.bind("<ButtonRelease-1>", on_release)
        w.configure(cursor="hand2")

    return tile

# ---------- WINDOWS ----------
def open_search_window(root):
    w = tk.Toplevel(root)
    w.title("SEARCH FOR PRODUCTS")
    w.geometry("980x520")
    w.configure(bg=THEME["window_bg"])

    container = tk.Frame(w, bg=THEME["window_bg"])
    container.pack(fill="both", expand=True, padx=18, pady=18)
    container.grid_columnconfigure(1, weight=1)
    container.grid_rowconfigure(1, weight=1)

    label(container, "ENTER MEDICINE NAME").grid(row=0, column=0, sticky="w", padx=(0, 12), pady=(0, 10))
    e = entry(container)
    e.grid(row=0, column=1, sticky="we", pady=(0, 10))

    out = output_text(container, height=18, width=80)
    out.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))

    side = tk.Frame(container, bg=THEME["window_bg"])
    side.grid(row=0, column=2, rowspan=2, sticky="ne", padx=(14, 0))

    def do_search():
        name = e.get().strip().upper()
        if not name:
            set_text(out, "Please enter a medicine name.")
            return
        try:
            cn = connect_db()
            cur = cn.cursor()
            cur.execute("SELECT price, box_no, shelf_no, batch_no FROM medicines WHERE name=%s", (name,))
            row = cur.fetchone()
            cur.close()
            cn.close()

            if row:
                price, box_no, shelf_no, batch_no = row
                msg = (f"{name} is AVAILABLE\n\n"
                       f"Price: {price}\nShelf No: {shelf_no}\nBox No: {box_no}\nBatch No: {batch_no}")
            else:
                msg = f"{name} IS NOT AVAILABLE"
            set_text(out, msg)
        except Error as ex:
            set_text(out, f"MySQL error:\n{ex}")

    sub_button(side, "SEARCH", do_search).pack(pady=(0, 14))
    sub_button(side, "CLOSE", w.destroy).pack()

def open_order_txt_window(root):
    w = tk.Toplevel(root)
    w.title("ORDER PRODUCTS (Order.txt)")
    w.geometry("980x520")
    w.configure(bg=THEME["window_bg"])

    container = tk.Frame(w, bg=THEME["window_bg"])
    container.pack(fill="both", expand=True, padx=18, pady=18)
    container.grid_columnconfigure(1, weight=1)
    container.grid_rowconfigure(1, weight=1)

    label(container, "ENTER MEDICINE NAME").grid(row=0, column=0, sticky="w", padx=(0, 12), pady=(0, 10))
    e = entry(container)
    e.grid(row=0, column=1, sticky="we", pady=(0, 10))

    out = output_text(container, height=18, width=80)
    out.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))

    side = tk.Frame(container, bg=THEME["window_bg"])
    side.grid(row=0, column=2, rowspan=2, sticky="ne", padx=(14, 0))

    def add_to_file():
        name = e.get().strip().upper()
        if not name:
            set_text(out, "Please enter a medicine name.")
            return

        try:
            cn = connect_db()
            cur = cn.cursor()
            cur.execute("SELECT 1 FROM medicines WHERE name=%s", (name,))
            ok = cur.fetchone() is not None
            cur.close()
            cn.close()
        except Error:
            ok = name in d

        if not ok:
            set_text(out, f"{name} is not available (cannot add).")
            return

        ORDER_TXT.touch(exist_ok=True)
        with ORDER_TXT.open("a", encoding="utf-8") as f:
            f.write(name + "\n")
        set_text(out, f"Added to Order.txt:\n\n{name}")

    sub_button(side, "ADD", add_to_file).pack(pady=(0, 14))
    sub_button(side, "CLOSE", w.destroy).pack()

def show_order_list(root):
    w = tk.Toplevel(root)
    w.title("SHOW ORDER LIST (Order.txt)")
    w.geometry("900x620")
    w.configure(bg=THEME["window_bg"])

    frame = tk.Frame(w, bg=THEME["window_bg"])
    frame.pack(fill="both", expand=True, padx=18, pady=18)

    txt = tk.Text(frame, bd=3, relief="sunken", wrap="word",
                  bg=THEME["text_bg"], fg=THEME["text_fg"], insertbackground=THEME["text_insert"])
    txt.pack(fill="both", expand=True)

    def load_lines():
        if not ORDER_TXT.exists():
            return []
        with ORDER_TXT.open("r", encoding="utf-8") as f:
            return [x.strip() for x in f.readlines() if x.strip()]

    def refresh_view():
        lines = load_lines()
        txt.delete("1.0", tk.END)
        if not lines:
            txt.insert(tk.END, "Order.txt is empty (or not found).")
        else:
            txt.insert(tk.END, "Medicines in Order.txt:\n\n")
            for i, med in enumerate(lines, start=1):
                txt.insert(tk.END, f"{i}. {med}\n")

    def clear_order_file():
        if not ORDER_TXT.exists() or ORDER_TXT.stat().st_size == 0:
            messagebox.showinfo("Clear Order List", "Order.txt is already empty.")
            return
        ok = messagebox.askyesno("Confirm", "Clear Order.txt completely?")
        if not ok:
            return
        ORDER_TXT.write_text("", encoding="utf-8")
        refresh_view()
        messagebox.showinfo("Done", "Order.txt cleared.")

    btns = tk.Frame(frame, bg=THEME["window_bg"])
    btns.pack(fill="x", pady=14)

    sub_button(btns, "REFRESH", refresh_view, width=12).pack(side="left", padx=6)
    sub_button(btns, "CLEAR", clear_order_file, width=12).pack(side="left", padx=6)
    sub_button(btns, "CLOSE", w.destroy, width=12).pack(side="right", padx=6)

    refresh_view()

def _format_invoice(order: dict, items: list[dict]) -> str:
    lines = []
    lines.append("=========== INVOICE ===========\n")
    lines.append(f"Order ID: {order['id']}")
    lines.append(f"Date/Time: {order['created_at']}\n")
    lines.append(f"Patient: {order['patient_name']}")
    lines.append(f"Mobile: {order['mobile']}")
    lines.append(f"Address: {order['address']}, {order['city']}, {order['state']} - {order['pincode']}\n")
    lines.append("Items:")
    lines.append("-" * 60)
    for idx, it in enumerate(items, start=1):
        lines.append(
            f"{idx}. {it['medicine_name']} | Qty: {it['qty']} | Batch: {it['batch_no']} | "
            f"Unit: {it['price']} | Line: {it['line_total']}"
        )
    lines.append("-" * 60)
    lines.append(f"\nMedicines Total: {order['total_medicines']}")
    lines.append(f"Delivery Fee: {order['delivery_fee']}")
    lines.append(f"Grand Total: {order['grand_total']}")
    return "\n".join(lines)

def open_invoice_window(root):
    w = tk.Toplevel(root)
    w.title("PRINT INVOICE (DB Orders)")
    w.geometry("1100x700")
    w.configure(bg=THEME["window_bg"])

    frame = tk.Frame(w, bg=THEME["window_bg"])
    frame.pack(fill="both", expand=True, padx=18, pady=18)

    # TOP BAR: dropdown + buttons
    top = tk.Frame(frame, bg=THEME["window_bg"])
    top.pack(fill="x", pady=(0, 12))

    label(top, "SELECT ORDER").pack(side="left", padx=(0, 10))

    order_var = tk.StringVar(value="")

    order_menu = tk.OptionMenu(top, order_var, "")
    order_menu.config(font=("Arial", 12))
    order_menu.pack(side="left")

    txt = tk.Text(frame, bd=3, relief="sunken", wrap="word",
                  bg=THEME["text_bg"], fg=THEME["text_fg"], insertbackground=THEME["text_insert"])
    txt.pack(fill="both", expand=True)

    def _set_text(msg: str):
        txt.delete("1.0", tk.END)
        txt.insert(tk.END, msg)

    def refresh_orders_dropdown():
        try:
            cn = connect_db()
            cur = cn.cursor(dictionary=True)
            cur.execute("""
                SELECT id, created_at, patient_name, grand_total
                FROM orders
                ORDER BY id DESC
                LIMIT 20
            """)
            rows = cur.fetchall()
            cur.close()
            cn.close()

            menu = order_menu["menu"]
            menu.delete(0, "end")

            if not rows:
                order_var.set("")
                menu.add_command(label="(No orders)", command=lambda: order_var.set(""))
                _set_text("No orders found.\n\nPlace a HOME DELIVERY order first.")
                return

            # build labels like: "ID 12 | Ishu | 2026-01-07 21:27 | ₹1600"
            options = []
            for r in rows:
                label_txt = f"ID {r['id']} | {r['patient_name']} | {r['created_at']} | Total {r['grand_total']}"
                options.append((label_txt, r["id"]))

            def make_cmd(val):
                return lambda: order_var.set(val)

            for lbl, oid in options:
                menu.add_command(label=lbl, command=make_cmd(str(oid)))

            # default selection = latest id
            order_var.set(str(rows[0]["id"]))

        except Error as ex:
            _set_text(f"MySQL error:\n{ex}")

    def load_invoice(order_id: int):
        try:
            cn = connect_db()
            cur = cn.cursor(dictionary=True)

            cur.execute("SELECT * FROM orders WHERE id=%s", (order_id,))
            order = cur.fetchone()
            if not order:
                _set_text("Order not found.")
                cur.close()
                cn.close()
                return

            cur.execute("""
                SELECT medicine_name, batch_no, price, qty, line_total
                FROM order_items
                WHERE order_id=%s
                ORDER BY id ASC
            """, (order_id,))
            items = cur.fetchall()

            cur.close()
            cn.close()

            _set_text(_format_invoice(order, items))

        except Error as ex:
            _set_text(f"MySQL error:\n{ex}")

    def load_selected():
        v = order_var.get().strip()
        if not v:
            _set_text("No order selected.")
            return
        try:
            load_invoice(int(v))
        except ValueError:
            _set_text("Invalid order selection.")

    def load_last():
        try:
            cn = connect_db()
            cur = cn.cursor()
            cur.execute("SELECT id FROM orders ORDER BY id DESC LIMIT 1")
            row = cur.fetchone()
            cur.close()
            cn.close()
            if not row:
                _set_text("No orders found.")
                return
            order_var.set(str(row[0]))
            load_invoice(int(row[0]))
        except Error as ex:
            _set_text(f"MySQL error:\n{ex}")

    # Buttons
    sub_button(top, "REFRESH LIST", refresh_orders_dropdown, width=14).pack(side="left", padx=10)
    sub_button(top, "LOAD SELECTED", load_selected, width=14).pack(side="left", padx=10)
    sub_button(top, "LOAD LAST", load_last, width=12).pack(side="left", padx=10)
    sub_button(top, "CLOSE", w.destroy, width=10).pack(side="right", padx=10)

    refresh_orders_dropdown()
    load_last()

def open_home_delivery_window(root):

    w = tk.Toplevel(root)
    w.title("HOME DELIVERY")
    w.geometry("1200x680")
    w.configure(bg=THEME["window_bg"])

    cart = {}

    outer = tk.Frame(w, bg=THEME["window_bg"])
    outer.pack(fill="both", expand=True, padx=18, pady=18)

    # Two columns: left form, right display
    outer.grid_columnconfigure(0, weight=1)
    outer.grid_columnconfigure(1, weight=2)
    outer.grid_rowconfigure(0, weight=1)
    outer.grid_rowconfigure(1, weight=0)

    left = tk.Frame(outer, bg=THEME["window_bg"])
    left.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
    left.grid_columnconfigure(0, weight=0)
    left.grid_columnconfigure(1, weight=1)

    right = tk.Frame(outer, bg=THEME["window_bg"])
    right.grid(row=0, column=1, sticky="nsew")
    right.grid_columnconfigure(0, weight=1)
    right.grid_rowconfigure(1, weight=1)
    right.grid_rowconfigure(2, weight=2)

    # ----- LEFT FORM (aligned grid) -----
    def make_row(r, title):
        label(left, title).grid(row=r, column=0, sticky="w", pady=8, padx=(0, 10))
        e = entry(left)
        e.grid(row=r, column=1, sticky="ew", pady=8)
        return e

    e_med = make_row(0, "MEDICINE NAME")

    label(left, "QUANTITY").grid(row=1, column=0, sticky="w", pady=8, padx=(0, 10))
    qty_var = tk.StringVar(value="1")
    sp_qty = tk.Spinbox(left, from_=1, to=50, textvariable=qty_var,
                        font=("Arial", 13), bd=3, relief="sunken",
                        bg=THEME["entry_bg"], fg=THEME["entry_fg"], width=8)
    sp_qty.grid(row=1, column=1, sticky="w", pady=8)

    e_name = make_row(2, "PATIENT NAME")
    e_mobile = make_row(3, "MOBILE NUMBER")
    e_addr = make_row(4, "ADDRESS")
    e_city = make_row(5, "CITY")
    e_state = make_row(6, "STATE")
    e_pin = make_row(7, "PINCODE")

    # ----- RIGHT PANEL -----
    label(right, "CART").grid(row=0, column=0, sticky="w")
    cart_box = tk.Listbox(right, height=10, bd=3, relief="sunken",
                          bg=THEME["entry_bg"], fg=THEME["entry_fg"])
    cart_box.grid(row=1, column=0, sticky="nsew", pady=(6, 12))

    out = output_text(right, height=12, width=70)
    out.grid(row=2, column=0, sticky="nsew")

    def fetch_medicine(cur, med_name: str):
        cur.execute("SELECT price, batch_no FROM medicines WHERE name=%s", (med_name,))
        return cur.fetchone()

    def refresh_cart():
        cart_box.delete(0, tk.END)
        total = 0
        try:
            cn = connect_db()
            cur = cn.cursor()
            for med, q in sorted(cart.items()):
                row = fetch_medicine(cur, med)
                if not row:
                    continue
                price, _batch = row
                line = int(price) * int(q)
                total += line
                cart_box.insert(tk.END, f"{med}  | qty: {q}  | unit: {price}  | line: {line}")
            cur.close()
            cn.close()
        except Error:
            pass

        grand = total + (DELIVERY_FEE if total > 0 else 0)
        set_text(out, f"Cart total: {total}\nDelivery fee: {DELIVERY_FEE if total>0 else 0}\nGrand total: {grand}")

    def add_med():
        name = e_med.get().strip().upper()
        if not name:
            set_text(out, "Enter a medicine name.")
            return
        try:
            qty = int(qty_var.get().strip())
            if qty <= 0:
                raise ValueError
        except ValueError:
            set_text(out, "Quantity must be a positive integer.")
            return

        try:
            cn = connect_db()
            cur = cn.cursor()
            row = fetch_medicine(cur, name)
            cur.close()
            cn.close()
            if not row:
                set_text(out, f"{name} is not available.")
                return
        except Error as ex:
            set_text(out, f"MySQL error:\n{ex}")
            return

        cart[name] = cart.get(name, 0) + qty
        refresh_cart()

    def delete_med():
        name = e_med.get().strip().upper()
        if not name:
            set_text(out, "Enter medicine name to delete.")
            return
        if name not in cart:
            set_text(out, f"{name} is not in cart.")
            return
        try:
            qty = int(qty_var.get().strip())
            if qty <= 0:
                raise ValueError
        except ValueError:
            qty = 1
        new_qty = cart[name] - qty
        if new_qty <= 0:
            del cart[name]
        else:
            cart[name] = new_qty
        refresh_cart()

    def clear_cart():
        if not cart:
            return
        if messagebox.askyesno("Confirm", "Clear the cart?"):
            cart.clear()
            refresh_cart()

    def valid_mobile(m: str) -> bool:
        m = m.strip()
        return m.isdigit() and len(m) == 10

    def valid_pincode(p: str) -> bool:
        p = p.strip()
        return p.isdigit() and len(p) == 6

    def place_order():
        if not cart:
            set_text(out, "Cart is empty. Add medicines first.")
            return

        patient_name = e_name.get().strip()
        mobile = e_mobile.get().strip()
        address = e_addr.get().strip()
        city = e_city.get().strip()
        state = e_state.get().strip()
        pincode = e_pin.get().strip()

        if not all([patient_name, mobile, address, city, state, pincode]):
            set_text(out, "Fill all customer details.")
            return
        if not valid_mobile(mobile):
            set_text(out, "Mobile number must be exactly 10 digits.")
            return
        if not valid_pincode(pincode):
            set_text(out, "Pincode must be exactly 6 digits.")
            return

        try:
            cn = connect_db()
            cur = cn.cursor()

            total_meds = 0
            items = []
            for med, qty in cart.items():
                row = fetch_medicine(cur, med)
                if not row:
                    raise ValueError(f"Medicine not found in DB: {med}")
                price, batch_no = row
                price = int(price)
                batch_no = int(batch_no)
                qty = int(qty)
                line_total = price * qty
                total_meds += line_total
                items.append((med, batch_no, price, qty, line_total))

            grand_total = total_meds + DELIVERY_FEE

            cur.execute("""
                INSERT INTO orders
                (created_at, patient_name, mobile, address, city, state, pincode,
                 delivery_fee, total_medicines, grand_total)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (datetime.now(), patient_name, mobile, address, city, state, pincode,
                  DELIVERY_FEE, total_meds, grand_total))
            order_id = cur.lastrowid

            cur.executemany("""
                INSERT INTO order_items (order_id, medicine_name, batch_no, price, qty, line_total)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [(order_id, med, batch, price, qty, line_total) for (med, batch, price, qty, line_total) in items])

            cn.commit()
            cur.close()
            cn.close()

            cart.clear()
            refresh_cart()
            set_text(out,
                     f"ORDER PLACED SUCCESSFULLY\n\n"
                     f"Order ID: {order_id}\n"
                     f"Medicines total: {total_meds}\n"
                     f"Delivery fee: {DELIVERY_FEE}\n"
                     f"Grand total: {grand_total}\n\n"
                     f"Now use PRINT INVOICE to see it.")

        except (Error, ValueError) as ex:
            set_text(out, f"Could not place order:\n{ex}")

    # ----- Bottom Buttons Row (aligned) -----
    btn_row = tk.Frame(outer, bg=THEME["window_bg"])
    btn_row.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(16, 0))
    btn_row.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

    sub_button(btn_row, "ADD", add_med, width=12).grid(row=0, column=0, padx=8, sticky="ew")
    sub_button(btn_row, "DELETE", delete_med, width=12).grid(row=0, column=1, padx=8, sticky="ew")
    sub_button(btn_row, "CLEAR CART", clear_cart, width=12).grid(row=0, column=2, padx=8, sticky="ew")
    sub_button(btn_row, "PLACE ORDER", place_order, width=14).grid(row=0, column=3, padx=8, sticky="ew")
    sub_button(btn_row, "CLOSE", w.destroy, width=12).grid(row=0, column=4, padx=8, sticky="ew")

    refresh_cart()

# ---------- MAIN ----------
def main():
    root = tk.Tk()
    root.title("PHARMACY_MANAGEMENT")
    root.geometry("750x720")
    root.configure(bg=THEME["main_bg"])

    ensure_database_and_tables()

    header = tk.Label(root, text="HELLO  WELCOME TO PHARMACY MANAGEMENT",
                      fg=THEME["header_fg"], bg=THEME["header_bg"], font=("Arial Black", 16))
    header.pack(fill="x")

    panel = tk.Frame(root, bg=THEME["main_bg"])
    panel.pack(expand=True)

    menu_tile(panel, "SEARCH FOR PRODUCTS", lambda: open_search_window(root)).pack(pady=14)
    menu_tile(panel, "ORDER PRODUCTS", lambda: open_order_txt_window(root)).pack(pady=14)
    menu_tile(panel, "SHOW ORDER LIST", lambda: show_order_list(root)).pack(pady=14)
    menu_tile(panel, "PRINT INVOICE", lambda: open_invoice_window(root)).pack(pady=14)
    menu_tile(panel, "HOME DELIVERY", lambda: open_home_delivery_window(root)).pack(pady=14)
    menu_tile(panel, "EXIT", root.destroy).pack(pady=22)

    root.mainloop()

if __name__ == "__main__":
    main()