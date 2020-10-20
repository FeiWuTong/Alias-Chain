#!/bin/sh
./geth --targetgaslimit 10100000 --datadir privateChain --networkid 20 --nodiscover --rpc --rpcapi "db,eth,net,web3,miner,personal,txpool" --rpcaddr localhost console 2>>geth.log
