from typing import List

from Field import Field

INF = 100000


# 0 - player, 1 - bot
# player == True => it's our turn
# else: it's bot's turn

scores = []


def evaluate(field: Field, player: bool) -> int:
    if field.check_win(player):
        return INF

    if field.check_win(not player):
        return -INF

    if field.check_draw():
        return 0

    res = field.count_3(player) * 10 - field.count_3(not player) * 10
    return res


def alpha_beta(field: Field, alpha: int, beta: int, depth: int, player: bool) -> (int, int):
    # print("depth: ", depth)
    if depth == 5:
        # print("max depth")
        return evaluate(field, player), 8
    
    if field.check_win(player):
        # print("I'm win")
        return INF, 8

    if field.check_win(not player):
        # print("He wins")
        return -INF, 8

    if field.check_draw():
        # print("draw")
        return 0, 8

    if depth == 0:
        global scores
        scores = [0 for x in range(7)]

    needed_col = 8
    for col in range(7):
        # print("COL {0} DEPTH {1}".format(col, depth))
        if field.used[col] < 6:
            field._put_chip(col, player)
            score, cur_col = alpha_beta(field, -beta, -alpha, depth + 1, not player)
            if depth == 0:
                scores[col] = score
            field.used[col] -= 1
            field.cells[col][field.used[col]] = 2
            score *= -1
            if score >= beta:
                return beta, col
            if score > alpha:
                alpha = score
                needed_col = col
    # print("needed col: ", needed_col)
    return alpha, needed_col


def make_alpha_beta(field: Field) -> (int, int, List[int]):
    alpha, needed_col = alpha_beta(field, -INF, INF, 0, True)
    return alpha, needed_col, scores