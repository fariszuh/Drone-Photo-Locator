import tkinter
import tkintermapview
from geopy.distance import great_circle

# 1. Setup your map and points
root_tk = tkinter.Tk()
root_tk.geometry(f"{800}x{600}")
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600)
map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# Example points (store coordinates and potentially marker objects)
# A list of (latitude, longitude, name) tuples
points_data = [
    (52.518, 13.400, "Berlin"),
    (48.856, 2.352, "Paris"),
    (51.507, -0.127, "London"),
    (-33.868, 151.207, "Sydney"),
]

# Add markers to the map
markers = []
jalur = []
for lat, lon, name in points_data:
    marker = map_widget.set_marker(lat, lon, text=name)
    markers.append((lat, lon, name, marker))
    # jalur = jalur + map_widget.set_marker(lat, lon).position
    # print(jalur)

# Index of the 'City' column to remove
label_column_index = 2

# Iterate through each inner list (row) and delete the element at the index
points_data_new = [row[:2] for row in points_data]

print(points_data_new)
continuous_route = map_widget.set_path(points_data_new, color="blue", width=4)


def find_closest_point_to_center():
    # 2. Get the reference point (e.g., current map center)
    center_coords = map_widget.get_position()
    center_point = (center_coords[0], center_coords[1])

    # 3. Use min() to find the closest point by distance
    # The key function calculates the great_circle distance for each point
    closest_point_info = min(markers, key=lambda p: great_circle(center_point, (p[0], p[1])).kilometers)

    lat, lon, name, marker_obj = closest_point_info
    distance = great_circle(center_point, (lat, lon)).kilometers

    print(f"Closest point to map center is {name} at {lat:.3f}, {lon:.3f}")
    print(f"Distance: {distance:.2f} KM")

    # Optional: Highlight the closest marker
    # (tkintermapview markers don't have built-in highlight methods,
    # but you can use print or UI elements to show the result)


# Add a button to trigger the function
button = tkinter.Button(root_tk, text="Find Closest Point to Center", command=find_closest_point_to_center)
button.pack(side=tkinter.BOTTOM, pady=10)

root_tk.mainloop()
