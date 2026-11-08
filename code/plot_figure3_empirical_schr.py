"""
plot_figure3_empirical_schr.py
Plots publication-quality Figure 3: Empirical SCHR (%) across Context Tiers (CT1-CT3)
and Simulated Obfuscation Templates (Obf0-Obf3).
"""

import os
os.environ["MPLCONFIGDIR"] = os.path.join(os.environ.get("TEMP", "C:/Temp"), "mpl_cache")

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Style configuration
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 9,
    "figure.titlesize": 12,
    "figure.dpi": 300,
    "axes.grid": True,
    "grid.linestyle": "--",
    "grid.alpha": 0.5,
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={"width_ratios": [1, 1.15]})

# -------------------------------------------------------------
# Panel (a): Context Tiers (CT1, CT2, CT3) - N=80 per tier
# -------------------------------------------------------------
tiers = ["CT1\n(Stripped C)", "CT2\n(+Assembly)", "CT3\n(+Spec/Callee)"]
x = np.arange(len(tiers))
width = 0.32

# LLaMA-3.1 8B data
llama_schr = [38.8, 36.2, 37.5]
llama_err_low = [38.8 - 28.8, 36.2 - 26.6, 37.5 - 27.7]
llama_err_high = [49.7 - 38.8, 47.2 - 36.2, 48.5 - 37.5]
llama_yerr = [llama_err_low, llama_err_high]

# Qwen2.5-Coder 14B data
qwen_schr = [23.8, 20.0, 23.8]
qwen_err_low = [23.8 - 15.8, 20.0 - 12.7, 23.8 - 15.8]
qwen_err_high = [34.1 - 23.8, 30.0 - 20.0, 34.1 - 23.8]
qwen_yerr = [qwen_err_low, qwen_err_high]

rects1 = ax1.bar(x - width/2, llama_schr, width, yerr=llama_yerr, capsize=4,
                 label="LLaMA-3.1 8B", color="#2b5c8f", edgecolor="black", linewidth=0.8, alpha=0.9)
rects2 = ax1.bar(x + width/2, qwen_schr, width, yerr=qwen_yerr, capsize=4,
                 label="Qwen2.5-Coder 14B", color="#d95f02", edgecolor="black", linewidth=0.8, alpha=0.9)

# Value annotations
for rect in rects1:
    h = rect.get_height()
    ax1.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width()/2, h),
                 xytext=(0, 14), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

for rect in rects2:
    h = rect.get_height()
    ax1.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width()/2, h),
                 xytext=(0, 12), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

ax1.set_ylabel("Security-Critical Hallucination Rate (SCHR %)")
ax1.set_title("(a) Passive Context Escalation (N = 80 per tier)")
ax1.set_xticks(x)
ax1.set_xticklabels(tiers)
ax1.set_ylim(0, 65)
ax1.legend(loc="upper left", framealpha=0.9)

# -------------------------------------------------------------
# Panel (b): Simulated Obfuscation Templates (Obf0-Obf3) - N=10 Pilot
# -------------------------------------------------------------
obf_labels = ["Obf0\n(Baseline)", "Obf1\n(CFF)", "Obf2\n(Sub)", "Obf3\n(Combined)"]
x2 = np.arange(len(obf_labels))

llama_obf = [30.0, 30.0, 30.0, 40.0]
qwen_obf = [10.0, 10.0, 10.0, 20.0]

rects3 = ax2.bar(x2 - width/2, llama_obf, width, label="LLaMA-3.1 8B",
                 color="#2b5c8f", edgecolor="black", linewidth=0.8, alpha=0.9)
rects4 = ax2.bar(x2 + width/2, qwen_obf, width, label="Qwen2.5-Coder 14B",
                 color="#d95f02", edgecolor="black", linewidth=0.8, alpha=0.9)

for rect in rects3:
    h = rect.get_height()
    ax2.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width()/2, h),
                 xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

for rect in rects4:
    h = rect.get_height()
    ax2.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width()/2, h),
                 xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

ax2.set_ylabel("Pilot SCHR (%)")
ax2.set_title("(b) Simulated Obfuscation Templates (N = 10 Pilot)")
ax2.set_xticks(x2)
ax2.set_xticklabels(obf_labels)
ax2.set_ylim(0, 65)
ax2.legend(loc="upper left", framealpha=0.9)

plt.tight_layout()

# Save outputs
root = Path(__file__).resolve().parent.parent
dest1 = root / "manuscript" / "02_Springer_LNICST_Format_10_14_Pages" / "figures" / "fig3_empirical_schr.png"
dest2 = root / "manuscript" / "01_IEEE_Conference_Format_8_10_Pages" / "figures" / "fig3_empirical_schr.png"

fig.savefig(dest1, dpi=300, bbox_inches="tight")
fig.savefig(dest2, dpi=300, bbox_inches="tight")

print(f"Figure 3 successfully regenerated at:\n - {dest1}\n - {dest2}")
