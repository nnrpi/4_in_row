from Field import Field

INF = 1000


# 0 - player, 1 - bot
# is_max_player == True => it's our turn
# else: it's bot's turn


def minimax(field: Field, depth: int, is_max_player: bool, alpha: int, beta: int) -> int:
    if depth == 6:
        if field._check_win(is_max_player):
            return INF
        if field._check_win(not is_max_player):
            return -INF
        return 0

    if is_max_player:
        best_val = -INF
        for col in range(7):
            if field.used[col] < 6:
                field._put_chip(col, False)
                cur_value = minimax(field, depth + 1, False, alpha, beta)
                field.used[col] -= 1
                field.cells[col][field.used[col]] = 2
                best_val = max(best_val, cur_value)
                alpha = max(alpha, best_val)
                if alpha >= beta:
                    break
        return best_val
    best_val = INF
    for col in range(7):
        if field.used[col] < 6:
            field._put_chip(col, True)
            cur_value = minimax(field, depth + 1, True, alpha, beta)
            field.used[col] -= 1
            field.cells[col][field.used[col]] = 2
            best_val = min(best_val, cur_value)
            beta = min(alpha, best_val)
            if alpha >= beta:
                break
    return best_val
