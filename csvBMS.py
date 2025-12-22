# Change csv of Google MyMaps Point to python function set_position in tkintermapview
import csv

def read_csv_from_row(csv_filepath, txt_filepath, start_row_index):
    """
    Reads a CSV file from a specified row index (0-based).
    """
    with open(csv_filepath, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)

        with open(txt_filepath, 'w') as file:
            # pass  # The 'pass' statement does nothing, but the act of opening in 'w' mode empties the file.
            file.write("def add_new_marker_label(self):" + '\n')
        print(f"Content of '{txt_filepath}' has been removed.")

        path = "    path = self.map_widget.set_path(["

        for i, row in enumerate(csv_reader):
            if i >= start_row_index:
                # if i == 5: # uji sampel jika row >5 break
                #     break
                point_latlong = row[0] # take first element in list 'row[0]' and becoming string datatype
                point_towerlabel = row[1] # label of latlong point
                lat,long,label = split_into_latlong(point_latlong,point_towerlabel)
                # print(latlong,label)
                path = path + "marker_" + str(i) + ".position,"
                updated_row = "    marker_" + str(i) + " = " + "self.map_widget.set_marker(" + lat + "," + long + ", text=\"" + label + "\")"
                # print(updated_row)
                with open(txt_filepath, 'a') as txtfile:
                    txtfile.write(''.join(updated_row) + '\n')
        path = path + "])"
        print(path)
        with open(txt_filepath, 'a') as txtfile:
            txtfile.write(''.join(path) + '\n')


def split_into_latlong(point_latlong,point_towerlabel):
    print(point_latlong)
    latlong = point_latlong.replace("POINT (","").replace(" ",",").replace(",0.0","").replace(")","")
    # print(point_towerlabel)
    label = point_towerlabel.replace("BNGKO - SPNUH #0","T.")
    # print(label)
    long = latlong.split(',')[0]
    lat = latlong.split(',')[1]
    return lat,long,label

# Example usage:
# Assuming 'data.csv' has headers in the first row and data starts from the second row (index 1)
read_csv_from_row('BMS no UPT.csv', 'tower_location_BMS.py', 2)