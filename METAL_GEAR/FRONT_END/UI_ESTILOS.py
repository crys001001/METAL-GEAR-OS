from tkinter import ttk

def aplicar_tema_tabela():
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="#2B2B2B", foreground="white", fieldbackground="#2B2B2B", borderwidth=0, rowheight=30)
    style.map('Treeview', background=[('selected', '#3A7EB8')])
    style.configure("Treeview.Heading", background="#1E1E1E", foreground="white", font=("Arial", 11, "bold"), borderwidth=0)
    style.map("Treeview.Heading", background=[('active', '#2B2B2B')])

MENU_PRODUTOS = {
    "font": ("Arial", 14, "bold"), "dropdown_font": ("Arial", 13, "bold"),
    "fg_color": "#1F538D", "button_color": "#14375E", "button_hover_color": "#1E4470",     
    "dropdown_fg_color": "#2B2B2B", "dropdown_hover_color": "#3A7EB8",   
    "dropdown_text_color": "white", "text_color": "white", "anchor": "center"                   
}

MENU_RELATORIO = {
    "font": ("Arial", 14, "bold"), "dropdown_font": ("Arial", 13, "bold"),
    "fg_color": "#2B2B2B", "border_color": "#3A7EB8", "border_width": 2,                   
    "button_color": "#3A7EB8", "button_hover_color": "#1E4470",     
    "dropdown_fg_color": "#2B2B2B", "dropdown_hover_color": "#3A7EB8",   
    "dropdown_text_color": "white", "text_color": "white", "state": "readonly", "justify": "center"                  
}

CHECKBOX = {
    "font": ("Arial", 14, "bold"),
    "checkbox_width": 26,
    "checkbox_height": 26,
    "border_width": 2,
    "corner_radius": 6
}