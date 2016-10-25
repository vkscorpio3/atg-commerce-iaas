ansible-playbook playbooks/instances/atgdb_instance_cleanup.yaml > logs/atgdb_instance_cleanup.log  2>&1
ansible-playbook playbooks/instances/otd_instance_cleanup.yaml > logs/otd_instance_cleanup.log  2>&1
ansible-playbook playbooks/instances/atgsupport_instance_cleanup.yaml > logs/atgsupport_instance_cleanup.log  2>&1
ansible-playbook playbooks/instances/atg2_instance_cleanup.yaml > logs/atg2_instance_cleanup.log  2>&1
ansible-playbook playbooks/instances/atg1_instance_cleanup.yaml > logs/atg1_instance_cleanup.log  2>&1
ansible-playbook playbooks/instances/endeca2_instance_cleanup.yaml > logs/endeca2_instance_cleanup.log  2>&1
ansible-playbook playbooks/instances/endeca1_instance_cleanup.yaml > logs/endeca1_instance_cleanup.log  2>&1
ansible-playbook playbooks/storage/wls_install_storage_storage_cleanup.yaml > logs/wls_install_storage_storage_cleanup.log  2>&1
ansible-playbook playbooks/storage/atg_install_storage_storage_cleanup.yaml > logs/atg_install_storage_storage_cleanup.log  2>&1
ansible-playbook playbooks/storage/atgdb_storage_storage_cleanup.yaml > logs/atgdb_storage_storage_cleanup.log  2>&1
ansible-playbook playbooks/secapp/secapp_cleanup.yaml > logs/secapp_cleanup.log  2>&1
ansible-playbook playbooks/seclist/seclist_cleanup.yaml > logs/seclist_cleanup.log  2>&1