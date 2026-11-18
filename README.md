# Classic RAG vs PageIndex testing

Two retrieval methods compared on the same corpus, the same ten questions and the same answering model (gemini-2.5-flash). Built for CBIS 5530, Introduction to RAG (final project).

| Notebook | What it does |
|---|---|
| `notebooks/classic_rag.ipynb` | Classic vector RAG: 1,000-character chunks with 150 overlap, gemini-embedding-001, top-4 cosine retrieval. Records thinking tokens and the question-embedding time per question. |
| `notebooks/pageindex_first_build.ipynb` | The first PageIndex-style build: 40-word node summaries written with thinking on, the question placed before the tree in the search prompt, one search run. It was the expensive one (about $18.68 per 1,000 questions). Kept so the first result can be rerun and compared. |
| `notebooks/pageindex_tree_retrieval.ipynb` | The cheaper PageIndex-style rebuild: 20-word summaries written with thinking off, the tree placed before the question so Gemini can cache it, and the search run twice (thinking off, then on). Same heading tree, same answer prompt. |
| `auto_score.py` | Scores retrieval and answers by script against ground-truth facts (also embedded in the PageIndex notebook). No hand ranking. |

## Documentation

- [`docs/HOW_TO_MODIFY.md`](docs/HOW_TO_MODIFY.md): how to run both notebooks on your own documents and questions, change the settings, and score the results.
- [`docs/RESULTS_HIGHLIGHTS.md`](docs/RESULTS_HIGHLIGHTS.md): the cost and retrieval numbers from the original test.

## Running

Both notebooks are for Google Colab. Add a Colab secret named `GEMINI_API_KEY` (Notebook access on), run the cells in order, and upload your own Markdown corpus files when asked. The corpus is not included in this repository. The ten test questions and ground-truth patterns are written for the author's two books, so use your own documents by replacing the questions and the fact patterns.

## Notes

- The two PageIndex notebooks differ in several things at once (summary length, summary thinking, tree position in the prompt, and the extra thinking-on search run), so the cost and accuracy gap between them cannot be traced to one change.
- The first-build notebook has no scoring cell. Score its saved results with `auto_score.py`.
- The PageIndex notebook uses PageIndex's Markdown tree builder with a search prompt written for this project. It is not the PageIndex SDK's own agent.
- Notebooks are stored without outputs.
