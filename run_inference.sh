source $1

if [ ! -d $outfolder ]; then
    mkdir $outfolder
fi
python least_squares.py -i $file
python sigma_level.py -i $file -o $outfolder
python gensamps.py -i $file -o $outfolder

python par_inference.py -i $file -o $outfolder -b $bounds -l $label -u $unit 2>/dev/null

if [ ! -f $outfolder"/draws/posteriors_single_event.pkl" ]; then
    figaro-hierarchical -i $outfolder"/experiments" -o $outfolder --symbol $label --unit $unit -b $bounds --name $outfolder -s
else
    figaro-hierarchical -i $outfolder"/experiments" -o $outfolder --symbol $label --unit $unit -b $bounds --name $outfolder -e
fi

python make_plots.py -i $file -o $outfolder -l $label -u $unit -v $codata_val -e $codata_err -n $outfolder
