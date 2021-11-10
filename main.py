import sys, argparse

class Machine:
    """Main Depression machine"""

    def __init__(self):
        self.__tape = []
        for i in range(32767):
            self.__tape.append(0)
        self.__tapeIndex = 0
        self.__prog = []
        self.__progIndex = 0

    def __twos_comp(self, val, bits):
        """compute the 2's complement of int value val"""
        if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)        # compute negative value
        return val                         # return positive value as is

    def load(self, fileName, clearPrevProg = True):
        if(clearPrevProg):
            self.__prog = []
            self.__progIndex = 0
        try:
            with open(fileName, "r") as file:
                data = file.read()
                split_data = data.split('\n')
                for item in split_data:
                    self.__prog.append(item)
        except:
            print("load failed")

    def parse(self, data):
        try:
            #3 symbols: -, |, ' '
            #syntax: negation_bit|instr|arg
            #if negation_bit has a '-', instr is inverted if applicable
            #arg is binary where a '-' is 0 and ' ' is 1
            data_parts = data.split('|')
            if(data_parts[0] == ''):
                data_parts[0] = ' '

            negated = 0
            instrnum = 0b0000
            arg = 0b0000
            s = {'-':0,' ':1}
            negated = s[data_parts[0]]

            if(negated == 0):
                negated = -1

            for char in data_parts[1]:
                instrnum ^= s[char]
                instrnum <<= 1
            instrnum >>= 1

            for char in data_parts[2]:
                arg ^= s[char]
                arg <<= 1
            arg >>= 1
            arg = self.__twos_comp(arg, 8)
            if(instrnum == 0):
                self.__tape[self.__tapeIndex] -= arg * negated
            if(instrnum == 1):
                self.__tapeIndex -= arg * negated
            if(instrnum == 2):
                if(self.__tape[self.__tapeIndex] != 0 and negated > 0):
                    self.__progIndex -= arg
                if(self.__tape[self.__tapeIndex] == 0 and negated < 0):
                    self.__progIndex -= arg
            if(instrnum == 3):
                if(negated > 0):
                    for i in range(arg):
                        sys.stdout.write(chr(self.__tape[self.__tapeIndex]))
                        self.__tapeIndex -= 1
                if(negated < 0):
                    for i in range(arg):
                        tchar = sys.stdin.read(1)
                        self.__tape[self.__tapeIndex] = ord(tchar)
                        self.__tapeIndex -= 1

            #sanity check after running
            if(self.__tapeIndex < 0):
                self.__tapeIndex = 0
            if(self.__tapeIndex > len(self.__tape)-1):
                self.__tape.append(0)

            #print("\n" + str(negated) + ":" + str(instrnum) + ":" + str(arg) + " " + str(self.tapeIndex) + ":" + str(self.progIndex))
        except:
            print("\nerr")

    def run(self):
        self.__progIndex = 0
        try:
            while(self.__progIndex < len(self.__prog)):
                self.parse(self.__prog[self.__progIndex])
                self.__progIndex += 1
        except:
            print("run err")

def interpreter():
    m = Machine()
    while True:
        print("\nready")
        data = input()#"depression> ")
        m.parse(data)

def executeFile(filename):
    m = Machine()
    m.load(filename)
    m.run()

def main(argv):
    parser = argparse.ArgumentParser(description='Depression esolang')
    parser.add_argument("-c", "--compile", default=None, metavar="file", help="runs a Depression file")
    args = parser.parse_args()
    if(args.compile != None):
        executeFile(args.compile)
    else:
        interpreter()
if(__name__ == "__main__"):
    main(sys.argv[1:])
