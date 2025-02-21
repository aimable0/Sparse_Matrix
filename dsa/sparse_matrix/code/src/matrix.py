class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=None, numCols=None):
        """
        Initialize a SparseMatrix object.

        Args:
            matrixFilePath (str, optional): Path to a file containing matrix data. Defaults to None.
            numRows (int, optional): Number of rows for an empty matrix. Defaults to None.
            numCols (int, optional): Number of columns for an empty matrix. Defaults to None.
        """
        if matrixFilePath:
            # Load matrix data from a file if a file path is provided
            self.load_from_file(matrixFilePath)
        else:
            # Initialize an empty matrix with the given dimensions
            self.numRows = numRows
            self.numCols = numCols
            self.data = (
                {}
            )  # Dictionary to store non-zero elements: key=(row, col), value=value

    def load_from_file(self, matrixFilePath):
        """
        Load matrix data from a file.

        Args:
            matrixFilePath (str): Path to the input file.

        Raises:
            ValueError: If the file format is invalid.
            FileNotFoundError: If the file does not exist.
        """
        try:
            with open(matrixFilePath, "r") as file:
                # Read and clean the file lines
                lines = [line.strip() for line in file if line.strip()]

                # Check if the file starts with "rows=" and "cols="
                if not lines[0].startswith("rows=") or not lines[1].startswith("cols="):
                    raise ValueError("Input file has wrong format")

                # Parse the number of rows and columns
                self.numRows = int(lines[0].split("=")[1].strip())
                self.numCols = int(lines[1].split("=")[1].strip())
                self.data = {}  # Dictionary to store non-zero elements

                # Parse the non-zero elements
                for line in lines[2:]:
                    try:
                        # Remove parentheses and split into row, column, and value
                        row, col, val = (
                            line.replace("(", "").replace(")", "").split(", ")
                        )
                        self.data[(int(row), int(col))] = int(val)
                    except ValueError:
                        raise ValueError("Input file has wrong format")
        except FileNotFoundError:
            raise FileNotFoundError(f"File {matrixFilePath} not found")

    def get_element(self, currRow, currCol):
        """
        Get the value at a specific position in the matrix.

        Args:
            currRow (int): Row index.
            currCol (int): Column index.

        Returns:
            int: The value at (currRow, currCol). Returns 0 if the element is not stored (i.e., it's zero).
        """
        return self.data.get((currRow, currCol), 0)

    def set_element(self, currRow, currCol, value):
        """
        Set the value at a specific position in the matrix.

        Args:
            currRow (int): Row index.
            currCol (int): Column index.
            value (int): Value to set.
        """
        if value != 0:
            # Store non-zero values in the dictionary
            self.data[(currRow, currCol)] = value
        elif (currRow, currCol) in self.data:
            # Remove the key if the value is zero (to maintain sparsity)
            del self.data[(currRow, currCol)]

    def add(self, other):
        """
        Add another sparse matrix to this matrix.

        Args:
            other (SparseMatrix): The matrix to add.

        Returns:
            SparseMatrix: The result of the addition.

        Raises:
            ValueError: If the matrices have incompatible dimensions.
        """
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions are incompatible for addition")

        # Create a new matrix to store the result
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)

        # Copy all non-zero elements from this matrix to the result
        for (row, col), value in self.data.items():
            result.set_element(row, col, value)

        # Add non-zero elements from the other matrix to the result
        for (row, col), value in other.data.items():
            result.set_element(row, col, result.get_element(row, col) + value)

        return result

    def subtract(self, other):
        """
        Subtract another sparse matrix from this matrix.

        Args:
            other (SparseMatrix): The matrix to subtract.

        Returns:
            SparseMatrix: The result of the subtraction.

        Raises:
            ValueError: If the matrices have incompatible dimensions.
        """
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions are incompatible for subtraction")

        # Create a new matrix to store the result
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)

        # Copy all non-zero elements from this matrix to the result
        for (row, col), value in self.data.items():
            result.set_element(row, col, value)

        # Subtract non-zero elements from the other matrix from the result
        for (row, col), value in other.data.items():
            result.set_element(row, col, result.get_element(row, col) - value)

        return result

    def multiply(self, other):
        """
        Multiply this sparse matrix with another sparse matrix.

        Args:
            other (SparseMatrix): The matrix to multiply with.

        Returns:
            SparseMatrix: The result of the multiplication.

        Raises:
            ValueError: If the matrices have incompatible dimensions.
        """
        if self.numCols != other.numRows:
            raise ValueError("Matrix dimensions are incompatible for multiplication")

        # Create a new matrix to store the result
        result = SparseMatrix(numRows=self.numRows, numCols=other.numCols)

        # Iterate over non-zero elements in this matrix
        for (i, k), val_self in self.data.items():
            # Iterate over non-zero elements in the other matrix where the row matches k
            for (k_other, j), val_other in other.data.items():
                if k == k_other:  # Ensure the column of self matches the row of other
                    # Multiply and accumulate the result
                    result.set_element(
                        i, j, result.get_element(i, j) + val_self * val_other
                    )

        return result

    def save_to_file(self, filename):
        """
        Save the matrix to a file.

        Args:
            filename (str): Path to the output file.
        """
        with open(filename, "w") as file:
            # Write the number of rows and columns
            file.write(f"rows={self.numRows}\n")
            file.write(f"cols={self.numCols}\n")

            # Write the non-zero elements
            for (row, col), value in self.data.items():
                file.write(f"({row}, {col}, {value})\n")

    def __str__(self):
        """
        Return a string representation of the matrix.

        Returns:
            str: A string showing the matrix dimensions and non-zero elements.
        """
        result = f"rows={self.numRows}\ncols={self.numCols}\n"
        for (row, col), value in self.data.items():
            result += f"({row}, {col}, {value})\n"
        return result


def main():
    # Use relative paths for input files
    matrixFilePath1 = "../../sample_inputs/matrix1.txt"
    matrixFilePath2 = "../../sample_inputs/matrix2.txt"

    try:
        # Load matrices from the input files
        matrix1 = SparseMatrix(matrixFilePath1)
        matrix2 = SparseMatrix(matrixFilePath2)
    except Exception as e:
        print(f"Error: {e}")
        return

    print("Select an operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    operation = int(input("Enter your choice: "))

    try:
        if operation == 1:
            result = matrix1.add(matrix2)
            result.save_to_file("../../results/addition_result.txt")
            print("Addition result saved to addition_result.txt")
        elif operation == 2:
            result = matrix1.subtract(matrix2)
            result.save_to_file("../../results/subtraction_result.txt")
            print("Subtraction result saved to subtraction_result.txt")
        elif operation == 3:
            result = matrix1.multiply(matrix2)
            result.save_to_file("../../results/multiplication_result.txt")
            print("Multiplication result saved to multiplication_result.txt")
        else:
            print("Invalid choice")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
