Script can be used to randomly generate 2 NxN matrices. User may prompt to then multiply these matrices, calculate the cumulative product, and then generate some statistics on the said cumulative product.

Command Line options are used to interact with the user

```
  --dimensions1 DIMENSIONS1
                        Tuple of dimensions for the matrices
  --dimensions2 DIMENSIONS2
                        Tuple of dimensions for the matrices
  --multiply            Flag to multiply generated matrices, default is false
  --cumulative_product CUMULATIVE_PRODUCT
                        Axis to calculate the cumulative product
  --outdir OUTDIR       Output directory to save files
  --stat_file_name STAT_FILE_NAME
                        Name of statistics csv
  --matrix_persist_name MATRIX_PERSIST_NAME
                        Persistent Matrix binary file name
  --matrix_binary_file MATRIX_BINARY_FILE
                        If this option is passed, all matrices generated will come from the passed binary file
```

Typical uses look like such 

Case 1. Generate a brand new set of two matrices, multiply them together, calculate the cumulative product, generate statistics, and then save the matrices to a human readable csv, as well as generate a binary file so that they may be loaded again at a future date.

```./matrix_challenge.py --dimensions1 3,3 --dimensions2 3,3 --cumulative_product 0 --outdir `pwd` --stat_file_name statistics_1 --matrix_persist_name matrix_gen_1 --multiply ```

Case 2. Regenerate a statistics file loading in matrices from a previously saved numpy binary file.

```./matrix_challenge.py --matrix_binary_file $full_file_location/$file.npz --outdir `pwd` --stat_file_name statistics_loaded_1```
