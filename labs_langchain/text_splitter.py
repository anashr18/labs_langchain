"""Functionality for splitting text."""
from abc import abstractmethod
from typing import List

class TextSplitter:
    """Interface for splitting text into chunks"""
    @abstractmethod
    def split_text(self, text:str)->List[str]:
        """Split text into multiple chunks."""

class CharacterTextSplitter(TextSplitter):
    def __init__(self, seperator="\n\n", chunk_size=4000, chunk_overlap=200):
        """Initialize with params"""
        if chunk_size < chunk_overlap:
            raise ValueError(
                "Chunk size should be larger than chunk ovrlap"
                f"Chunksize:{chunk_size} ChunkOverlap:{chunk_overlap}"
            )
        self._seperator = seperator
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap

    def split_text(self, text)-> List[str]:
        """Split text into multiple chunks."""
        splits = text.split(self._seperator)
        total = 0
        docs = []
        current_doc:List[str] = []
        for d in splits:
            if total > self._chunk_size:
                docs.append(self._seperator.join(current_doc))
                while total > self._chunk_overlap:
                    total =-len(current_doc[0])
                    current_doc = current_doc[1:]
            total =+ len(d)
            current_doc.append(d)
        docs.append(self._seperator.join(current_doc))
        return docs
