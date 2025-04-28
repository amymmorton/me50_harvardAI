from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

playerA = And(
    #A has to be knave or knight but not both
    Or(AKnave,AKnight), Not(And(AKnave,AKnight))
)
playerB = And(
    #B has to be knave or knight but not both
    Or(BKnave,BKnight), Not(And(BKnave,BKnight))
)
playerC = And(
    #C has to be knave or knight but not both
    Or(CKnave,CKnight), Not(And(CKnave,CKnight))
)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    playerA,

    #Knave tells lies
    Implication(AKnave, Not(And(AKnight,AKnave))),

    #Knight tells the truth
    Implication(AKnight, And(AKnight,AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    playerA,
    playerB,

    #Knave tells lies
    Implication(AKnave, Not(And(AKnave,BKnave))),
    #Knight tells the truth
    Implication(AKnight, And(AKnave,BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    playerA,
    playerB,

    Implication(AKnave, Not(And(AKnave,BKnave))),
    Implication(AKnight, And(AKnight,BKnight)),

    Implication(BKnave, Not(And(BKnave, AKnight))),
    Implication(BKnight, And(BKnight,AKnave))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    #All players:
    playerA,
    playerB,
    playerC,
    Implication(AKnave, Not(Or(AKnave, AKnight))),
    Implication(AKnight, Or(AKnave, AKnight)),
                
    Implication(AKnave, Not(BKnave)),
    Implication(AKnight, BKnave),
    
    Implication(BKnave, Not(CKnave)),
    Implication(BKnight, CKnave),

    Implication(CKnave, Not(AKnight)),
    Implication(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
