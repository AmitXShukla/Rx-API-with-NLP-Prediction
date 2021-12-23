# !pip install scispacy
# !pip install https://urldefense.com/v3/__https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_ner_bc5cdr_md-0.4.0.tar.gz__;!!BZ50a36bapWJ!_16-fIfsVFVDBcawRNdvySRtDW-k6BW3llIgCqWwXPARYOL_O2oJL-ze6lwe6WOblQ$ 
# !pip install https://urldefense.com/v3/__https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_core_sci_lg-0.4.0.tar.gz__;!!BZ50a36bapWJ!_16-fIfsVFVDBcawRNdvySRtDW-k6BW3llIgCqWwXPARYOL_O2oJL-ze6lwiIgfPWw$ 
# !pip install https://urldefense.com/v3/__https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_ner_bionlp13cg_md-0.4.0.tar.gz__;!!BZ50a36bapWJ!_16-fIfsVFVDBcawRNdvySRtDW-k6BW3llIgCqWwXPARYOL_O2oJL-ze6lyYBooRbQ$ 

import spacy
import scispacy
from scispacy.linking import EntityLinker
from scispacy.abbreviation import AbbreviationDetector

nlp_bc5cdr = spacy.load("en_ner_bc5cdr_md")
# Add the abbreviation pipe to the spacy pipeline.
nlp_bc5cdr.add_pipe("abbreviation_detector")
nlp_bc5cdr.add_pipe("scispacy_linker", config={"linker_name": "umls", "resolve_abbreviations": True, "threshold": 0.9})



nlp_sci_lg = spacy.load("en_core_sci_lg")
nlp_sci_lg.add_pipe("abbreviation_detector")
nlp_sci_lg.add_pipe("scispacy_linker", config={"linker_name": "umls", "resolve_abbreviations": True, "threshold": 0.9})
umls_linker = nlp_sci_lg.get_pipe("scispacy_linker")


nlp_bio = spacy.load("en_ner_bionlp13cg_md")
