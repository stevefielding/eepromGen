# --------------------------- eepromGen.py ---------------------------------------
# Generate a hex file to intialize an EEPROM. This particular example is for
# a 0x400 byte eeprom inside an ATMega328pb
# usage example
# eepromGen.py --nodeId 1 --serialNum bogusSerialNum1234 --nodeDesc "I am a controller" -o "hexfiles/node.eep" -nodeName escNode

from intelhex import IntelHex
import argparse

EEPROM_SIZE = 0x400
TABLE_VERSION_ADDR = 0x0
NODE_ID_ADDR = 0x4
SER_NUM_ADDR = 0x10
MAX_SER_NUM_LEN = 0x20
DESC_ADDR = 0x40
MAX_DESC_LEN = 0x40
NODE_NAME_ADDR = 0x80
MAX_NODE_NAME_LEN = 0x20
CHECK_SUM_ADDR = 0x1ff  # only use half the eeprom

allowedNodeNames = ["escNode", "bstNode", "icNode", "awNode", "asNode", "tpmsNode", "aeNode"]
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--nodeId", required=True, type=int, choices=range(1, 256),
  help="RS485 node ID (1 - 255). ID: 0 is reserved")
ap.add_argument("-s", "--serialNum", required=True, type=str,
  help="serial number")
ap.add_argument("-n", "--nodeName", required=True, type=str, choices=allowedNodeNames,
  help="Node name")
ap.add_argument("-d", "--nodeDesc", required=True, type=str,
  help="Node description")
ap.add_argument("-o", "--outputFile", required=True, type=str,
  help="Output eep hex file")
args = vars(ap.parse_args())
print("[INFO] node ID: {}".format(args["nodeId"]))
print("[INFO] Node name: \"{}\"".format(args["nodeName"]))
print("[INFO] Node description: \"{}\"".format(args["nodeDesc"]))
print("[INFO] Serial number: \"{}\"".format(args["serialNum"]))
print("[INFO] Output file: \"{}\"".format(args["outputFile"]))

# check arguements are within range. Leave room for string terminating null char
sn = args["serialNum"]
if len(sn) > MAX_SER_NUM_LEN-1:
  print("[ERROR] Serial num: {}, too long, max len: {}".format(sn, MAX_SER_NUM_LEN-1))
nodeDesc = args["nodeDesc"]
if len(nodeDesc) > MAX_DESC_LEN-1:
  print("[ERROR] Description: {}, too long, max len: {}".format(nodeDesc, MAX_DESC_LEN-1))
nodeName = args["nodeName"]
if len(nodeName) > MAX_NODE_NAME_LEN-1:
  print("[ERROR] Description: {}, too long, max len: {}".format(nodeName, MAX_NODE_NAME_LEN-1))

ih = IntelHex()   # create empty object
# init entire eeprom to 0x00
ih[0:EEPROM_SIZE] = [0x00] * EEPROM_SIZE
#print("[INFO] Min address: {}, Max address: {}".format(ih.minaddr(), ih.maxaddr()))

# write the table contents
ih[TABLE_VERSION_ADDR:2] = [0x1, 0x0] # eeprom table format version number
ih[NODE_ID_ADDR] = args["nodeId"] # node ID
ih.puts(SER_NUM_ADDR, sn) # serial number
ih.puts(DESC_ADDR, nodeDesc)  # Node description
ih.puts(NODE_NAME_ADDR, nodeName)  # Node name

# add the checksum
checkSum = 0
for i in range(CHECK_SUM_ADDR):
  checkSum += ih[i]
checkSum &= 0xff
ih[CHECK_SUM_ADDR] = checkSum # checksum

# Write the new hex data to file
ih.write_hex_file(args["outputFile"])
print("[INFO] Created output hex file: \"{}\"".format(args["outputFile"]))
