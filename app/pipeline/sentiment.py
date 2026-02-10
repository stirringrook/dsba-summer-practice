from typing import Tuple

from .text_preprocess import normalize_text

# Transparent lexicon-based baseline (reproducible, interpretable).
POS_WORDS = {
    "good","great","excellent","nice","love","perfect","amazing","fast","quality","recommend","satisfied",
    "awesome","best","wonderful","works","worked","happy","pleasant","reliable","delivery","packaging"
}
NEG_WORDS = {
    "bad","terrible","awful","poor","hate","broken","slow","worse","worst","refund","scam","fake","defect",
    "disappointed","damaged","delay","problem","useless","not working","waste"
}


def sentiment_score_and_label(text: str) -> Tuple[float, str]:
    t = normalize_text(text)
    if not t:
        return 0.0, "neu"

    score = 0.0
    for w in POS_WORDS:
        if w in t:
            score += 1.0
    for w in NEG_WORDS:
        if w in t:
            score -= 1.0

    # Normalize by rough length proxy to avoid long-text bias
    score = score / max(1.0, (len(t) / 120.0))

    if score >= 0.6:
        return float(score), "pos"
    if score <= -0.6:
        return float(score), "neg"
    return float(score), "neu"
