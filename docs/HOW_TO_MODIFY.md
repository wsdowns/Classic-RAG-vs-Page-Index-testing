# How to run these notebooks on your own questions

Two Colab notebooks, one question set. Run the same questions through both and compare cost, speed, retrieval and answers.

| Notebook | Method |
|---|---|
| `notebooks/classic_rag.ipynb` | Cut the documents into fixed-size chunks, embed them, retrieve the closest few for each question. |
| `notebooks/pageindex_first_build.ipynb` | The first, more expensive PageIndex build (40-word summaries, thinking on). Same steps as the cheaper notebook; use it to reproduce the first run. |
| `notebooks/pageindex_tree_retrieval.ipynb` | The cheaper rebuild (20-word summaries, tree cached, search with thinking off and on). Build a tree from the documents' headings, summarize each section, let a model read the tree and pick the sections that hold the answer. |

## Before you start

1. **Google Colab and a Gemini API key.** In Colab, open the key icon in the left sidebar, add a secret named `GEMINI_API_KEY`, and switch Notebook access on.
2. **Your documents.** Classic RAG accepts PDF, Word (.docx), .txt and .md. The PageIndex notebook needs **Markdown with real headings** (`#`, `##`, `###`), because the tree is built from the headings. Convert PDFs and Word files to Markdown first.
3. **Privacy.** Everything you upload, and every question, is sent to Google's API. The free tier may use content to improve Google's models. Do not upload anything confidential, privileged, regulated or under an NDA unless your environment has zero data retention or a private instance.
4. **Name the files so they sort in reading order**, for example `Doc1_name.md`, `Doc2_name.md`. Both notebooks join files in file-name order. The PageIndex notebook labels sections `B1-0001`, `B2-0001` by file order, so use at most 9 files.
5. **Cost.** For about 560,000 characters, classic indexing cost about $0.003 and PageIndex indexing about $0.07. Questions cost from about $1.60 to $19 per 1,000 (see `RESULTS_HIGHLIGHTS.md`). Ten questions cost cents.

## Change the questions

**Classic notebook.** Go to the last code cell (its first line is `import json, csv, re, time`) and edit the `QUESTIONS` list. Each item is an id and the question text:

```python
QUESTIONS = [
    ("Q1", "Your first question?"),
    ("Q2", "Your second question?"),
]
```

**PageIndex notebook.** Edit the same `QUESTIONS` list in the cell headed `# Step 8`. Keep the ids identical to the classic notebook so you can compare them.

Tips for a good test set:
- Write questions whose answers you know and can point to in the text. Note where the answer lives.
- Include a few the documents cannot answer (a near miss that sounds answerable). The right behavior is to say there is not enough information.
- Include a question that does not name the document it comes from. This is where retrieval methods differ most.
- Include one with numbers or a table, and one that needs two passages.
- Write the answer key before you run anything.

## Change the settings

**Classic notebook, Step 2A cell** (`PROVIDER`, `CHUNK_SIZE`, `CHUNK_OVERLAP`, `TOP_K`):

| Setting | Default | Meaning |
|---|---|---|
| `CHUNK_SIZE` | 1000 | Characters per chunk |
| `CHUNK_OVERLAP` | 150 | Characters shared between neighbors; must be smaller than `CHUNK_SIZE` |
| `TOP_K` | 4 | Chunks retrieved per question |
| `MAX_CHUNKS` (Step 6 cell) | 1000 | A safety stop. Raise it for a longer corpus |

Change one setting at a time and re-run from Step 4 so you know what caused a difference.

**PageIndex notebook, Step 2 cell** (defaults shown are for the cheaper `pageindex_tree_retrieval.ipynb`; the first-build notebook has `SUMMARY_WORDS = 40`, no `SUMMARY_THINK` switch, and no thinking-off/on search variants):

