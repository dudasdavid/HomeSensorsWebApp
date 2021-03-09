#/usr/bin/bash

###################################################
#
# Script to upload a Let's Encrypt certificate
# (or other) into Oracle Cloud Load Balancer
# Carlos Santos - April 2020
#
###################################################

####################################
#                                  #
#       Variable definition        #
#                                  #
####################################

now=$(date "+%Y%m%d_%H%M")
CertificateName=Certificate-$now
Protocol=HTTP
Port=443
ocicli=/home/opc/bin/oci
#
# Only change the variables below
#
ListenerName=HTTPS-Listener
BackendName=TLS-DEMO
LB_OCID=ocid1.loadbalancer.oc1.eu-cloud-1.aaaaaaaaexampleexampleexampleocid
certificate_path=/etc/letsencrypt/live/tls-example.com

####################################
# Create Certificate in LB         #
####################################
echo "Creating Certificate $CertificateName in Listener $ListenerName"

$ocicli lb certificate create \
--auth instance_principal \
--certificate-name $CertificateName \
--load-balancer-id $LB_OCID \
--private-key-file "$certificate_path/privkey.pem" \
--public-certificate-file "$certificate_path/fullchain.pem"

#
# Give it 10 seconds for the certificate to be available
#
echo "-- Waiting 10 seconds for certificate to be available on OCI"
sleep 10

####################################
#  Update certificate on Listener  #
####################################
echo "Configuring Listener $ListenerName with certificate $CertificateName"

$ocicli lb listener update \
--auth instance_principal \
--default-backend-set-name $BackendName \
--listener-name $ListenerName \
--load-balancer-id $LB_OCID \
--port $Port \
--protocol $Protocol \
--ssl-certificate-name $CertificateName \
--force
