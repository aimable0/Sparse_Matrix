#!/usr/bin/python3


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
                lines = [stripped for line in file if (stripped := line.strip())]

                # Check if the file starts with "rows=" and "cols="
                if not lines[0].startswith("rows=") or not lines[1].startswith("cols="):
                    raise ValueError("Input file has wrong format")

                # Parse the number of rows and columns
                self.numRows = int(lines[0].split("=")[1])
                self.numCols = int(lines[1].split("=")[1])
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

    def add(self, other_matrix):
        # check if the cols and rows are equal for both matrices
        if (
            self.numCols == other_matrix.numCols
            and self.numRows == other_matrix.numRows
        ):
            # make a new matrix that stores the added values
            result = SparseMatrix(None, self.numCols, self.numRows)
            for (row, col), val in self.data.items():
                result.set_element(
                    row,
                    col,
                    (val + other_matrix.get_element(row, col)),
                )
            for i, val in result.data.items():
                print(i, val)
        else:
            print("Matrices provided are not compatible")

    def sub(self, other_matrix):
        # check if the cols and rows are equal for both matrices
        if (
            self.numCols == other_matrix.numCols
            and self.numRows == other_matrix.numRows
        ):
            # make a new matrix that stores the substracted values
            result = SparseMatrix(None, self.numCols, self.numRows)
            for (row, col), val in self.data.items():
                result.set_element(
                    row,
                    col,
                    (val - other_matrix.get_element(row, col)),
                )
            for i, val in result.data.items():
                print(i, val)
        else:
            print("Matrices provided are not compatible")

    def mult(self, other_matrix):
        # check if the cols and rows are equal for both matrices
        if (
            self.numCols == other_matrix.numCols
            and self.numRows == other_matrix.numRows
        ):
            # make a new matrix that stores the multiplied values
            result = SparseMatrix(None, self.numCols, self.numRows)
            for (row, col), val in self.data.items():
                result.set_element(
                    row,
                    col,
                    (val * other_matrix.get_element(row, col)),
                )
            for i, val in result.data.items():
                print(i, val)
        else:
            print("Matrices provided are not compatible")


def main():
    # Use relative paths for input files
    matrixFilePath1 = "../../sample_inputs/matrix1.txt"
    matrixFilePath2 = "../../sample_inputs/matrix2.txt"

    try:
        # Load matrices from the input files
        matrix1 = SparseMatrix(matrixFilePath1)
        matrix2 = SparseMatrix(matrixFilePath2)
        matrix1.add(matrix2)
        matrix2.sub(matrix1)
        matrix1.mult(matrix2)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
