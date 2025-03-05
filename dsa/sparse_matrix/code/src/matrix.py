#!/usr/bin/env python3


class SparseMatrix:
    def __init__(self, rows=0, cols=0):
        """
        Initialize a sparse matrix with specified dimensions.

        Args:
            rows (int): Number of rows in the matrix
            cols (int): Number of columns in the matrix
        """
        self.rows = rows
        self.cols = cols
        self.data = {}  # Dictionary to store non-zero elements

    @classmethod
    def from_file(cls, filename):
        """
        Create a SparseMatrix by reading from a file.

        Args:
            filename (str): Path to the input file

        Returns:
            SparseMatrix: Constructed sparse matrix
        """
        matrix = cls()
        try:
            with open(filename, "r") as file:
                # Read rows
                rows_line = file.readline().strip()
                if not rows_line.startswith("rows="):
                    raise ValueError("Invalid file format: rows line missing")
                matrix.rows = int(rows_line.split("=")[1])

                # Read columns
                cols_line = file.readline().strip()
                if not cols_line.startswith("cols="):
                    raise ValueError("Invalid file format: columns line missing")
                matrix.cols = int(cols_line.split("=")[1])

                # Read matrix elements
                for line in file:
                    line = line.strip()
                    if line:
                        # Remove parentheses and split
                        row, col, value = map(int, line.strip("()").split(", "))
                        matrix.set_element(row, col, value)

            return matrix
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
            return None
        except ValueError as e:
            print(f"Error parsing file: {e}")
            return None

    def set_element(self, row, col, value):
        """
        Set an element in the sparse matrix.

        Args:
            row (int): Row index
            col (int): Column index
            value (int): Value to set
        """
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise IndexError("Index out of matrix bounds")

        if value != 0:
            self.data[(row, col)] = value
        elif (row, col) in self.data:
            del self.data[(row, col)]

    def get_element(self, row, col):
        """
        Get an element from the sparse matrix.

        Args:
            row (int): Row index
            col (int): Column index

        Returns:
            int: Value at the specified position
        """
        return self.data.get((row, col), 0)

    def add(self, other):
        """
        Add two sparse matrices.

        Args:
            other (SparseMatrix): Matrix to add

        Returns:
            SparseMatrix: Resulting matrix after addition
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition")

        result = SparseMatrix(self.rows, self.cols)

        # Combine keys from both matrices
        all_keys = set(self.data.keys()).union(other.data.keys())

        for row, col in all_keys:
            value = self.get_element(row, col) + other.get_element(row, col)
            result.set_element(row, col, value)

        return result

    def subtract(self, other):
        """
        Subtraction method
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction")

        result = SparseMatrix(self.rows, self.cols)

        # Combine keys from both matrices
        all_keys = set(self.data.keys()).union(other.data.keys())

        for row, col in all_keys:
            value = self.get_element(row, col) - other.get_element(row, col)
            result.set_element(row, col, value)

        return result

    def multiply(self, other):
        """
        Multiply two sparse matrices.

        Args:
            other (SparseMatrix): Matrix to multiply with

        Returns:
            SparseMatrix: Resulting matrix after multiplication
        """
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions incompatible for multiplication")

        result = SparseMatrix(self.rows, other.cols)

        for (row, k), val1 in self.data.items():
            for col in range(other.cols):
                val2 = other.get_element(k, col)
                if val2 != 0:
                    current_val = result.get_element(row, col)
                    result.set_element(row, col, current_val + val1 * val2)

        return result

    def save_to_file(self, filename):
        """
        Save the sparse matrix to a file.

        Args:
            filename (str): Path to the output file
        """
        with open(filename, "w") as file:
            file.write(f"rows={self.rows}\n")
            file.write(f"cols={self.cols}\n")

            for (row, col), value in sorted(self.data.items()):
                file.write(f"({row}, {col}, {value})\n")

    def __str__(self):
        """
        Ensure a consistent sorted output
        Sort first by row, then by column
        """
        output = f"rows={self.rows}\ncols={self.cols}\n"
        # Sort the data keys first by row, then by column
        sorted_entries = sorted(self.data.items(), key=lambda x: (x[0][0], x[0][1]))

        for (row, col), value in sorted_entries:
            output += f"({row}, {col}, {value})\n"
        return output


def main():
    # Interactive menu for matrix operations
    while True:
        print("\nSparse Matrix Operations:")
        print("1. Load Matrices and Perform Operation")
        print("2. Exit")

        choice = input("Enter your choice (1-2): ")

        if choice == "1":
            try:
                # Load first matrix
                matrix1_path = "../../sample_inputs/matrix1.txt"
                matrix1 = SparseMatrix.from_file(matrix1_path)

                if matrix1 is None:
                    continue

                # Load second matrix
                matrix2_path = "../../sample_inputs/matrix2.txt"
                matrix2 = SparseMatrix.from_file(matrix2_path)

                if matrix2 is None:
                    continue

                # Operation selection
                print("\nSelect Operation:")
                print("1. Addition")
                print("2. Subtraction")
                print("3. Multiplication")

                op_choice = input("Enter operation (1-3): ")

                # Perform selected operation
                if op_choice == "1":
                    result = matrix1.add(matrix2)
                    output_file = "../../results/addition_result.txt"
                elif op_choice == "2":
                    result = matrix1.subtract(matrix2)
                    output_file = "../../results/subtraction_result.txt"
                elif op_choice == "3":
                    result = matrix1.multiply(matrix2)
                    output_file = "../../results/multiplication_result.txt"
                else:
                    print("Invalid operation choice.")
                    continue

                # Display and save result
                print("\nResult:")
                print(result)

                result.save_to_file(output_file)
                print(f"Result saved to {output_file}")

            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == "2":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
