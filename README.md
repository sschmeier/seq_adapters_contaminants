# seq_adapters_contaminants
Sequencing adapters and contaminants collection from different tools for easy download.

## Tools

- bbmap - [https://sourceforge.net/projects/bbmap/](https://sourceforge.net/projects/bbmap/)
- atropos - [https://github.com/jdidion/atropos/](https://github.com/jdidion/atropos/)
- FastQC - [https://github.com/s-andrews/FastQC](https://github.com/s-andrews/FastQC)


## One combined file

Read all fasta adapter files. Make a file with unique sequences. Id will be the first occurrence.

```bash
python union.py atropos/xxx/sequencing_adapters.fa bbmap/xxx/adapters.fa fastqc/xxx/contaminant_list.fa > adapters_union.fa
```
