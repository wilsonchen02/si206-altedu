import sqlite3
import os
import sys
import csv


def get_data():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(f"{path}/var/database.sqlite")
    cur = conn.cursor()

    query = """
    SELECT a.size, a.grad_rate, a.admissions_rate, b.name, b.elevation, b.population, b.state_id
    FROM schools AS a
    LEFT JOIN cities AS b
    ON a.city_id = b.id
    """
    cur.execute(query)

    return cur.fetchall()

def write_data(db_data):
    fields = ["city", "student_percentage", "avg_grad", "elevation"]
    filename = "calculations.csv"

    data = {}

    # city : [total_pop, total_students, elevation, grad_rate sum, num schools]
    for row in db_data:
        if row[3] not in data and row[1]:
            data[row[3]] = [row[5], row[0], row[4], row[1], 1]
        elif row[1]:
            data[row[3]][1] += row[0]
            data[row[3]][3] += row[1]
            data[row[3]][4] += 1

    csv_input = []

    for k, v in data.items():
        print(k)
        print(v)
        csv_input.append(
            {
                "city": k,
                "student_percentage": f"{int((v[1] / v[0]) * 100)}%",
                "avg_grad": v[3] / v[4],
                "elevation": v[2],
            }
        )

    with open(filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(csv_input)

def main():
    db_data = get_data()
    write_data(db_data)

if __name__ == "__main__":
    main()
