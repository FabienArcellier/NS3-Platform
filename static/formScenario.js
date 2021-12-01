var diagram = document.getElementById("img_traffic");
var network = document.getElementById("network");
var direction = document.getElementById("traffic_direction");
var traffic_profile = document.getElementById("traffic_profile");
network.addEventListener("change", onChangeSelectNetwork);
direction.addEventListener("change", onChangeSelectDirection);
traffic_profile.addEventListener("change", onChangeSelectTrafficProfile);
var load_freq = document.getElementById("load_freq");
var lbl_load_freq = document.getElementById("lbl_load_freq");
var mean_load =document.getElementById("mean_load");
var lbl_mean_load = document.getElementById("lbl_mean_load");

//hiding load_freq and mean_load before choosing traffic profile
load_freq.style.display = "none";
lbl_load_freq.style.display = "none";
mean_load.style.display = "none";
lbl_mean_load.style.display = "none";

var lbl_sf = document.getElementById("lbl_sf");
var sf = document.getElementById("sf");

var num_devices = document.getElementById("num_devices");
var dist_devices_gateway = document.getElementById("dist_devices_gateway");
var simulation_time = document.getElementById("simulation_time");

var lbl_prop_delay = document.getElementById("lbl_prop_delay");
var prop_delay = document.getElementById("prop_delay");
var lbl_prop_loss = document.getElementById("lbl_prop_loss");
var prop_loss = document.getElementById("prop_loss");
var lbl_cyclic_redundacy_check = document.getElementById("lbl_cyclic_redundacy_check");
var cyclic_redundacy_check = document.getElementById("cyclic_redundacy_check");
var lbl_low_data_rate_optimization  = document.getElementById("lbl_low_data_rate_optimization");
var low_data_rate_optimization  = document.getElementById("low_data_rate_optimization");
var lbl_implicit_header_mode  = document.getElementById("lbl_implicit_header_mode");
var implicit_header_mode  = document.getElementById("implicit_header_mode");


var lbl_mcs = document.getElementById("lbl_mcs");
var mcs = document.getElementById("mcs");
var lbl_fps = document.getElementById("lbl_fps");
var fps = document.getElementById("fps");
var lbl_bandwidth = document.getElementById("lbl_bandwidth");
var bandwidth = document.getElementById("bandwidth");
var lbl_spatial_streams = document.getElementById("lbl_spatial_streams");
var spatial_streams = document.getElementById("spatial_streams");
var lbl_tx = document.getElementById("lbl_tx");
var tx = document.getElementById("tx");
var lbl_rx = document.getElementById("lbl_rx");
var rx = document.getElementById("rx");
var lbl_tx_factor = document.getElementById("lbl_tx_factor");
var tx_factor = document.getElementById("tx_factor");
var lbl_rx_factor = document.getElementById("lbl_rx_factor");
var rx_factor = document.getElementById("rx_factor");
var lbl_voltage = document.getElementById("lbl_voltage");
var voltage = document.getElementById("voltage");
var lbl_battery_cap = document.getElementById("lbl_battery_cap");
var battery_cap = document.getElementById("battery_cap");

//hiding all advanced parameters if checkboxChange is unchecked 

lbl_prop_delay.style.display = "none";
prop_delay.style.display = "none";
lbl_prop_loss.style.display = "none";
prop_loss.style.display = "none";
lbl_cyclic_redundacy_check.style.display = "none";
cyclic_redundacy_check.style.display = "none";
lbl_low_data_rate_optimization.style.display = "none";
low_data_rate_optimization.style.display = "none";
lbl_implicit_header_mode.style.display = "none";
implicit_header_mode.style.display = "none";

lbl_mcs.style.display = "none";
mcs.style.display = "none";
lbl_fps.style.display = "none";
fps.style.display = "none";
//hiding SF before choosing LoRaWAN
lbl_sf.style.display = "none";
sf.style.display = "none";     
lbl_bandwidth.style.display = "none";
bandwidth.style.display = "none";
lbl_spatial_streams.style.display = "none";
spatial_streams.style.display = "none";
lbl_tx.style.display = "none";
tx.style.display = "none";
lbl_rx.style.display = "none";
rx.style.display = "none";
lbl_tx_factor.style.display = "none";
tx_factor.style.display = "none";
lbl_rx_factor.style.display = "none";
rx_factor.style.display = "none";
lbl_voltage.style.display = "none";
voltage.style.display = "none";
lbl_battery_cap.style.display = "none";
battery_cap.style.display = "none";

