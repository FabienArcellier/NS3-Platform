# LIP Network simulation
This is for an interface for a configuration of NS-3 simulation. 
# How to deploy (under an environment of Linux Ubuntu)
# Install virtualenv if not exist
sudo apt install python3.8-venv
# Creat virtual environment
python3 -m venv env 
# Activate virtualenv
source env/bin/activate
# Install requirements.txt
pip3 install -r requirements.txt
# To deactivate virtualenv
deactivate
# After install requirements.txt
it need to buid NS-3 with waf. Navigate inside the directory of NS3 (wifi simulmateur) in static
# Build with waf
 ./waf configure --build-profile=optimized --enable-examples --enable-tests
./waf
# Remove error as a false
./waf configure --disable-werror

# Run project
./waf --run "scratch/wifi-overload-throughput-ac.cc --distance=$DISTANCE --nWifi=$NUMDEVICES --trafficDirection=$TRAFFICDIR --trafficProfile=$TRAFFICPROF --payloadSize=$PACKETSIZE --loadFreq=$LOADFREQ --meanLoad=$MEANLOAD --hiddenDevices=$HIDDENDEVICES --mcs=$MCS --channelWidth=$BANDWIDTH --propDelay=$PROPDELAY --propLoss=$PROPLOSS --spatialStreams=$SPATIALSTREAMS --tx=$TX --rx=$RX --txFactor=$TXFACTOR --rxFactor=$RXFACTOR --voltage=$VOLTAGE --batteryCap=$BATTERYCAP"


