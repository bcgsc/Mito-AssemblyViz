from turtle import title
from pygenomeviz import GenomeViz
import pandas as pd

# user inputs
#fas_file_list = ['data/mtGasp_k91.fas', 'data/GetOrganelle_k91.fas', 'data/MitoZ_k61.fas', 'data/NC_009692.1.fas']
#genome_coverage_file_list = ['data/mtGasp_k91.txt', 'data/GetOrganelle_k91.txt', 'data/MitoZ_k61.txt']
#size_list = [16409, 16450, 16460, 16431]


def run(title_list, fas_file_list, genome_coverage_file_list, size_list, output_path):
    # start of GenomeViz
    def parse_fas(fas_file):
        with open(fas_file, 'r') as f:
            header_list = [line for line in f if line.startswith('>')]
        end_pos, start_pos, gene_names, strand = [], [], [], []
        for header in header_list:
            start_pos.append(int(header.split('; ')[1].split('-')[0]))
            end_pos.append(int(header.split('; ')[1].split('-')[1]))
            gene_names.append(header.split('; ')[3].rstrip())
            strand.append(1 if header.split('; ')[2] == '+' else -1)
        return start_pos, end_pos, strand, gene_names

    def create_tuple(fas_file):
        tuple = ()
        for x, y, z in zip(parse_fas(fas_file)[0], parse_fas(fas_file)[1], parse_fas(fas_file)[2]):
            tuple += ((x, y, z),)
        return tuple

    def color(x):
        if x == 1:
            return 'orange'
        else:
            return 'grey'

    def parse_coverage_file(genome_coverage_file):
        df = pd.read_csv(genome_coverage_file, sep='\t', header=None)
        df.columns = ['scaffold', 'nucleotide_position', 'coverage']
        pos_list = df['nucleotide_position'].tolist()
        cov_list = df['coverage'].tolist()
        return pos_list, cov_list

    genome_list = [
        {
            "name": "Mitogenome " + str(i + 1),
            "size": size_list[i],
            "cds_list": create_tuple(fas_file_list[i])
        } for i in range(len(fas_file_list) - 1)
    ]

    genome_list.append(
        {
            "name": "Reference",
            "size": size_list[-1],
            "cds_list": create_tuple(fas_file_list[-1])
        }
    )
    
    #genome_list = (
    #    {"name": "Mitogenome 1", "size": size_list[0], "cds_list": create_tuple(fas_file_list[0])},
    #    {"name": "Mitogenome 2", "size": size_list[1], "cds_list": create_tuple(fas_file_list[1])},
    #    {"name": "Mitogenome 3", "size": size_list[2], "cds_list": create_tuple(fas_file_list[2])},
    #    {"name": "Reference", "size": size_list[3], "cds_list": create_tuple(fas_file_list[3])},
    #)

    gene_list = []
    for file in fas_file_list:
        gene_list.append(parse_fas(file)[3])

    gv = GenomeViz(tick_style="axis")

    # Add subtracks for plotting 'Genome Coverage'

    cov = []
    for file in genome_coverage_file_list:
        cov += [parse_coverage_file(file)[1]]

    max_cov = max([max(x) for x in cov])

    for i in range(len(genome_list)):
        genome = genome_list[i]

        name, size, cds_list = genome["name"], genome["size"], genome["cds_list"]
        track = gv.add_feature_track(name, size)
        for idx, cds in enumerate(cds_list):
            start, end, strand = cds
            track.add_feature(start, end, strand, label=f"{gene_list[i][idx]}", labelcolor=color(strand),
                              edgecolor=color(strand), facecolor=color(strand), linewidth=2, size_ratio=0.2,
                              labelrotation=60, labelsize=5)
            track.set_sublabel(text=f"{size} bp", position='top-right', size=10)

    for i in range(len(title_list)):
        gv.get_feature_tracks()[i].add_subtrack(ratio=0.8)

    fig = gv.plotfig()
    for i in range(len(genome_coverage_file_list)):
        pos_list = parse_coverage_file(genome_coverage_file_list[i])[0]
        cov_list = parse_coverage_file(genome_coverage_file_list[i])[1]
        cov_track = gv.get_feature_tracks()[i].subtracks[0].ax
        cov_track.set_ylim(bottom=0, top=max_cov)
        cov_track.fill_between(pos_list, cov_list, color='blue', alpha=0.5)
        cov_track.set_ylabel('Genome Coverage', fontsize=10, color='blue')
        cov_track.set_xlabel('Nucleotide Position', fontsize=10, color='blue')
        cov_track.tick_params(axis='both', colors='blue', labelsize=10)

        cov_track.set_title(title_list[i], fontsize=15, color='grey')
        cov_track.set_facecolor('white')

    gv.savefig_html(output_path, fig)
