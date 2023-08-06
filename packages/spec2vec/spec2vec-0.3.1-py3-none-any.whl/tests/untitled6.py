import sys
sys.path.insert(0, "C:\\OneDrive - Netherlands eScience Center\\Project_Wageningen_iOMEGA\\matchms")


import numpy
from matchms import Spectrum
from spec2vec import SpectrumDocument
from spec2vec.model_building import set_learning_rate_decay
from spec2vec.model_building import train_new_word2vec_model


# def test_set_learning_rate_decay():
#     """Test if correct alpha and min_alpha are calculated."""
#     alpha, min_alpha = set_learning_rate_decay(0.5, 0.05, 8)
#     assert alpha == 0.5, "Expected different alpha."
#     assert min_alpha == 0.5 - 8 * 0.05, "Expected different min_alpha"


# def test_set_learning_rate_decay_rate_too_high():
#     """Test if correct alpha and min_alpha are calculated if rate is too high."""
#     alpha, min_alpha = set_learning_rate_decay(0.5, 0.05, 20)
#     assert alpha == 0.5, "Expected different alpha."
#     assert min_alpha == 0.0, "Expected different min_alpha"



"""Test training of a dummy model."""
# Create fake corpus
documents = []
for i in range(100):
    spectrum = Spectrum(mz=numpy.linspace(i, 9+i,10),
                        intensities=numpy.ones((10)).astype("float"),
                        metadata={})
    documents.append(SpectrumDocument(spectrum, n_decimals=1))
model = train_new_word2vec_model(documents, iterations=20, size=10, negative=0,
                                 progress_logger=False)

assert model.sg == 0, "Expected different default value."
assert model.negative == 0, "Expected changed default value."
assert model.window == 500, "Expected different default value."
assert model.alpha == 0.025, "Expected different default value."
assert model.min_alpha == 0.02, "Expected different default value."
assert model.epochs == 20, "Expected differnt number of epochs."
assert model.wv.vector_size == 10, "Expected differnt vector size."
assert len(model.wv.vocab) == 109, "Expected different number of words in vocab."
assert model.wv.get_vector(documents[0].words[1]).shape[0] == 10, "Expected differnt vector size."
