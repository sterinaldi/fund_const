# Probability distribution for the gravitational constant $G$ (and other fundamental constants)
Inference of the gravitational constant $G$ using the experiments listed in [Tisinga et al. (2021)](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.93.025010).

This code implements the two inferences described in Rinaldi et al (in preparation). To run it, just use the command `source run_inference.sh config/newtonG_config.sh`. This is expected to complete in o(20 minutes).

It is also possible to use this code to infer other fundamental constants: in order to do so, just add a `.dat` file to the `data` folder and a `_config.sh` file to the `config` folder, both following the existing templates. We provide config files and data for the gravitational constant $G$, the Boltzmann's constant $\beta$ and the Planck's constant $h$.

Before running the inference, please install [FIGARO](https://github.com/sterinaldi/figaro) and [this branch of CPNest](https://github.com/johnveitch/cpnest/tree/massively_parallel).
