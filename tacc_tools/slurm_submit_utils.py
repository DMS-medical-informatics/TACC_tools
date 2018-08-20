import os

slurm_configuration_dictionary = {"job_name": "bids_job",
                                  "job_index": 0,
                                  "output_file": "bids_job.o%j",
                                  "total_number_of_jobs": 4,
                                  "number_of_nodes_requested": 1,
                                  "number_of_jobs_per_node": 3,
                                  "number_of_threads_per_job": 8,
                                  "number_of_threads_per_node": 24,
                                  "amount_of_memory_GB_per_job": 16,
                                  "time_required": "01:30:00",
                                  "bids_dir": "s3://fcp-indi/data/Projects/Cambridge_Buckner/sourcedata/",
                                  "output_dir": "/work/05254/craddock/hikari/cpac_out/output",
                                  "queue_name": "normal",
                                  "mail_to_address": None,
                                  "command": "participant",
                                  "log_file_path_prefix": "/work/05254/craddock/hikari/cpac_out/log",
                                  "path_to_container": "/work/05254/craddock/singularity_images/fcpindi_cpac_v1.3.img",
                                  "other_flags": "--data_config_file /work/05254/craddock/hikari/cpac_out/configs/data_config.yml --pipeline_config_file /work/05254/craddock/hikari/cpac_out/configs/pipeline_config.yml --aws_input_creds /work/05254/craddock/hikari/cpac_out/configs/cc-fcp.csv" }

def format_slurm_configuration_string(configuration_dictionary):
    slurm_base_configuration_string = "#SBATCH -J {job_name} # job name\n" \
                                      "#SBATCH -o {output_file} # output and error file name\n" \
                                      "#SBATCH -N {number_of_nodes_requested} # number of nodes requested\n" \
                                      "#SBATCH -n {number_of_threads_per_node} # total number of mpi tasks requested\n" \
                                      "#SBATCH -t {time_required} # run time (hh:mm:ss)\n" \
                                      "#SBATCH -p {queue_name} # job will run in the normal queue\n\n"

    slurm_email_configuration_string = "#SBATCH --mail-user={mail_to_address}\n" \
                                       "#SBATCH --mail-type=begin   # email me when the job starts\n" \
                                       "#SBATCH --mail-type=end     # email me when the job finishes\n"

    slurm_execution_variables_string = "ARRAY_JOB_ID = {job_index}\n" \
                                       "NUM_JOBS = {number_of_jobs_per_node}\n\n" \
                                       "for i in $(seq 0 $(( {number_of_jobs_per_node} - 1 )) )\n" \
                                       "do\n" \
                                       "    ( singularity {path_to_container} {other_flags} --participant_ndx $(( ARRAY_JOB_ID + $i )) {bids_dir} {output_dir} {command} > {log_file_path_prefix}_$(( ARRAY_JOB_ID + $i )).log 2>&1 )&\n" \
                                       "done\n" \
                                       "wait\n"

    slurm_configuration_string = slurm_base_configuration_string.format(**configuration_dictionary)
    
    if "mail_to_address" in configuration_dictionary and configuration_dictionary["mail_to_address"] is not None:
         slurm_configuration_string += slurm_email_configuration_string.format(**configuration_dictionary)

    if "other_flags" not in configuration_dictionary or configuration_dictionary["other_flags"] is None:
        configuration_dictionary["other_flags"] = ""

    if "number_of_threads_per_job" in configuration_dictionary and configuration_dictionary["number_of_threads_per_job"]:
        configuration_dictionary["other_flags"] += " --n_cpus {number_of_threads_per_job}"

    if "amount_of_memory_GB_per_job" in configuration_dictionary and configuration_dictionary["amount_of_memory_GB_per_job"]:
        configuration_dictionary["other_flags"] += " --mem_GB {amount_of_memory_GB_per_job}"

    configuration_dictionary["other_flags"] = configuration_dictionary["other_flags"].format(**configuration_dictionary)

    slurm_configuration_string += slurm_execution_variables_string.format(**configuration_dictionary)

    return(slurm_configuration_string)

if __name__ == "__main__":
    print("started!")
    print(format_slurm_configuration_string(slurm_configuration_dictionary))
