wmd: word mover's distance
==========================

Actually this directory contains some files that measure ordinary cosine distance as well as word mover's distance.

Experiment 1 aligns with the first experiment in the [first registration.](https://github.com/tedunderwood/reviews/blob/master/bpo/corexperiment/registrations/firstregistration.md)

Experiment 2a begins to test the second: word mover's distance on the top categories in matched books. We need to eventually test the top 87; this script started with the top 25.

Experiment 2b addresses the second part of experiment 2: 25 categories selected to be recognizable as "genres." We're not sure there's really a crisp distiction between subject, form, and genre categories, but since some readers will believe there is it seems wise to be cautious and test a conservative definition of the term.

2b*prime* was created because we recognized that our strategy of pairing in-genre and random texts was flawed. Instead of comparing A<->B (in genre) and randomA <-> randomB (out of genre control) it makes sense to make the out of genre control relative to in-genre texts

    distance from A to randomB and
    distance from B to randomA

This is important because some genres may be located in a very sparse and spacious portion of the feature space. Everything could be distant from everything. So if we compare in-genre distances to average random distances, we'll get a misleading impression that these works aren't close to each other, when in reality they are *closer* to each other than they are to anything else.

Experiment 2c shifted from word mover's distance to ordinary cosine distance. Although our wmd experiment successfully produced a strong correlation between books and reviews, we didn't feel confident about interpreting the results. Cosine distance proved easier to interpret, both because it's simpler and because the results were more parallel to predictive modeling results.
