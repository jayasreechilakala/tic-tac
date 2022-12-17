PLAYER = 'X'
COMPUTER = 'O'
EMPTY = '-'
INFINITY = 100
NEG_INFINITY = -100


def get_index(position):
    return position // 3, position % 3


def print_board(board):
    for i in range(3):
        for j in range(3):
            print(board[i][j], end='\t')
        print()
    print()


def are_3_same(array):
    if (len(set(array)) == 1) and (array[0] != EMPTY):
        return True, (INFINITY if array[0] == COMPUTER else NEG_INFINITY)

    return False, None


def is_game_ended(board):
    if all(all(map(lambda element: element != EMPTY, row)) for row in board):
        return True, 0

    possibilities = [are_3_same(board[0]),
                     are_3_same(board[1]),
                     are_3_same(board[2]),
                     are_3_same([board[i][0] for i in range(3)]),
                     are_3_same([board[i][1] for i in range(3)]),
                     are_3_same([board[i][2] for i in range(3)]),
                     are_3_same([board[i][i] for i in range(3)]),
                     are_3_same([board[i][2 - i] for i in range(3)])]

    for possibility in possibilities:
        if possibility[0]:
            return possibility

    return False, None


def get_empty_indices(board):
    return [(i, j) for i in range(3)
            for j in range(3)
            if board[i][j] == EMPTY]


def minimax(maximizing_player, board):
    game_ended, score = is_game_ended(board)
    if game_ended:
        return score

    if maximizing_player:
        max_eval = NEG_INFINITY
        empty_indices = get_empty_indices(board)
        for empty_index in empty_indices:
            board[empty_index[0]][empty_index[1]] = COMPUTER
            current_eval = minimax(False, board)
            board[empty_index[0]][empty_index[1]] = EMPTY
            max_eval = max(max_eval, current_eval)
        return max_eval
    else:
        min_eval = INFINITY
        empty_indices = get_empty_indices(board)
        for empty_index in empty_indices:
            board[empty_index[0]][empty_index[1]] = PLAYER
            current_eval = minimax(True, board)
            board[empty_index[0]][empty_index[1]] = EMPTY
            min_eval = min(min_eval, current_eval)
        return min_eval


def get_best_move(board):
    max_eval = NEG_INFINITY
    empty_indices = get_empty_indices(board)
    best_move = empty_indices[0]
    for empty_index in empty_indices:
        board[empty_index[0]][empty_index[1]] = COMPUTER
        current_eval = minimax(False, board)
        board[empty_index[0]][empty_index[1]] = EMPTY
        if current_eval > max_eval:
            max_eval = current_eval
            best_move = empty_index
        max_eval = max(max_eval, current_eval)

    return best_move


def main():
    print("Sample for positions")
    print_board([[0, 1, 2], [3, 4, 5], [6, 7, 8]])

    board = [[EMPTY] * 3 for _ in range(3)]
    print_board(board)

    game_ended, score = is_game_ended(board)

    while not game_ended:
        position = int(input('Please enter a position '))
        index = get_index(position)

        if board[index[0]][index[1]] != EMPTY:
            print("\nPlease enter Empty Position")
            print_board(board)
            continue

        board[index[0]][index[1]] = PLAYER
        print_board(board)

        game_ended, score = is_game_ended(board)
        if game_ended:
            break

        best_move = get_best_move(board)
        board[best_move[0]][best_move[1]] = COMPUTER
        print_board(board)

        game_ended, score = is_game_ended(board)

    if score > 0:
        print("Computer WON")
    elif score == 0:
        print("DRAW")
    else:
        print("Player WON")


if __name__ == '__main__':
    main()
