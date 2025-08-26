from Bio import SeqIO
gbk_filename = "c00079_GUT_GEN...region001.gbk"#.gbk文件名
faa_filename = "c00079_GUT_GEN...region001.fna"#输出文件名
input_handle  = open(gbk_filename, "r")
output_handle = open(faa_filename, "w")

for seq_record in SeqIO.parse(input_handle, "genbank") :
    print("Dealing with GenBank record %s" % seq_record.id)
    output_handle.write(">%s %s\n%s\n" % (
           seq_record.id,
           seq_record.description,
           seq_record.seq))

output_handle.close()
input_handle.close()