"""Run synthetic data validation and save dashboard image."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os, pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
from scipy.special import rel_entr
from statsmodels.tsa.stattools import adfuller
import warnings
warnings.filterwarnings('ignore')

df_val = pd.read_csv('instagram_comments_dataset.csv')
df_val['comment_text'] = df_val['comment_text'].astype(str)
df_val['token_length'] = df_val['comment_text'].str.split().str.len()
df_val['post_date']    = pd.to_datetime(df_val['post_date'])

# Chi-square
obs_counts = df_val['account_username'].value_counts().sort_index().values
n_acc      = len(obs_counts)
expected   = np.full(n_acc, obs_counts.sum() / n_acc)
chi2, p_chi = stats.chisquare(obs_counts, f_exp=expected)

# Monthly stationarity
monthly    = df_val.set_index('post_date').resample('ME').size()
cv_m       = monthly.std() / monthly.mean()
adf_res    = adfuller(monthly.values, autolag='AIC')

# KL divergence
bins       = np.arange(1, 31)
sc, _      = np.histogram(df_val['token_length'].values, bins=np.append(bins,31))
sp         = (sc + 1e-9) / (sc.sum() + 1e-9 * len(bins))
nbr_raw    = stats.nbinom.pmf(bins-1, 3.0, 0.27)
rp         = (nbr_raw + 1e-9) / (nbr_raw.sum() + 1e-9 * len(bins))
kl         = float(np.sum(rel_entr(sp, rp)))
kl_r       = float(np.sum(rel_entr(rp, sp)))
jsd        = 0.5*kl + 0.5*kl_r

# Benchmark deviations
bm = {
    'Token\nLen\n(mean)': (df_val['token_length'].mean(), 8.4),
    'Token\nLen\n(std)':  (df_val['token_length'].std(),  6.2),
    'Comment\nLikes':     (df_val['likes_comment'].mean(),5.1),
    'Commenter\nUnique':  (df_val['comment_username'].nunique()/len(df_val), 0.87),
}
devs  = [abs(s-r)/r*100 for s,r in bm.values()]
clrs  = ['green' if d<15 else 'orange' if d<35 else 'red' for d in devs]

print("VALIDATION RESULTS")
print(f"  Chi2={chi2:.4f}, p={p_chi:.4f}")
print(f"  CV={cv_m:.3f}, ADF_p={adf_res[1]:.4f}")
print(f"  KL(S||R)={kl:.4f}, JSD={jsd:.4f}")
print(f"  Deviations: {[round(d,1) for d in devs]}")

# Dashboard
fig = plt.figure(figsize=(14, 10))
gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

ax1 = fig.add_subplot(gs[0,0])
ax1.bar(bins[:20]-0.3, sp[:20], width=0.4, label='Synthetic', color='steelblue', alpha=0.85)
ax1.bar(bins[:20]+0.1, rp[:20], width=0.4, label='Reference NegBinom', color='tomato', alpha=0.75)
ax1.set_xlabel('Comment Length (tokens)')
ax1.set_ylabel('Probability')
ax1.set_title(f'(A) Token Length Distribution\nJSD = {jsd:.4f}')
ax1.legend(fontsize=8)

ax2 = fig.add_subplot(gs[0,1])
acc = df_val['account_username'].value_counts().sort_values()
ax2.barh(acc.index, acc.values, color='mediumseagreen', alpha=0.85, edgecolor='black')
ax2.axvline(obs_counts.sum()/n_acc, color='red', linestyle='--',
            label=f'Expected ({int(obs_counts.sum()/n_acc):,})')
ax2.set_title(f'(B) Account Distribution\nChi2={chi2:.2f}, p={p_chi:.3f}')
ax2.set_xlabel('Comment Count')
ax2.legend(fontsize=8)

ax3 = fig.add_subplot(gs[1,0])
ax3.plot(monthly.index, monthly.values, color='darkorange', lw=2, marker='o', ms=3)
ax3.fill_between(monthly.index, monthly.values, alpha=0.2, color='darkorange')
ax3.axhline(monthly.mean(), color='red', linestyle='--',
            label=f'Mean = {monthly.mean():.0f}')
ax3.set_title(f'(C) Monthly Comment Volume\nCV={cv_m:.3f} | ADF p={adf_res[1]:.3f}')
ax3.set_xlabel('Month')
ax3.set_ylabel('Comment Count')
ax3.legend(fontsize=8)
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')

ax4 = fig.add_subplot(gs[1,1])
ax4.bar(list(bm.keys()), devs, color=clrs, alpha=0.85, edgecolor='black')
ax4.axhline(15, color='orange', linestyle='--', lw=1.5, label='15% threshold (acceptable)')
ax4.axhline(35, color='red',    linestyle='--', lw=1.5, label='35% critical')
ax4.set_ylabel('Deviation from Benchmark (%)')
ax4.set_title('(D) Benchmark Deviation\nvs. Indonesian NLP Literature')
ax4.legend(fontsize=8)
for i, v in enumerate(devs):
    ax4.text(i, v+0.5, f'{v:.1f}%', ha='center', fontsize=9, fontweight='bold')

fig.suptitle(
    'Synthetic Dataset Statistical Validation Dashboard\n'
    'vs. Published Indonesian Social Media Benchmarks',
    fontsize=12, fontweight='bold'
)
out = 'synthetic_validation_dashboard.png'
plt.savefig(out, bbox_inches='tight', dpi=150, facecolor='white')
plt.close()
sz = os.path.getsize(out)
print(f"Saved: {out}  ({sz/1024:.1f} KB)")