//Hide spinner loading 
const spinner = document.getElementById("spinner");
spinner.style.display = "none";
const submit_btn = document.getElementById("submit_btn");
//Toggle spinner loading when click submit button
submit_btn.addEventListener("click", function(){
    spinner.style.display = "inherit";
    //setTimeout(stopSpinner,99999999);
});

function stopSpinner(){
    spinner.style.display = "none";
}

var checkboxChange = document.getElementById("change");
checkboxChange.addEventListener("change", onChangeCheckbox);

function onChangeCheckbox(){

    onCheck();
}

function onCheck(){
    if (checkboxChange.checked)
    {
        lbl_prop_delay.style.display = "inherit";
        prop_delay.style.display = "inherit";
        lbl_prop_loss.style.display = "inherit";
        prop_loss.style.display = "inherit";
        lbl_bandwidth.style.display = "inherit";
        bandwidth.style.display = "inherit";
        lbl_tx.style.display = "inherit";
        tx.style.display = "inherit";
        lbl_rx.style.display = "inherit";
        rx.style.display = "inherit";
        lbl_tx_factor.style.display = "inherit";
        tx_factor.style.display = "inherit";
        lbl_rx_factor.style.display = "inherit";
        rx_factor.style.display = "inherit";
        lbl_voltage.style.display = "inherit";
        voltage.style.display = "inherit";
        lbl_battery_cap.style.display = "inherit";
        battery_cap.style.display = "inherit";

        if (network.value =='Wi-Fi 802.11ac' || network.value == 'Wi-Fi 802.11ax')
        {
            lbl_mcs.style.display = "inherit";
            mcs.style.display = "inherit";
            lbl_spatial_streams.style.display = "inherit";
            spatial_streams.style.display = "inherit";
        }
        else if(network.value == "LoRaWAN")
        {
            //advanced parameters of LoRaWAN shown
            lbl_cyclic_redundacy_check.style.display = "inherit";
            cyclic_redundacy_check.style.display = "inherit";
            lbl_low_data_rate_optimization.style.display = "inherit";
            low_data_rate_optimization.style.display = "inherit";
            lbl_implicit_header_mode.style.display = "inherit";
            implicit_header_mode.style.display = "inherit";
            lbl_sf.style.display = "inherit";
            sf.style.display = "inherit";
        }
        
    }
    else
    {
        lbl_prop_delay.style.display = "none";
        prop_delay.style.display = "none";
        lbl_prop_loss.style.display = "none";
        prop_loss.style.display = "none";
        lbl_cyclic_redundacy_check.style.display = "none";
        cyclic_redundacy_check.style.display = "none";
        lbl_low_data_rate_optimization.style.display = "none";
        low_data_rate_optimization.style.display = "none";
        lbl_implicit_header_mode.style.display = "none";
        implicit_header_mode.style.display = "none";
       
        lbl_mcs.style.display = "none";
        mcs.style.display = "none";
        //lbl_fps.style.display = "none";
        fps.style.display = "none";
        lbl_sf.style.display = "none";
        sf.style.display = "none";     
        lbl_bandwidth.style.display = "none";
        bandwidth.style.display = "none";
        lbl_spatial_streams.style.display = "none";
        spatial_streams.style.display = "none";
        lbl_tx.style.display = "none";
        tx.style.display = "none";
        lbl_rx.style.display = "none";
        rx.style.display = "none";
        lbl_tx_factor.style.display = "none";
        tx_factor.style.display = "none";
        lbl_rx_factor.style.display = "none";
        rx_factor.style.display = "none";
        lbl_voltage.style.display = "none";
        voltage.style.display = "none";
        lbl_battery_cap.style.display = "none";
        battery_cap.style.display = "none";
    }
}

    

//Preset radiobuttons for all parameters
    var packet_size_wifi = document.getElementById("packet_size_wifi");
    var lbl_packet_size_wifi = document.getElementById("lbl_packet_size_wifi");
    var packet_size_lorawan = document.getElementById("packet_size_lorawan");
    var lbl_packet_size_lorawan = document.getElementById("lbl_packet_size_lorawan");
    var wifi_error = document.getElementById("wifi_error");
    var lorawan_error = document.getElementById("lorawan_error");
    var dist_devices_gateway_error = document.getElementById("dist_devices_gateway_error");
    var simulation_time_error = document.getElementById("simulation_time_error");
    var num_devices_error = document.getElementById("num_devices_error");
    var fps_error = document.getElementById("fps_error");

  
