"""
SCHR-Bench: Evaluation Engine & Statistical Rig
Computes SCHR, Miss Rate, BLEU Score, Wilson Confidence Intervals, and McNemar's Test.
"""

import math
import numpy as np
from scipy import stats
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# Ensure tokenizer is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

class EvaluationEngine:
    @staticmethod
    def calculate_schr(n_wrong, n_valid):
        """
        Security-Critical Hallucination Rate (SCHR)
        SCHR = (N_wrong / N_valid) * 100%
        """
        if n_valid == 0:
            return 0.0
        return (n_wrong / n_valid) * 100.0

    @staticmethod
    def calculate_miss_rate(n_identical_mutant_to_orig, n_total):
        """
        Miss Rate: cases where mutant output is identical to original output.
        """
        if n_total == 0:
            return 0.0
        return (n_identical_mutant_to_orig / n_total) * 100.0

    @staticmethod
    def calculate_bleu(reference_text, candidate_text):
        """
        Calculate sentence BLEU score between original response and mutant response.
        """
        ref_tokens = [reference_text.strip().lower().split()]
        cand_tokens = candidate_text.strip().lower().split()
        
        smooth = SmoothingFunction().method1
        return sentence_bleu(ref_tokens, cand_tokens, weights=(0.5, 0.5), smoothing_function=smooth)

    @staticmethod
    def wilson_score_interval(successes, total, confidence=0.95):
        """
        Wilson Score 95% Confidence Interval for binomial proportion.
        Used for reporting SCHR error margins in scientific papers.
        """
        if total == 0:
            return (0.0, 0.0, 0.0)
            
        p = successes / total
        z = stats.norm.ppf(1 - (1 - confidence) / 2)
        
        denominator = 1 + (z**2) / total
        centre = (p + (z**2) / (2 * total)) / denominator
        spread = (z * math.sqrt((p * (1 - p) / total) + (z**2) / (4 * total**2))) / denominator
        
        lower = max(0.0, centre - spread)
        upper = min(1.0, centre + spread)
        return (p * 100.0, lower * 100.0, upper * 100.0)

    @staticmethod
    def mcnemar_test(b, c):
        """
        McNemar's test with Edward's continuity correction on paired binary outputs.
        Tests Hypothesis H3: Does Assembly (CT2) significantly reduce hallucination vs Pseudocode (CT1)?
        b: Number of samples Wrong in CT1 but Correct in CT2
        c: Number of samples Correct in CT1 but Wrong in CT2
        """
        total_discordant = b + c
        if total_discordant == 0:
            return {"chi2": 0.0, "p_value": 1.0, "significant": False}
            
        chi2 = ((abs(b - c) - 1.0) ** 2) / total_discordant
        p_val = stats.chi2.sf(chi2, df=1)
        
        return {
            "b_improved": b,
            "c_regressed": c,
            "chi2": float(chi2),
            "p_value": float(p_val),
            "significant_at_0_01": bool(p_val < 0.01),
            "significant_at_0_05": bool(p_val < 0.05)
        }

if __name__ == "__main__":
    print("[*] Testing Evaluation Engine...")
    schr = EvaluationEngine.calculate_schr(15, 40)
    print(f"SCHR: {schr:.2f}%")
    
    p, low, up = EvaluationEngine.wilson_score_interval(15, 40)
    print(f"Wilson 95% CI: {p:.2f}% [{low:.2f}%, {up:.2f}%]")
    
    mcn = EvaluationEngine.mcnemar_test(b=14, c=2)
    print(f"McNemar Test: chi2={mcn['chi2']:.4f}, p-value={mcn['p_value']:.4e}, significant={mcn['significant_at_0_01']}")
