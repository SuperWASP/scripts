
for i in 2 4 5 6 7; do
    scp wasp-dataloader:/data/das${i}/NORMAL/DAS${i}_$1.fts . && python36 trim.py DAS${i}_$1.fts && solve-field DAS${i}_$1.fts --parity neg --overwrite --scale-units arcsecperpix --scale-high 14.5 --use-sextractor --scale-low 14;
done

swarp DAS*_$1.new

python36 plot.py $1
