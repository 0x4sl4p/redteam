#!/bin/bash
for sub in $(cat $2);do
	host -t cname $sub.$1 | grep "alias for"
done