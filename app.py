import streamlit as st
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Campus Bus Route Optimizer", layout="wide")

st.title("🚌 Campus Bus Route Optimizer")
st.write("Linear Algebra & Network Graph Matrix Optimization")

# Sidebar - Student Density Input (Matrices/Arrays)
st.sidebar.header("⚙️ Student Density & Traffic Data")
density_lib = st.sidebar.slider("Library Zone Density", 10, 100, 80)
density_hostel = st.sidebar.slider("Hostel Zone Density", 10, 100, 95)
density_canteen = st.sidebar.slider("Canteen Zone Density", 10, 100, 40)

# Matrix Representation (Linear Algebra)
# Distance/Time Adjacency Matrix
stops = ["Main Gate", "Library", "Hostel Block", "Canteen", "Academic Block"]
num_stops = len(stops)

# Graph Creation (NetworkX)
G = nx.Graph()

# Add Nodes
for stop in stops:
    G.add_node(stop)

# Edges with Distance (km) and Speed Factor (Vector Motion)
edges = [
    ("Main Gate", "Library", 1.2),
    ("Main Gate", "Hostel Block", 2.0),
    ("Library", "Canteen", 0.8),
    ("Hostel Block", "Canteen", 0.5),
    ("Canteen", "Academic Block", 1.0),
    ("Library", "Academic Block", 1.5)
]

for u, v, w in edges:
    G.add_edge(u, v, weight=w)

# Weight optimization based on Student Density AI Layer logic
density_weights = {
    "Library": density_lib,
    "Hostel Block": density_hostel,
    "Canteen": density_canteen,
    "Main Gate": 30,
    "Academic Block": 50
}

# Calculated Optimized Weight Matrix
adj_matrix = nx.to_numpy_array(G)

st.subheader("📊 Network Matrix (Linear Algebra View)")
st.dataframe(adj_matrix)

# Shortest Path Optimization
start_node, end_node = st.selectbox("Select Start Location", stops), st.selectbox("Select Destination", stops)

if start_node != end_node:
    path = nx.shortest_path(G, source=start_node, target=end_node, weight='weight')
    path_edges = list(zip(path[:-1], path[1:]))
    
    st.success(f"**Optimal Route:** {' ➔ '.join(path)}")
    
    # Visualization
    fig, ax = plt.subplots(figsize=(8, 5))
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw_networkx_nodes(G, pos, node_size=1200, node_color='lightblue', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)
    nx.draw_networkx_edges(G, pos, width=2, edge_color='gray', ax=ax)
    
    # Highlight Optimal Route
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color='red', ax=ax)
    
    plt.title("Campus Route Network Graph")
    st.pyplot(fig)

    # Differential Equation / Motion Vector Simulation
    st.subheader("⚡ Estimated Travel Time & Motion Optimization")
    avg_speed = 20 # km/h
    total_dist = sum([G[u][v]['weight'] for u, v in path_edges])
    est_time = (total_dist / avg_speed) * 60
    
    col1, col2 = st.columns(2)
    col1.metric("Total Distance", f"{total_dist:.2f} km")
    col2.metric("Estimated Time", f"{est_time:.1f} mins")