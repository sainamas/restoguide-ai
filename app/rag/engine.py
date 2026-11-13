from pathlib import Path
from typing import TypedDict

import json
import re

import faiss
from ddgs import DDGS
from langgraph.graph import END, StateGraph
from sentence_transformers import SentenceTransformer

from app.services.documents import load_file
from app.services.operational_analysis import get_operational_evidence
from app.services.operational_reasoning import (
    build_operational_reasoning_context,
)


class State(TypedDict, total=False):
    question: str
    hits: list[dict]
    use_web: bool
    web: list[dict]
    answer: str
    sources: list[dict]
    route: str

    operational: bool
    operational_evidence: dict
    reasoning_context: dict


class Engine:
    def __init__(
        self,
        model_name,
        index_dir,
        top_k=5,
        threshold=0.70,
        web=True,
    ):
        self.model = SentenceTransformer(model_name)
        self.folder = Path(index_dir)
        self.folder.mkdir(parents=True, exist_ok=True)

        self.k = top_k
        self.threshold = threshold
        self.web = web

        self.docs = []
        self.index = None

        self._load()

    def _load(self):
        index_path = self.folder / "index.faiss"
        metadata_path = self.folder / "docs.json"

        if index_path.exists() and metadata_path.exists():
            self.index = faiss.read_index(str(index_path))
            self.docs = json.loads(
                metadata_path.read_text(encoding="utf-8")
            )

    def rebuild(self, folder):
        docs = []

        for path in Path(folder).rglob("*"):
            if (
                path.is_file()
                and path.suffix.lower()
                in {
                    ".pdf",
                    ".docx",
                    ".txt",
                    ".md",
                }
            ):
                docs += load_file(path)

        self.docs = docs

        if not docs:
            self.index = None
            return 0

        vectors = self.model.encode(
            [doc["text"] for doc in docs],
            normalize_embeddings=True,
        ).astype("float32")

        self.index = faiss.IndexFlatIP(vectors.shape[1])
        self.index.add(vectors)

        faiss.write_index(
            self.index,
            str(self.folder / "index.faiss"),
        )

        (self.folder / "docs.json").write_text(
            json.dumps(docs, ensure_ascii=False),
            encoding="utf-8",
        )

        return len(docs)

    def _title_match_score(self, question, document):
        text = document.get("text", "")

        first_line = next(
            (
                line.strip()
                for line in text.splitlines()
                if line.strip()
            ),
            "",
        )

        title = re.sub(r"^#+\s*", "", first_line)

        title = re.split(
            r"\bCategory\s*:",
            title,
            flags=re.IGNORECASE,
        )[0]

        title = re.sub(
            r"\b(?:REC|REF)-\d+\b",
            "",
            title,
            flags=re.IGNORECASE,
        )

        stop_words = {
            "how",
            "do",
            "i",
            "prepare",
            "make",
            "the",
            "a",
            "an",
            "what",
            "is",
            "for",
            "to",
            "of",
        }

        question_words = set(
            re.findall(r"[a-z0-9]+", question.lower())
        )

        title_words = set(
            re.findall(r"[a-z0-9]+", title.lower())
        )

        question_words -= stop_words
        title_words -= stop_words

        if not title_words:
            return 0.0

        return len(question_words & title_words) / len(title_words)

    def retrieve(self, q):
        """
        Retrieve and rank internal restaurant documents.

        Relevance is based on:
        1. Semantic similarity from the embedding model.
        2. Keyword overlap between the question and document title.
        """

        if self.index is None or not self.docs:
            return []

        vector = self.model.encode(
            [q],
            normalize_embeddings=True,
        ).astype("float32")

        scores, ids = self.index.search(
            vector,
            min(self.k, len(self.docs)),
        )

        results = []

        for score, doc_id in zip(scores[0], ids[0]):
            if doc_id < 0:
                continue

            document = self.docs[int(doc_id)]

            semantic_score = float(score)

            title_score = self._title_match_score(
                q,
                document,
            )

            relevance_score = (
                semantic_score + (0.20 * title_score)
            )

            results.append(
                {
                    **document,
                    "score": semantic_score,
                    "title_score": title_score,
                    "relevance_score": relevance_score,
                }
            )

        results.sort(
            key=lambda item: item["relevance_score"],
            reverse=True,
        )

        return results

    def web_search(self, q):
        """
        Search the external web when internal restaurant
        knowledge is not sufficiently relevant.
        """

        if not self.web:
            return []

        try:
            with DDGS() as search:
                return [
                    {
                        "text": (
                            f'{result.get("title", "")}. '
                            f'{result.get("body", "")}'
                        ),
                        "source": result.get(
                            "title",
                            "Web result",
                        ),
                        "url": result.get("href", ""),
                        "source_type": "external",
                        "score": None,
                    }
                    for result in search.text(
                        q,
                        max_results=4,
                    )
                ]

        except Exception as e:
            print(f"Web search error: {e}")
            return []

    def rebuild_from_documents(self, docs):
        """
        Rebuild the FAISS index from an already-loaded
        list of documents.
        """

        self.docs = docs

        if not docs:
            self.index = None
            return 0

        vectors = self.model.encode(
            [doc["text"] for doc in docs],
            normalize_embeddings=True,
        ).astype("float32")

        self.index = faiss.IndexFlatIP(vectors.shape[1])
        self.index.add(vectors)

        faiss.write_index(
            self.index,
            str(self.folder / "index.faiss"),
        )

        (self.folder / "docs.json").write_text(
            json.dumps(docs, ensure_ascii=False),
            encoding="utf-8",
        )

        return len(docs)

    def _is_operational_question(self, question):
        """
        Detect whether the question requires structured
        restaurant operational data.

        This is intentionally conservative. Questions that
        clearly ask about waste, sales, preparation, inventory,
        purchasing, or branch performance are routed to the
        operational evidence path.
        """

        operational_terms = {
            "waste",
            "wasted",
            "food waste",
            "sales",
            "sold",
            "selling",
            "preparation",
            "prepared",
            "inventory",
            "stock",
            "spoilage",
            "purchase",
            "purchases",
            "branch",
            "branches",
            "performance",
            "demand",
            "remaining",
            "over-preparation",
        }

        normalized = question.lower()

        return any(
            term in normalized
            for term in operational_terms
        )

    def _build(self):
        graph = StateGraph(State)

        def classify_question(state):
            question = state["question"]

            return {
                "operational": self._is_operational_question(
                    question
                )
            }

        def retrieve_node(state):
            return {
                "hits": self.retrieve(
                    state["question"]
                )
            }

        def grade(state):
            sufficient_evidence = bool(
                state.get("hits")
                and state["hits"][0]["relevance_score"]
                >= self.threshold
            )

            return {
                "use_web": not sufficient_evidence,
                "route": (
                    "internal"
                    if sufficient_evidence
                    else "web"
                ),
            }

        def search(state):
            return {
                "web": self.web_search(
                    state["question"]
                )
            }

        def operational_data_node(state):
            return {
                "operational_evidence": (
                    get_operational_evidence()
                )
            }

        def operational_rag_node(state):
            return {
                "hits": self.retrieve(
                    state["question"]
                )
            }

        def operational_context_node(state):
            return {
                "reasoning_context": (
                    build_operational_reasoning_context(
                        question=state["question"],
                        operational_evidence=(
                            state["operational_evidence"]
                        ),
                        rag_evidence=state.get(
                            "hits",
                            [],
                        ),
                    )
                )
            }

        def operational_answer(state):
            context = state["reasoning_context"]

            return self._answer_operational(
                state["question"],
                context,
            )

        def answer_internal(state):
            hits = [
                hit
                for hit in state["hits"]
                if hit["relevance_score"]
                >= self.threshold
            ]

            return self._answer(
                state,
                hits,
                "internal",
            )

        def answer_web(state):
            return self._answer(
                state,
                state.get("web", []),
                "web",
            )

        graph.add_node(
            "classify",
            classify_question,
        )

        graph.add_node(
            "retrieve",
            retrieve_node,
        )

        graph.add_node(
            "grade",
            grade,
        )

        graph.add_node(
            "search",
            search,
        )

        graph.add_node(
            "internal_answer",
            answer_internal,
        )

        graph.add_node(
            "web_answer",
            answer_web,
        )

        graph.add_node(
            "operational_data",
            operational_data_node,
        )

        graph.add_node(
            "operational_rag",
            operational_rag_node,
        )

        graph.add_node(
            "operational_context",
            operational_context_node,
        )

        graph.add_node(
            "operational_answer",
            operational_answer,
        )

        graph.set_entry_point("classify")

        graph.add_conditional_edges(
            "classify",
            lambda state: (
                "operational"
                if state["operational"]
                else "rag"
            ),
            {
                "operational": "operational_data",
                "rag": "retrieve",
            },
        )

        graph.add_edge(
            "operational_data",
            "operational_rag",
        )

        graph.add_edge(
            "operational_rag",
            "operational_context",
        )

        graph.add_edge(
            "operational_context",
            "operational_answer",
        )

        graph.add_edge(
            "operational_answer",
            END,
        )

        graph.add_edge(
            "retrieve",
            "grade",
        )

        graph.add_conditional_edges(
            "grade",
            lambda state: (
                "search"
                if state["use_web"]
                else "internal_answer"
            ),
            {
                "search": "search",
                "internal_answer": "internal_answer",
            },
        )

        graph.add_edge(
            "search",
            "web_answer",
        )

        graph.add_edge(
            "web_answer",
            END,
        )

        graph.add_edge(
            "internal_answer",
            END,
        )

        return graph.compile()

    def _answer_operational(
        self,
        question,
        context,
    ):
        facts = context.get(
            "observed_facts",
            [],
        )

        knowledge = context.get(
            "restaurant_knowledge",
            [],
        )

        contributors = context.get(
            "potential_contributors",
            [],
        )

        gaps = context.get(
            "evidence_gaps",
            [],
        )

        sections = [
            "Operational analysis for: "
            + question,
            "",
            "Observed operational evidence:",
        ]

        if facts:
            sections.extend(
                f"- {fact}"
                for fact in facts
            )
        else:
            sections.append(
                "- No operational evidence was found."
            )

        sections.append(
            "\nRelevant internal restaurant knowledge:"
        )

        if knowledge:
            for item in knowledge[:3]:
                sections.append(
                    f"- {item.get('title') or item.get('source')}: "
                    f"{item.get('content', '')[:500]}"
                )
        else:
            sections.append(
                "- No relevant internal knowledge was retrieved."
            )

        sections.append(
            "\nPotential contributors:"
        )
        if contributors:
           for contributor in contributors:
                sections.append(
                    f"- {contributor}"
            )
        else:
         sections.append(
                   "- No potential contributor was identified "
                   "from the current evidence."
            )
       
        

        sections.append(
            "\nEvidence limitation:"
        )

        sections.extend(
            f"- {gap}"
            for gap in gaps
        )

        return {
            "answer": "\n".join(sections),
            "sources": knowledge,
            "route": "operational",
            "operational_evidence": (
                context.get(
                    "observed_facts",
                    [],
                )
            ),
        }

    def _answer(self, state, hits, route):
        if not hits:
            message = (
                "I could not find sufficiently relevant evidence. "
                "Please check with an authorised manager."
            )

        elif route == "internal":
            details = "\n\n---\n\n".join(
                item["text"][:1000]
                for item in hits[:3]
            )

            message = (
                "Information retrieved from internal "
                "restaurant documents:\n\n"
                + details
            )

        else:
            result_sections = []

            for number, hit in enumerate(
                hits[:4],
                start=1,
            ):
                title = (
                    hit.get("source")
                    or f"Web result {number}"
                )

                description = (
                    hit.get("text", "")
                    .strip()
                )

                url = (
                    hit.get("url", "")
                    .strip()
                )

                section = (
                    f"{number}. {title}\n"
                    f"{description[:700]}"
                )

                if url:
                    section += (
                        f"\nSource: {url}"
                    )

                result_sections.append(section)

            message = (
                "No sufficient internal evidence "
                "was found.\n\n"
                "External web information "
                "(not approved restaurant procedures):\n\n"
                + "\n\n---\n\n".join(
                    result_sections
                )
            )

        return {
            "answer": message,
            "sources": hits,
            "route": route,
        }

    def ask(self, q):
        return self._build().invoke(
            {"question": q}
        )