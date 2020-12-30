1930s parsing
=============

First of all, for future reference, how do you start a new decade?

Copy over the old code into a new folder. Change names as needed. Visit [brdmetadata.tsv](https://github.com/tedunderwood/reviews/blob/master/metadata/brdmetadata.tsv) in order to find the volIDs for volumes. Create a new metadata file in secure_volume/brd/meta, using those volIDs and start/end pages you determine manually.

Then see how it's running on the new material. In this case I noticed two issues that could be improved:

1) There were often publisher names missing in the "publisher" field but present in the lines that precede ```<endsubj>``` in the review itself. I fixed this by adding an if-statement in ```quotationmaker``` that searches for publisher names (or *partial* publisher names in the tokens preceding ```<endsubj>```).

2) The routine was failing to divide citations if the wordcount got OCR'd as something like lOOw (instead of 100w). I fixed this by creating ```ocrwordcountregex```, which catches those sorts of things. Interpreting them numerically is a task for later in the pipeline.

I also wrote ```publisherfinder.py``` which gives me a way to dynamically and iteratively update my lists of publisher and review names by checking the ```publisher``` and ```publication``` columns in recent output for strings that are not present in the files we use to store those names. I can then manually edit the files.
