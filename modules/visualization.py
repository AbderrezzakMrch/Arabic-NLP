# visualization.py
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import json
import os
from matplotlib import font_manager as fm

import matplotlib
# Use a font with full Arabic support (ensure it's installed)
matplotlib.rcParams['font.family'] = 'Arial'  # or 'Noto Naskh Arabic', 'Amiri', etc.
import matplotlib.font_manager as fm
for font in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
    if "arab" in font.lower():
        print(font)
class VisualizationGenerator:
    def __init__(self, config):
        self.config = config
        self.word_probs = None
        self.char_probs = None

    def load_data(self):
        """Load the probability matrices"""
        with open(self.config["word_matrix_file"], 'r', encoding='utf-8') as f:
            self.word_probs = json.load(f)
        with open(self.config["char_matrix_file"], 'r', encoding='utf-8') as f:
            self.char_probs = json.load(f)

    def generate_word_transition_graph(self, output_dir="visualizations"):
        """Generate a transition graph for word matrix"""
        if not self.word_probs:
            raise ValueError("Word probabilities not loaded")

        os.makedirs(output_dir, exist_ok=True)

        # Create a sample graph with top connections
        G = nx.DiGraph()
        top_words = sorted(self.word_probs.keys(),
                           key=lambda x: sum(self.word_probs[x].values()),
                           reverse=True)[:20]  # Top 20 words

        for word in top_words:
            for next_word, prob in sorted(self.word_probs[word].items(),
                                          key=lambda x: x[1],
                                          reverse=True)[:3]:  # Top 3 connections
                G.add_edge(word, next_word, weight=prob)

        plt.figure(figsize=(15, 10))
        pos = nx.spring_layout(G, k=0.5)

        # Draw edges with width proportional to weight
        edges = G.edges(data=True)
        widths = [d['weight'] * 5 for (u, v, d) in edges]
        nx.draw_networkx_edges(G, pos, width=widths, edge_color='gray')

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=2000,
                               node_color='skyblue', alpha=0.8)

        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=10,
                                font_weight='bold')

        plt.title("Word Transition Graph (Top Connections)")
        plt.axis('off')
        plt.savefig(f"{output_dir}/word_transition_graph.png")
        plt.close()

    def generate_char_transition_graph(self, output_dir="visualizations"):
        """Generate a transition graph for character matrix"""
        if not self.char_probs:
            raise ValueError("Character probabilities not loaded")

        os.makedirs(output_dir, exist_ok=True)

        # Create a sample graph with top connections
        G = nx.DiGraph()
        top_prefixes = sorted(self.char_probs.keys(),
                              key=lambda x: sum(self.char_probs[x].values()),
                              reverse=True)[:15]  # Top 15 prefixes

        for prefix in top_prefixes:
            for next_char, prob in sorted(self.char_probs[prefix].items(),
                                          key=lambda x: x[1],
                                          reverse=True)[:3]:  # Top 3 connections
                G.add_edge(prefix, prefix + next_char, weight=prob)

        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=0.3)

        # Draw edges
        edges = G.edges(data=True)
        widths = [d['weight'] * 10 for (u, v, d) in edges]
        nx.draw_networkx_edges(G, pos, width=widths, edge_color='gray')

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=1500,
                               node_color='lightgreen', alpha=0.8)

        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=8,
                                font_weight='bold')

        plt.title("Character Transition Graph (Top Connections)")
        plt.axis('off')
        plt.savefig(f"{output_dir}/char_transition_graph.png")
        plt.close()

    def generate_char_heatmap(self, output_dir="visualizations"):
        """Generate a heatmap for character transitions"""
        if not self.char_probs:
            raise ValueError("Character probabilities not loaded")

        os.makedirs(output_dir, exist_ok=True)

        # Select sample prefixes (2-3 characters long)
        sample_prefixes = [p for p in self.char_probs.keys()
                           if 2 <= len(p) <= 3][:10]

        # Get all possible next characters
        all_chars = set()
        for prefix in sample_prefixes:
            all_chars.update(self.char_probs[prefix].keys())
        all_chars = sorted(all_chars)

        # Create probability matrix
        prob_matrix = []
        for prefix in sample_prefixes:
            row = [self.char_probs[prefix].get(char, 0) for char in all_chars]
            prob_matrix.append(row)

        plt.figure(figsize=(12, 6))
        sns.heatmap(prob_matrix,
                    annot=True,
                    fmt='.2f',
                    cmap='YlOrRd',
                    xticklabels=all_chars,
                    yticklabels=sample_prefixes)

        plt.title("Character Transition Probabilities")
        plt.xlabel("Next Character")
        plt.ylabel("Current Prefix")
        plt.tight_layout()
        plt.savefig(f"{output_dir}/char_transition_heatmap.png")
        plt.close()