//hide packet sizes fields
console.log("wifi-error :"+wifi_error.innerText.length);
console.log("LoRaWAN error :"+lorawan_error.innerText.length);
if(wifi_error.innerText.length!=0)
{
    packetSizeShow("Wi-Fi");
}
else if(lorawan_error.innerText.length!=0)
{
    packetSizeShow("LoRaWAN");
}   
else
{
    packetSizeShow("");
} 


 //function for show packet size field
 function packetSizeShow(networkType){
    if(networkType=="Wi-Fi")
    {
        lbl_packet_size_wifi.style.display = "inherit";
        packet_size_wifi.style.display = "inherit";
        wifi_error.style.display = "inherit";
        lbl_packet_size_lorawan.style.display = "none";
        packet_size_lorawan.style.display = "none";
        lorawan_error.style.display = "none";

    }
    else if (networkType=="LoRaWAN")
    {
        lbl_packet_size_lorawan.style.display = "inherit";
        packet_size_lorawan.style.display = "inherit";
        lorawan_error.style.display = "inherit";
        lbl_packet_size_wifi.style.display = "none";
        packet_size_wifi.style.display = "none";
        wifi_error.style.display = "none";
    }
    else
    {
        //hide packet sizes fields
        lbl_packet_size_wifi.style.display = "none";
        packet_size_wifi.style.display = "none";
        lbl_packet_size_lorawan.style.display = "none";
        packet_size_lorawan.style.display = "none";
        wifi_error.style.display = "none";
        lorawan_error.style.display = "none";
    }
 }   

 function clearErrors(){
     wifi_error.innerText = "";
     lorawan_error.innerText = "";
     num_devices_error.innerText = "";
     fps_error.innerText = "";
     dist_devices_gateway_error.innerText = "";
     simulation_time_error.innerText = "";
 }

 function selectBandwidth(selectNetwork){
     switch(selectNetwork){
          //set a bandwidth label depending on a network
        case 'LoRaWAN':
                lbl_bandwidth.textContent = "Bandwidth, KHz"
                optionBandwidth = '<option selected value="125">125</option>'+
                                '<option value="250">250</option>'+
                                '<option value="500">500</option>';
                break;                
        default :  
                 lbl_bandwidth.textContent = "Bandwidth, MHz"
                 optionBandwidth = '<option value="20">20</option>'+
                                   '<option value="40">40</option>'+
                                   '<option selected value="80">80</option>'+
                                   '<option value="160">160</option>';
     }
     bandwidth.innerHTML = optionBandwidth;
 }
    
    //Uncheck checkboxChange after reload/submit
    checkboxChange.checked = false;
    //set Bandwith according to selected network
    selectBandwidth(network.value);
    var preset = document.querySelectorAll('input[name="radioPreset"]');
    var select_preset = false;

    for(let i=0; i<preset.length; i++)
    {
        console.log("Preset"+preset[i].value);
        preset[i].addEventListener("change", function(){
            if(this.checked)
            {
                //uncheck checkboxChange
                checkboxChange.checked = false;
                onCheck();
                //clear packet size error fields
                clearErrors();  
                select_preset = this.value;
                console.log("Selected preset value :"+select_preset);
                //Add full choices of traffic direction and traffic profile before preset
                var optionDirection = '<option disabled hidden>Choose traffic direction</option>'+
                                    '<option value="upstream">Upstream</option>'+
                                    '<option value="downstream">Downstream</option>';
                var optionProfile =  '<option disabled hidden>Choose traffic profile</option>'+
                                    '<option value="periodic">Periodic</option>'+
                                    '<option value="cbr">CBR</option>'+
                                    '<option value="vbr">VBR</option>';
                direction.innerHTML = optionDirection;
                traffic_profile.innerHTML = optionProfile;
                
                var optionBandwidth = "";
                if (select_preset != "4")
                {                   
                   //set a default value to battery capacity depending on a network, here is wifi
                    battery_cap.value = "5200";
                    voltage.value = "12";
                    packetSizeShow("Wi-Fi");        
                }
                else
                {
                    //set a default value to battery capacity depending on a network, here is LoRaWAN
                    battery_cap.value = "2400";    
                    voltage.value = "3";   
                    packetSizeShow("LoRaWAN");    
                                    
                }

                switch(select_preset)
                {
                    case '1'://Telemetry 
                        network.selectedIndex = "1";            //set to Wi-Fi 5
                        console.log("Selected network =", network.value);
                        direction.selectedIndex = "1";          //set to Upstream
                        traffic_profile.selectedIndex = "1";    //set to Periodic
                        packet_size_wifi.value = "1024",             //set to 1024 bytes
                        load_freq.value = "1";                  //set to 1 packet/sec
                        num_devices.value = "1";                //set to 20 devices
                        dist_devices_gateway.value = "1";       //set distance to 1 meter
                        simulation_time.value = "5";
                        //The rest advanced parameter are set to default; listed in the documentation
                        //Set a picture to upstream direction
                        diagram.setAttribute('src', '../static/img/diagram_traffic_upstream.png');
                        break;
                    case '2'://Video-surveillance 
                        network.selectedIndex = "1";             //set to Wi-Fi 5  
                        console.log("Selected network =", network.value);
                        console.log("Selected index = ", network.selectedIndex);
                        direction.selectedIndex = "1";          //set to Upstream
                        traffic_profile.selectedIndex = "2";    //set to Stochastic
                        packet_size_wifi.value = "1024",             //set to 1024 bytes
                        mean_load.value = "2";                  //set to 2 Mbps
                        num_devices.value = "1";                //set to 20 devices
                        //fps.value = "30";                //FPS=30
                        dist_devices_gateway.value = "1";       //set distance to 1 meter
                        simulation_time.value = "5";
                        //The rest advanced parameter are set to default; listed in the documentation
                        diagram.setAttribute('src', '../static/img/diagram_traffic_upstream.png');
                        break;
                    case '3'://Webcast 
                        network.selectedIndex = "1";             //set to Wi-Fi 5 
                        console.log("Selected network =", network.value);
                        direction.selectedIndex = "2";          //set to Downstream
                        traffic_profile.selectedIndex = "2";    //set to Stochastic
                        packet_size_wifi.value = "1024",             //set to 1024 bytes
                        mean_load.value = "2";                  //set to 2 Mbps
                        num_devices.value = "1";               //set to 20 devices
                        dist_devices_gateway.value = "1";       //set distance to 1 meter
                        simulation_time.value = "5";
                        //The rest advanced parameter are set to default; listed in the documentation
                        //Set the picture to downstream direction
                        diagram.setAttribute('src', '../static/img/diagram_traffic_downstream.png');
                        break;
                    case '4'://smart metering
                        network.selectedIndex = "3";             //set to LoRaWAN
                        console.log("Selected network =", network.value);
                        direction.selectedIndex = "1";          //set to Upstream
                        traffic_profile.selectedIndex = "1";    //set to Periodic
                        packet_size_lorawan.value = "23",               //set to 23 bytes
                        load_freq.value = "360";           //set to 3600 packet/sec or 1 packet/hr
                        num_devices.value = "1" ;           //set to 1 devices
                        dist_devices_gateway.value = "100";    //set distance to 100 m
                        simulation_time.value = "3600";
                        sf.selectedIndex = "0";                 //set SF to 7
                        //The rest advanced parameter are set to default; listed in the documentation
                        diagram.setAttribute('src', '../static/img/diagram_traffic_upstream.png');
                        break;
                }   
                //Set meanload or load freq according to traffic direction
                onChangeTrafficProfile();
                 //set choices to bandwidth depending on a network
                 selectBandwidth(network.value);
            }
        });   
        
    }

