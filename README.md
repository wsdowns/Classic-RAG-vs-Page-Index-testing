# Classic RAG vs PageIndex testing

Two retrieval methods compared on the same corpus, the same ten questions and the same answering model (gemini-2.5-flash). Built for CBIS 5530, Introduction to RAG (final project).

| Notebook | What it does |
|---|---|
| `notebooks/classic_rag.ipynb` | Classic vector RAG: 1,000-character chunks with 150 overlap, gemini-embedding-001, top-4 cosine retrieval. Records thinking tokens and the question-embedding time per question. |
| `notebooks/pageindex_tree_retrieval.ipynb` | PageIndex-style vectorless retrieval: a heading tree built with PageIndex's Markdown indexer, short node summaries, and a model that reads the tree to pick sections. Runs the search with thinking off and on. |
| `auto_score.py` | Scores retrieval and answers by script against ground-truth facts (also embedded in the PageIndex notebook). No hand ranking. |

## Documentation

- [`docs/HOW_TO_MODIFY.md`](docs/HOW_TO_MODIFY.md): how to run both notebooks on your own documents and questions, change the settings, and score the results.
- [`docs/RESULTS_HIGHLIGHTS.md`](docs/RESULTS_HIGHLIGHTS.md): the cost and retrieval numbers from the original test.

## Running

Both notebooks are for Google Colab. Add a Colab secret named `GEMINI_API_KEY` (Notebook access on), run the cells in order, and upload your own Markdown corpus files when asked. The corpus is not included in this repository. The ten test questions and ground-truth patterns are written for the author's two books, so use your own documents by replacing the questions and the fact patterns.

## Notes

- The PageIndex notebook uses PageIndex's Markdown tree builder with a search prompt written for this project. It is not the PageIndex SDK's own agent.
- Notebooks are stored without outputs.
