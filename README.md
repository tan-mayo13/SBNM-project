# Sample-specific regulatory networks with LIONESS: lung adenocarcinoma vs normal lung

Course project, CB5313 Systems Biology and Network Modelling (topic 3).

## Question

Do sample-specific networks estimated with LIONESS differ in how similar they are
within tumour samples and within normal samples, and does this tell us anything
beyond what the expression data already show?

## Method in brief

LIONESS (Kuijjer et al., 2019, iScience 14:226-240) estimates a network for each
sample by comparing an aggregate network built from all samples with one built
without that sample, then scaling the difference. Here the aggregate network is built
with PANDA from netZooPy.

## Data

GEO series GSE10072 (lung adenocarcinoma and normal lung, Affymetrix microarray):
107 samples (58 tumour, 49 normal) from 74 patients. 33 patients have both a tumour and a
normal sample. The raw file is not stored in this repository, run the download script below.

## Repository layout

```
data/                 downloaded series matrix (not committed)
notebooks/            LIONESS_GSE10072_Analysis.ipynb (main analysis)
scripts/              download_data.py
results/              tables and figures produced by the notebook
environment.yml       conda environment
```

## How to run

```bash
conda env create -f environment.yml
conda activate lioness
python scripts/download_data.py
jupyter lab
```

Open `notebooks/LIONESS_GSE10072_Analysis.ipynb` and choose Kernel > Restart and Run All.
Outputs are written to `results/`.

## Analysis steps

1. Keep the 100 most variable probes across all samples.
2. Build the PANDA aggregate network (no motif or PPI prior supplied) and run LIONESS
   to get one network per sample.
3. Remove the 100 self-edges. The network is symmetric, so the remaining 9,900 directed
   edges are 4,950 unique gene pairs.
4. Spearman correlation between every pair of sample networks; compare
   Tumour-Tumour, Normal-Normal and Tumour-Normal similarity.
5. Threshold sensitivity: 90th, 95th and 99th percentile of pooled absolute edge weights,
   and per-sample network density at each threshold.

### Changes beyond the tutorial

- New dataset (GSE10072).
- Label-permutation test for the Normal-Normal minus Tumour-Tumour gap.
- Control with plain expression-profile similarity on the same probes.
- Gene-set sweep: top 50, 100, 200 and 500 most variable probes, plus 10 random sets of 100 probes.
- Check of how closely LIONESS edges follow the product of the two genes' z-scores.

## Results

**Threshold analysis (pooled absolute edge weight, self-edges removed)**

| Percentile | Threshold | Overall density |
|---|---|---|
| 90 | 1.287 | 0.100 |
| 95 | 1.653 | 0.050 |
| 99 | 2.744 | 0.010 |

Overall density is fixed by construction at about 10%, 5% and 1%. The informative part is the
per-sample spread: at the 90th percentile, mean per-sample density was 0.140 in tumours
(range 0.023-0.432) and 0.053 in normals (range 0.006-0.116).

**Mean pairwise Spearman similarity between sample networks (top 100 probes)**

| Comparison | Pairs | LIONESS network | z-score product | Expression profile |
|---|---|---|---|---|
| Tumour-Tumour | 1,653 | 0.307 | 0.162 | 0.542 |
| Normal-Normal | 1,176 | 0.561 | 0.450 | 0.866 |
| Tumour-Normal | 2,842 | 0.405 | 0.264 | 0.333 |

Permutation test (5,000 label shuffles) on the Normal-Normal minus Tumour-Tumour gap
(0.254): p < 0.001. Pairs are not independent observations, so no p-value is reported from
the pair counts.

**Gene-set sweep**

| Gene set | Network gap (NN-TT) | Expression gap (NN-TT) | Network TN-TT |
|---|---|---|---|
| top 50 | 0.164 | 0.302 | 0.073 |
| top 100 | 0.254 | 0.324 | 0.098 |
| top 200 | 0.275 | 0.235 | 0.103 |
| top 500 | 0.301 | 0.205 | 0.105 |
| random 100 (mean of 10, range) | 0.110 (0.093-0.127) | 0.027 (0.016-0.038) | 0.040 (0.034-0.044) |

**Other checks**

- LIONESS edges vs z-score products, per-sample Spearman: median 0.96 (range 0.53-0.99).
  7 of the 8 lowest-agreement samples are tumours. This is not explained by how
  extreme a sample is (Spearman of r vs mean |z| = +0.58).
- Same-patient tumour-normal pairs (n = 33): mean similarity 0.366, versus 0.406 for
  different-patient pairs.

## Interpretation

[Write this section in your own words. Suggested points to cover:
- What the Normal > Tumour pattern shows and how far it can be trusted (permutation test, sweep, random probes).
- Why Tumour-Normal is above Tumour-Tumour in the networks but not in expression (z-score product).
- What this means for what LIONESS adds in this setup.
- What you would NOT conclude (regulation, causality, validated interactions).]

## Limitations

- Edges are inferred associations, not experimentally validated regulatory interactions.
- PANDA was run without a motif or PPI prior, so the aggregate network behaves like a
  co-expression network between probes, not a TF-to-gene regulatory network.
- Probes were chosen by variance across all samples, which favours tumour-versus-normal
  differences. The sweep and random-probe controls address this only partly.
- Pairwise similarities are not independent. The design is partly paired (33 patients).
- LIONESS edges here are very close to z-score products, so the networks add little beyond
  the expression data for this question.
- The random-probe control uses 10 draws, so ranges are descriptive.

## AI use

[State how AI assistance was used, per the course policy, e.g. help with debugging and
reviewing code, and checking numbers. The synopsis and the biological interpretation are my own.]

## References

Kuijjer ML, Tung MG, Yuan G, Quackenbush J, Glass K (2019). Estimating sample-specific
regulatory networks. iScience 14:226-240. https://doi.org/10.1016/j.isci.2019.03.021

Glass K, Huttenhower C, Quackenbush J, Yuan GC (2013). Passing messages between biological
networks to refine predicted interactions. PLoS One 8:e64832.
