from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class GraficoProducao:
    def __init__(self, frame_pai):
        self.fig, self.ax = plt.subplots(figsize=(4, 1.8), facecolor="#2B2B2B")
        self.ax.set_facecolor("#2B2B2B")
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_pai)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.atualizar(0, 0)

    def atualizar(self, aprovados, rejeitados):
        self.ax.clear()
        if aprovados == 0 and rejeitados == 0:
            self.ax.text(0.5, 0.5, "Aguardando registros...", color="yellow", ha="center", va="center", fontname="Arial", fontsize=11, fontweight="bold")
            self.ax.axis('off')
        else:
            labels = ['Aprovados', 'Rejeitados']
            valores = [aprovados, rejeitados]
            cores = ['#1A4D2E', '#780000']
            self.ax.axis('on')
            bars = self.ax.barh(labels, valores, color=cores, height=0.5)
            self.ax.tick_params(colors='white', labelsize=10)
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['left'].set_color('white')
            self.ax.spines['bottom'].set_color('white')
            self.ax.grid(axis='x', linestyle='--', alpha=0.3, color='white')
            for bar in bars:
                width = bar.get_width()
                if width > 0:
                    self.ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{int(width)}', va='center', ha='left', color='white', fontweight='bold')
        self.fig.tight_layout()
        self.canvas.draw()