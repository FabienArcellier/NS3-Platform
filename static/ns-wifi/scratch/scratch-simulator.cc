#include "ns3/command-line.h"
#include "ns3/config.h"
#include "ns3/uinteger.h"
#include "ns3/boolean.h"
#include "ns3/double.h"
#include "ns3/string.h"
#include "ns3/log.h"
#include "ns3/yans-wifi-helper.h"
#include "ns3/ssid.h"
#include "ns3/mobility-helper.h"
#include "ns3/internet-stack-helper.h"
#include "ns3/ipv4-address-helper.h"
#include "ns3/udp-client-server-helper.h"
#include "ns3/packet-sink-helper.h"
#include "ns3/on-off-helper.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/packet-sink.h"
#include "ns3/wifi-net-device.h"
#include "ns3/wifi-mac-header.h"
#include "ns3/wifi-mac.h"
#include "ns3/yans-wifi-channel.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("scratch-simulator");

int main (int argc, char *argv[]) {
  //Principal parameters
  double simulationTime = 1; // Seconds
  double distance = 1.0; // Meters
  uint32_t nWifi = 1; // Number of stations
  bool agregation = false; // Allow or not the packet agregation
  std::string trafficDirection = "upstream";
  std::string trafficProfile = "periodic";
  uint32_t payloadSize = 1472; //1500 byte IP packet
  double loadFreq = 1.0; //packet per sec
  uint32_t meanLoad = 2; // Mean Load in Mbps
  int hiddenDevices = 1; //Indicate whether devices are hidden or not (O = Yes, 1 = No)
  
  //Avanced parameters
  int mcs = 5; // -1 indicates an unset value
  int channelWidth = 80; // BW Channel Width
  int sgi = 0; // Indicates whether Short Guard Interval is enabled or not (SGI==1 <==> GI=400ns)
  std::string propDelay = "ConstantSpeedPropagationDelayModel";
  std::string propLoss = "LogDistancePropagationLossModel";
  int spatialStreams = 1;
  //Energy parameters
  double tx = 0.52;  // in W
  double rx = 0.16;  // in W
  double txFactor = 0.93; // in mJ
  double rxFactor = 0.93; // in mJ
  double baseline = 3.56; // in W
  uint32_t batteryCap = 500; // Battery capacity in mAh

  CommandLine cmd (__FILE__);
  cmd.AddValue ("distance", "Distance in meters between the station and the access point", distance);
  cmd.AddValue ("simulationTime", "Simulation time in seconds", simulationTime);
  cmd.AddValue("nWifi", "Number of all stations", nWifi);
  cmd.AddValue("trafficDirection", "Traffic Direction", trafficDirection);
  cmd.AddValue("trafficProfile", "Traffic Profile, periodic or stochastic", trafficProfile );
  cmd.AddValue("payloadSize", "Packet size in bytes", payloadSize);
  cmd.AddValue("loadFreq", "Load Frequency (only periodic) in packet/sec", loadFreq);
  cmd.AddValue("meanLoad", "Mean Load (only stochastic) in Mbps", meanLoad);
  cmd.AddValue("hiddenDevices", "Indicate whether devices are hidden or not (O = NO, 1 = Yes)", hiddenDevices);

  cmd.AddValue("mcs", "Modulation and Coding Scheme", mcs);
  cmd.AddValue("channelWidth", "Bandwidth, MHz", channelWidth);
  cmd.AddValue("sgi", "Indicates whether Short Guard Interval is enabled or not (SGI==1 <==> GI=400ns)", sgi);
  cmd.AddValue("propDelay", "Propagation Delay Model", propDelay);
  cmd.AddValue("propLoss" , "Propagation Loss Model", propLoss);
  cmd.AddValue("spatialStreams", "Number of antennas", spatialStreams);
  cmd.AddValue("tx", "Transmitter power consumption in w", tx);
  cmd.AddValue("rx", "Reciever power consumption in W", rx);
  cmd.AddValue("txFactor", "Transmitter energy factor, mJ", txFactor);
  cmd.AddValue("rxFactor", "Receiver energy factor, mJ", rxFactor);
  cmd.AddValue("baseline", "Baseline energy consumption, w", baseline);
  cmd.AddValue("batteryCap", "Battery cpacity, mAh", batteryCap);
  cmd.Parse (argc,argv);

  //std::cout << "Number of stations : " << nWifi << std::endl;

  //std::cout << "MCS value" << "\t\t" << "Channel width" << "\t\t" << "short GI" << "\t\t" << "Throughput" << '\n';

  NodeContainer wifiStaNodes;
  wifiStaNodes.Create (nWifi);
  NodeContainer wifiApNode;
  wifiApNode.Create (1);

  YansWifiChannelHelper channel = YansWifiChannelHelper::Default ();
  YansWifiPhyHelper phy;
  phy.SetChannel (channel.Create ());

  WifiMacHelper mac;
  WifiHelper wifi;
  wifi.SetStandard (WIFI_STANDARD_80211ac);

  
  std::ostringstream oss;
  oss << "VhtMcs" << mcs;
  wifi.SetRemoteStationManager ("ns3::ConstantRateWifiManager","DataMode", StringValue (oss.str ()),
                                "ControlMode", StringValue (oss.str ()));

  Ssid ssid = Ssid ("ns3-80211ac");

  // Installing phy & mac layers on the overloading stations
  mac.SetType ("ns3::StaWifiMac",
              "Ssid", SsidValue (ssid));
  NetDeviceContainer staDevices;
  staDevices = wifi.Install (phy, mac, wifiStaNodes);

  // Installing phy & mac layers on the AP
  mac.SetType ("ns3::ApWifiMac",   
              "EnableBeaconJitter", BooleanValue (false),
              "Ssid", SsidValue (ssid));
  NetDeviceContainer apDevice;
  apDevice = wifi.Install (phy, mac, wifiApNode);

  // Set channel width
  Config::Set ("/NodeList/*/DeviceList/*/$ns3::WifiNetDevice/Phy/ChannelWidth", UintegerValue (channelWidth));

  // Set guard interval
  Config::Set ("/NodeList/*/DeviceList/*/$ns3::WifiNetDevice/HtConfiguration/ShortGuardIntervalSupported", BooleanValue (sgi));

  // Setting stations' positions
  MobilityHelper mobility;

  Ptr<ListPositionAllocator> positionAlloc = CreateObject<ListPositionAllocator> ();

  for (uint32_t i = 0; i < nWifi; i++) {
      positionAlloc->Add (Vector (distance, 0.0, 0.0));
  }

  mobility.SetPositionAllocator (positionAlloc);
  mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
  mobility.Install (wifiStaNodes);

  Ptr<ListPositionAllocator> positionAllocAp = CreateObject<ListPositionAllocator> ();
  positionAllocAp->Add (Vector (0.0, 0.0, 0.0));
  mobility.SetPositionAllocator (positionAllocAp);
  mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
  mobility.Install (wifiApNode);

  /* Internet stack*/
  InternetStackHelper stack;
  stack.Install (wifiApNode);
  stack.Install (wifiStaNodes);

  // Setting IP addresses
  Ipv4AddressHelper address;
  address.SetBase ("10.0.0.0", "255.255.0.0");
  Ipv4InterfaceContainer ApInterface;
  ApInterface = address.Assign (apDevice);
  Ipv4InterfaceContainer StaInterface;
  StaInterface = address.Assign (staDevices);

  Ipv4GlobalRoutingHelper::PopulateRoutingTables ();

  if (agregation == false) {
    // Disable A-MPDU & A-MSDU in AP
    Ptr<NetDevice> dev = wifiApNode.Get(0)-> GetDevice(0);
    Ptr<WifiNetDevice> wifi_dev = DynamicCast<WifiNetDevice> (dev);
    wifi_dev->GetMac ()->SetAttribute ("BE_MaxAmpduSize", UintegerValue (0));
    wifi_dev->GetMac ()->SetAttribute ("BE_MaxAmsduSize", UintegerValue (0));
  }

  /* Setting applications */
  ApplicationContainer sourceApplications, sinkApplications;
  uint32_t portNumber = 9;

  if (trafficDirection == "upstream") {
    auto ipv4 = wifiApNode.Get (0)->GetObject<Ipv4> ();
    const auto address = ipv4->GetAddress (1, 0).GetLocal ();
    InetSocketAddress sinkSocket (address, portNumber);
      
    PacketSinkHelper packetSinkHelper ("ns3::UdpSocketFactory", sinkSocket);
    sinkApplications.Add (packetSinkHelper.Install (wifiApNode.Get (0)));
    for (uint32_t index = 0; index < nWifi; ++index) {
      if (agregation == false) {
        // Disable A-MPDU & A-MSDU in each station
        Ptr<NetDevice> dev = wifiStaNodes.Get (index)->GetDevice (0);
        Ptr<WifiNetDevice> wifi_dev = DynamicCast<WifiNetDevice> (dev);
        wifi_dev->GetMac ()->SetAttribute ("BE_MaxAmpduSize", UintegerValue (0));
        wifi_dev->GetMac ()->SetAttribute ("BE_MaxAmsduSize", UintegerValue (0));
      }
 
      // UDP Client application to be installed in the stations
      OnOffHelper server ("ns3::UdpSocketFactory", sinkSocket);
      server.SetAttribute ("PacketSize", UintegerValue (payloadSize));
      server.SetAttribute ("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
      server.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
      server.SetAttribute ("DataRate", DataRateValue (DataRate ("100Kbps")));

      sourceApplications.Add (server.Install (wifiStaNodes.Get (index)));
    }
  }
  else {
    for (uint32_t index = 0; index < nWifi; ++index) {
      if (agregation == false) {
        // Disable A-MPDU & A-MSDU in each station
        Ptr<NetDevice> dev = wifiStaNodes.Get (index)->GetDevice (0);
        Ptr<WifiNetDevice> wifi_dev = DynamicCast<WifiNetDevice> (dev);
        wifi_dev->GetMac ()->SetAttribute ("BE_MaxAmpduSize", UintegerValue (0));
        wifi_dev->GetMac ()->SetAttribute ("BE_MaxAmsduSize", UintegerValue (0));
      }

      auto ipv4 = wifiStaNodes.Get (index)->GetObject<Ipv4> ();
      const auto address = ipv4->GetAddress (1, 0).GetLocal ();
      InetSocketAddress sinkSocket (address, portNumber);
      
      // UDP Client application to be installed in the stations
      OnOffHelper server ("ns3::UdpSocketFactory", sinkSocket);
      server.SetAttribute ("PacketSize", UintegerValue (payloadSize));
      server.SetAttribute ("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
      server.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
      server.SetAttribute ("DataRate", DataRateValue (DataRate ("100Kbps")));

      sourceApplications.Add(server.Install (wifiApNode.Get(0)));
      
      PacketSinkHelper packetSinkHelper ("ns3::UdpSocketFactory", sinkSocket);
      sinkApplications.Add(packetSinkHelper.Install (wifiStaNodes.Get (index)));      
    }
  }
  //ApInterface.GetAddress(0).Print(std::cout);

  // Start the UDP Client & Server applications
  sinkApplications.Start (Seconds (0.0));
  sinkApplications.Stop (Seconds (simulationTime + 1));
  sourceApplications.Start (Seconds (1.0));
  sourceApplications.Stop (Seconds (simulationTime + 1));

  AsciiTraceHelper ascii;

  phy.SetPcapDataLinkType (WifiPhyHelper::DLT_IEEE802_11_RADIO);
  /*std::string s = "wifi/overload/throughput/" + trafficDirection + "/ac/traces2/" + std::to_string(nWifi);
  phy.EnableAsciiAll (ascii.CreateFileStream(s+".tr"));
  phy.EnablePcap (s+".pcap", apDevice.Get(0), false, true);
  */

  Simulator::Stop (Seconds (simulationTime + 1));
  Simulator::Run ();

  double throughput = 0;
  for (uint32_t index = 0; index < sinkApplications.GetN (); ++index) {
    uint64_t totalPacketsThrough = DynamicCast<PacketSink> (sinkApplications.Get (index))->GetTotalRx ();
    throughput += ((totalPacketsThrough * 8) / ((simulationTime) * 1000000.0)); //Mbit/s
  }

  Simulator::Destroy ();

  //std::cout << mcs << "\t\t\t" << channelWidth << " MHz\t\t\t" << sgi << "\t\t\t" << throughput << " Mbit/s" << std::endl;
  std::cout << "Throughput: " << throughput << std::endl;
  std::cout << "Success Rate: " << 100 << std::endl;
  
  return 0;
}