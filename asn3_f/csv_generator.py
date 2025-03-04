import csv

def update_csv(f_path, data):
    with open(f_path, 'a', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(data)

    file.close()
