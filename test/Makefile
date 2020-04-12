PYTHON = python3
TESTS = $(wildcard test_*.py)

all:
	@- $(foreach TEST,$(TESTS), \
		echo === Running test: $(TEST); \
		$(PYTHON) $(TEST); \
		)

clean:
	rm *.log
		
scraper:
	$(PYTHON) test_scraper.py

base:
	$(PYTHON) test_base.py

base_headless:
	$(PYTHON) test_base_headless.py

amazon:
	$(PYTHON) test_amazon.py

amazon_headless:
	$(PYTHON) test_amazon_headless.py


.PHONY: all clean scraper base base_headless amazon amazon_headless