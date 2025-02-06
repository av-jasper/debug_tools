// use mavlink::common::MavMessage;
// use mavlink::{self, MavConnection, MavlinkVersion, Message};

// fn main() {
//     // Connect to the UDP server
//     let mut udp_client = match mavlink::connect("udpin:127.0.0.1:5555") {
//         // let mut udp_client = match mavlink::connect("tcpin:0.0.0.0:1234") {
//         Ok(conn) => conn,
//         Err(e) => {
//             eprintln!("Failed to connect to the UDP server: {}", e);
//             return;
//         }
//     };
//     // udp_client.set_protocol_version(MavlinkVersion::V2);

//     println!("Connected to MAVLink server. Listening for messages...");

//     loop {
//         // Receive messages from the server
//         match udp_client.recv() {
//             Ok((_, msg)) => {
//                 if let MavMessage::PARAM_VALUE(param_value_data) = msg {
//                     // Print out the details of the PARAM_VALUE message
//                     let param_id = String::from_utf8(param_value_data.param_id.to_vec()).unwrap();

//                     println!(
//                         "Received PARAM_VALUE message: param_id = {}, param_value = {}, param_type = {:?}, param_count = {}, param_index = {}",
//                         param_id,
//                         param_value_data.param_value,
//                         param_value_data.param_type,
//                         param_value_data.param_count,
//                         param_value_data.param_index,
//                     );
//                 } else {
//                     // Handle other messages if necessary
//                     println!("Received other message: {:?}", msg);
//                 }
//             }
//             Err(e) => {
//                 eprintln!("Error receiving message: {}", e);
//                 break;
//             }
//         }
//     }
// }

use std::io::ErrorKind;
use std::thread::sleep;
use std::time::Duration;

use mavlink::common::{MavCmd, MavMessage};
use mavlink::{self, MavConnection, MavHeader, MavlinkVersion, Message};

fn main() {
    // let mut udp_client = match mavlink::connect("tcpin:10.223.0.4:5760") {
    let mut udp_client: Box<dyn MavConnection<mavlink::common::MavMessage> + Send + Sync> =
        match mavlink::connect("udpin:127.0.0.1:14591") {
            Ok(conn) => conn,
            Err(e) => {
                eprintln!("Failed to connect to the UDP server: {}", e);
                return;
            }
        };
    println!("Connected to MAVLink server. Listening for messages...");

    // udp_client.set_protocol_version(MavlinkVersion::V1);
    udp_client.set_protocol_version(MavlinkVersion::V2);

    //         // Create the PARAM_VALUE message
    //         let param_value_msg = MavMessage::PARAM_VALUE(mavlink::common::PARAM_VALUE_DATA {
    //             param_id: array,
    //             param_value,
    //             param_type: mavlink::common::MavParamType::MAV_PARAM_TYPE_UINT8, // TODO experiment
    //             param_count: 1,
    //             param_index: 0,
    //         });

    //         // Send the PARAM_VALUE message
    //         match udp_server.send(&MavHeader::default(), &param_value_msg) {
    //             Ok(_) => println!("Sent PARAM_VALUE message: {} = {}", param_id, param_value),
    //             Err(e) => eprintln!("Failed to send PARAM_VALUE message: {}", e),
    //         }

    loop {
        // Receive messages from the server
        println!("New MSG...");
        match udp_client.recv() {
            Ok((_, msg)) => {
                println!("Received message: {:?}", msg);
            }
            Err(e) => {
                match &e {
                    mavlink::error::MessageReadError::Io(error) => {
                        if error.kind() == ErrorKind::WouldBlock {
                            continue;
                        }
                    }
                    mavlink::error::MessageReadError::Parse(_parser_error) => continue,
                }
                eprintln!("Error receiving message: {}", e);
                break;
            }
        }
    }
}
