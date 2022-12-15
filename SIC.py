# -*- coding: utf-8 -*-
class Data:
    def __init__(self, loc, symbol, opcode, operand):
        self.loc = loc
        self.symbol = symbol
        self.opcode = opcode
        self.operand = operand

    def getline(self):
        temp = self.symbol.ljust(8) + '\t' + self.opcode.ljust(6) + '\t' + self.operand + '\t'
        return temp

def str_to_int( input_str ):
    output_int = 0
    for i in range(0, len(input_str)):
        output_int += ord(input_str[i]) * (i + 1)
    return output_int



def hash_insert( hashmap, key, value ):
    hashkey = str_to_int( key ) % 100
    while hashmap.get(hashkey, "emptyBucket") != "emptyBucket"  :
        hashkey = hashkey + 1
        if hashkey > 99:
            hashkey = 0
    hashmap[hashkey] = [key, value]


# ********************************************** Main **********************************************

# ************************* 檔案讀取 *************************

filename = str(input('輸入檔案名稱'))
f = open(filename + '.txt')
f1 = f.readlines()
file = []
for i in f1:
    addfile = []
    i = i.strip()
    if i == '':
        continue
    elif i[0] == '.':
        addfile = ['', '.', i[1:]]
    else:
        addfile = i.split()
        if len(addfile) == 0:
            addfile = ['']
        if len(addfile) == 1:
            addfile.append('')
        if len(addfile) == 2:
            addfile.insert(0, '')
    if addfile != ['', '', '']:
        file.append(addfile)
f.close()
t1 = open('Table1.table')
table1 = t1.read().splitlines()
table1_upper = []
for i in table1:
    table1_upper.append(i.upper())
t1.close()
t1_2 = open('Table1_2.table')
table1_1 = t1_2.readlines()
table1_2 = []
for i in range(0, len(table1_1)):
    table1_2.append(table1_1[i].split())
t1_2.close()

t2 = open('Table2.table')
table2 = t2.read().splitlines()
t2.close()
t3 = open('Table3.table')
table3 = t3.read().splitlines()
t3.close()
t4 = open('Table4.table')
table4 = t4.read().splitlines()
t4.close()
t5 = open('Table5.table', 'w+')
t6 = open('Table6.table', 'w+')
output = open(filename + '_output.txt', 'w+')
table5_hash = {}
table6 = {}
# table1, 1_upper, 1-2, 2 ,3, 4, 5, 6
data = []
# *********************************** pass1 ***********************************
start = 0
loc = 0
SYM_TAB = {}

for line in file: # 0:symbol, 1:opcode, 2:operand
    locctr = loc
    if line[1] == table2[0]:  # START
         start = int(line[2], 16)
         loc = start
         data.append(Data(hex(loc)[2:].upper().zfill(4), line[0], line[1], line[2]))
    elif line[1] == table2[1] or line[1] == '.':  # END or comment
        data.append(Data("\t", line[0], line[1], line[2]))
    elif line[1] == table2[6]:
        data.append(Data(hex(int(line[2]))[2:], line[0], line[1], line[2]))
    else:
        if line[0] != '':
            if line[0] in SYM_TAB:
                print(hex(loc)[2:].upper().zfill(4) + " \"" + line[0] + "\" Error: Symbol Redefinition")
            else:
                SYM_TAB[line[0]] = hex(loc)[2:].upper()  # 建立symbol table
                hash_insert(table5_hash, line[0], hex(loc)[2:].upper().zfill(4))
        if line[1] in table1: # op table
             locctr += int(table1_2[table1.index(line[1])][0])
        elif line[1] in table1_upper:
            locctr += int(table1_2[table1_upper.index(line[1])][0])
        elif line[1] == table2[2]:  # BYTE
            if line[2][0] == 'C':
                locctr += (len(line[2]) - 3)  # 減去C''的字元數
                hash_insert(table6, line[2][2:-1], hex(loc)[2:].upper() + " " + hex(locctr)[2:].upper())
            elif line[2][0] == 'X':
                locctr += int(len(line[2][2:-1])/2)  # X'F1' 僅算1
                hash_insert(table6, line[2][2:-1], hex(loc)[2:].upper() + " " + hex(locctr)[2:].upper())
            else:
                locctr += int(len(line[2])/2)
                hash_insert(table6, line[2], hex(loc)[2:].upper() + " " + hex(locctr)[2:].upper())
        elif line[1] == table2[3]:  # WORD
            locctr += 3
            hash_insert(table6, line[2], hex(loc)[2:].upper() + " " + hex(locctr)[2:].upper())
        elif line[1] == table2[4]:  # RESB
            locctr += int(line[2])
            hash_insert(table6, line[2], hex(loc)[2:].upper() + " " + hex(locctr)[2:].upper())
        elif line[1] == table2[5]:  # RESW
            locctr += (int(line[2]) * 3)
            hash_insert(table6, line[2], hex(loc)[2:].upper() + " " + hex(locctr)[2:].upper())
        else:
            print(hex(loc)[2:].upper() + " \"" + line[1] + "\" Error: Unknown Instruction")
        data.append(Data(hex(loc)[2:].upper().zfill(4), line[0], line[1], line[2]))
        loc = locctr

