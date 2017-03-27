#!/usr/bin/perl
#
use strict;
use warnings;


use Getopt::Long;
my $message = <<"END_MSG";

-param: input parameter file name
-width: Enter the operand width (decimal value from 1 - 64)
-stages: Enter the number of pipeline stages (decimal value from 2 - 128)
-reset: Enter the 'reset'value of the register
-outfile: Enter the desired verilog file name with extension .v

Note: Cannot enter parameter file along with other parameters. 

END_MSG

my $help;
my $param;
my $width;
my $stages;
my $reset;
my $outfile;
GetOptions ("param=s"=> \$param,
            "width=i" => \$width,
            "stages=i" => \$stages,
            "reset=s" => \$reset,
            "outfile=s" => \$outfile,
            "help" => \$help
            )
or die ("Error in command line argument\n $message\n;");

my $reset_dec;

&cmd_arg;
&if_param;

sub cmd_arg
{
if (defined $param && (defined $width || defined $stages || defined $reset || defined $outfile || defined $help))
  {

die ("Cannot enter param and other parameters together\n $message\n");
  }

if (!(defined $width && defined $stages && defined $reset && defined $outfile) && !defined $param &&  !defined $help)
{die ("Invalid parameter. Enter all the parameters correctly \n $message\n");}


if(defined $help)
  {
    die "$message";
  }
}


sub if_param
{
if(defined $param) {
open (my $fh1, '<', $param);
while (my $row = <$fh1>)
{
if($row=~ m/\s*width\s*=\s*\d+;/)
    {
($width) = $row=~ m/\s*width\s*=\s*(\d+)/
    } 

elsif($row=~ m/\s*stages\s*=\s*\d+;/)
    {
($stages) = $row =~ m/\s*stages\s*=\s*(\d+)\s*/i
    } 

elsif($row=~ m/\s*reset\s*=\s*0x\d+;/)
    {
($reset) = $row=~ m/\s*reset\s*=\s*0x(\d+)/;
 $reset_dec = hex ($reset);
    } 

elsif($row=~ m/\s*reset\s*=\s*\d+;/)
    {
($reset) = $row=~ m/\s*reset\s*=\s*(\d+)/;
$reset_dec = $reset;
    } 


elsif($row=~ m/\s*outfile\s*=\s*\X+;/)
    {
($outfile) = $row=~ m/\s*outfile\s*=\s*(\X+);/
    } 
}
if (!defined $width)
   {
 die ("width is not defined\n $message\n");
   }

if (!defined $stages)
   {
 die ("stages is not defined\n $message\n");
   }

if (!defined $reset)
   {
 die ("reset is not defined\n $message\n");
   }

if (!defined $outfile)
   {
 die ("outfile is not defined\n $message\n");
   } 
}  
} 
if (!defined $param) 
{
    if ($reset =~ m/\s*0x\d+/)
    {
        $reset_dec= hex($reset);
    }
    else 
    {
        $reset_dec= $reset;
    }
}



my $width_i= $width -1;
my $stages_i= $stages -2;

&param_check;

sub param_check
{
if($width > 64 || $width  < 1) 
{
    die ("width cannot be less than 1 and greater than 64\n $message\n");
}
 
if($stages > 128 || $stages  < 2) 
{
    die ("stages cannot be less than 2 and greater than 128\n $message\n");
}

if($reset_dec > 2**$width) 
{
    die ("Reset value cannot be greater than width\n $message\n");
}
} 
open (my $fh, '>', $outfile) or die("$message\n");

print $fh "module chkreg (
           reset,
           clk,
           scan_in0,
           scan_en,
           test_mode,
           scan_out0,
	   data_in,
	   data_out
       ); \n";
print $fh "input
    reset,                      // system reset
    clk;                        // system clock

input
    scan_in0,                   // test scan mode data input
    scan_en,                    // test scan mode enable
    test_mode;                  // test mode select 

output
    scan_out0;                  // test scan mode data output

input [$width_i:0] data_in;  

output reg [$width_i:0] data_out; 

reg [$width_i:0] temp [$stages_i:0];

always @(posedge clk or posedge reset)
begin
   if (reset == 1'b1) 
      begin\n";

my $j=0;

 while ($j < $stages)
       
  { print $fh " temp[$j] <= $reset_dec;\n";
        $j++;
  } 

 print $fh " data_out <= $reset_dec;
    end
 else
    begin
 temp[0] <= data_in;\n";
my $i=1;
my $i_dec=0;

 while ($i < $stages)
       
  { print $fh " temp[$i] <= temp[$i_dec];\n";
        $i++;
        $i_dec++;
  } 
    
  print $fh " data_out <= temp[$stages_i];
   end

end

endmodule \n";            
  

close $fh;

=pod

=head1 NAME

             md_perl -  Perl code for generating synthesizable Verilog HDL for a multistage pipeline register.

=head1 SYNOPSIS

              Perl md_perl.pl [OPTIONS][PARAMETERS] 

=head1 DESCRIPTION

            md_perl is a perl code which generates a Verilog code for a multistage shift register. The generated Verilog code is synthesizable. User provides required width, stages and reset value for the register. Width is the operand width and should be from 1 to 64 while stages is the number of pipeline stages and the decimal value should be from 2 to 128.

=head1 OPTIONS

=head3 -help: Prints the command line options.
 
=head3 -param: input parameter file name

=head3 -width: Enter the operand width (decimal value from 1 to 64)

=head3 -stages: Enter the number of pipeline stages (decimal value from 2 to 128)

=head3 -reset: Enter the reset value of the register in decimal or hex

=head3 -outfile: Enter the desired verilog file name  

=head2 Example terminal commands:

=head3 perl md_perl.pl  -param param.txt

=head3 perl md_perl.pl -width 5 -stages 6 -reset 2 -outfile ver.v

=head3 perl md_perl.pl -help

=head2 Example parameter text file:

=head3 width = 16;

=head3 stages = 10;

=head3 outfile = chkreg.v;

=head3 reset = 8;


=head1 BUGS

If you find any bug please send an email to md6625@rit.edu.

=head1 AUTHOR

Mayank Dhull

=head1 COPYRIGHT

This perl code is free to use and can be used under the terms of Rochester Institute of Technology Copyright policy C03.2.

=cut








 
