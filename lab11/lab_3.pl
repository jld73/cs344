burns(X):- wood(X).
witch(X):- burns(X).
bridgeMaterial(X):- wood(x); stone(x).
floats(X):- wood(X).
floats(apples).
floats(very_small_rocks).
floats(cider).
floats(gravy).
floats(cherries).
floats(mud).
floats(churches).
floats(lead).
floats(duck).
wood(X):- sameWeight(X, duck).
sameWeight(woman, duck).



witch(woman): true