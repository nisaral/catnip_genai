import networkx as nx
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(coord1, coord2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    r = 6371000  # Radius of earth in meters
    
    return c * r

def create_india_graph():
    """
    Create a graph representing major Indian cities and their connections
    Coordinates are in (latitude, longitude) format
    """
    G = nx.Graph()
    
    # Define major Indian cities with their coordinates
    locations = {
        "Delhi": (28.6139, 77.2090),
        "Mumbai": (19.0760, 72.8777),
        "Bangalore": (12.9716, 77.5946),
        "Chennai": (13.0827, 80.2707),
        "Kolkata": (22.5726, 88.3639),
        "Hyderabad": (17.3850, 78.4867),
        "Ahmedabad": (23.0225, 72.5714),
        "Pune": (18.5204, 73.8567),
        "Jaipur": (26.9124, 75.7873),
        "Lucknow": (26.8467, 80.9462),
        "Bhopal": (23.2599, 77.4126),
        "Patna": (25.5941, 85.1376),
        "Nagpur": (21.1458, 79.0882),
        "Chandigarh": (30.7333, 76.7794),
        "Kochi": (9.9312, 76.2673),
        "Visakhapatnam": (17.6868, 83.2185),
        "Guwahati": (26.1445, 91.7362),
        "Bhubaneswar": (20.2961, 85.8245),
        "Varanasi": (25.3176, 82.9739),
        "Amritsar": (31.6340, 74.8723)
    }
    
    # Add nodes with position attributes
    for node, coords in locations.items():
        G.add_node(node, pos=coords)
    
    # Define major routes connecting cities
    # These connections roughly follow major highways and railway routes
    routes = [
        # Northern Routes
        ("Delhi", "Chandigarh"), ("Delhi", "Jaipur"), ("Delhi", "Lucknow"),
        ("Chandigarh", "Amritsar"), ("Lucknow", "Varanasi"), ("Lucknow", "Patna"),
        
        # Western Routes
        ("Mumbai", "Pune"), ("Mumbai", "Ahmedabad"), ("Ahmedabad", "Jaipur"),
        
        # Central Routes
        ("Bhopal", "Nagpur"), ("Bhopal", "Delhi"), ("Nagpur", "Mumbai"),
        ("Bhopal", "Ahmedabad"), ("Nagpur", "Hyderabad"),
        
        # Eastern Routes
        ("Kolkata", "Patna"), ("Kolkata", "Bhubaneswar"), ("Kolkata", "Guwahati"),
        
        # Southern Routes
        ("Bangalore", "Chennai"), ("Bangalore", "Hyderabad"), ("Chennai", "Hyderabad"),
        ("Bangalore", "Kochi"), ("Chennai", "Visakhapatnam"), ("Visakhapatnam", "Bhubaneswar"),
        
        # Additional Cross-Country Routes
        ("Hyderabad", "Nagpur"), ("Patna", "Varanasi"), ("Jaipur", "Bhopal"),
        ("Pune", "Bangalore"), ("Ahmedabad", "Bhopal")
    ]
    
    # Add edges with real distances and estimated durations
    for n1, n2 in routes:
        dist = haversine_distance(locations[n1], locations[n2])
        # Assume average speed of 60 km/h (16.67 m/s) for duration calculation
        # This accounts for highways, but also traffic and road conditions
        duration = dist / 16.67
        G.add_edge(n1, n2, weight=dist, duration=duration)
    
    return G

def get_route_data(start_coords, end_coords):
    """
    Get the optimal route between two coordinates
    
    Args:
        start_coords: Tuple of (latitude, longitude) for start point
        end_coords: Tuple of (latitude, longitude) for end point
    
    Returns:
        dict: Contains route geometry, distance, and duration
    """
    # Create the India graph
    G = create_india_graph()
    
    # Find nearest nodes to start and end coordinates
    def find_nearest_node(coords):
        return min(G.nodes(), 
                  key=lambda n: haversine_distance(coords, G.nodes[n]['pos']))
    
    start_node = find_nearest_node(start_coords)
    end_node = find_nearest_node(end_coords)
    
    try:
        # Find shortest path using A* algorithm
        def heuristic(n1, n2):
            return haversine_distance(G.nodes[n1]['pos'], G.nodes[n2]['pos'])
        
        route = nx.astar_path(G, start_node, end_node, 
                            heuristic=heuristic, weight='weight')
        
        # Calculate total distance and duration
        distance = 0
        duration = 0
        route_geometry = []
        
        for i in range(len(route) - 1):
            distance += G[route[i]][route[i + 1]]['weight']
            duration += G[route[i]][route[i + 1]]['duration']
            route_geometry.append(G.nodes[route[i]]['pos'])
        
        route_geometry.append(G.nodes[route[-1]]['pos'])
        
        return {
            "geometry": route_geometry,
            "distance": round(distance/1000, 2),  # Distance in kilometers
            "duration": round(duration/3600, 2),  # Duration in hours
            "path": route,
            "start_city": start_node,
            "end_city": end_node
        }
        
    except nx.NetworkXNoPath:
        return None

# Example usage
if __name__ == "__main__":
    # Example: Route from Delhi to Bangalore
    start = (28.6139, 77.2090)  # Delhi coordinates
    end = (12.9716, 77.5946)    # Bangalore coordinates
    
    result = get_route_data(start, end)
    if result:
        print(f"\nRoute from {result['start_city']} to {result['end_city']}:")
        print(f"Path: {' -> '.join(result['path'])}")
        print(f"Distance: {result['distance']:.2f} km")
        print(f"Estimated duration: {result['duration']:.2f} hours")