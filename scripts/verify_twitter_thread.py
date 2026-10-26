import re

tweets = [
    # Tweet 1: Hook & Core Base SVR Finding (with infographic image)
    (
        "How effective is liquidation value recapture on @base?\n\n"
        "We analyzed 105 Smart Value Recapture (SVR) transactions on @MorphoLabs ($190.5k gross incentive, Oct 2026):\n\n"
        "• 94.38% ($179.8k) recaptured by SVR contracts\n"
        "• 98.30% median per-tx recapture\n\n"
        "Data breakdown 🧵👇 [1/5]"
    ),
    # Tweet 2: Solver Auction Dynamics
    (
        "Why does SVR work so efficiently on @base?\n\n"
        "In our sample, median solver margin compressed to -1.55%.\n\n"
        "Solvers compete aggressively and subsidize priority gas to win bundles. The auction successfully routes value back to protocol contracts rather than MEV searchers. [2/5]"
    ),
    # Tweet 3: Contrast with Ethereum L1 Fat-Tail Leakage
    (
        "The contrast with Ethereum L1 is striking.\n\n"
        "Analyzing 1,049 non-SVR Morpho liquidations on L1 reveals extreme fat-tail leakage:\n\n"
        "Just the 22 largest transactions account for 95.94% ($351.3k of $366.1k) of all builder bribe payments. L1 leaks value to builder cartels. [3/5]"
    ),
    # Tweet 4: Live Surveillance & Radar Architecture
    (
        "To monitor these dynamics live, we built Werracle Radar:\n\n"
        "📡 https://radar.werracle.com\n\n"
        "• Actively surveilling $2.20B+ clean borrow debt across 38 verified markets\n"
        "• 45 unlisted/synthetic spam markets isolated ($2.31B noise filtered)\n"
        "• Real-time Bad Debt (HF<0.95) alerts [4/5]"
    ),
    # Tweet 5: Open Science, Links & Team
    (
        "100% open-access & reproducible:\n\n"
        "📂 Dataset: https://huggingface.co/datasets/pCwOrM/defi-oev-liquidations-l1-base\n"
        "📜 Zenodo: https://doi.org/10.5281/zenodo.22942598\n"
        "📑 Paper: arXiv:2609.30719 & SSRN: 7626279\n\n"
        "Built on @base by @ITouchSystems with Mersin & Toros Univ. researchers. Feedback welcome! [5/5]"
    )
]

def twitter_char_count(text):
    # Twitter t.co replaces any URL with 23 characters
    urls = re.findall(r'https?://\S+', text)
    length = len(text)
    for u in urls:
        length = length - len(u) + 23
    return length

all_pass = True
print("=== TWITTER THREAD CHARACTER LENGTH VERIFICATION (280 LIMIT) ===")
for i, t in enumerate(tweets, 1):
    cnt = twitter_char_count(t)
    status = "PASS" if cnt <= 280 else "FAIL"
    print(f"\nTweet {i}/5: {cnt}/280 chars -> {status}")
    print("-" * 50)
    print(t.encode('ascii', errors='replace').decode('ascii'))
    if cnt > 280:
        all_pass = False

print("\n" + "=" * 50)
print(f"Overall Thread Verification: {'ALL TWEETS PASS (<= 280)' if all_pass else 'SOME TWEETS EXCEED LIMIT'}")
