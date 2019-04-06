scp wasp-dataloader:/data/das$1/NORMAL/DAS$1_$2.fts . && python36 trim.py DAS$1_$2.fts && solve-field DAS$1_$2.fts --parity neg --overwrite --scale-units arcsecperpix --scale-high 14.5 --use-sextractor --scale-low 14;

python36 focus.py $1
