#!/usr/bin/env python3

import unicodedata

import regex as re


def align_nfc(nfc, orig):
    """Character alignment from NFC version to original string."""
    assert len(nfc) <= len(orig)
    alignment = {}
    if nfc == "":
        assert orig == ""
        return alignment
    nfc_i, nfc_j = 0, 0
    orig_i, orig_j = 0, 0
    assert unicodedata.combining(nfc[0]) == 0
    assert unicodedata.combining(orig[0]) == 0
    while nfc_j < len(nfc):
        nfc_j = nfc_i + 1
        while (nfc_j < len(nfc)) and (unicodedata.combining(nfc[nfc_j]) > 0):
            nfc_j += 1
        orig_j = orig_i + 1
        while (orig_j < len(orig)) and (unicodedata.combining(orig[orig_j]) > 0):
            orig_j += 1
        assert nfc[nfc_i:nfc_j] == unicodedata.normalize("NFC", orig[orig_i:orig_j])
        alignment[(nfc_i, nfc_j)] = (orig_i, orig_j)
        nfc_i = nfc_j
        orig_i = orig_j
    assert orig_j == len(orig)
    return alignment


def token_offsets(tokens, raw):
    """Determine start and end positions of tokens in the original raw (NFC) input."""
    offsets = []
    raw_i = 0
    for token in tokens:
        text = token.text
        if token.original_spelling is not None:
            text = token.original_spelling
        pattern = ".*?(" + ".*?".join([re.escape(c) for c in text]) + ")"
        m = re.search(pattern, raw, pos=raw_i)
        assert m
        start, end = m.span(1)
        offsets.append((start, end))
        raw_i = end
    return offsets
