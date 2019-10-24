import sys
from helpers import SetUp
import masking_constants as MASKs

class State():
    dataval = []
    PC = 96
    cycle = 1
    R = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    def __init__(self, opcodes, dataval, addrs, arg1, arg2, arg3, numInstructs, opcodeStr, arg1Str, arg2Str, arg3Str):
        #self.instructions = instrs
        self.opcode = opcodes
        self.dataval = dataval
        self.address = addrs
        self.numInstructions = numInstructs
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.opcodeStr = opcodeStr
        self.arg1Str = arg1Str
        self.arg2Str = arg2Str
        self.arg3Str = arg3Str

    def getIndexOfMemAddress(self, currAddr):
        return (currAddr - 96) / 4
    def incrementPC(self):
        self.PC = self.PC + 4

    #def printState(self):


class Simulator():

    def __init__(self, opcode, dataval, address, arg1, arg2, arg3, numInstructs, opcodeStr, arg1Str, arg2Str, arg3Str):
        self.opcode = opcode
        self.dataval = dataval
        self.address = address
        self.numInstructs = numInstructs
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.opcodeStr = opcodeStr
        self.arg1Str = arg1Str
        self.arg2Str = arg2Str
        self.arg3Str = arg3Str
        self.specialMask = MASKs.specialMask

    def run(self):
        foundBreak = False
        armState = State(self.opcode, self.dataval, self.address, self.arg1, self.arg2, self.arg3,
                         self.numInstructs, self.opcodeStr, self.arg1Str, self.arg2Str, self.arg3Str)

        while(foundBreak == False):
            jumpAddr = armState.PC

            i = int(armState.getIndexOfMemAddress(armState.PC))

            if(self.opcode[i] == 0):
                #armState.printState()
                armState.incrementPC()
                armState.cycle += 1
                continue
            elif (self.opcode[i] >= 160 and self.opcode[i] <=191):#B
                jumpAddr = jumpAddr + ((self.arg1[i] * 4) - 4)
            elif self.opcode[i] == 1112: #ADD
                armState.R[self.arg3[i]] = armState.R[self.arg2[i]] + armState.R[self.arg1[i]]
            elif self.opcode[i] == 1624: #SUB
                armState.R[self.arg3[i]] = armState.R[self.arg2[i]] - armState.R[self.arg1[i]]
            elif self.opcode[i] == 1104: #AND
                armState.R[self.arg3[i]] = armState.R[self.arg2[i]] & armState.R[self.arg1[i]]
            elif self.opcode[i] == 1360: #ORR
                armState.R[self.arg3[i]] = armState.R[self.arg2[i]] | armState.R[self.arg1[i]]
            elif (self.opcode[i] >= 1160 and self.opcode[i] <= 1161): #ADDI
                armState.R[self.arg3[i]] = self.arg2[i] + armState.R[self.arg1[i]]
            elif (self.opcode[i] >= 1672 and self.opcode[i] <= 1673): #SUBI
                armState.R[self.arg3[i]] = armState.R[self.arg1[i]] - self.arg2[i]
            elif (self.opcode[i] >= 1440 and self.opcode[i] <= 1447): #CBZ
                if armState.R[self.arg2[i]] == 0:
                    jumpAddr = jumpAddr + ((self.arg1[i] * 4) - 4)
            elif (self.opcode[i] >= 1448 and self.opcode[i] <= 1455): #CBNZ
                if armState.R[self.arg2[i]] != 0:
                    jumpAddr = jumpAddr + ((self.arg1[i] * 4) - 4)
            elif (self.opcode[i] >= 1684 and self.opcode[i] <= 1687): #MOVZ
                armState.R[self.arg2[i]] = 0
                armState.R[self.arg2[i]] = armState.R[self.arg3[i]] * self.arg1[i]
            elif (self.opcode[i] >= 1940 and self.opcode[i] <= 1943): #MOVK
                armState.R[self.arg2[i]] = armState.R[self.arg2[i]] + (armState.R[self.arg3[i]] * self.arg1[i])
            elif self.opcode[i] == 1690: #LSL
                armState.R[self.arg1[i]] = armState.R[self.arg3[i]] / (2**self.arg2[i])
            elif self.opcode[i] == 1691: #LSR
                armState.R[self.arg1[i]] = armState.R[self.arg3[i]] * (2**self.arg2[i])
            elif self.opcode[i] == 1872: #EOR
                armState.R[self.arg3[i]] = armState.R[self.arg1[i]] ^ armState.R[self.arg2[i]]
            elif self.opcode[i] == 2038: #BREAK
                foundBreak = True

            else: #ERROR
                print("IN SIM -- UNKNOWN INSTRUCTION ------------------ !!!!")

            #armState.printState()
            armState.PC = jumpAddr
            armState.incrementPC()
            armState.cycle += 1