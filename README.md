# seq_adapters_contaminants
Sequencing adapters and contaminants collection from different tools for easy download.

## Tools

- bbmap - [https://sourceforge.net/projects/bbmap/](https://sourceforge.net/projects/bbmap/)
- atropos - [https://github.com/jdidion/atropos/](https://github.com/jdidion/atropos/)
- FastQC - [https://github.com/s-andrews/FastQC](https://github.com/s-andrews/FastQC)


## One combined file

Read all fasta adapter files. Make a file with unique sequences. Id will be the first occurrence.

**For some tools the order of the sequences in the adapter file matter(e.g. bbduk), thus here we keep the order as first seen first in union.**


```bash
python union.py bbmap/xxx/adapters.fa atropos/xxx/sequencing_adapters.fa fastqc/xxx/contaminant_list.fa > adapters_union.fa
```
