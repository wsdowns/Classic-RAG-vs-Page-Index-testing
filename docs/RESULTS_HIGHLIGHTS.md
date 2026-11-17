# Results highlights: cost and retrieval

What happened when classic RAG and a PageIndex-style tree retrieval were run on the same corpus, the same ten questions and the same answering model. These are single runs on a small test set. Read them as a description of what kind of behavior each system has, not as a ranking.

## The setup

- **Corpus:** two books by the author, about 88,000 words (558,568 characters), as Markdown.
- **Questions:** ten. Eight have an answer in the text; two do not (a correct answer is to decline).
- **Models:** `gemini-2.5-flash` answers for both systems. `gemini-embedding-001` embeds for classic RAG.
- **Classic RAG:** 658 chunks of 1,000 characters with 150 overlap, top 4 by cosine similarity.
- **PageIndex-style:** 460 heading sections; a model reads the tree of titles and summaries and picks up to 4. It uses PageIndex's Markdown tree builder with a search prompt written for this project, not the PageIndex SDK's own agent.
- **Prices used:** Gemini 2.5 Flash paid tier, $0.30 per million input tokens, $2.50 per million output tokens (thinking tokens count as output), $0.03 per million cached input tokens. Runs were made in November 2026; check current prices.
- **Scoring:** a script checks each retrieved passage and each answer against facts from the answer key. It matched the author's hand marks on 28 of 28 PageIndex passages and 30 of 32 classic passages.

## Retrieval and answers

| Run | Recall | Precision | MRR | First pick relevant | Answers correct | Wrong |
|---|---|---|---|---|---|---|
| Classic RAG (first run) | 8/8 | 0.56 | 0.94 | 7 | 9/10 | Q7 |
| Classic RAG (replay) | 8/8 | 0.56 | 0.94 | 7 | 9/10 | Q7 |
| PageIndex, first build | 7/8 | 0.52 | 0.69 | 5 | 8/10 | Q5, Q7 |
| PageIndex, cheaper build, search thinking off | 8/8 | 0.53 | 0.69 | 4 | 9/10 | Q7 |
| PageIndex, cheaper build, search thinking on | 8/8 | 0.60 | 0.69 | 4 | 10/10 | none |

Recall is over the 8 answerable questions. MRR is the mean reciprocal rank of the first relevant passage.

## Cost and speed per 1,000 questions

| Run | Prompt tokens per question | Seconds per question | Cost, no cache | Cost, with cache |
|---|---|---|---|---|
| Classic RAG | 1,015 | 3.7 | $1.58 | n/a |
| PageIndex, first build | 34,094 | 16.2 | $18.68 | n/a |
| PageIndex, cheaper, thinking off | 20,717 | 5.4 | $8.63 | $3.38 |
| PageIndex, cheaper, thinking on | 20,525 | 13.7 | $13.00 | $8.28 |
| Whole corpus in every prompt (estimate, not run) | about 140,000 | not run | about $42 | about $4.2 |

Classic's cost includes about 401 thinking tokens per question, which the first run did not record. Thinking is 79% of classic's billed output and 88% of the first PageIndex build's.

## One-time indexing cost

| | Time | Input tokens | Output tokens | Thinking tokens | Approximate cost |
|---|---|---|---|---|---|
| Classic RAG (embeddings) | seconds | about 164,000 | none | none | $0.003 |
| PageIndex, first build | 27.5 min | 134,190 | 23,715 | 275,036 | about $0.79 |
| PageIndex, cheaper build | 3.9 min | 138,195 | 10,404 | 0 | about $0.07 |

The cheaper build used 20-word summaries with no lead-in, thinking off while writing them, and put the tree ahead of the question so Gemini could cache it. The tree shrank from 151,746 to 81,402 characters.

## What the failures were

- **Classic, Q7 (generation failure).** The chunk holding the answer was retrieved at rank 2, and the model refused. The chunk never named the book, and a chapter in the other book discussed the same topic with a different answer. Chunking dropped the book and chapter names. This repeated in the replay. Untested fix: prefix each chunk with its book and chapter.
- **PageIndex first build, Q5 (retrieval failure).** The question mentioned a "ledger" without naming a book. The search matched the word in four section titles in the wrong book and never reached the right one. The cheaper build found it. A likely reason, not tested: its summaries state the figures the question asks about, so the question's words had something to match.
- **PageIndex, Q7.** Correct with search thinking on, half-correct with it off.
- **Unanswerable questions.** No system invented an answer. With search thinking on, one PageIndex run refused one of them for the wrong reason: the search selected no sections.

## Takeaways

1. **Thinking is most of the bill.** On the cheaper tree, turning thinking off for the search step cut the cost by about a third ($13.00 to $8.63), and caching cut what remained by more than half ($3.38). Where an answer needs care, it bought accuracy on one question.
2. **PageIndex's cost is the tree.** Every search reads the whole tree, so cost scales with the number of sections and the length of their summaries, not with the question.
3. **Cheaper was not worse here.** The cheaper PageIndex build matched classic's recall and was at least as accurate. One run on ten questions cannot show that this holds in general.
4. **Provenance matters.** A chunk that does not say where it came from invites a refusal. A section path in the prompt (book, chapter, section) fixed that for PageIndex.
5. **Retrieval is repeatable; generation is not.** Replaying classic retrieved identical chunks on all ten questions but reworded nine answers.
6. **Classic is still the cheapest and fastest.** It cost about $1.58 per 1,000 questions and answered in 3.7 s. PageIndex's draw is that it needs no vector store and keeps the document's structure.

## Limits

Ten questions, one run per setting, one corpus written by the person who wrote the questions. The cheaper PageIndex build was rebuilt from scratch, so its differences from the first build cannot be traced to a single change. The scoring script checks for facts, not reasoning.
