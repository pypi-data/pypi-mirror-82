from srrTomat0.processor.gtf import load_gtf_to_dataframe, open_window, GTF_CHROMOSOME, SEQ_START, SEQ_STOP, GTF_STRAND
from srrTomat0.processor.prior import build_prior_from_atac_motifs, MotifScorer
from srrTomat0.motifs.motif_scan import MotifScan
from srrTomat0.motifs import motifs_to_dataframe, INFO_COL, MOTIF_NAME_COL

import argparse
import pandas as pd


def main():
    ap = argparse.ArgumentParser(description="Create a prior from open chromatin peaks and motif peaks")
    ap.add_argument("-m", "--motif", dest="motif", help="Motif MEME file", metavar="PATH", required=True)
    ap.add_argument("-a", "--atac", dest="atac", help="ATAC BED file", metavar="FILE", default=None)
    ap.add_argument("-f", "--fasta", dest="fasta", help="Genomic FASTA file", metavar="FILE", required=True)
    ap.add_argument("-g", "--gtf", dest="annotation", help="GTF Annotation File", metavar="PATH", required=True)
    ap.add_argument("-o", "--out", dest="out", help="Output PATH", metavar="PATH", required=True)
    ap.add_argument("-w", "--window", dest="window_size", help="Window around genes", type=int, default=0, nargs="+")
    ap.add_argument("-c", "--cpu", dest="cores", help="Number of cores", metavar="CORES", type=int, default=1)
    ap.add_argument("--tss", dest="tss", help="Use TSS for window", action='store_const', const=True, default=False)
    ap.add_argument("--scan", dest="scanner", help="FIMO or HOMER", type=str, default='fimo')
    ap.add_argument("--motif_preprocessing_ic", dest="min_ic", help="Minimum information content",
                    metavar="BITS", type=int, default=None)
    ap.add_argument("--tandem_window", dest="tandem", help="Bases between TF bindings to consider an array",
                    metavar="BASES", type=int, default=100)
    ap.add_argument("--threshold", nargs="+", default=None, type=str)

    args = ap.parse_args()

    if args.threshold is None:
        prior_edges, prior_matrix, raw_matrix = build_atac_motif_prior(args.motif, args.atac, args.annotation, args.fasta,
                                                                       window_size=args.window_size, num_cores=args.cores,
                                                                       use_tss=args.tss, motif_ic=args.min_ic,
                                                                       scaner_type=args.scanner)

        prior_matrix.astype(int).to_csv(args.out, sep="\t")
        prior_edges.to_csv(args.out + ".edges.tsv.gz", sep="\t")
        raw_matrix.to_csv(args.out + ".raw.tsv", sep="\t")
    else:
        motifs = MotifScan.load_motif_file(args.motif)
        motif_information = motifs_to_dataframe(motifs)
        motif_information = motif_information[[MOTIF_NAME_COL, INFO_COL]].groupby(MOTIF_NAME_COL).agg("max")

        edge_count = {}
        for t in args.threshold:
            prior_edges, prior_matrix, raw_matrix = build_atac_motif_prior(args.motif, args.atac, args.annotation,
                                                                           args.fasta,
                                                                           window_size=args.window_size,
                                                                           num_cores=args.cores,
                                                                           use_tss=args.tss, motif_ic=args.min_ic,
                                                                           scaner_type=args.scanner,
                                                                           scanner_thresh=t)

            edge_count[t] = (raw_matrix != 0).sum(axis=0)

        edge_count = pd.concat(edge_count, axis=1)
        edge_count = edge_count.join(motif_information[INFO_COL])

        edge_count.to_csv(args.out, sep="\t")


def build_atac_motif_prior(motif_meme_file, atac_bed_file, annotation_file, genomic_fasta_file, window_size=0,
                           use_tss=True, scaner_type='fimo', num_cores=1, motif_ic=6, tandem=100,
                           truncate_motifs=0.35, scanner_thresh="5e-4"):
    # Set the scanner type
    if scaner_type.lower() == 'fimo':
        MotifScan.set_type_fimo()
    elif scaner_type.lower() == 'homer':
        MotifScan.set_type_homer()
    else:
        raise ValueError("motif_type must be fimo or homer")

    # PROCESS GENE ANNOTATIONS #

    print("Loading genes from file ({f})".format(f=annotation_file))
    # Load genes and open a window
    genes = load_gtf_to_dataframe(annotation_file)
    print("\t{n} genes loaded".format(n=genes.shape[0]))

    genes = open_window(genes, window_size=window_size, use_tss=use_tss)
    print("\tPromoter regions defined with window {w}".format(w=window_size))

    # PROCESS MOTIF PWMS #

    print("Loading motifs from file ({f})".format(f=motif_meme_file))
    motifs = MotifScan.load_motif_file(motif_meme_file)
    motif_information = motifs_to_dataframe(motifs)
    print("\t{n} motifs loaded".format(n=len(motif_information)))

    if truncate_motifs is not None:
        [x.truncate(threshold=truncate_motifs) for x in motifs]

    # SCAN CHROMATIN FOR MOTIFS #

    # Load and scan target chromatin peaks
    print("Scanning target chromatin ({f_c}) for motifs ({f_m})".format(f_c=atac_bed_file, f_m=motif_meme_file))

    gene_locs = genes.loc[:, [GTF_CHROMOSOME, SEQ_START, SEQ_STOP, GTF_STRAND]].copy()
    gene_locs[[SEQ_START, SEQ_STOP]] = gene_locs[[SEQ_START, SEQ_STOP]].astype(int)

    motif_peaks = MotifScan.scanner(motifs=motifs, num_workers=num_cores).scan(genomic_fasta_file,
                                                                               constraint_bed_file=atac_bed_file,
                                                                               promoter_bed=gene_locs,
                                                                               min_ic=motif_ic,
                                                                               threshold=scanner_thresh)

    # PROCESS CHROMATIN PEAKS INTO NETWORK MATRIX #

    # Processing into prior
    print("Processing TF binding sites into prior")
    MotifScorer.set_information_criteria(min_binding_ic=motif_ic, max_dist=tandem)
    prior_edges, prior_matrix, raw_matrix = build_prior_from_atac_motifs(genes, motif_peaks, motif_information,
                                                                         num_workers=num_cores)
    print("Prior matrix with {n} edges constructed".format(n=prior_edges.shape[0]))
    return prior_edges, prior_matrix, raw_matrix


if __name__ == '__main__':
    main()
