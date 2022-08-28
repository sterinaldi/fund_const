if [ ! -d "output" ]; then
    mkdir output
fi
python least_squares.py
python sigma_level.py
python gensamps.py

python par_inference.py 2>/dev/null
if [ ! -f "output/draws/posteriors_single_event.pkl" ]; then
    figaro-hierarchical -i experiments -o output --symbol 'G' --unit '\times 10^{-11}\ \mathrm{m}^3\mathrm{km}^{-1}\mathrm{s}^{-2}' -b '[6.668, 6.678]' -s
else
    figaro-hierarchical -i experiments -o output --symbol 'G' --unit '\times 10^{-11}\ \mathrm{m}^3\mathrm{km}^{-1}\mathrm{s}^{-2}' -b '[6.668, 6.678]' -e
fi

python make_plots.py
