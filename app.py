from flask import Flask, render_template, request, jsonify
import osmnx as ox
import networkx as nx

app = Flask(__name__)

# Function to calculate the shortest path
def calculate_shortest_path(origin_lat, origin_lon, dest_lat, dest_lon):
    # Download the graph for Bengaluru, India (driving network)
    G = ox.graph_from_place('Bengaluru, India', network_type='drive')

    # Get the nearest network nodes to the origin and destination coordinates
    origin_node = ox.distance.nearest_nodes(G, X=origin_lon, Y=origin_lat)
    dest_node = ox.distance.nearest_nodes(G, X=dest_lon, Y=dest_lat)

    # Debugging: print nodes for origin and destination
    print(f"Origin Node: {origin_node}, Destination Node: {dest_node}")
    
    # Calculate the shortest path using Dijkstra's algorithm
    try:
        route = nx.shortest_path(G, origin_node, dest_node, weight='length')
    except nx.NetworkXNoPath:
        print("No path found between origin and destination.")
        return []

    # Debugging: check route
    print(f"Route: {route}")

    # Get the latitude and longitude of the route
    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
    return route_coords

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_route', methods=['POST'])
def get_route():
    try:
        # Get the coordinates from the form input
        origin_lat = float(request.form['origin_lat'])
        origin_lon = float(request.form['origin_lon'])
        dest_lat = float(request.form['dest_lat'])
        dest_lon = float(request.form['dest_lon'])

        # Debugging: print inputs
        print(f"Origin: {origin_lat}, {origin_lon}, Destination: {dest_lat}, {dest_lon}")

        # Calculate the route coordinates
        route_coords = calculate_shortest_path(origin_lat, origin_lon, dest_lat, dest_lon)

        # Debugging: check if route_coords is empty
        print(f"Route Coordinates: {route_coords}")

        if not route_coords:
            return jsonify({"error": "No valid route found"})

        # Return the route coordinates as JSON
        return jsonify(route_coords=route_coords)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Invalid input data or unable to compute route."})

if __name__ == '__main__':
    app.run(debug=True)
