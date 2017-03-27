#!/usr/bin/python

"""
DESCRIPTION
              Python md_py.py [OPTIONS][PARAMETERS] 

            md_py is a python code which generates a Verilog code for a multistage shift register. The generated Verilog code is synthesizable. User provides required width, stages and reset value for the register. Width is the operand width and should be from 1 to 64 while stages is the number of pipeline stages and the decimal value should be from 2 to 128.


OPTIONS

	 --help or -h: Prints the command line options.
	 
	 --param or -p: input parameter file name

	 --width or -w: Enter the operand width (decimal value from 1 to 64)

	 --stages or -s: Enter the number of pipeline stages (decimal value from 2 to 128)

	 --reset or -r: Enter the reset value of the register in decimal or hex

	 --outfile or -o: Enter the desired verilog file name  

	 Example terminal commands:

	python md_py.py  --param param.txt
	python md_py.py  -p param.txt

	python md_py.py --width 5 --stages 6 --reset 2 --outfile ver.v

	python md_py.py --help
        pydoc md_py

	Example parameter text file:

	width = 16;

	stages = 10;

	outfile = chkreg.v;

	reset = 8;


BUGS

	If you find any bug please send an email to md6625@rit.edu.

AUTHOR

	Mayank Dhull

COPYRIGHT

	This python code is free to use and can be used under the terms of Rochester Institute of Technology Copyright policy C03.2.
"""


import random
import sys
import os
import getopt
import re
import pydoc

def help():
	print('''--param: input parameter file name
--width: Enter the operand width (decimal value from 1 - 64)
--stages: Enter the number of pipeline stages (decimal value from 2 - 128)
--reset: Enter the 'reset'value of the register
--outfile: Enter the desired verilog file name with extension .v

Note: Cannot enter parameter file along with other parameters. ''')

message = '''

--param: input parameter file name
--width: Enter the operand width (decimal value from 1 - 64)
--stages: Enter the number of pipeline stages (decimal value from 2 - 128)
--reset: Enter the 'reset'value of the register
--outfile: Enter the desired verilog file name with extension .v

Note: Cannot enter parameter file along with other parameters. '''

try:
   opts, args= getopt.getopt(sys.argv[1:],'w:s:r:o:p:h',["help", "width=", "stages=", "reset=", "outfile=", "param="])
except getopt.GetoptError:
   print "Error in command line arguments"
   sys.exit()		

hf=0     # these are the flags that will be used later to check if all the parameters are defined or not
wf=0
sf=0
rf=0
of=0
pf=0


for opt, arg in opts:        # reading arguments from terminal
    if opt in ('--help', '-h'):
       hf=1
       print(message)
       sys.exit()
    elif opt in ('--stages', '-s'):
       stages = arg
       sf=1	
    elif opt in ('--width','-w'):
       width = arg
       wf=1
    elif opt in ('--reset','-r'):
       reset = arg
       rf=1
    elif opt in ('--outfile','-o'):
       outfile = arg
       of=1
    elif opt in ('--param','-p'):
       param = arg
       pf=1
    else:
       usage()
       sys.exit()	
    

def func():
	global reset
	global width
	global stages
	global outfile	
	if (pf ==1 and (rf==1 or wf==1 or sf==1 or hf==1)):
	   print("Cannot enter param and other parameters together" + message)
	   sys.exit()
	if (pf==0 and hf==0 and (rf==0 or wf==0 or sf==0 or of==0)):
	   print("Invalid parameter. Enter all the parameters correctly" + message)
	   sys.exit()
	if (hf==1 and pf==0 and rf==0 and wf==0 and sf==0 and of==0):
	   help()
	   sys.exit()


	if (pf==1):
	    try:
		fh1= open(param)
	    except:
		print ("Cannot open parameter file" + message)
		sys.exit()

	    while 1:
		    
		    read = fh1.readline()
		    if not read:
			break
		    if(re.match(r'\s*(stages)\s*', read, re.I)):
			matching = re.match(r'\s*(stages)\s*=\s*(.*)\s*;', read, re.I)
			stages= matching.group(2)
	
		   
		    elif re.match(r"\s*(width)\s*", read, re.I):
			matching = re.match(r"\s*(width)\s*=\s*(.*)\s*;", read, re.I)
			width= matching.group(2)
	
		   
		    elif re.match(r"\s*(outfile)\s*", read, re.I):
			matching = re.match(r"\s*(outfile)\s*=\s*(.*)\s*;", read, re.I)
			outfile= matching.group(2)
	

		    elif re.match(r"\s*(reset)\s*", read, re.I):
			matching = re.match(r"\s*(reset)\s*=\s*(.*)\s*;", read, re.I)
			reset= matching.group(2)
	
		    elif re.match(r"\s*", read, re.I):
			break
		    else:
		       print ("Incorrect arguments, Please check the parameter file"+ message)
		       sys.exit()	


def chk():
	global reset
	global width
	global stages

	if '0x' in reset:
	   reset= int (reset, 16)   #convert hex to decimal
	else:
	   reset= reset

	try:
	  stages= int(stages)
	except:
	  print("Stages should be a valid integer value")
	  sys.exit()
	try:
	  width= int(width)
	except:
	  print("Width should be a valid integer value")
	  sys.exit()
	try:
	  reset= int(reset)
	except:
	  print("Reset should be a valid integer value")
	  sys.exit()


def ver_code():
        global reset
	global width
	global stages
	global outfile
   
        outf= outfile.strip('.v')
	reset_dec = reset
	width_i= width -1 
	stages_i = stages -2

	#check conditions
	if((width > 64) or (width  < 1)): 
	  print('width cannot be less than 1 and greater than 64' + message)    
	  sys.exit ()

	if(stages > 128 or stages  < 2): 
	    print ("stages cannot be less than 2 and greater than 128" + message)
	    sys.exit ()
	if(reset_dec > (2**width - 1)): 
	    print("Reset value cannot be greater than allowed number of bits" + message)
	    sys.exit ()



	#write verilog code
	fh = open(outfile, "wb")
	text1 = '''module %s (
		   reset,
		   clk,
		   scan_in0,
		   scan_en,
		   test_mode,
		   scan_out0,
		   data_in,
		   data_out
	       );
	   input
	    reset,                      // system reset
	    clk;                        // system clock

	   input
	    scan_in0,                   // test scan mode data input
	    scan_en,                    // test scan mode enable
	    test_mode;                  // test mode select 

	output
	    scan_out0;                  // test scan mode data output
	     
	input [%d:0] data_in;  

	output reg [%d:0] data_out; 

	reg [%d:0] temp [%d:0];

	always @(posedge clk or posedge reset)
	begin
	   if (reset == 1'b1) 
	      begin\n
	'''%(outf, width_i, width_i, width_i, stages_i)

	fh.writelines (text1)


	j=0

	while (j < (stages-1)):    
	 text2= ''' temp[%d] <= %d;\n'''%(j,reset_dec)
	 fh.writelines (text2)
	 j+= 1
	  

	text3= ''' data_out <= %d;
	    end
	 else
	    begin
	 temp[0] <= data_in; \n'''%(reset_dec)

	i=1;
	i_dec=0;
	fh.writelines (text3)

	while (i < (stages-1)):      
		text4 = ''' temp[%d] <= temp[%d]; \n'''%(i, i_dec)
		fh.writelines (text4)
		i= i+1
		i_dec+=1
	  
	    
	text5 = ''' data_out <= temp[%d];
	   end

	end

	endmodule '''%(stages_i)   


	fh.writelines (text5)

	fh.close()
if __name__== '__main__':
	func()
	chk()
	ver_code()

