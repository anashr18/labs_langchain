"""Wrapper for wikipedia."""
from typing import Tuple, Optional
from labs_langchain.docstore.base import Docstore
from labs_langchain.docstore.document import Document

class Wikipedia(Docstore):
    """Wrapper around wikipedia API."""
    def __init__(self):
        """Check that if Wikipedia package is intalled."""
        try:
            import wikipedia
        except ImportError:
            raise ValueError(
                "Could not import wikipedia python package. "
                "Please it install it with `pip install wikipedia`."
            )

    def search(self, search: str)-> Tuple[str, Optional[Document]]:
        """Search for document.

        If page exists, return the page summary, and a Document object.
        If page does not exist, return similar entries.
        """
        import wikipedia
        try:
            page_content = wikipedia.page(search).content
            wiki_document = Document(page_content=page_content)
            observation = wiki_document.summary
        except wikipedia.PageError:
            wiki_document = None
            observation = f"Could not find {search}. Similar: {wikipedia.search(search)}"
        except wikipedia.DisambiguationError:
            wiki_document = None
            observation = f"Could not find {search}. Similar: {wikipedia.search(search)}"
        return observation, wiki_document
        