t5.write("hashkey\tkey\tloc\n")
for i in sorted(table5_hash):
    t5.write(str(i) + '\t' + str(table5_hash[i][0]) + '\t' + str(table5_hash[i][1]) + '\n')
t5.close()
t6.write("hashkey\tkey\tstartloc endloc\n")
for i in sorted(table6):
    t6.write(str(i) + '\t' + str(table6[i][0]) + '\t' + str(table6[i][1]) + '\n')
t6.close()

# *********************************** pass2 ***********************************

for line in data:
    objcode = ''
    if line.opcode == table2[0]:
        output.write('%6s %-6s %s\n' %( line.loc, line.getline(), ''))
    elif line.opcode == table2[1] or line.opcode == '.':
        output.write('%6s %-6s %s\n' % ('\t', line.getline(), ''))
    else:
        if line.opcode in table1:
            if line.operand == '':
                objcode = table1_2[table1.index(line.opcode)][1].ljust(6, '0')
            elif ',X' in line.operand:  # 遇到,X 加8000
                if line.operand[:-2] in SYM_TAB:
                    objcode = table1_2[table1.index(line.opcode)][1] + \
                              hex(int(SYM_TAB[line.operand[:-2]], 16) + int("8000", 16))[2:]
                else:
                    objcode = table1_2[table1.index(line.opcode)][1].ljust(6, '0')
                    print(hex(loc)[2:].upper() + " \"" + line.operand[:-2] + "\" Error: Symbol Undefined")
            elif line.operand in SYM_TAB:
                objcode = table1_2[table1.index(line.opcode)][1] + SYM_TAB[line.opcode]
            else:
                objcode = table1_2[table1.index(line.opcode)][1].ljust(6, '0')
                print(hex(loc)[2:].upper() + " \"" + line.operand + "\" Error: Symbol Undefined")
        elif line.opcode in table1_upper:
            if line.operand == '':
                objcode = table1_2[table1_upper.index(line.opcode)][1].ljust(6, '0')
            elif ',X' in line.operand:  # 遇到,X 加8000
                if line.operand[:-2] in SYM_TAB:
                    objcode = table1_2[table1_upper.index(line.opcode)][1] + \
                              hex(int(SYM_TAB[line.operand[:-2]], 16) + int("8000", 16))[2:]
                else:
                    objcode = table1_2[table1_upper.index(line.opcode)][1].ljust(6, '0')
                    print(hex(loc)[2:].upper() + " \"" + line.operand[:-2] + "\" Error: Symbol Undefined")
            elif line.operand in SYM_TAB:
                objcode = table1_2[table1_upper.index(line.opcode)][1] + SYM_TAB[line.operand]
            else:
                objcode = table1_2[table1_upper.index(line.opcode)][1].ljust(6, '0')
                print(hex(loc)[2:].upper() + " \"" + line.operand + "\" Error: Symbol Undefined")
        elif line.opcode == table2[2]:
            if line.operand[0] == 'C':
                for i in range(2, len(line.operand) - 1):
                    objcode += hex(ord(line.operand[i]))[2:].upper()
            elif line.operand[0] == 'X':
                objcode = line.operand[2:-1]
            else:
                objcode = hex(int(line.operand))[2:].upper()
        elif line.opcode == table2[3]:
            if line.operand[0] == '-':
                objcode = 'fff' + hex(4096 - int(line.operand[1:]))[2:].upper()
            else:
                objcode = hex(int(line.operand))[2:].zfill(6)
        else:
            objcode = "      "

        newobj = ''

        output.write('%6s %-6s %s\n' % (line.loc, line.getline(),objcode ))
        print('%6s %-6s %s' % (line.loc, line.getline(),objcode ))
output.close()


