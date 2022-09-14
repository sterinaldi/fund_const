file="newtonsConstantWithLabels.dat"
outfolder="newtonG"
label="G"
unit="\times 10^{-11}\ \mathrm{m}^3\mathrm{km}^{-1}\mathrm{s}^{-2}"
bounds="[6.668, 6.678]"
codata_val="6.67430"
codata_err="0.00015"

if [ ! -d $outfolder ]; then
    mkdir $outfolder
fi
python least_squares.py -i $file
python sigma_level.py -i $file -o $outfolder
python gensamps.py -i $file -o $outfolder

python par_inference.py -i $file -o $outfolder -b $bounds -l $label -u $unit 2>/dev/null

if [ ! -f $outfolder"/draws/posteriors_single_event.pkl" ]; then
    figaro-hierarchical -i experiments -o $outfolder --symbol $label --unit $unit -b $bounds --name $outfolder -s
else
    figaro-hierarchical -i experiments -o $outfolder --symbol $label --unit $unit -b $bounds --name $outfolder -e
fi

python make_plots.py -i $file -o $outfolder -l $label -u $unit -v $codata_val -e $codata_err -n $outfolder
