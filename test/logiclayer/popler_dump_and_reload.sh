#!bin/bash
python ~/Desktop/git/database-development/test/droprecords.py
py.test ~/Desktop/git/database-development/test/logiclayer/test_mergedtoupload_count.py
py.test ~/Desktop/git/database-development/test/logiclayer/test_mergedtoupload_biomass.py
py.test ~/Desktop/git/database-development/test/logiclayer/test_mergedtoupload_density.py
py.test ~/Desktop/git/database-development/test/logiclayer/test_mergedtoupload_percent_cover.py
py.test ~/Desktop/git/database-development/test/logiclayer/test_mergedtoupload_individual.py
