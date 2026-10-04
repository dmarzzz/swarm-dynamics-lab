# Development replay01: reject unrestricted spatial extraction

Saved train40–59 only;20 used receipts,19 scorable,0 new OCR calls. The first prototype raised R0 from11 correct/0 wrong to13/1 and T1 from1/0 to2/3. Targeted fallback was13/3 versus primary13/1. This is not qualification and does not justify deployment.

Saved-observation diagnosis found two contract defects: `SUB.TOTAL` bypassed the punctuation-limited subtotal exclusion, and a readable generic TOTAL quantity was accepted despite an explicitly present but unreadable GRAND TOTAL field. Before replay02, extend the exclusion across subtotal punctuation and make an unresolved explicit final-total field block a generic-total fallback. Add negative regression fixtures without using case IDs or gold in the parser. Preserve replay01. Wrong digits in Tesseract remain genuine OCR errors; these parser repairs cannot fix them.

Tesseract remains an unsuitable checker on these development observations. Do not rerun native Q0 merely because the old two-correct family floor might become reachable. The strengthened v8 per-worker competence requirement is unchanged. A candidate replacement perception path needs development and fresh qualification before S1.
