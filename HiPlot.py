# mtGasp Assembly Evaluation
import hiplot as hip
import csv


def read_csv(path):
    data = []
    file = open(path)
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        parsed_dic = {}
        for i in range(len(header)):
            parsed_dic[header[i]] = row[i]
        data.append(parsed_dic)
    # print(data)
    return data


def run(csv_path):
    data = read_csv(csv_path)
    hip.Experiment.from_iterable(data).to_html("templates/HiPlot_result.html")


# data = [{'K-mer Size':61, 'Number of Gaps': 0, 'Number of Sequences': 1, 'Number of Misassemblies': 0, 'Sequence Length (bp)': 16349.0, 'Genome Fraction (%)': 99.957},
#         {'K-mer Size':81, 'Number of Gaps': 0, 'Number of Sequences': 1, 'Number of Misassemblies': 0, 'Sequence Length (bp)': 16409.0, 'Genome Fraction (%)': 99.957},
#         {'K-mer Size':91, 'Number of Gaps': 0, 'Number of Sequences': 1, 'Number of Misassemblies': 0, 'Sequence Length (bp)': 16409.0, 'Genome Fraction (%)': 99.957}]
# generate hiplot experiment
# exp = hip.Experiment.from_iterable(data)
# display the experiment
# exp.display()
