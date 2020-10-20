#!/usr/bin/perl
use JSON;
use Data::Dumper;

my $file_count = 1;
my $prefix = "contract1_smtx_conv1";
my $output = "sm_sccall1";
my $account = 0;

for (my $i = 1; $i <= $file_count; $i++) {
	my @txs;
	my %tx;
	my %json;
	open(INPUT, '<', $prefix.$i) or die "$prefix cannot open: $!";
	while (<INPUT>) {
		if (/, /) {
			next;
		}
		(undef, $tx{'to'}, $tx{'value'}, $tx{'input'}) = split;
		if ($tx{'to'} eq 'null' || length($tx{'input'}) > 30000) {
			next;
		}
		$tx{'from'} = $account;
		push @txs, {%tx};
	}
	close INPUT or die "$prefix cannot close: $!";
	open(OUTPUT, '>', $output.$i.'.json') or die "$output cannot open: $!";
	@{$json{'txs'}} = @txs;
	print OUTPUT encode_json \%json;
	close OUTPUT or die "$output cannot close: $!";
}
