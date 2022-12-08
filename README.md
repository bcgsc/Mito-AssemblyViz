# Mito-AssemblyVis
Mitochondrial Genome Assembly Assessment Visualization

By: Armaghan Sarvar, Cecilia Yang

## Overview

Our project is implemented as an interactive web application using the Flask framework written in Python.

The main components are:

### The Visualization Modules:

* GGisy [1]: A Circos-based genome assembly consistency plot which is given a set of contigs relative to a reference genome and results in a quick qualitative view of the misassemblies in a genome assembly.


* HiPlot [2]: Given a set of hyper-parameters used by different assembly pipelines, the HiPlot tool is used to illustrate the relationships between these parameters, such as the k-mer sizes, and the final assembly results, such as the genome completeness.


* PyGenomeViz [3]:  

### The Web Application Modules:

`data/`: Prepared data corresponding to Sea Otter species for comparing the three example mitogenome assembly pipelines: mtGasp (the novel in-house pipeline), MitoZ [4], and GetOrganelle [5]. 

`templates/`: The HTML files belonging to the web application

`static/`: The application .css file and used logos

## Setup

To run the app (in development mode), simply run:

```
python Flask.py
```

The app will be listening on port 31807.


## References
[1] Sandro Valenzuela. GGisy. https://github.com/Sanrrone/GGisy. 2017.

[2] Facebook Research. HiPlot: High-dimensional interactive plots made easy. https://ai.facebook.com/blog/ hiplot-high-dimensional-interactive-plots-made-easy/.  Accessed:  2022-10-18.

[3] Moshi. pyGenomeViz. https://github.com/moshi4/pyGenomeViz. 2022. 

[4] Guanliang Meng et al. “MitoZ: a toolkit for animal mitochondrial genome assembly, annotation and visualization”. In: Nucleic Acids Research 47.11 (2019), e63.

[5] Jian-Jun Jin et al. “GetOrganelle: a fast and versatile toolkit for accurate de novo assembly of organelle genomes”. In: Genome biology 21.1 (2020), pp. 1–31.
