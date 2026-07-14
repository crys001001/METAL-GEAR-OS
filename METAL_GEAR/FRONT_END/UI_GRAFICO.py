from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class GraficoProducao:
    def __init__(self, frame_pai):
        self.fig, self.ax = plt.subplots(figsize=(4.2, 1.28), facecolor="#11141B")
        self.ax.set_facecolor("#11141B")
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_pai)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.atualizar(0, 0)

    def atualizar(self, aprovados, rejeitados):
        self.ax.clear()
        self.ax.set_facecolor("#11141B")

        if aprovados == 0 and rejeitados == 0:
            self.ax.text(
                0.5,
                0.5,
                "AGUARDANDO REGISTROS",
                color="#98A2B3",
                ha="center",
                va="center",
                fontname="Segoe UI",
                fontsize=11,
                fontweight="bold",
            )
            self.ax.axis("off")
        else:
            labels = ["Aprovados", "Rejeitados"]
            valores = [aprovados, rejeitados]
            cores = ["#22C55E", "#F43F5E"]
            barras = self.ax.barh(labels, valores, color=cores, height=0.48)

            self.ax.tick_params(colors="#98A2B3", labelsize=10)
            self.ax.spines["top"].set_visible(False)
            self.ax.spines["right"].set_visible(False)
            self.ax.spines["left"].set_color("#2B3240")
            self.ax.spines["bottom"].set_color("#2B3240")
            self.ax.grid(
                axis="x",
                linestyle="--",
                linewidth=0.7,
                alpha=0.28,
                color="#98A2B3",
            )
            self.ax.set_axisbelow(True)

            maior = max(valores) if valores else 1
            self.ax.set_xlim(0, max(1, maior * 1.18))
            for barra in barras:
                largura = barra.get_width()
                self.ax.text(
                    largura + max(0.08, maior * 0.025),
                    barra.get_y() + barra.get_height() / 2,
                    f"{int(largura)}",
                    va="center",
                    ha="left",
                    color="#F5F7FB",
                    fontsize=11,
                    fontweight="bold",
                )

        self.fig.subplots_adjust(left=0.27, right=0.91, bottom=0.20, top=0.94)
        self.canvas.draw_idle()
