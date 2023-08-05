**INFOTOPO**


**InfoTopo: Topological Information Data Analysis. Deep statistical unsupervised and supervised learning.**

For a complete documentation, see `read the doc site infotopo <https://infotopo.readthedocs.io/en/latest/>`_

For installation (`PyPI install infotopo <https://pypi.org/project/infotopo/>`_
), presuming you have numpy and networkx installed:
**pip install infotopo**

InfoTopo is a Machine Learning method based on Information Cohomology, a cohomology of statistical systems [1,8,9]. 
It allows to estimate higher order statistical structures, dependences and (refined) independences or generalised (possibly non-linear) correlations and to uncover their structure as simplicial complex.
It provides estimations of the basic information functions, entropy, joint and condtional, multivariate Mutual-Informations (MI) and conditional MI, Total Correlations...

InfoTopo is at the cross-road of Topological Data Analysis, Deep Neural Network learning, statistical physics and complex systems:
 1. With respect to Topological Data Analysis (TDA), it provides intrinsically probabilistic methods that does not assume metric (Random Variable's alphabets are not necessarilly ordinal) [2,3,6].

 2. With respect to Deep Neural Networks (DNN), it provides a simplical complex constrained DNN structure with topologically derived unsupervised and supervised learning rules (forward propagation, differential statistical operators). The neurons are random Variables, the depth of the layers corresponds to the dimensions of the complex [3,4,5].

 3. With respect to statistical physics, it provides generalized correlation functions, free and internal energy functions, estimations of the n-body interactions contributions to energy functional, that holds in non-homogeous and finite-discrete case, without mean-field assumptions. Cohomological Complex implements the minimum free-energy principle. Information Topology is rooted in cognitive sciences and computational neurosciences, and generalizes-unifies some consciousness theories [5].

 4. With respect to complex systems studies, it generalizes complex networks and Probabilistic graphical models to higher degree-dimension interactions [2,3].

It assumes basically:
 1. a classical probability space (here a discrete finite sample space), geometrically formalized as a probability simplex with basic conditionning and Bayes rule and implementing  
 2. a complex (here simplicial) of random variable with a joint operators
 3. a quite generic coboundary operator (Hochschild, Homological algebra with a (left) action of conditional expectation)

The details for the underlying mathematics and methods can be found in the papers:

[1] Vigneaux J., Topology of Statistical Systems. A Cohomological Approach to Information Theory. Ph.D. Thesis, Paris 7 Diderot University, Paris, France, June 2019. `PDF-1 <https://webusers.imj-prg.fr/~juan-pablo.vigneaux/these.pdf>`_
 
[2] Baudot P., Tapia M., Bennequin, D. , Goaillard J.M., Topological Information Data Analysis. 2019, Entropy, 21(9), 869  `PDF-2 <https://www.mdpi.com/1099-4300/21/9/869>`_
 
[3] Baudot P., The Poincaré-Shannon Machine: Statistical Physics and Machine Learning aspects of Information Cohomology. 2019, Entropy , 21(9),  `PDF-3 <https://www.mdpi.com/1099-4300/21/9/881>`_

[4] Baudot P. , Bernardi M.,  The Poincaré-Boltzmann Machine: passing the information between disciplines, ENAC Toulouse France. 2019 `PDF-4 <https://drive.google.com/open?id=1bo_tju7BLYTdAcZasDPtx-xQ2HOc3E8A>`_

[5] Baudot P. , Bernardi M.,  Information Cohomology methods for learning the statistical structures of data. DS3 Data Science, Ecole Polytechnique 2019 `PDF-5 <https://www.google.com/url?q=https%3A%2F%2Fwww.ds3-datascience-polytechnique.fr%2Fwp-content%2Fuploads%2F2019%2F06%2FDS3-426_2019_v2.pdf&sa=D&sntz=1&usg=AFQjCNHWjQjdREgj7K10jKpLKnTVWTL5iA>`_  

[6] Tapia M., Baudot P., Dufour M., Formizano-Treziny C., Temporal S., Lasserre M., Kobayashi K., Goaillard J.M.. Neurotransmitter identity and electrophysiological phenotype are genetically coupled in midbrain dopaminergic neurons. Scientific Reports. 2018. `PDF-6 <https://www.nature.com/articles/s41598-018-31765-z>`_
 
[7] Baudot P., Elements of qualitative cognition: an Information Topology Perspective. Physics of Life Reviews. 2019. extended version on Arxiv. `PDF-7 <https://arxiv.org/abs/1807.04520>`_
 
[8] Baudot P., Bennequin D., The homological nature of entropy. Entropy, 2015, 17, 1-66; doi:10.3390. `PDF-8 <https://www.mdpi.com/1099-4300/17/5/3253>`_
 
[9] Baudot P., Bennequin D., Topological forms of information. AIP conf. Proc., 2015. 1641, 213. `PDF-9 <https://aip.scitation.org/doi/abs/10.1063/1.4905981>`_
 


The previous version of the software  INFOTOPO : the 2013-2017 scripts are available at `Github infotopo <https://github.com/pierrebaudot/INFOTOPO/>`_
 



