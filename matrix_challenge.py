#!/usr/local/bin/python3
import numpy as np
import pandas as pd
import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
import argparse
import sys

def parseArgOptions():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dimensions1', type = str, help = 'Tuple of dimensions for the matrices')
    parser.add_argument('--dimensions2', type = str, help = 'Tuple of dimensions for the matrices')
    parser.add_argument('--multiply', action = 'store_true', default = False, help = 'Flag to multiply generated matrices, default is false')
    parser.add_argument('--cumulative_product', type = int, help = 'Axis to calculate the cumulative product')
    parser.add_argument('--outdir', type = str, help = 'Output directory to save files')
    parser.add_argument('--stat_file_name', type = str, help = 'Name of statistics csv')
    parser.add_argument('--matrix_persist_name', type = str, help = 'Persistent Matrix binary file name')
    parser.add_argument('--matrix_binary_file', type = str, help = 'If this option is passed, all matrices generated will come from the passed binary file', default = None)

    global args
    args = parser.parse_args()

def generateRandomMatrices(dimensions):
    """
    Generate a matrix with random values based on the given dimensions

    For simplicity we limit the matrix to 2 dimensions. Given that this is the
    heart of the code if we cannot generate a valid 2d matrix we'll exit
    """
    if len(dimensions) > 2:
        logging.error('Invalid dimensions given, please only provide 2 dimensions')
        sys.exit(-1)

    logging.info(f'Generating matrices with dimensions {dimensions}')
    rows = int(dimensions[0])
    cols = int(dimensions[1])

    matrix = np.random.rand(rows, cols)

    return matrix

def checkMatrixCompatibility(matrix1, matrix2):
    """
    Helper method to determine whether two matrices may be multiplied
    """

    logging.info('Validating matrix multiplication compatibility')
    m1_dimensions = matrix1.shape
    m2_dimensions = matrix2.shape

    if m1_dimensions[1] != m2_dimensions[0]:
        logging.warning(f'{m1_dimensions[1]} and {m2_dimensions[0]} incompatible for multiplication')
        return False

    return True

def multiplyMatrices(matrix1, matrix2):
    """
    Tries to perform matrix multiplication if len(col[m1]) == len(row[m2])
    If not possible we'll return false so we can understand that the multiplication failed.
    """
    logging.info('Performing matrix multiplication')

    if checkMatrixCompatibility(matrix1, matrix2):
        dot_product = np.dot(matrix1, matrix2)
        return dot_product

    return False

def calcCumulativeProduct(result_matrix, axis):
    """
    Wrapper method for numpy cumprod to handle errors and check validity
    """
    logging.info('Calculating cumulative product')

    if axis not in [0, 1]:
        logging.warning('Please provide an axis in [0, 1]')
        return False

    cumulative_result = np.cumprod(result_matrix, axis)
    return cumulative_result

def getMatrixStats(cumulative_result):
    """
    Generate analytics for the cumulative product results
    """
    if cumulative_result is False:
        return {}

    logging.info('Generating matrix stats')
    result_max = cumulative_result.max()
    result_min = cumulative_result.min()
    result_mean = cumulative_result.mean()
    result_std = cumulative_result.std()
    result_med = np.median(cumulative_result)

    stat_dict = {'max' : result_max, 'min' : result_min, 'mean' : result_mean, 'std' : result_std, 'median' : result_med}

    return stat_dict

def saveDictToCsv(stat_dict, outdir, stat_file_name):
    """
    Use Pandas to save a dictionary to csv, Can be achieved in vanilla python
    but Pandas is cleaner.

    Data saved as csv can be loaded into excel, grepped, and manipulated using awk and other linux tools
    Can also be loaded into a df and viewed/used that way
    """

    if not stat_dict:
        logging.warning('Statistics Dictionary Empty, not writing file')
        return False

    full_path = f"{outdir}/{stat_file_name}.csv"
    stat_df = pd.DataFrame.from_records([stat_dict])
    logging.info(f"Saving CSV as {full_path}")
    stat_df.to_csv(full_path, index = False)

def matrixSaver(matrix, full_path, matrix_name):
    """
    Helper Method to save matrices as readable csv's
    """
    matrix_csv_path = f"{full_path}_{matrix_name}.csv"
    logging.info(f"Writing to {matrix_csv_path}")
    np.savetxt(matrix_csv_path, matrix, delimiter=",", fmt = "%20.10f")


def saveMatricesToDisk(matrix1, matrix2, dp_matrix, cum_res_matrix, outdir, matrix_persist_name):
    """
    Save our numpy matrices to a binary file so that it may be loaded in later

    Additionally save csv versions of our matrices for quick viewing, note that they are rounded to 10 decimals
    """
    full_path = f"{outdir}/{matrix_persist_name}"

    logging.info(f"Saving np matrices to {full_path}")
    np.savez(full_path, mat1 = matrix1, mat2 = matrix2, dp_mat = dp_matrix, cum_res_mat = cum_res_matrix)

    matrixSaver(matrix1, full_path, 'matrix1')
    matrixSaver(matrix2, full_path, 'matrix2')
    matrixSaver(dp_matrix, full_path, 'dot_product_matrix')
    matrixSaver(cum_res_matrix, full_path, 'cum_res_matrix')

def main():
    parseArgOptions()
    outdir = args.outdir
    stat_file_name = args.stat_file_name
    matrix_binary_file = args.matrix_binary_file


    if matrix_binary_file is None:
        dimensions1 = args.dimensions1.split(',')
        dimensions2 = args.dimensions2.split(',')
        multiply = args.multiply
        axis = args.cumulative_product
        matrix_persist_name = args.matrix_persist_name

        matrix1 = generateRandomMatrices(dimensions1)
        matrix2 = generateRandomMatrices(dimensions2)

        if multiply:
            dot_product = multiplyMatrices(matrix1, matrix2)

        if multiply and dot_product is not False and axis is not None:
            cumulative_result = calcCumulativeProduct(dot_product, axis)

            if cumulative_result is not False:
                result_stats = getMatrixStats(cumulative_result)

                saveDictToCsv(result_stats, outdir, stat_file_name)
                saveMatricesToDisk(matrix1, matrix2, dot_product, cumulative_result, outdir, matrix_persist_name)
    else:
        logging.info(f"Loading Matrix Binary from {matrix_binary_file}")
        loaded_matrix_data = np.load(matrix_binary_file)
        matrix1 = loaded_matrix_data['mat1']
        matrix2 = loaded_matrix_data['mat2']
        dot_product = loaded_matrix_data['dp_mat']
        cumulative_result = loaded_matrix_data['cum_res_mat']

        result_stats = getMatrixStats(cumulative_result)
        saveDictToCsv(result_stats, outdir, stat_file_name)


if __name__ == '__main__':
    main()
