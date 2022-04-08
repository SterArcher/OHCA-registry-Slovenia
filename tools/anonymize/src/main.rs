use clap::{Command, Arg};
use std::{
    io::{self, Read, Write, BufRead, BufReader},
    fs::{self},
    path::Path,
    collections::HashMap
};
use sha2::{Sha256, Digest};

enum Input {
    File(fs::File),
    Stdin(io::Stdin),
}

impl Read for Input {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        match *self {
            Input::File(ref mut file) => file.read(buf),
            Input::Stdin(ref mut stdin) => stdin.read(buf),
        }
    }
}

fn read_line_lossy<R: BufRead>(reader: &mut R) -> Result<String, String> {
    let mut buf: Vec<u8> = Vec::new();
    return match reader.read_until(b'\n', &mut buf) {
        Ok(_) => {
            if buf.is_empty() {
                return Err("Reader empty".to_string());
            }
            let _ = &buf.pop();
            if buf.last() == Some(&b'\r') {
                let _ = &buf.pop();
            }
            return Ok(String::from_utf8_lossy(&buf).to_string());
        }
        Err(e) => Err(e.to_string())
    };
}

fn hash(input: impl AsRef<[u8]>) -> String {
    let mut hasher = Sha256::new();
    hasher.update(input);
    return format!("{:X}", hasher.finalize());
}

fn calculate_caseid(name: &str, surname: &str, timestamp: &str) -> String{
    let input = String::from(&name[0..0]) + timestamp + &surname[0..0];
    return hash(input);
}

fn calculate_dispatchid(vehicle: &str, timestamp: &str) -> String {
    let input = String::from(vehicle) + timestamp;
    return hash(input);
}

fn main() -> Result<(), io::Error> {
    // Collect help information and arguments
    let matches = Command::new("anonymize")
        .version("0.1.0")
        .author("G. Tomšič (SiOHCA Team)")
        .about("Anonymize CSV data for posting to OHCA API Server.\nOutputs data to stdout.")
        .arg(
            Arg::new("INPUT")
                .help("Sets input file(s). - reads from stdin.")
                .allow_hyphen_values(true)
                .required(true)
                .takes_value(true)
        )
        .get_matches();

    let reqs_case = ["name", "surname", "timestamp"];
    let reqs_disp = ["vehicleID", "timestamp"];

    let columns = [
        "caseID", "dispatchID",
        "dispIdentifiedCA", "dispProvidedCPRinst",
        "age", "gender", "witnesses", "location",
        "bystanderResponse", "bystanderResponseTime",
        "bystanderAED", "bystanderAEDTime",
        "deadOnArrival", "firstMonitoredRhy",
        "pathogenesis", "independentLiving",
        "comorbidities", "vad", "cardioverterDefib",
        "stemiPresent", "responseTime", "defibTime",
        "ttm", "ttmTemp", "drugs", "airwayControl",
        "cprQuality", "shocks", "drugTimings",
        "vascularAccess", "mechanicalCPR",
        "targetVent", "reperfusionAttempt",
        "reperfusionTime", "ecls", "iabp",
        "ph", "lactate", "glucose", "neuroprognosticTests",
        "specialistHospital", "hospitalVolume", "ecg",
        "ecgBLOB", "targetBP", "survived", "rosc",
        "roscTime", "SurvivalDischarge30d",
        "cpcDischarge", "mrsDischarge",
        "survivalStatus", "transportToHospital",
        "treatmentWithdrawn", "cod", "organDonation",
        "patientReportedOutcome", "qualityOfLife"
    ];

    let input = match matches.value_of("INPUT").unwrap() {
        "-" => {Input::Stdin(io::stdin())},
        filename => {Input::File(fs::File::open(Path::new(filename)).expect("No such file!"))}
    };

    // Read file lines as vector of bytes (by line), don't destroy non UTF8 data
    let mut reader = BufReader::new(input);
    let mut writer = io::stdout();

    let mut b_caseid = false;
    let mut b_dispid = false;

    let mut titles: HashMap<String, usize> = HashMap::new();
    let mut first_loop = true;
    loop {
        match read_line_lossy(&mut reader) {
            Ok(line) => {
                // Main program
                let data: Vec<&str> = line.split(',').collect();
                let mut output: Vec<String> = Vec::new();

                // Only run this on the first loop
                // Get the column titles
                if first_loop {
                    for i in 0..data.len() {
                        titles.insert(String::from(data[i]), i);
                    }
                    b_caseid = reqs_case.iter().all(|item| titles.keys().collect::<Vec<_>>().contains(&&item.to_string()));
                    b_dispid = reqs_disp.iter().all(|item| titles.keys().collect::<Vec<_>>().contains(&&item.to_string()));
                    first_loop = false;
                    continue;
                }

                for title in columns {
                    match title {
                        "caseID" => {
                            let name = data[titles["name"]];
                            let surname = data[titles["surname"]];
                            let timestamp = data[titles["timestamp"]];
                            output.push(
                                match b_caseid || name.len() == 0 || surname.len() == 0 || timestamp.len() == 0 {
                                    false => calculate_caseid(name, surname, timestamp),
                                    true => String::from("NULL")
                                }
                            );
                        },
                        "dispatchID" => {
                            let vehicle = data[titles["vehicle"]];
                            let timestamp = data[titles["timestamp"]];
                            output.push(
                                match b_dispid || vehicle.len() == 0 || timestamp.len() == 0 {
                                    false => calculate_dispatchid(vehicle, timestamp),
                                    true => String::from("NULL")
                                }
                            );
                        },
                        title => {
                            output.push(
                                match data[titles[title]] {
                                    "" => String::from("NULL"),
                                    value => String::from(value)
                                }
                            )
                        }
                    } 
                }

                write!(writer, "{}\n", output.join(","))?;
            },
            Err(e) => {
                if &e == "Reader empty" {
                    return Ok(());
                } else {
                    eprintln!("{}", e)
                }
            }
        }
    }
}