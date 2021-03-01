from flask import Flask
import csv
from collections import defaultdict

app = Flask(__name__)


@app.before_first_request
def sorting():
    """Creating and sorting a dict for use in the next func"""
    global result
    result = defaultdict(list)
    with open(file=r'recommends.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for line in reader:
            if not result:
                result[line[0]] = [[line[1], line[2]]]
            else:
                result[line[0]] += [[line[1], line[2]]]
    return result


@app.route('/<string:sku>/<float:param>')
def collecting(sku, param):
    """Getting dictionary values by a key"""
    for_sorting = result.get(sku)
    try:
        ready_res = sorted(for_sorting, key=lambda closeness: float(closeness[1]))
        data_out = [elem[0] for elem in ready_res if float(elem[1]) >= param]
        return ', '.join(data_out)
    except TypeError as exc:
        return f'Несуществующий товар - ошибка {exc}'


if __name__ == '__main__':
    app.run(debug=True)
