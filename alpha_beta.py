from Field import Field

INF = 1000


# 0 - player, 1 - bot
# player == True => it's our turn
# else: it's bot's turn


def evaluate(field: Field, player: bool) -> int:
    if field._check_win(True):
        return INF

    if field._check_win(False):
        return -INF

    for col in range(7):
        if field.used[col] != 6:
            break
    else:
        return 0

    if player:
        return INF + field.count_3(player) * 10

    return -INF-(field.count_3(player) * 10)


def minimax(field: Field, depth: int, player: bool, alpha: int, beta: int) -> (int, int):
    if depth == 6:
        return evaluate(field, player), -1

    needed_col = -1
    if player:
        best_value = -INF
        for col in range(7):
            if field.used[col] < 6:
                field._put_chip(col, True)
                cur_value, cur_col = minimax(field, depth + 1, False, alpha, beta)
                field.used[col] -= 1
                field.cells[col][field.used[col]] = 2
                if cur_value > best_value:
                    best_value = max(best_value, cur_value)
                    needed_col = col
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break
        return best_value, needed_col
    best_value = INF
    for col in range(7):
        if field.used[col] < 6:
            field._put_chip(col, False)
            cur_value, cur_col = minimax(field, depth + 1, True, alpha, beta)
            field.used[col] -= 1
            field.cells[col][field.used[col]] = 2
            if cur_value < best_value:
                best_value = min(best_value, cur_value)
                needed_col = col
            beta = min(alpha, best_value)
            if alpha >= beta:
                break
    return best_value, needed_col
