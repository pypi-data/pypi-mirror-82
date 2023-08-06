from Corpus.Corpus cimport Corpus


cdef class AnnotatedCorpus(Corpus):

    cpdef checkMorphologicalAnalysis(self)
    cpdef checkNer(self)
    cpdef checkShallowParse(self)
    cpdef checkSemantic(self)
