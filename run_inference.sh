source $1

if [ ! -d $outfolder ]; then
    mkdir $outfolder
fi
python fund_const/least_squares.py -i $file
python fund_const/sigma_level.py -i $file -o $outfolder
python fund_const/gensamps.py -i $file -o $outfolder -b $bounds

python fund_const/par_inference.py -i $file -o $outfolder -b $bounds -l $label -u $unit 2>/dev/null
figaro-hierarchical -i $outfolder"/experiments" -o $outfolder --symbol $label --unit $unit -b $bounds --name $outfolder -e --draws 1000 --no_probit

python fund_const/make_plots.py -i $file -o $outfolder -l $label -u $unit -v $codata_val -e $codata_err -n $outfolder
