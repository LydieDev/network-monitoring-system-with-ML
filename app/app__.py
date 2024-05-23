from flask import Flask, render_template, Response
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import networkx as nx
import random
from io import BytesIO

app = Flask(__name__)

def generate_protocol_usage_graph():
    # Sample protocol usage data (protocol1, protocol2, usage_count)
    protocol_usage_data = [('TCP', 'HTTP', 20),
                           ('UDP', 'DNS', 15),
                           ('TCP', 'UDP', 10),
                           ('HTTP', 'DNS', 25),
                           ('ICMP', 'UDP', 8)]

    # Create a directed graph to represent protocol usage
    G = nx.DiGraph()

    # Add edges with usage counts
    for protocol1, protocol2, usage_count in protocol_usage_data:
        G.add_edge(protocol1, protocol2, weight=usage_count)

    # Draw the graph using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=10, arrows=True, ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', ax=ax)
    plt.title('Protocol Usage Graph')
    plt.tight_layout()

    return fig

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot.png')
def plot_png():
    fig = generate_protocol_usage_graph()
    output = BytesIO()
    FigureCanvas(fig).print_png(output)
    plt.close(fig)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
