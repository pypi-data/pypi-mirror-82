from AnnotatedTree.ParseTreeDrawable cimport ParseTreeDrawable


cdef class AutoMetaMorphemeMover:

    cpdef metaMorphemeMoveWithRules(self, ParseTreeDrawable parseTree):
        pass

    cpdef autoPosMove(self, ParseTreeDrawable parseTree):
        self.metaMorphemeMoveWithRules(parseTree)
        parseTree.saveWithFileName()
