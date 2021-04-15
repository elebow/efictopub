#!/bin/sh

case "$@" in
	*-k*) partial_test=1 ;;
esac

if [ "$partial_test" = 1 ]; then
	coverage_arg=''
else
	#show code coverage for the dir `efictopub`
  coverage_arg='--cov=efictopub'
fi

# -s         do not capture output. This is needed for ipdb.set_trace()

# clear HTTP cache
rm -rf test_cache

python3 -m pytest -s --color=yes $coverage_arg "$@"

# clear HTTP cache again, to clean up
rm -rf test_cache

exit $?
