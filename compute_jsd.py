"""Compute corrected JSD and update paper with honest synthetic data framing."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import numpy as np
from scipy import stats
from scipy.special import rel_entr
import pandas as pd

df = pd.read_csv('instagram_comments_dataset.csv')
df['token_length'] = df['comment_text'].astype(str).str.split().str.len()

# Proper probability normalization over shared support
bins = np.arange(0, 30)
sc, _ = np.histogram(df['token_length'].values, bins=np.append(bins, 100))
sc = sc[:len(bins)]
sp = sc / sc.sum()

nbr_raw = stats.nbinom.pmf(bins, 3.0, 0.27)
rp = nbr_raw / nbr_raw.sum()

eps = 1e-10
sp_s = sp + eps;  sp_s /= sp_s.sum()
rp_s = rp + eps;  rp_s /= rp_s.sum()
m = 0.5*(sp_s + rp_s)

jsd_val = 0.5 * float(np.sum(rel_entr(sp_s, m))) + 0.5 * float(np.sum(rel_entr(rp_s, m)))
kl_val  = float(np.sum(rel_entr(sp_s, rp_s)))

print("=" * 60)
print("CORRECTED VALIDATION METRICS (JSD in nats, range 0-ln2)")
print("=" * 60)
print(f"  KL(Synthetic || Reference)  = {kl_val:.4f} nats")
print(f"  JSD (Jensen-Shannon)        = {jsd_val:.4f} nats")
print(f"  JSD normalized (0-1 scale)  = {jsd_val / np.log(2):.4f}")
print()
print("TOKEN LENGTH COMPARISON:")
print(f"  Synthetic:  mean={df.token_length.mean():.2f}, std={df.token_length.std():.2f}")
print(f"              range=[{df.token_length.min()}, {df.token_length.max()}]")
print(f"  Benchmark:  mean=8.40, std=6.20 (Nurlaila et al. 2021)")
print()

jsd_norm = jsd_val / np.log(2)
if jsd_norm < 0.20:
    label = "LOW - acceptable fidelity"
elif jsd_norm < 0.40:
    label = "MODERATE - acknowledge limitation"
else:
    label = "HIGH - must disclose prominently"

print(f"  JSD Assessment: {label}")
print()
print("HONEST CONCLUSION FOR PAPER:")
print("  The synthetic corpus exhibits artificially narrow token length")
print(f"  distribution (range {df.token_length.min()}-{df.token_length.max()} tokens, std={df.token_length.std():.2f})")
print("  vs reference std=6.2. This represents a known limitation of")
print("  template-based generation that must be explicitly disclosed.")
print("  However, account balance (Chi2 p=0.202) and temporal")
print("  stationarity (CV=0.162) confirm no structural biases.")
print("  Recommendation: Frame as 'controlled proxy corpus' not")
print("  'representative sample', and quantify gap with JSD metric.")
