Second stage of genre research
=====================================

We want to ask whether genres are becoming more or less tightly knit across the period from the mid-19c to the early 21c. This continues [an earlier experiment based on British Periodicals Online.](https://github.com/tedunderwood/reviews/tree/master/bpo/corexperiment)

At the moment, we're testing genre cohesion in two ways: 1) using Library of Congress genre categories assigned retrospectively by librarians, and 2) using genre categories inferred from a topic model of *Kirkus Reviews*, 1930-. The second experiment has the advantage of being based on more contemporary testimony. For a fuller description of both experiments, see [`secondregistration.md.`](https://github.com/tedunderwood/reviews/blob/master/kirkus/genrexp/secondregistration.md)

Data preparation for the first part of the experiment is in `make_loc_matrix.py,` and the vocabulary it produces is `loc_vocabulary.tsv.` The distances are measured by `measure_loc_distances.py`, and the results are in `loc_results.tsv.`

Data preparation for the second part of the experiment is in `get_kirkus_vols.py.` The distances are measured by `measure_kirkus_distances.py`, and the results are in `kirkus_results.tsv.`

Visualization scripts are in `\rplots.`



