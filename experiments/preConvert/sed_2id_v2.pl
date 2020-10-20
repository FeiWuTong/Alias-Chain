#!usr/bin/perl

use JSON;

my $addr_id_file = 'AddrIdMap10';
my $target = 'sm_sccall_conv1';
my $target_cnt = 1;
my $output_file = 'sm_sccall_conv_id1';
my %addr_id;
my $addr;
my $id;

open(INPUT, '<', $addr_id_file) or die "Error: $!";
while (<INPUT>) {
	($addr, $id) = split;
	$addr_id{$addr} = $id;
}
close INPUT or die "Error: $!";

open(LOG, '>', "./sed_2id.log") or die "Log error: $!";

# two loops, recommend outer loop to traverse files, inner loop to traverse pair addr-id, only (1 + $target_cnt) file-io 
# or, swap two loops will cause (10M+ * $target_cnt) file-io, which is slower
for (my $i = 1; $i <= $target_cnt; $i++) {
	my $json;
	open(INPUT, '<', $target.$i.".json") or die "Error: $!";
	$json = <INPUT>;
	close INPUT or die "Error: $!";

	$json = decode_json($json);
	foreach my $json_obj (@{$json->{'txs'}}) {
		$addr = $json_obj->{'to'};
		if (exists $addr_id{$addr}) {
			$id = $addr_id{$addr};
			$json_obj->{'id'}  = $id;
			delete $json_obj->{'to'};
		}
	}

	open(OUTPUT, '>', $output_file.$i.".json") or die "$output_file cannot open: $!";
	print OUTPUT encode_json $json;
	close OUTPUT or die "$output_file cannot close: $!";
	
	print LOG "[Complete] $target\n";
}

close LOG or die "Log error: $!";
