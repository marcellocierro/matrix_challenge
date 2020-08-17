#!/usr/local/bin/python3

import numpy as np
import unittest
import matrix_challenge


class testMatrixChallenge(unittest.TestCase):

    def setUp(self):
        self.matrix1 = np.random.rand(2, 3)
        self.matrix2 = np.random.rand(3, 5)

        self.matrix3 = np.random.rand(2, 3)
        self.matrix4 = np.random.rand(7, 5)

    def tearDown(self):
        pass

    def testMatrixCompatibility(self):
        result = matrix_challenge.checkMatrixCompatibility(self.matrix1, self.matrix2)
        self.assertTrue(result)

        result = matrix_challenge.checkMatrixCompatibility(self.matrix3, self.matrix4)
        self.assertFalse(result)

    def testMatrixMultiplication(self):
        result = matrix_challenge.multiplyMatrices(self.matrix1, self.matrix2)
        self.assertIsNot(False, result)

        result = matrix_challenge.multiplyMatrices(self.matrix3, self.matrix4)
        self.assertFalse(result)


    def testCumulativeProduct(self):
        multiplied_matrix = matrix_challenge.multiplyMatrices(self.matrix1, self.matrix2)

        result = matrix_challenge.calcCumulativeProduct(multiplied_matrix, 'sdsd')
        self.assertFalse(result)

        result = matrix_challenge.calcCumulativeProduct(multiplied_matrix, 2)
        self.assertFalse(result)

        result = matrix_challenge.calcCumulativeProduct(multiplied_matrix, 1)
        self.assertIsNot(False, result)

        result = matrix_challenge.calcCumulativeProduct(multiplied_matrix, 0)
        self.assertIsNot(False, result)

    def testMatrixStats(self):
        multiplied_matrix = matrix_challenge.multiplyMatrices(self.matrix1, self.matrix2)
        cum_prod_matrix = matrix_challenge.calcCumulativeProduct(multiplied_matrix, 0)
        result = matrix_challenge.getMatrixStats(cum_prod_matrix)
        self.assertNotEqual(result, {})

        cum_prod_matrix = matrix_challenge.calcCumulativeProduct(multiplied_matrix, 2)
        result = matrix_challenge.getMatrixStats(cum_prod_matrix)
        self.assertEqual(result, {})

    def testSaveDict(self):
        multiplied_matrix = matrix_challenge.multiplyMatrices(self.matrix1, self.matrix2)
        cum_prod_matrix = matrix_challenge.calcCumulativeProduct(multiplied_matrix, 2)
        stats = matrix_challenge.getMatrixStats(cum_prod_matrix)

        self.assertFalse(stats)

if __name__ == '__main__':
    unittest.main()
