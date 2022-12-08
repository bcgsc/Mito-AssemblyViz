from fileinput import filename
from flask import Flask, render_template, request, redirect, send_from_directory
import os
from pdf2image import convert_from_path
import PyGenomeViz
import time
import HiPlot
import matplotlib
matplotlib.use('agg')
app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'
app.config['TEMP_FOLDER'] = 'temp'


@app.route("/", methods=['GET', 'POST'])
@app.route("/index.html", methods=['GET', 'POST'])
def indexPage():
    if request.method == "POST":
        if request.form['action'] == "search":
            module = request.form['search bar']
            print(module)
        # return redirect("/render.html")
        return redirect("/result.html")
    return render_template('index.html')


@app.route("/GGisy_result.html")
def GGisyResultPage():
    pdf_path = os.path.join(app.config['STATIC_FOLDER'], 'synteny.pdf')
    page = convert_from_path(pdf_path)
    page[0].save(os.path.join(app.config['STATIC_FOLDER'], 'synteny.jpg'), 'JPEG')
    return render_template('GGisy_result.html', user_pdf=os.path.join(app.config['STATIC_FOLDER'], 'synteny.jpg'))


@app.route("/GGisy.html", methods=['GET', 'POST'])
def GGisyPage():
    if request.method == "POST":
        file_reference = request.files["ggisy_r"]
        file_query = request.files["ggisy_q"]
        align_l = request.form["ggisy_l"]
        identity_i = request.form["ggisy_i"]
        coverage_c = request.form["ggisy_c"]
        threads_t = request.form["ggisy_t"]
        interm_k = request.form.get("ggisy_k")
        interm_k = interm_k is not None
        ref_path = os.path.join(app.config['TEMP_FOLDER'], file_reference.filename)
        query_path = os.path.join(app.config['TEMP_FOLDER'], file_query.filename)
        if os.path.isfile(ref_path):
            os.remove(ref_path)
        if os.path.isfile(query_path):
            os.remove(query_path)
        if file_reference:
            file_reference.save(ref_path)
        if file_query:
            file_query.save(query_path)
        command = "python ./GGisy.py -r " + ref_path + " -q " + query_path + " -l " + align_l + " -i " + identity_i \
                + " -c " + coverage_c + " -t " + threads_t + " -k " + str(interm_k) + ' -o ' + app.config['STATIC_FOLDER'] + "/synteny"
        print(command)
        if os.system(command) != 0:
            print("GGisy Error!")
            return render_template('GGisy.html', onload="alert(\'GGisy Error!\');")

        return redirect('GGisy_result.html')

    return render_template('GGisy.html')


def add_after(str, pattern, after_pattern):
    # Find where the pattern ends in the string.
    index = str.find(pattern) + len(pattern)
    return str[:index] + after_pattern + str[index:]


@app.route("/HiPlot_result.html")
def HiPlotResultPage():
    with open('templates/HiPlot_result.html') as file:
        all_file = file.read()
    pattern = "<body style=\"margin:0px\">"
    new_code = "<link rel=\"stylesheet\" href=\"../static/main.css\"> <div id=\"option_title_div\"> \
            <h1 id=\"option_title_hiplot\"> \
                HiPlots for Hyperparameter Tuning <br/> \
                <a href=\"index.html\" style=\"font-size: 0.5em;\"> Back to Main Page </a>\
            </h1> \
            </div>"
    start_pattern = all_file.find(pattern)
    end_pattern = start_pattern + len(pattern)
    new_content = all_file[:start_pattern] + pattern + new_code + all_file[end_pattern:]
    with open('templates/HiPlot_result.html', 'w') as file:
        file.write(new_content)
    return render_template('HiPlot_result.html')


@app.route("/HiPlot.html", methods=['GET', 'POST'])
def HiPlotPage():
    if request.method == "POST":
        csv_file = request.files["hiplot_csv"]
        csv_path = os.path.join(app.config['TEMP_FOLDER'], csv_file.filename)
        if os.path.isfile(csv_path):
            os.remove(csv_path)
        if csv_file:
            csv_file.save(csv_path)
        try:
            HiPlot.run(csv_path)
        except:
            print("HiPlot Error!")
            return render_template('HiPlot.html', onload="alert(\'HiPlot Error!\');")
        return redirect('HiPlot_result.html')
    return render_template('HiPlot.html')


@app.route("/PyGenomeViz_result.html")
def PyGenomeVizResultPage():
    with open('templates/PyGenomeViz_result.html') as file:
        all_file = file.read()

    pattern = "<body>"
    new_code = "<link rel=\"stylesheet\" href=\"../static/main.css\"> <div id=\"option_title_div\"> \
            <h1 id=\"option_title_hiplot\"> \
                PyGenomeViz Annotation Visualization <br/> \
                <a href=\"index.html\" style=\"font-size: 0.5em;\"> Back to Main Page </a>\
            </h1> \
            </div>"

    new_content = add_after(all_file, pattern, new_code)

    with open('templates/PyGenomeViz_result.html', 'w') as file:
        file.write(new_content)

    return render_template('PyGenomeViz_result.html')


@app.route("/PyGenomeViz.html", methods=['GET', 'POST'])
def PyGenomeVizPage():
    if request.method == 'POST':
        option_count = int(request.form['options'])

        file_ref = request.files["reference_annotation_file"]
        size_ref = request.form["reference_genome_size"]

        ref_path = os.path.join(app.config['TEMP_FOLDER'], file_ref.filename)

        if file_ref.filename:
            file_ref.save(ref_path)

        titles = []
        annotations = []
        coverages = []
        sizes = []
        output = os.path.join("templates", "PyGenomeViz_result.html")
        
        for i in range(option_count):
            titles.append(request.form["title_" + str(i)])
            sizes.append(int(request.form["genome_size_" + str(i)]))

            anno_file = request.files["annotation_file_" + str(i)]
            cov_file = request.files["coverage_file_" + str(i)]
            
            anno_file_path = os.path.join(app.config['TEMP_FOLDER'], anno_file.filename)
            cov_file_path = os.path.join(app.config['TEMP_FOLDER'], cov_file.filename)
            
            if anno_file.filename:
                anno_file.save(anno_file_path)

            if cov_file.filename:
                cov_file.save(cov_file_path)

            annotations.append(anno_file_path)
            coverages.append(cov_file_path)

        annotations.append(ref_path)
        sizes.append(int(size_ref))

        try:
            if os.path.exists(output):
                os.remove(output)

            PyGenomeViz.run(titles, annotations, coverages, sizes, output)
            time.sleep(1)
        except:
            print("PyGenomeViz Error!")
            return render_template('PyGenomeViz.html', onload="alert(\'PyGenomeViz Error!\');")
        
        return redirect('PyGenomeViz_result.html')

    return render_template('PyGenomeViz.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=31807)
