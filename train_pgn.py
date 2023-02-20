#!/usr/bin/python3

import argparse
import chess.pgn
import sys
from pathlib import Path

delete_nags = set((chess.pgn.NAG_BLUNDER,
                   chess.pgn.NAG_MISTAKE,
                   chess.pgn.NAG_DUBIOUS_MOVE))

def processNode(node, repertoire_color):
    remove_variation = False
    if node.move is not None:
        if len(delete_nags.intersection(node.nags)) and node.turn != repertoire_color:
            node.parent.remove_variation(node)
            remove_variation = True
    if not remove_variation:
        for variation in node.variations:
            processNode(variation, repertoire_color)

def main():
    parser = argparse.ArgumentParser( description = 'Remove blunder/mistake/dubious moves from a pgn repertoire file')
    parser.add_argument('src', help='input pgn file')
    parser.add_argument('dst', help='output pgn file')
    parser.add_argument('-f', action='store_true', help='overwite destination file if it exists') 
    parser.add_argument('--color', '-c', default='w', choices=('w','white','b','black'),help='white (default) or black repertoire file') 

    args = parser.parse_args()

    if args.color.lower() in ('white','w'):
        repertoire_color = chess.WHITE
    else:
        repertoire_color = chess.BLACK

    pgn = open(args.src)
    dst = Path(args.dst)
    if dst.exists and not args.f:
        print('error: destination file exists, use -f to overwrite')
        sys.exit(-1)
    f_dst = open(dst,'w')

    while (game := chess.pgn.read_game(pgn)) is not None:
        processNode(game, repertoire_color)
        print(game, file=f_dst, end="\n\n")

    f_dst.close()

if __name__=="__main__":
    main()
