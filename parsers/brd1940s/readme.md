1940s parsing
=============

Changes here:

1) The pronunciation lines that were common in the 30s vanish, so I can cut that bit of code.

2) I was having lots of problems with reviews getting divided in the middle of a quotation, whenever numbers would happen to be mentioned. After some diagnostics, I found that way too many things were counting as review words. In particular, it was a bad idea to allow lowercase versions of the words, "and" / "&", and the word "Review," which appears commonly in self-references to Book Review Digest. I created a new version of ```read_pubnames.py``` that doesn't allow those. Then I also tightened the logic for recognizing a line as a review-citation. I now require *both* a reviewword and a numberword, but also allow certain very citation-y kinds of numbers (like 32:456, p23, and 400w) to add up to the equivalent of a reviewword. This ensures that I'm able to recognize new publication names when they get added in subsequent years. The upshot of this change is that we now have both fewer false negatives and fewer false positives. It's important enough that I migrated this back to the 1930s and may need to extend it all the way back to the 20s.

3) Another very important change: when a review-citation fails to end with a wordcount, I was looking forward to the next line and grabbing it if it ends with a wordcount, on the theory that it's a continuation. As quotation/reviews have gotten shorter and in some cases vanished, that became a bad idea. It started to create lots of cases where one citation was eating the next. This was easily addressed by adding a condition that checks whether the next line is < 3 words long, and only takes it if that's true.
