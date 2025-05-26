# -*- coding: utf-8 -*-
import Prog_Funcoes1
import os

def isInt(inString):
    try:
        int(inString)
        return True
    except ValueError:
        return False


def TrataInd(CodigoPDB):

    arquivo = os.getcwd()
    print(CodigoPDB)
    arquivo1 = arquivo[0:17]

    PastaArq = arquivo1 + "/arquivos/"
    proteinArq = "pdb/" + CodigoPDB[0:4] + ".pdb"
    proteinScore = "A3D/" + CodigoPDB[0:4] + ".csv"

    pdbFilename = PastaArq + proteinArq
    A3DFilename = PastaArq + proteinScore

    chamador = 0
    desliga = 0
    flag = 0
    with open(pdbFilename) as pdbFile:
        pdbLines = pdbFile.readlines()

    with open(A3DFilename) as A3DFile:
        A3DLines = A3DFile.readlines()

    chain = " "
   # print("leu")
    for line in pdbLines:
        words = line
        if len(words) < 1:
            pass
        else:
            # print(words)
            if (words[0:4] == "ENDM"):
                desliga = 1
            else:
                if (words[0:4] == "ATOM") and (desliga == 0):
                    # print(words[21])
                    if (words[21] != chain):
                        # if (words[21] == "A"):
                        chain = words[21]
                       # print("inicial ",words)
                        # if (flag == 0):
                        #   flag = 1
                        Prog_Funcoes1.movimenta(
                            proteinArq, pdbLines, A3DLines, chain, CodigoPDB, chamador)

    return
