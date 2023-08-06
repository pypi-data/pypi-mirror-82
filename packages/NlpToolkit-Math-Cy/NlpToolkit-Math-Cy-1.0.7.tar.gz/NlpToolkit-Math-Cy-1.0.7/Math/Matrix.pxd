from Math.Vector cimport Vector


cdef class Matrix(object):

    cdef int __row, __col
    cdef list __values

    cpdef initZeros(self)
    cpdef Matrix clone(self)
    cpdef double getValue(self, int rowNo, int colNo)
    cpdef setValue(self, int rowNo, int colNo, double value)
    cpdef addValue(self, int rowNo, int colNo, double value)
    cpdef increment(self, int rowNo, int colNo)
    cpdef int getRow(self)
    cpdef Vector getRowVector(self, int row)
    cpdef int getColumn(self)
    cpdef list getColumnVector(self, int column)
    cpdef columnWiseNormalize(self)
    cpdef multiplyWithConstant(self, double constant)
    cpdef divideByConstant(self, double constant)
    cpdef add(self, Matrix m)
    cpdef addRowVector(self, int rowNo, Vector v)
    cpdef subtract(self, Matrix m)
    cpdef Vector multiplyWithVectorFromLeft(self, Vector v)
    cpdef Vector multiplyWithVectorFromRight(self, Vector v)
    cpdef double columnSum(self, int columnNo)
    cpdef Vector sumOfRows(self)
    cpdef double rowSum(self, int rowNo)
    cpdef Matrix multiply(self, Matrix m)
    cpdef Matrix elementProduct(self, Matrix m)
    cpdef double sumOfElements(self)
    cpdef double trace(self)
    cpdef Matrix transpose(self)
    cpdef Matrix partial(self, int rowStart, int rowEnd, int colStart, int colEnd)
    cpdef bint isSymmetric(self)
    cpdef double determinant(self)
    cpdef inverse(self)
    cpdef Matrix choleskyDecomposition(self)
    cpdef __rotate(self, double s, double tau, int i, int j, int k, int l)