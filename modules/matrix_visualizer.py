import seaborn as sns
import networkx as nx
import json
import os
from matplotlib import font_manager as fm
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib.pyplot as plt
class MatrixVisualizer:
    def __init__(self, config):
        self.config = config
        os.makedirs("output", exist_ok=True)
        self.font_path = self._find_best_arabic_font()
        self.font_prop = fm.FontProperties(fname=self.font_path) if self.font_path else None
        if self.font_prop:
            plt.rcParams['font.family'] = self.font_prop.get_name()

    def _find_best_arabic_font(self):
        font_candidates = [
            'Amiri-Regular.ttf',
            'NotoNaskhArabic-Regular.ttf',
            'arial.ttf',
            'tahoma.ttf',
            'me_quran.ttf',
            'Simplified Arabic.ttf'
        ]
        for font in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
            font_name = os.path.basename(font).lower()
            if any(candidate.lower() in font_name for candidate in font_candidates):
                return font
        for file in font_candidates:
            if os.path.exists(file):
                return file
        print("⚠️ Arabic font not found. Warnings may occur.")
        return None

    def _load_matrix(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _reshape(self, text):
        return get_display(arabic_reshaper.reshape(text))

    def _create_data_matrix(self, matrix, all_prefixes=None):
        if not all_prefixes:
            all_prefixes = list(matrix.keys())

        all_targets = sorted({c for prefix in matrix for c in matrix[prefix].keys()})
        data = []
        for prefix in all_prefixes:
            row = [matrix.get(prefix, {}).get(t, 0.0) for t in all_targets]
            data.append(row)
        return np.array(data), all_prefixes, all_targets

    def plot_char_heatmap(self):
        try:
            matrix = self._load_matrix(self.config["char_matrix_file"])
            all_prefixes = list(matrix.keys())
            data, y_labels, x_labels = self._create_data_matrix(matrix, all_prefixes)

            reshaped_y = [self._reshape(label) for label in y_labels]
            reshaped_x = [self._reshape(label) for label in x_labels]

            mask = np.isclose(data, 0.0)
            annot_data = np.where(mask, "", data.astype(str))

            plt.figure(figsize=(max(10, len(x_labels)//2), max(10, len(y_labels)//2)))
            ax = sns.heatmap(
                data,
                xticklabels=reshaped_x,
                yticklabels=reshaped_y,
                cmap='YlOrRd',
                annot=annot_data,
                fmt='',
                linewidths=.5,
                linecolor='lightgray'
            )
            if self.font_prop:
                for label in ax.get_xticklabels():
                    label.set_fontproperties(self.font_prop)
                for label in ax.get_yticklabels():
                    label.set_fontproperties(self.font_prop)
            plt.title(self._reshape("مصفوفة انتقال الأحرف"), fontproperties=self.font_prop)
            plt.xlabel(self._reshape("الحرف التالي"), fontproperties=self.font_prop)
            plt.ylabel(self._reshape("الحرف الحالي"), fontproperties=self.font_prop)
            plt.tight_layout()
            plt.savefig("output/char_heatmap.png", dpi=300, bbox_inches='tight')
            plt.close()
            print("✅ Saved: output/char_heatmap.png")
        except Exception as e:
            print(f"❌ Failed to generate char heatmap: {e}")

    def _plot_graph(self, matrix_file, output_path, title, max_nodes=None):
        try:
            matrix = self._load_matrix(matrix_file)
            G = nx.DiGraph()

            # Use all nodes
            for src in matrix:
                for tgt, weight in matrix[src].items():
                    if weight > 0:
                        G.add_edge(self._reshape(src), self._reshape(tgt), weight=weight)

            plt.figure(figsize=(24, 18))
            pos = nx.spring_layout(G, k=0.9, seed=42)

            nx.draw_networkx_edges(G, pos, width=1.5, edge_color='gray')
            nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='skyblue')

            nx.draw_networkx_labels(G, pos, font_size=10, font_family=self.font_prop.get_name() if self.font_prop else None)

            plt.title(self._reshape(title), fontproperties=self.font_prop)
            plt.axis('off')
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"✅ Saved: {output_path}")
        except Exception as e:
            print(f"❌ Failed to generate {title}: {e}")

    def plot_char_graph(self):
        self._plot_graph(
            matrix_file=self.config["char_matrix_file"],
            output_path="output/char_transition_graph.png",
            title="مخطط انتقال الأحرف"
        )

    def plot_word_graph(self):
        self._plot_graph(
            matrix_file=self.config["word_matrix_file"],
            output_path="output/word_transition_graph.png",
            title="مخطط انتقال الكلمات"
        )

    def generate_all(self):
        self.plot_word_graph()
        self.plot_char_graph()
        self.plot_char_heatmap()