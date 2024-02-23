#!/bin/bash
#Script to provision Form Recognizer
grn=$'\e[1;32m'
end=$'\e[0m'

set -e

# Start of script
SECONDS=0
printf "${grn}Starting creation of Form Recognizer resource...${end}\n"

# Source subscription ID, and prep config file
source sub.env
sub_id=$SUB_ID

# Set the default subscription 
az account set -s $sub_id

# Create the resource group, location
number=$[ ( $RANDOM % 10000 ) + 1 ]
root_word='fr'
resourcegroup=$root_word$number'rg'
cognitiveservice=$root_word$number'cogaccount'
location='westus2'

printf "${grn}STARTING CREATION OF RESOURCE GROUP...${end}\n"
rgCreate=$(az group create --name $resourcegroup --location $location)
printf "Result of resource group create:\n $rgCreate \n"

## Create Form recognizer resource
printf "${grn}CREATING THE COGNITIVE SERVICES RESOURCE...${end}\n"
cognitiveServices=$(az cognitiveservices account create \
	--kind CognitiveServices --location $location --name $cognitiveservice --sku S0\
	-g $resourcegroup  --yes)
printf "Result of cognitive services create:\n $cognitiveServices \n"

## Retrieve key from cognitive services
printf "${grn}RETRIEVE KEY FOR COGNITIVE SERVICES...${end}\n"
cogKey=$(az cognitiveservices account keys list -g $resourcegroup --name $cognitiveservice --query "key1" -o tsv)

# # Remove double quotes from primary key
# cogkey=$(sed -e 's/^"//' -e 's/"$//' <<<"$cogKey")
#
## Retrieve the endpoint
printf "${grn}RETRIEVE KEY FOR COGNITIVE SERVICES...${end}\n"
endpoint=$(az cognitiveservices account show -g $resourcegroup --name $cognitiveservice --query properties.endpoint -o tsv)

sleep 5 # just to give time for artifacts to settle in the system, and be accessible
printf "${grn}WRITING OUT ENVIRONMENT VARIABLES...${end}\n"
configFile='variables.env'
printf "RESOURCE_GROUP=$resourcegroup \n"> $configFile
printf "LOCATION=$location \n">> $configFile
printf "ENDPOINT=$endpoint \n">> $configFile
printf "COG_RESOURCE=$cognitiveservice \n">> $configFile
printf "COG_KEY=$cogKey \n">> $configFile
