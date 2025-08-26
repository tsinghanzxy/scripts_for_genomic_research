for i in {2..268..2}; do
    outfile="/home/tsinghan/134LLO_core/file_$i"
    ls  /home/tsinghan/data_Legionella/LLO_data_new/LLO_new_faa0408/core_134LLO/*.faa|while read id
    do
        awk -v line=$i 'NR==line {print $0}' $id >> "$outfile"
    done
done