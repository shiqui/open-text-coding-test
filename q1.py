def make_triangle(M: int = 3, N: int = 4) -> None:
    """
    This function prints a right-angled triangle of height M and width N, defaults to M=3 and N=4.
    The triangle is made of asterisks, and aligns to the left.
    Args:
        M (int): Number of rows
        N (int): Number of columns

    """
    [print("*" * int(N * row_index / M)) for row_index in range(1, M + 1)]


if __name__ == "__main__":
    make_triangle(3, 4)
