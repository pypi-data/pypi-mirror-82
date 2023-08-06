#!/bin/bash

set -eux
set -o pipefail
export PYTHONUNBUFFERED=1
SCRIPT_HOME="$(cd "$(dirname "$0")" && pwd)"
BIFROST_HOME=$SCRIPT_HOME/..
ANSIBLE_INSTALL_ROOT=${ANSIBLE_INSTALL_ROOT:-/opt/stack}
USE_DHCP="${USE_DHCP:-false}"
USE_VENV="${USE_VENV:-false}"
BUILD_IMAGE="${BUILD_IMAGE:-false}"
BAREMETAL_DATA_FILE=${BAREMETAL_DATA_FILE:-'/tmp/baremetal.json'}
ENABLE_KEYSTONE="${ENABLE_KEYSTONE:-false}"
ZUUL_BRANCH=${ZUUL_BRANCH:-}

# Set defaults for ansible command-line options to drive the different
# tests.

# NOTE(TheJulia/cinerama): The variables defined on the command line
# for the default and DHCP tests are to drive the use of Cirros as the
# deployed operating system, and as such sets the test user to cirros,
# and writes a debian style interfaces file out to the configuration
# drive as cirros does not support the network_info.json format file
# placed in the configuration drive. The "build image" test does not
# use cirros.

VM_DOMAIN_TYPE=qemu
export VM_DISK_CACHE="unsafe"
TEST_VM_NUM_NODES=1
USE_CIRROS=true
TESTING_USER=cirros
TEST_PLAYBOOK="test-bifrost.yaml"
USE_INSPECTOR=true
INSPECT_NODES=true
INVENTORY_DHCP=false
INVENTORY_DHCP_STATIC_IP=false
DOWNLOAD_IPA=true
CREATE_IPA_IMAGE=false
WRITE_INTERFACES_FILE=true
PROVISION_WAIT_TIMEOUT=${PROVISION_WAIT_TIMEOUT:-900}
NOAUTH_MODE=true
CLOUD_CONFIG=""
WAIT_FOR_DEPLOY=true
ENABLE_VENV=false

# This sets up the MySQL database like it's done for all OpenStack
# projects for CI testing.
mysql_setup() {
    # The root password for the MySQL database; pass it in via
    # MYSQL_ROOT_PW.
    local DB_ROOT_PW=${MYSQL_ROOT_PW:-insecure_slave}

    # This user and its password are used by the tests, if you change it,
    # your tests might fail.
    local DB_USER=openstack_citest
    local DB_PW=openstack_citest

    # Make sure MySQL is running
    sudo service mysql start || sudo service mysqld start || sudo service mariadb start

    sudo -H mysqladmin -u root password $DB_ROOT_PW

    # It's best practice to remove anonymous users from the database.  If
    # an anonymous user exists, then it matches first for connections and
    # other connections from that host will not work.
    sudo -H mysql -u root -p$DB_ROOT_PW -h localhost -e "
        DELETE FROM mysql.user WHERE User='';
        FLUSH PRIVILEGES;
        GRANT ALL PRIVILEGES ON *.*
            TO '$DB_USER'@'%' identified by '$DB_PW' WITH GRANT OPTION;"

    # Now create our database.
    mysql -u $DB_USER -p$DB_PW -h 127.0.0.1 -e "
        SET default_storage_engine=MYISAM;
        DROP DATABASE IF EXISTS openstack_citest;
        CREATE DATABASE openstack_citest CHARACTER SET utf8;"
}

# Setup openstack_citest database if run in OpenStack CI.
if [ "$ZUUL_BRANCH" != "" ] ; then
    mysql_setup
fi

if [ ${USE_VENV} = "true" ]; then
    export VENV=/opt/stack/bifrost
    $SCRIPT_HOME/env-setup.sh
    # Note(cinerama): activate is not compatible with "set -u";
    # disable it just for this line.
    set +u
    source ${VENV}/bin/activate
    set -u
    ANSIBLE=${VENV}/bin/ansible-playbook
    ENABLE_VENV="true"
    ANSIBLE_PYTHON_INTERP=${VENV}/bin/python
else
    $SCRIPT_HOME/env-setup.sh
    ANSIBLE=${HOME}/.local/bin/ansible-playbook
    ANSIBLE_PYTHON_INTERP=$(which python)
fi

