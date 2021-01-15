# eepromGen.py 
Generate a hex file to intialize an EEPROM. This particular example is for
a 0x400 byte eeprom inside an ATMega328pb
usage example
eepromGen.py --nodeId 1 --serialNum bogusSerialNum1234 --nodeDesc "I am a controller" -o "hexfiles/node.eep" -nodeName escNode
