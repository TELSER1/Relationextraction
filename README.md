Relationextraction
==================

As part of my effort to learn more about sequence models in NLP and information extraction (as opposed to bag-of-words text classification models that comprise my background), I'm building out a set of tools towards that end: first up is an implementation of distant supervision for relation extraction without labeled data (http://www.stanford.edu/~jurafsky/mintz.pdf), although I suspect many of my intended uses won't have a sufficiently large corpus and the precision/recall scores reported in the paper are probably too low.

Short term to-dos:

-Automatic model fitting
-Handle more general input
-incorporate syntactical variation
-move conditionals out of for loops for speed increase, maybe at expense of readibility.