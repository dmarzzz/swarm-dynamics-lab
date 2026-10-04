# PI review decision guide

Open [the dark visual guide](index.html) in a browser. It puts all ten projects in one comparison table and gives each three next-step options. A six-row project-wide quality table and all 57 audit findings sit alongside the full scientific review.

| Color | Meaning |
| --- | --- |
| Green | Sound or useful within the stated scope. |
| Yellow | Limited; improve before making a broader claim. |
| Red | A specific defect blocks an inference. |
| Gray | Unrun or not assessed. |

Read the four columns separately: **idea**, **evidence**, **scenarios**, **controls**. Green is not launch approval. A valid null or adverse finding is not a red result.

This is a presentation update of [the original dated PI review](../pi-review-2026-10-04/README.md), not a reassessment of later runs. Its source cutoffs remain October 4, 2026, 02:30–03:40 UTC as specified in the original package. Recommendations are editorial, not completed experiments. For the current iteration, see [the direct-launch and native-trace cycle](../pi-direct-launch-trace-cycle-2026-10-04/README.md). For earlier follow-up work, see [the Dmarz response](../pi-review-response-dmarz-2026-10-04/README.md) and [dated confidence/sample-size records](../../../../experiments/EVIDENCE.md).

## Update the guide

Edit `review-guide.json` for experiment assessments and `project-quality.json` for the overall quality table; `guide.css` and `guide.js` control presentation. The archived scientific JSON supplies all 21 detailed study reviews, 110 scenario/condition assessments, 16 original proposals and eight research areas. The original package and its manifest remain unchanged. [Provenance](provenance.json) pins the input hashes and scope.

```sh
python3 build.py
python3 build.py --check
```

`index.html` embeds its data, styles and script. It opens offline with no installation; evidence links require internet access. GitHub displays HTML as source, so download or clone it to view the interactive page.
