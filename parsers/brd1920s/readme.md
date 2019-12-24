1920s parsing
=============

An important difference in this decade is the introduction of page numbers, like "320p," which tend to appear right before the prices. This provides a much-needed clue that the next number is likely a price. These actually appear on the scene in 1922, so the divide between teens and twenties is actually a divide between 21 and 22.

I also increased the dollar limit on prices (to $40), and did some fiddling to expand the different kinds of uppercase text that count as a signal to start a new citation (i.e., book).

The pctupin15 flag (percentage uppercase letters in first 15 characters) proved so useful in this context that I backported it to the original (teens) instance of the parser.

Finally, the twenties see the introduction of Dewey decimal numbers and subject headings as the last line of the citation (before the reviews begin). Along with hyphen numbers, like 24-7569, these can be useful as signals to end the citation. But they aren't consistently present, and it would be dangerous to rely on them. One consequence of this variability is that subject headings will sometimes trail in the "publisher" column and sometimes be the first line in the first "review." To separate them from the rest of the review, I created an ```<endsubj>``` tag that separates trailing bibliographic lines from the review proper. There can be one or more of these.
