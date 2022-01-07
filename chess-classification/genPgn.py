"""
Output PGN files with stockfish and python-chess.

`PGN parsing and writing <https://python-chess.readthedocs.io/en/latest/pgn.html>`_
`How to create pgn from a game play #63 <https://github.com/niklasf/python-chess/issues/63>`_
"""

import asyncio
import chess
import chess.engine
import chess.pgn
import argparse
import os

async def main(path="train-pgn", loop=1, time=20) -> None:
    transport, engine = await chess.engine.popen_uci(r"/usr/games/stockfish")

    os.makedirs(path, exist_ok=True)

    for i in range(loop):
        board = chess.Board()
        game = chess.pgn.Game()
        game.headers["Event"]
        game.setup(board)
        node = game
        while not board.is_game_over():
            # result = await engine.play(board, chess.engine.Limit(time=0.1))
            # result = await engine.play(board, chess.engine.Limit(time=20))
            result = await engine.play(board, chess.engine.Limit(time=time))
            board.push(result.move)
            print(board)
            print("\n")
            node = node.add_variation(result.move)
        game.headers["Result"] = board.result()
        print(game)
        with open(os.path.join(path, f"train-{i}.pgn"), mode='w') as f:
            exporter = chess.pgn.FileExporter(f)
            game.accept(exporter)

    await engine.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-p", "--path", dest='path', default="train-pgn", type=str, help="Directory where you want to save.  Default is train-pgn.")
    parser.add_argument("-l", "--loop", dest='loop', default=1, type=int, help="How many PGN files you want.  Default is 1.")
    parser.add_argument("-t", "--time", dest='time', default=20, type=float, help="Minimum thinking time.  Default is 20.")
    args = parser.parse_args()

    asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
    asyncio.run(main(args.path, args.loop, args.time))
