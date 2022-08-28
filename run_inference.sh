if [ !-d "output" ]; then
    mkdir output
fi
python least_squares.py
python sigma_level.py
python gensamps.py

python par_inference.py
figaro-hierarchical -i experiments -o output --symbol 'G' --unit '\times 10^{-11}\ m^3km^{-1}s^{-2}' -b '[6.668, 6.678]' -s

python make_plots.py
