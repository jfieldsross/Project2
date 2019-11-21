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

    def printState(self):
        outputFileName = SetUp.get_output_filename()

        with open(outputFileName + "_sim.txt", 'a') as outFile:

            i = int(self.getIndexOfMemAddress(self.PC))
            outFile.write("====================\n")
            outFile.write("cycle:" + str(self.cycle) + "\t" + str(self.PC) + "\t" + self.opcodeStr[i] + self.arg1Str[i]
                          + self.arg2Str[i] + self.arg3Str[i] + "\n")
            outFile.write("\n")
            outFile.write("registers:\n")
            outStr = "r00:"
            for i in range(0, 8):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outStr = "r08:"
            for i in range(8, 16):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outStr = "r16:"
            for i in range(16, 24):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outStr = "r24:"
            for i in range(24, 32):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outFile.write("\ndata:\n")
            outStr = "\n"
            for i in range(len(self.dataval)):

                if i % 8 == 0 and i != 0 or i == len(self.dataval):
                    outFile.write(outStr + "\n")

                if i % 8 == 0:
                    outStr = str(self.address[i + self.numInstructions]) + ":" + str(self.dataval[i])

                if (i % 8 != 0):
                    outStr = outStr + "\t" + str(self.dataval[i])

            outFile.write(outStr + "\n")
            outFile.close()


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
                armState.printState()
                armState.incrementPC()
                armState.cycle += 1
                continue
            elif (self.opcode[i] >= 160 and self.opcode[i] <=191):#B
                jumpAddr = jumpAddr + ((self.arg1[i] * 4) - 4)
            elif self.opcode[i] == 1112: #ADD
                armState.R[self.arg3[i]] = armState.R[self.arg2[i]] + armState.R[self.arg1[i]]
            elif self.opcode[i] == 1624: #SUB
                armState.R[self.arg3[i]] = armState.R[self.arg1[i]] - armState.R[self.arg2[i]]
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
                armState.R[self.arg3[i]] = 0
                armState.R[self.arg3[i]] = self.arg2[i] * self.arg1[i]
            elif (self.opcode[i] >= 1940 and self.opcode[i] <= 1943): #MOVK
                if self.arg1[i] == 0:
                    armState.R[self.arg3[i]] = armState.R[self.arg3[i]] & 0xFFFFFFFFFFFF0000
                elif self.arg1[i] == 16:
                    armState.R[self.arg3[i]] = armState.R[self.arg3[i]] & 0xFFFFFFFF0000FFFF
                elif self.arg1[i] == 32:
                    armState.R[self.arg3[i]] = armState.R[self.arg3[i]] & 0xFFFF0000FFFFFFFF
                else:
                    armState.R[self.arg3[i]] = armState.R[self.arg3[i]] & 0x0000FFFFFFFFFFFF
                armState.R[self.arg3[i]] = self.arg2[i] + (armState.R[self.arg3[i]] * self.arg1[i])
            elif self.opcode[i] == 1692: #ASR
                armState.R[self.arg3[i]] = armState.R[self.arg1[i]] >> self.arg2[i]
            elif self.opcode[i] == 1691: #LSL
                armState.R[self.arg3[i]] = (armState.R[self.arg1[i]] % (1 << 32)) << (self.arg2[i])
            elif self.opcode[i] == 1690: #LSR
                armState.R[self.arg3[i]] = (armState.R[self.arg1[i]] % (1 << 32)) >> (self.arg2[i])
            elif self.opcode[i] == 1872: #EOR
                armState.R[self.arg3[i]] = armState.R[self.arg1[i]] ^ armState.R[self.arg2[i]]
            elif self.opcode[i] == 1986: #LDUR
                addrOffest = armState.R[self.arg2[i]] + (self.arg1[i] * 4)
                found = False
                if addrOffest <= armState.address[len(armState.address) - 1]:
                    found = True
                if not found:
                    lastAddr = armState.address[len(armState.address) - 1] + 4
                    while lastAddr != addrOffest + 4:
                        armState.address.append(lastAddr)
                        lastAddr += 4
                    while len(armState.address) - armState.numInstructions > len(armState.dataval):
                        armState.dataval.append(0)
                    armState.R[self.arg3[i]] = 0

                if found:
                    addrIn = 0
                    for j in range(len(armState.address)):
                        if armState.address[j] == addrOffest:
                            addrIn = j

                    dataIn = addrIn - armState.numInstructions

                    if dataIn < 0:
                        armState.R[self.arg3[i]] = armState.R[self.arg3[addrIn]]
                    else:
                        armState.R[self.arg3[i]] = armState.dataval[dataIn]
            elif self.opcode[i] == 1984: #STUR
                addrOffest = armState.R[self.arg2[i]] + (self.arg1[i] * 4)
                found = False
                if addrOffest <= armState.address[len(armState.address) - 1]:
                    found = True
                if not found:
                    lastAddr = armState.address[len(armState.address) - 1] + 4
                    while lastAddr != addrOffest + 4:
                        armState.address.append(lastAddr)
                        lastAddr += 4
                    while len(armState.address) - armState.numInstructions - 1 > len(armState.dataval):
                        armState.dataval.append(0)
                    armState.dataval.append(armState.R[self.arg3[i]])
                if found:
                    addrIn = 0
                    for j in range(len(armState.address)):
                        if armState.address[j] == addrOffest:
                            addrIn = j

                    dataIn = addrIn - armState.numInstructions

                    if dataIn < 0:
                        armState.R[self.arg3[addrIn]] = armState.R[self.arg3[i]]
                    else:
                        armState.dataval[dataIn] = armState.R[self.arg3[i]]
            elif self.opcode[i] == 2038: #BREAK
                foundBreak = True

            else: #ERROR
                print("IN SIM -- UNKNOWN INSTRUCTION ------------------ !!!!")

            armState.printState()
            armState.PC = jumpAddr
            armState.incrementPC()
            armState.cycle += 1