function clearPresetRdb(){
    preset.forEach(element => {
        element.checked = false;
    });
}
//if a user selects or inputs parameters by himself or herself, uncheck preset radiobuttons
const selectedItems = document.querySelectorAll(".form-select, .form-control");
console.log("Number of selected items : "+selectedItems.length);
selectedItems.forEach(selectedItem => {
    selectedItem.addEventListener("change", function(){
        //uncheck preset radiobuttons
        clearPresetRdb();
        
    });
});

function onChangeSelectNetwork(){
   var select_network = network.value;
   console.log("selected network:"+select_network);
   var optionDirection="";
   var optionProfile="";
   var optionBandwidth = "";
   //uncheck checkboxChange
   checkboxChange.checked = false;
    onCheck();
    //clear packet size error fields
    clearErrors(); 
    //set seclect Bandwidth
    selectBandwidth(select_network);

    if (select_network == 'Wi-Fi 802.11ac' || select_network == 'Wi-Fi 802.11ax')
    {
        optionDirection = '<option selected disabled hidden>Choose traffic direction</option>'+
                          '<option value="upstream">Upstream</option>'+
                          '<option value="downstream">Downstream</option>';
        optionProfile =   '<option selected disabled hidden>Choose traffic profile</option>'+
                          '<option value="periodic">Periodic</option>'+
                          '<option value="cbr">CBR</option>'+
                          '<option value="vbr">VBR</option>';    
       
       // num_devices.placeholder = "max 22"; 
        dist_devices_gateway.placeholder = "max 10";
        //set a default value to battery capacity depending on a network
        battery_cap.value = "5200"; 
        voltage.value = "12"; 
        packetSizeShow("Wi-Fi");

    }
    else if (select_network == 'LoRaWAN')
    {
        optionDirection = '<option disabled hidden>Choose traffic direction</option>'+
                          '<option selected value="upstream">Upstream</option>';
        optionProfile = '<option diabled hidden>Choose traffic direction</option>'+
                        '<option selected value="periodic">Periodic</option>';  
       // num_devices.placeholder = "max 70000";    
        dist_devices_gateway.placeholder = "max 8000";        
         //set a default value to battery capacity depending on a network
         battery_cap.value = "1000"; 
         voltage.value = "3";    
         packetSizeShow("LoRaWAN");     
    }
    else
    {
        num_devices.placeholder ="";
        dist_devices_gateway.placeholder = "";
        diagram.setAttribute('src', '../static/img/network-IOT_640.png');
        packetSizeShow("");   
    }
    direction.innerHTML = optionDirection;
    traffic_profile.innerHTML = optionProfile;
}

