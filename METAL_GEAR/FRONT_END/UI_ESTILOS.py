from tkinter import ttk


# Paleta central — Dark Stylish / Obsidian Violet
CORES = {
    "fundo": "#0B0D12",
    "painel": "#11141B",
    "cartao": "#171B23",
    "cartao_2": "#1D2230",
    "borda": "#2B3240",
    "texto": "#F5F7FB",
    "texto_secundario": "#98A2B3",
    # Mantidos os nomes por compatibilidade com a interface
    "azul": "#8B5CF6",
    "azul_escuro": "#6D28D9",
    "ciano": "#2DD4BF",
    "verde": "#22C55E",
    "verde_escuro": "#14532D",
    "vermelho": "#F43F5E",
    "vermelho_escuro": "#881337",
    "amarelo": "#F59E0B",
    "cinza": "#667085",
}

FONTE = "Segoe UI"


def aplicar_tema_tabela():
    style = ttk.Style()
    style.theme_use("default")

    style.configure(
        "Treeview",
        background=CORES["cartao"],
        foreground=CORES["texto"],
        fieldbackground=CORES["cartao"],
        borderwidth=0,
        rowheight=30,
        font=(FONTE, 11),
    )
    style.map(
        "Treeview",
        background=[("selected", CORES["azul_escuro"])],
        foreground=[("selected", "white")],
    )
    style.configure(
        "Treeview.Heading",
        background=CORES["painel"],
        foreground=CORES["texto_secundario"],
        font=(FONTE, 11, "bold"),
        relief="flat",
        borderwidth=0,
    )
    style.map(
        "Treeview.Heading",
        background=[("active", CORES["cartao_2"])],
    )


MENU_PRODUTOS = {
    "font": (FONTE, 13, "bold"),
    "dropdown_font": (FONTE, 12),
    "fg_color": CORES["cartao_2"],
    "button_color": CORES["azul_escuro"],
    "button_hover_color": CORES["azul"],
    "dropdown_fg_color": CORES["painel"],
    "dropdown_hover_color": CORES["azul_escuro"],
    "dropdown_text_color": CORES["texto"],
    "text_color": CORES["texto"],
    "anchor": "center",
}

MENU_RELATORIO = {
    "font": (FONTE, 13, "bold"),
    "dropdown_font": (FONTE, 12),
    "fg_color": CORES["cartao_2"],
    "border_color": CORES["borda"],
    "border_width": 1,
    "button_color": CORES["azul_escuro"],
    "button_hover_color": CORES["azul"],
    "dropdown_fg_color": CORES["painel"],
    "dropdown_hover_color": CORES["azul_escuro"],
    "dropdown_text_color": CORES["texto"],
    "text_color": CORES["texto"],
    "state": "readonly",
    "justify": "center",
}

CHECKBOX = {
    "font": (FONTE, 12, "bold"),
    "checkbox_width": 21,
    "checkbox_height": 21,
    "border_width": 2,
    "corner_radius": 6,
    "fg_color": CORES["azul"],
    "hover_color": CORES["azul_escuro"],
    "border_color": CORES["cinza"],
}
