from typing import Union, List

from danlp.download import DEFAULT_CACHE_DIR, download_model, \
    _unzip_process_func

from spacy.tokens import Doc

def load_spacy_model(cache_dir=DEFAULT_CACHE_DIR, verbose=False, textcat=None, vectorError=False):
    """
    Loads a spacy model.
    
    OBS vectorError is a TEMP ugly work around error encounted by keeping two models an not been able to find referece name for vectros
    """
    from spacy.util import load_model_from_path

    if textcat==None or vectorError==True:
        modelname='spacy'

        model_weight_path = download_model(modelname, cache_dir,
                                           process_func=_unzip_process_func,
                                           verbose=verbose)
        nlp = load_model_from_path(model_weight_path)
        
    
    if textcat=='sentiment':
        modelname='spacy.sentiment'
        
        model_weight_path = download_model(modelname, cache_dir,
                                           process_func=_unzip_process_func,
                                           verbose=verbose)
        # quick fix from not aligned models storage:
        import os
        model_weight_path =  os.path.join(model_weight_path, 'spacy.sentiment')
        
        nlp = load_model_from_path(model_weight_path)
    
    
    return nlp


def load_spacy_chunking_model(spacy_model=None,cache_dir=DEFAULT_CACHE_DIR, verbose=False):
    return SpacyChunking(model=spacy_model, cache_dir=cache_dir, verbose=verbose)



class SpacyChunking:
    """
    Spacy Chunking Model 
    """

    def __init__(self, model=None, cache_dir=DEFAULT_CACHE_DIR, verbose=False):

        if model == None:
            self.model = load_spacy_model(cache_dir=cache_dir, verbose=verbose)
        else:
            self.model = model

    def predict(self, text: Union[str, List[str]], bio=True):
        """
        Predict NP chunks (BIO format) from raw text or tokenized text.

        E.g. "Jeg kommer fra en lille by." become 
            - a list of BIO tags: ['B-NP', 'O', 'O', 'O', 'B-NP', 'I-NP', 'I-NP']
            - or a list of triplets (start id, end id, chunk label): [(0, 1, 'NP'), (4, 7, 'NP')]

        :param text: Can either be a raw text or a list of tokens
        :param bool bio: True to return a list of BIO labels (same length as the sentence), False to return a list of NP-chunks
        :return: NP chunks
        """
        
        if isinstance(text, str):
            doc = self.model(text)

            return get_noun_chunks(doc, bio=bio)

        if isinstance(text, list):

            parser = self.model.parser
            tagger = self.model.tagger

            doc = Doc(self.model.vocab, words=text)
            doc = tagger(doc)
            doc = parser(doc)

            return get_noun_chunks(doc, bio=bio)




left_labels = ["det", "fixed", "nmod:poss", "amod", "flat", "goeswith", "nummod", "appos"]
right_labels = ["fixed", "nmod:poss", "amod", "flat", "goeswith", "nummod", "appos"]
stop_labels = ["punct"]

np_label = "NP"

def get_noun_chunks(spacy_doc, bio=True, nested=False):

    def is_verb_token(tok):
        return tok.pos_ in ['VERB', 'AUX']

    def get_left_bound(doc, root):
        left_bound = root
        for tok in reversed(list(root.lefts)):
            if tok.dep_ in left_labels:
                left_bound = tok
        return left_bound

    def get_right_bound(doc, root):
        right_bound = root
        for tok in root.rights:
            if tok.dep_ in right_labels:
                right = get_right_bound(doc, tok)
                if list(
                    filter(
                        lambda t: is_verb_token(t) or t.dep_ in stop_labels,
                        doc[root.i : right.i],
                    )
                ):
                    break
                else:
                    right_bound = right
        return right_bound

    def get_bounds(doc, root):
        return get_left_bound(doc, root), get_right_bound(doc, root)


    chunks = []
    for token in spacy_doc:
        if token.pos_ in ["PROPN", "NOUN", "PRON"]:
            left, right = get_bounds(spacy_doc, token)
            chunks.append((left.i, right.i + 1, np_label))
            token = right

    is_chunk = [True for _ in chunks]
    if not nested:
        # remove nested chunks
        for i, i_chunk in enumerate(chunks[:-1]):
            i_left, i_right, _ = i_chunk 
            for j, j_chunk in enumerate(chunks[i+1:], start=i+1):
                j_left, j_right, _ = j_chunk
                if j_left <= i_left < i_right <= j_right:
                    is_chunk[i] = False
                if i_left <= j_left < j_right <= i_right:
                    is_chunk[j] = False

    final_chunks = [c for c, ischk in zip(chunks, is_chunk) if ischk]
    return chunks2bio(final_chunks, len(spacy_doc)) if bio else final_chunks

def chunks2bio(chunks, sent_len):
    bio_tags = ['O'] * sent_len
    for (start, end, label) in chunks:
        bio_tags[start] = 'B-'+label
        for j in range(start+1, end):
            bio_tags[j] = 'I-'+label
    return bio_tags