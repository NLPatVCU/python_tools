"""Parse BRAT format files"""
__author__ = "Nicholas Rodriguez"

from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from typing import List, Union, Set, Tuple
import warnings


@dataclass
class TextAnnotation:
    """Class for storing an NER annotation."""
    tid: str
    entity_type: str
    start: int
    end: int
    text: str


@dataclass
class RelAnnotation:
    """Class for storing Relation Extraction annotations"""
    rid: str
    rel_type: str
    arg1: str
    arg2: str


class BratParse:
    """Parses BRAT/standoff formatted files.

    Args:
        path_to_annotations (Path or str): path to directory containing annotation files in BRAT/Standoff format.
        skip_list (List[str]): a list containing the basename of the files to be skipped.

    Attributes:
        doc_ids (List[str]): list of basenames of the annotations and text files (both should have the same basenames).
        text_files (List: list of text files found in the path to annotations as <annotation_basename>.txt.
        ann_files: list of annotation files found as <annotation_basename>.ann.

    Returns:
        an iterable object containing text and annotations (see examples).

    Examples:
        >>> bp = BratParse(path_to_annotations="data/processed/brat_files/")
        >>> print(bp.doc_ids)
        >>> print(bp.text_files)
        >>> print(bp.ann_files)
        # Get one file's annotations. Currently doesn't support slicing
        >>> one_annotation = bp[0]
        # Parse into a list of tuples
        >>> all_annotations = [(text, annotations) for text, annotations in bp]
        # Parse into a dictionary indexed by document basename
        >>> all_annotations = {bp.doc_ids[i]: {'text': text, 'annotations': annotations} for i, (text, annotations) in enumerate(bp)}
    """

    def __init__(self,
                 path_to_annotations: Union[str, PathLike[str]],
                 skip_list: List[str] = None):

        self.skip_list = skip_list if skip_list is not None else []
        self.path_to_annotations = Path(path_to_annotations)
        self.path_to_text = Path(path_to_annotations)
        self.doc_ids = sorted(
            [text_file.stem for text_file in self.path_to_text.glob('*txt') if text_file.stem not in self.skip_list])
        self.text_files = sorted(
            [text_file for text_file in self.path_to_text.glob('*txt') if text_file.stem not in self.skip_list])
        self.ann_files = sorted(
            [ann_file for ann_file in self.path_to_text.glob('*ann') if ann_file.stem not in self.skip_list])
        assert all(x.stem == y.stem for x, y in zip(self.text_files, self.ann_files))

    def _parse_annotations(self, annlines, textlines, doc_idx):
        """
        Parses annotations for a single file pair
        Args:
            annlines: list of strings containing brat format annotations
            textlines: a string of text to which annotations refer
            doc_idx: the document index (for printing warnings)

        Returns:
            List of annotations
        """
        current_annotations = []
        for line in annlines:
            if line.startswith('T'):  # text bound annotations
                tid, type_span, text = line.strip().split('\t')
                assert len(type_span.split(
                    ' ')) == 3, 'Text bound annotation should be a tuple containing type, start, end'
                entity_type, span_start, span_end = type_span.split(' ')
                span_start, span_end = int(span_start), int(span_end)
                current_annotation = TextAnnotation(tid, entity_type, span_start, span_end, text)
                current_annotations.append(current_annotation)
                if not current_annotation.text == textlines[span_start: span_end]:
                    warnings.warn(
                        f'In document {self.doc_ids[doc_idx]}, '
                        f'annotation text for `{current_annotation.text}` '
                        f'does not match document `{textlines[span_start: span_end]}`. '
                        f'Check offsets {span_start} {span_end}')
            elif line.startswith('R'):  # relation annotation
                rid, info_tuple = line.strip().split('\t')
                assert len(info_tuple.split(' ')) == 3, 'Relation annotation should contain rid, type, arg1, arg2'
                rel_type, arg1, arg2 = info_tuple.split(' ')
                current_annotations.append(
                    RelAnnotation(rid, rel_type, arg1.replace('Arg1:', ''), arg2.replace('Arg2:', ''))
                )
        return current_annotations

    def __len__(self):
        return len(self.ann_files)

    def __getitem__(self, doc_idx: int):
        """
        Gets a text and annotations from a single document by index

        Args:
            doc_idx (int): index of document to parse

        Returns:
            a tuple containing the text and a list of annotations as `TextAnnotation` or `RelAnnotation`.
        """
        # Get sentence-level NER and RE data
        # should be a valid ann file
        with open(self.ann_files[doc_idx]) as annfile:
            annlines = annfile.readlines()
        with open(self.text_files[doc_idx]) as textfile:
            textlines = textfile.read()
        annotations = self._parse_annotations(annlines, textlines, doc_idx)
        return textlines, annotations
