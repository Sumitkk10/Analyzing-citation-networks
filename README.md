# Analyzing-citation-networks
This project involves exploring the High-energy physics citation network. Arxiv HEP-PH (high energy physics phenomenology) citation graph is from the e-print arXiv and covers all the citations within a dataset of 34,546 papers with 421,578 edges.

## Instructions to run:

Make sure you have installed networkx library. Run the following on terminal if you are using linux:
```
pip install networkx[default]
```

### Exploration.py:
1) Run exploration.py from code directory of this repository.
2) The dataset is huge and the code may not run locally because of compute constraints. So it is recommened to run the code on google colab.
3) Various graphs have been plotted which are explained in the detailed report.
4) I have used ```matplotlib``` to plot all the graphs.

### louvain.py:
1) Various graphs have been plotted which are explained in the detailed report.
2) I have used ```random``` module to randomly choose 1% of the dataset to plot communities.

### girvan_newman.py:
1) The computational complexity is pretty high for this algorithm.
2) As a user input, you can give till which year do you want to find the communities and it will return a plot of different communities.
3) Various graphs have been plotted which are explained in the detailed report.

## References:

    https://networkx.org/documentation/stable/tutorial.html
    https://arxiv.org/pdf/0803.0476.pdf
    https://medium.com/data-science-in-your-pocket/community-detection-in-a-graph-using-louvain-algorithm-with-example-7a77e5e4b079
    https://youtu.be/me3UsMm9QEs?si=_SIvOcKQtsfhFFWw
    https://medium.com/analytics-vidhya/girvan-newman-the-clustering-technique-in-network-analysis-27fe6d665c92
    https://stellargraph.readthedocs.io/en/stable/demos/link-prediction/node2vec-link-prediction.html
