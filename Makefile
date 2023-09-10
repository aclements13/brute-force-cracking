test:
	@$(MAKE) -sk test-all

test-all:	test-scripts test-hulk

test-scripts:
	curl -sLO https://raw.githubusercontent.com/nd-cse-20289-sp23/cse-20289-sp23-assignments/master/homework06/test_hulk.sh
	curl -sLO https://raw.githubusercontent.com/nd-cse-20289-sp23/cse-20289-sp23-assignments/master/homework06/test.py
	curl -sLO https://raw.githubusercontent.com/nd-cse-20289-sp23/cse-20289-sp23-assignments/master/homework06/hashes.txt
	chmod +x test_hulk.sh test.py

test-hulk:
	./test_hulk.sh