| Setting | Default | Meaning |
|---|---|---|
| `CHAT_MODEL` | `gemini-2.5-flash` | Model for summaries, search and answers |
| `MAX_NODES` | 4 | Sections the search may pick (set equal to classic's `TOP_K` for a fair comparison) |
| `SUMMARY_WORDS` | 20 | Length of each section summary |
| `SUMMARY_THINK` | `False` | Whether the model "thinks" while writing summaries |
| `MAX_NODE_CHARS` | 12000 | Cap on how much of one section is sent to the answer step |
| `PRICE_IN`, `PRICE_CACHED`, `PRICE_OUT` | 0.30, 0.03, 2.50 | USD per million tokens, used for the cost estimate. **Check your provider's current prices and change these** |

In Step 8, `VARIANTS` runs the search with thinking off and on. Remove one entry to halve the search cost.

If you change the model, the model must support a thinking budget of zero for `think=False` to work. Thinking controls need the `v1beta` API version, which the notebook already sets.

## Score the results with the script (no hand ranking)

The last cell of the PageIndex notebook (Step 9) scores retrieval and answers against facts you list. The same logic is in `auto_score.py`. You need to edit four things:

1. `FACT`: for each answerable question id, one regular expression that matches **any** single required fact. A retrieved passage counts as relevant if its text matches. Example: `"Q3": r"83\.8|0\.239"`.
2. `ANS`: for each answerable id, a list of regular expressions that must **all** match for the answer to count as correct. Example: `"Q3": [r"83\.8", r"0\.239"]`.
3. `UNANSWERABLE`: the ids whose correct behavior is to decline. For these, the answer is correct if it matches `DECLINE`.
4. `DECLINE`: the phrases a refusal uses. Add the wording your model tends to use.

Rules for the keys:
- Write them **before** you look at any answer, from your own answer key.
- Make them loose enough to accept paraphrases (`"deterministic"` not a full sentence) and tight enough to reject wrong answers.
- Check the script against your own judgment on a few questions. In this project it matched 28 of 28 hand-marked passages for PageIndex and 30 of 32 for classic. It checks for facts, not reasoning, so it can pass a right answer given for a wrong reason.

The classic notebook does not score itself. Save its results file and score it with `auto_score.py` (it expects the same result structure: a list of `hits` with `text`, and an `answer`).

## What the runs save

| Notebook | Files | Contents |
|---|---|---|
| Classic | `classic_rerun_results.json`, `classic_rerun_dump.md`, `classic_rerun_results.csv` | Retrieved chunks, answers, tokens, timing, thinking tokens |
| PageIndex | `pi_cheap_results.json`, `pi_cheap_summary.json`, `pi_cheap_dump.md`, `pi_cheap_tree.json` | Retrieved sections, answers, tokens, cached tokens, scores, the tree |

The `dump.md` files list each question with the retrieved passages in full. Read them: the numbers tell you whether something failed, and the passages tell you why.

## Good practice

- Run the classic notebook twice. The retrieved chunks will be identical, but the answers will be reworded and the timings will move. One run does not show that spread.
- Keep the answering model, answer prompt and number of retrieved passages the same across the two systems, so only retrieval changes.
- Read the retrieved passages for every failure and decide whether retrieval or generation failed. They are different problems with different fixes.
- Ten questions cannot rank two systems. They show what kind of failure each has.
- If you rebuild the PageIndex tree, say so. Different summaries can change which sections are found.

## Common problems

| Message | Cause and fix |
|---|---|
| `No key found under the name GEMINI_API_KEY` | The secret is missing or Notebook access is off. |
| `400 INVALID_ARGUMENT ... Thinking is not enabled for api version v1` | The client must use `api_version="v1beta"`. The PageIndex notebook sets this. |
| `STOPPED. N chunks is more than expected` (classic) | Raise `MAX_CHUNKS`, or lower `CHUNK_OVERLAP`. |
| Search returns no sections (PageIndex) | The tree may not match the question. Read the model's reasoning in `pi_cheap_dump.md`. |
| Step 5 seems frozen (PageIndex) | It prints progress every 50 sections. With thinking off, 460 sections take about 4 minutes. |
| Zero cached tokens | Gemini's cache is implicit and not guaranteed. Cost is reported with and without it. |
