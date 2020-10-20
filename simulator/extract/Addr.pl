#!/usr/bin/perl -wl
use strict;

# parameters here
my $target_file = 'txStatis';
my $output_file1 = 'FromStatis40';
my $output_file2 = 'ToStatis40';
my $target_separator = '\\s+';
my $underground = 1951;
my $target_filecount = $underground + 49;
my @temp;

open(WF1, '>>', $output_file1) or die "Can't not write ${output_file1}: $!";
open(WF2, '>>', $output_file2) or die "Can't not write ${output_file2}: $!";
foreach my $cur_file ($underground..$target_filecount) {
	open(RF, '<', $target_file.$cur_file) or die "Can't not read ${target_file}: $!";
	while (<RF>) {
		# ignore blockheight line
		@temp = split /$target_separator/;
		if (@temp < 4) {
			next;
		}
		print WF1 $temp[0];
		print WF2 $temp[1];
	}
	close(RF) or die "Can't close ${target_file}${cur_file}: $!";
}
close(WF1) or die "Can't close ${output_file1}: $!";
close(WF2) or die "Can't close ${output_file2}: $!";