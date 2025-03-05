# def add(self, other):
    #     """
    #     Add another sparse matrix to this matrix.

    #     Args:
    #         other (SparseMatrix): The matrix to add.

    #     Returns:
    #         SparseMatrix: The result of the addition.

    #     Raises:
    #         ValueError: If the matrices have incompatible dimensions.
    #     """
    #     if self.numRows != other.numRows or self.numCols != other.numCols:
    #         raise ValueError("Matrix dimensions are incompatible for addition")

    #     # Create a new matrix to store the result
    #     result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)

    #     # Copy all non-zero elements from this matrix to the result
    #     for (row, col), value in self.data.items():
    #         result.set_element(row, col, value)

    #     # Add non-zero elements from the other matrix to the result
    #     for (row, col), value in other.data.items():
    #         result.set_element(row, col, result.get_element(row, col) + value)

    #     return result

    # def subtract(self, other):
    #     """
    #     Subtract another sparse matrix from this matrix.

    #     Args:
    #         other (SparseMatrix): The matrix to subtract.

    #     Returns:
    #         SparseMatrix: The result of the subtraction.

    #     Raises:
    #         ValueError: If the matrices have incompatible dimensions.
    #     """
    #     if self.numRows != other.numRows or self.numCols != other.numCols:
    #         raise ValueError("Matrix dimensions are incompatible for subtraction")

    #     # Create a new matrix to store the result
    #     result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)

    #     # Copy all non-zero elements from this matrix to the result
    #     for (row, col), value in self.data.items():
    #         result.set_element(row, col, value)

    #     # Subtract non-zero elements from the other matrix from the result
    #     for (row, col), value in other.data.items():
    #         result.set_element(row, col, result.get_element(row, col) - value)

    #     return result

    # def multiply(self, other):
    #     """
    #     Multiply this sparse matrix with another sparse matrix.

    #     Args:
    #         other (SparseMatrix): The matrix to multiply with.

    #     Returns:
    #         SparseMatrix: The result of the multiplication.

    #     Raises:
    #         ValueError: If the matrices have incompatible dimensions.
    #     """
    #     if self.numCols != other.numRows:
    #         raise ValueError("Matrix dimensions are incompatible for multiplication")

    #     # Create a new matrix to store the result
    #     result = SparseMatrix(numRows=self.numRows, numCols=other.numCols)

    #     # Iterate over non-zero elements in this matrix
    #     for (i, k), val_self in self.data.items():
    #         # Iterate over non-zero elements in the other matrix where the row matches k
    #         for (k_other, j), val_other in other.data.items():
    #             if k == k_other:  # Ensure the column of self matches the row of other
    #                 # Multiply and accumulate the result
    #                 result.set_element(
    #                     i, j, result.get_element(i, j) + val_self * val_other
    #                 )

    #     return result

    # def save_to_file(self, filename):
    #     """
    #     Save the matrix to a file.

    #     Args:
    #         filename (str): Path to the output file.
    #     """
    #     with open(filename, "w") as file:
    #         # Write the number of rows and columns
    #         file.write(f"rows={self.numRows}\n")
    #         file.write(f"cols={self.numCols}\n")

    #         # Write the non-zero elements
    #         for (row, col), value in self.data.items():
    #             file.write(f"({row}, {col}, {value})\n")

    # def __str__(self):
    #     """
    #     Return a string representation of the matrix.

    #     Returns:
    #         str: A string showing the matrix dimensions and non-zero elements.
    #     """
    #     result = f"rows={self.numRows}\ncols={self.numCols}\n"
    #     for (row, col), value in self.data.items():
    #         result += f"({row}, {col}, {value})\n"
    #     return result