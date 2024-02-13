# Analyzing-citation-networks
This project involves exploring the High-energy physics citation network. Arxiv HEP-PH (high energy physics phenomenology) citation graph is from the e-print arXiv and covers all the citations within a dataset of 34,546 papers with 421,578 edges.

## Instructions to run:

### Exploration.py:
1) Make sure you have installed networkx library. Run the following on terminal if you are using linux:
    ```
    pip install networkx[default]
    ```
2) Run exploration.py from code directory of this repository.
3) The dataset is huge and the code may not run locally because of compute constraints. So it is recommened to run the code on google colab.

## References:

    https://networkx.org/documentation/stable/tutorial.html
    https://medium.com/data-science-in-your-pocket/community-detection-in-a-graph-using-louvain-algorithm-with-example-7a77e5e4b079

** For degree centrality, could have plotted in-degree and out-degree centrality seperately to show how many cited and how many cititations
** Number of citations doesnt reach 421,578 cause there are some nodes in edges which are out of the network