function onChangeSelectDirection(){
    var select_direction = direction.value;
    console.log("selected direction: "+select_direction);
    switch(select_direction)
    {
        case 'upstream' :
                diagram.setAttribute('src', '../static/img/diagram_traffic_upstream.png');
                break;
        case 'downstream' :
                diagram.setAttribute('src', '../static/img/diagram_traffic_downstream.png');
                break;
        default :
                diagram.setAttribute('src', '../static/img/network-IOT_640.png');
    }        
}  

function onChangeSelectTrafficProfile(){
    onChangeTrafficProfile();
}

function onChangeTrafficProfile(){
    var select_trafficProfile = traffic_profile.value;
    console.log("selected profile : "+select_trafficProfile);
    switch(select_trafficProfile)
    {
        case 'periodic' :
            if (network.value=="LoRaWAN") {
                packet_size_wifi.style.display = "none";
                lbl_packet_size_wifi.style.display = "none";
                packet_size_lorawan.style.display = "inherit";
                lbl_packet_size_lorawan.style.display = "inherit";
            }
            else {
                packet_size_wifi.style.display = "inherit";
                lbl_packet_size_wifi.style.display = "inherit";
                packet_size_lorawan.style.display = "none";
                lbl_packet_size_lorawan.style.display = "none";
            }
                load_freq.style.display = "inherit";
                lbl_load_freq.style.display = "inherit";
                mean_load.style.display = "none";
                lbl_fps.style.display = "none";
                fps.style.display = "none";
                lbl_mean_load.style.display = "none";
                break;
        case 'cbr' :
                load_freq.style.display = "none";
                lbl_load_freq.style.display = "none";
                packet_size_wifi.style.display = "inherit";
                lbl_packet_size_wifi.style.display = "inherit";
                mean_load.style.display = "inherit";
                lbl_fps.style.display = "none";
                fps.style.display = "none";
                lbl_mean_load.style.display = "inherit";
                break;
        case 'vbr' :
                load_freq.style.display = "none";
                packet_size_wifi.style.display = "none";
                lbl_packet_size_wifi.style.display = "none";
                lbl_load_freq.style.display = "none";
                mean_load.style.display = "inherit";
                lbl_mean_load.style.display = "inherit";
                lbl_fps.style.display = "inherit";
                fps.style.display = "inherit";
                break;
        default :
                load_freq.style.display = "none";
                lbl_load_freq.style.display = "none";
                mean_load.style.display = "none";
                lbl_fps.style.display = "none";
                fps.style.display = "none";
                lbl_mean_load.style.display = "none";
    }

}  