# Adjust options for DHCP, VM, or Keystone tests
if [ ${USE_DHCP} = "true" ]; then
    ENABLE_INSPECTOR=false
    INSPECT_NODES=false
    TEST_VM_NUM_NODES=5
    INVENTORY_DHCP=true
    INVENTORY_DHCP_STATIC_IP=true
    WRITE_INTERFACES_FILE=false
elif [ ${BUILD_IMAGE} = "true" ]; then
    USE_CIRROS=false
    TESTING_USER=root
    VM_MEMORY_SIZE="4096"
    ENABLE_INSPECTOR=false
    INSPECT_NODES=false
    DOWNLOAD_IPA=false
    CREATE_IPA_IMAGE=true
elif [ ${ENABLE_KEYSTONE} = "true" ]; then
    NOAUTH_MODE=false
    CLOUD_CONFIG="-e cloud_name=bifrost"
fi

logs_on_exit() {
    $SCRIPT_HOME/collect-test-info.sh
}
trap logs_on_exit EXIT

# Change working directory
cd $BIFROST_HOME/playbooks

# Syntax check of dynamic inventory test path
for task in syntax-check list-tasks; do
    ${ANSIBLE} -vvvv \
           -i inventory/localhost \
           test-bifrost-create-vm.yaml \
           --${task}
    ${ANSIBLE} -vvvv \
           -i inventory/localhost \
           ${TEST_PLAYBOOK} \
           --${task} \
           -e testing_user=${TESTING_USER}
done

# Create the test VM
${ANSIBLE} -vvvv \
       -i inventory/localhost \
       test-bifrost-create-vm.yaml \
       -e ansible_python_interpreter="${ANSIBLE_PYTHON_INTERP}" \
       -e test_vm_num_nodes=${TEST_VM_NUM_NODES} \
       -e test_vm_memory_size=${VM_MEMORY_SIZE:-512} \
       -e test_vm_domain_type=${VM_DOMAIN_TYPE} \
       -e test_vm_disk_gib=${VM_DISK:-5} \
       -e baremetal_json_file=${BAREMETAL_DATA_FILE} \
       -e enable_venv=${ENABLE_VENV}

if [ ${USE_DHCP} = "true" ]; then
    # reduce the number of nodes in JSON file
    # to limit number of nodes to enroll for testing purposes
    python $BIFROST_HOME/scripts/split_json.py 3 \
        ${BAREMETAL_DATA_FILE} \
        ${BAREMETAL_DATA_FILE}.new \
        ${BAREMETAL_DATA_FILE}.rest \
        && mv ${BAREMETAL_DATA_FILE}.new ${BAREMETAL_DATA_FILE}
fi

set +e

# Set BIFROST_INVENTORY_SOURCE
export BIFROST_INVENTORY_SOURCE=${BAREMETAL_DATA_FILE}

# Execute the installation and VM startup test.

${ANSIBLE} -vvvv \
    -i inventory/bifrost_inventory.py \
    ${TEST_PLAYBOOK} \
    -e ansible_python_interpreter="${ANSIBLE_PYTHON_INTERP}" \
    -e use_cirros=${USE_CIRROS} \
    -e testing_user=${TESTING_USER} \
    -e test_vm_num_nodes=${TEST_VM_NUM_NODES} \
    -e inventory_dhcp=${INVENTORY_DHCP} \
    -e inventory_dhcp_static_ip=${INVENTORY_DHCP_STATIC_IP} \
    -e enable_venv=${ENABLE_VENV} \
    -e enable_inspector=${USE_INSPECTOR} \
    -e inspect_nodes=${INSPECT_NODES} \
    -e download_ipa=${DOWNLOAD_IPA} \
    -e create_ipa_image=${CREATE_IPA_IMAGE} \
    -e write_interfaces_file=${WRITE_INTERFACES_FILE} \
    -e wait_timeout=${PROVISION_WAIT_TIMEOUT} \
    -e noauth_mode=${NOAUTH_MODE} \
    -e enable_keystone=${ENABLE_KEYSTONE} \
    -e use_public_urls=${ENABLE_KEYSTONE} \
    -e wait_for_node_deploy=${WAIT_FOR_DEPLOY} \
    -e not_enrolled_data_file=${BAREMETAL_DATA_FILE}.rest \
    ${CLOUD_CONFIG}
EXITCODE=$?

if [ $EXITCODE != 0 ]; then
    echo "****************************"
    echo "Test failed. See logs folder"
    echo "****************************"
fi

exit $EXITCODE
