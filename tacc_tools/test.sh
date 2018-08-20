ARRAY_JOB_ID=0
NUM_JOBS=3

for i in $(seq 0 $(( 3 - 1 )) )
do
    ( singularity run /work/05254/craddock/singularity_images/fcpindi_cpac_v1.3.img \
            --skip_bids_validator \
            --data_config_file /work/05254/craddock/hikari/cpac_out/configs/data_config.yml \
            --aws_input_creds /work/05254/craddock/hikari/cpac_out/configs/cc-fcp.csv \
            --n_cpus 8 \
            --mem_gb 16 \
            s3://fcp-indi/data/Projects/Cambridge_Buckner/sourcedata/ \
            s3://fcp-indi/data/Projects/Cambridge_Buckner/cpac_output/ \
            participant \
            --participant_ndx "$(( ARRAY_JOB_ID + $i ))" > /tmp/cpac_out/log_$(( ARRAY_JOB_ID + $i )).log 2>&1 )&
done

echo "finished starting jobs, now waiting"

wait
