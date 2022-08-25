# Probability distribution for the gravitational constant G
Inference of the gravitational constant probability G using the experiments listed in [Tisinga et al. (2021)](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.93.025010).

The parametric inference runs with `python par_inference.py`.

The nonparametric reconstruction requires [figaro](https://github.com/sterinaldi/figaro). Before running this inference, please run `python gensamps.py`, to generate the samples to be fed to figaro. FIGARO runs with `figaro-hierarchical -i experiments -o output --symbol 'G\times 10^{-11}' --unit 'm^3km^{-1}s^{-2}' -b '[6.668, 6.678]' -s`.
