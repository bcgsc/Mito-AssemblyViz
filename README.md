# Mito-AssemblyVis
Mitochondrial Genome Assembly Assessment Visualization

By: Armaghan Sarvar, Cecilia Yang

## Overview

Our project is implemented as an interactive web application using the Flask framework written in Python.

The main components are:

* GGisy: A Circos-based genome assembly consistency plot which is given a set of contigs relative to a reference genome and results in a quick qualitative view of the misassemblies in a genome assembly.


* HiPlot: Given a set of hyper-parameters used by different assembly pipelines, the HiPlot tool is used to illustrate the relationships between these parameters, such as the k-mer sizes, and the final assembly results, such as the genome completeness.


* PyGenomeViz:  

`data/`: Prepared Data corresponding to Sea Otter for comparing the three example mitogenome assembly pipelines: mtGasp, MitoZ, and GetOrganelle. 

`templates/`: The HTML files belonging to the web application

`static/`: The application .css file and used logos

