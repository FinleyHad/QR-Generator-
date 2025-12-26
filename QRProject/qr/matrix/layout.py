def create_base_matrix():
    size = 21
    matrix = [[None] * size for _ in range(size)]
    
    def place_finder_pattern(row, col):
        pattern = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        for i in range(7):
            for j in range(7):
                matrix[row + i][col + j] = pattern[i][j]
    
    place_finder_pattern(0, 0)
    place_finder_pattern(0, 14)
    place_finder_pattern(14, 0)
    
    for i in range(8, 13):
        matrix[6][i] = 1 if (i - 8) % 2 == 0 else 0
        matrix[i][6] = 1 if (i - 8) % 2 == 0 else 0
    
    matrix[8][13] = 1
    
    for i in range(9):
        if i < 6:
            matrix[8][i] = None
            matrix[i][8] = None
        if i < 7:
            matrix[8][14 + i] = None
            matrix[14 + i][8] = None
    
    return matrix


def place_data(matrix, encoded_bits, ecc_codewords):
    size = 21
    all_bits = list(encoded_bits)
    
    if isinstance(ecc_codewords, list):
        for codeword in ecc_codewords:
            if isinstance(codeword, int):
                all_bits.extend(format(codeword, '08b'))
            else:
                all_bits.extend(str(codeword))
    else:
        all_bits.extend(str(ecc_codewords))
    
    bit_index = 0
    
    def is_reserved(row, col):
        if row < 9 and col < 9:
            return True
        if row < 9 and col >= 13:
            return True
        if row >= 13 and col < 9:
            return True
        if row == 6 or col == 6:
            return True
        if row == 8 and col == 13:
            return True
        return False
    
    col = size - 1
    up = True
    
    while col > 0:
        if col == 6:
            col -= 1
            continue
        
        if up:
            for row in range(size - 1, -1, -1):
                if not is_reserved(row, col):
                    if bit_index < len(all_bits):
                        matrix[row][col] = int(all_bits[bit_index])
                        bit_index += 1
                    else:
                        matrix[row][col] = 0
                
                if not is_reserved(row, col - 1):
                    if bit_index < len(all_bits):
                        matrix[row][col - 1] = int(all_bits[bit_index])
                        bit_index += 1
                    else:
                        matrix[row][col - 1] = 0
        else:
            for row in range(size):
                if not is_reserved(row, col):
                    if bit_index < len(all_bits):
                        matrix[row][col] = int(all_bits[bit_index])
                        bit_index += 1
                    else:
                        matrix[row][col] = 0
                
                if not is_reserved(row, col - 1):
                    if bit_index < len(all_bits):
                        matrix[row][col - 1] = int(all_bits[bit_index])
                        bit_index += 1
                    else:
                        matrix[row][col - 1] = 0
        
        up = not up
        col -= 2
    
    for row in range(size):
        for col in range(size):
            if matrix[row][col] is None:
                matrix[row][col] = 0
    
    return matrix