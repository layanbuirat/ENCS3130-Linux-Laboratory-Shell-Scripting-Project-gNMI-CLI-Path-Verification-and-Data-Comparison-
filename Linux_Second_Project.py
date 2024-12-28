'''
- Project Title: gNMI-CLI Path Verification and Data Comparison Tool

- Project Description: 
    This project aims to develop a Python-based tool for verifying data accuracy between gNMI telemetry data and CLI command outputs for 
    network device configurations and operational states. The tool will be implemented using Python classes and functions to ensure 
    modularity and maintainability.

- Students Information:
    ~ First Student:
        - Name: Raghad Murad Buzia
        - ID: 1212214
        - Section: 1
    ~ Second Student:
        - Name: Layan burait 
        - ID: 1211439
        - Section: 1
'''

########################################################################################################################################
#                                                      Import Important Libraries                                                      #
########################################################################################################################################

'''
Importing 'json' library: 
    - The 'json' library is a built-in Python library that provides functions to work with JSON (JavaScript Object Notation) data. 
    - It allows us to parse JSON strings, convert Python objects to JSON format, and read/write JSON data from/to files. 
    - JSON is a lightweight data interchange format that is easy to read and write for humans, and easy to parse and generate for machines. 
Importing 'csv' library: # 
    - The 'csv' library is a built-in Python library that provides functions to work with CSV (Comma-Separated Values) files. 
'''
import json
import csv

########################################################################################################################################
#                                                         gNMI Query Execution                                                         #
########################################################################################################################################

'''
 --> Declare the GNMI class which is responsible for loading GNMI data from a JSON file and fetching data based on provided gNMI paths.
     This class ensures that GNMI data is loaded into a dictionary format and provides methods to fetch specific data paths.
'''
class GNMI:

    '''
    The constructor initializes the GNMI object by loading data from the specified JSON file into the `data` attribute
    '''
    def __init__(self, json_file):
        self.data = self.load_data(json_file)

    '''
    This method attempts to open and load the JSON file:
        If the file is not found, it raises a FileNotFoundError.
        If the file contains invalid JSON, it raises a JSONDecodeError.
    '''
    def load_data(self, json_file):
        # Load GNMI data from a JSON file into a dictionary:
        try:
            with open(json_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{json_file}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file '{json_file}'.")

    '''
    This method retrieves data from the loaded GNMI dictionary based on the provided path.
        If the path is found, it returns the data as a formatted JSON string.
        If the path is not found, it returns None.
    '''  
    def fetch_data(self, gnmi_path):
        data = self.data.get(gnmi_path, None)
        if data is not None:
            return json.dumps(data, indent=4)  # Return data as a JSON string
        return None

########################################################################################################################################
#                                                         CLI Command Mapping                                                          #
########################################################################################################################################
'''
 --> Declare the CLI class which is responsible for simulating the execution of CLI commands based on provided gNMI paths.
     This class maintains two types of command mappings:
        1. Single command mappings for gNMI paths that correspond to a single CLI command.
        2. Multi-command mappings for gNMI paths that correspond to multiple CLI commands.
'''
class CLI:

    '''
    The constructor initializes two dictionaries:
        1. single_command: Maps gNMI paths to a single CLI command.
        2. multi_commands: Maps gNMI paths to a list of multiple CLI commands.
    '''
    def __init__(self):
        self.single_command = {
            "/interfaces/interface[name=eth0]/state/counters": "show interfaces eth0 counters",
            "/system/memory/state": "show memory",
            "/interfaces/interface[name=eth1]/state/counters": "show interfaces eth1 counters",
            "/system/cpu/state/usage": "show cpu",
            "/routing/protocols/protocol[ospf]/ospf/state": "show ospf status"
        }
        
        self.multi_commands = {
            "/interfaces/interface[name=eth0]/state": [
                "show interfaces eth0 status",
                "show interfaces eth0 mac-address",
                "show interfaces eth0 mtu",
                "show interfaces eth0 speed"
            ],
            "/bgp/neighbors/neighbor[neighbor_address=10.0.0.1]/state": [
                "show bgp neighbors 10.0.0.1",
                "show bgp neighbors 10.0.0.1 received-routes",
                "show bgp neighbors 10.0.0.1 advertised-routes"
            ],
            "/system/cpu/state": [
                "show cpu usage",
                "show cpu user",
                "show cpu system",
                "show cpu idle"
            ],
            "/ospf/areas/area[id=0.0.0.0]/state": [
                "show ospf area 0.0.0.0",
                "show ospf neighbors"
            ],
            "/system/disk/state": [
                "show disk space",
                "show disk health"
            ]
        }

    '''
    This method checks if the provided GNMI path is mapped to a single CLI command or multiple CLI commands.
    It then simulates the execution of the corresponding CLI command(s) and returns their outputs.
    '''
    def execute_command(self, gnmi_path):
        """Simulate execution of CLI commands based on GNMI path."""
        if gnmi_path in self.single_command:
            command = self.single_command[gnmi_path]
            output = self.get_cli_output(command)
            return command, "\n".join([f"{key}: {output[key]}" for key in output])
        elif gnmi_path in self.multi_commands:
            commands = self.multi_commands[gnmi_path]
            outputs = {}
            for command in commands:
                out = self.get_cli_output(command)
                if isinstance(out, list):
                    for index, item in out:
                        if isinstance(item, dict):
                            for key, value in item.items():
                                outputs[key] = value
                if isinstance(out, dict):
                    for key, value in out.items():
                        outputs[key] = value
            return commands, "\n".join([f"{key}: {outputs[key]}" for key in outputs])
        return None, None

    '''
    This method returns a predefined output for each CLI command.
    '''
    def get_cli_output(self, cli_command):
        """Simulate CLI command outputs."""
        cli_outputs = {
            "show interfaces eth0 counters": {
                "in_octets": 1500000,
                "out_octets": 1400000,
                "in_errors": 10,
                "out_errors": 2
            },
            "show memory": {
                "total_memory": 4096000,
                "available_memory": 1000000
            },
            "show interfaces eth1 counters": {
                "in_octets": 200000,
                "out_octets": 100000
            },
            "show cpu": {
                "cpu_usage": 65
            },
            "show ospf status": {
                "ospf_area": "0.0.0.0",
                "ospf_state": "down"
            },
            "show interfaces eth0 status": {
                "admin_status": "up",
                "oper_status": "up"
            },
            "show interfaces eth0 mac-address": {
                "mac_address": "00:1C:42:2B:60:5A"
            },
            "show interfaces eth0 mtu": {
                "mtu": 1500
            },
            "show interfaces eth0 speed": {
                "speed": 1000
            },
            "show bgp neighbors 10.0.0.1": {
                "peer_as": 65001,
                "connection_state": "Established"
            },
            "show bgp neighbors 10.0.0.1 received-routes": {
                "received_prefix_count": 120
            },
            "show bgp neighbors 10.0.0.1 advertised-routes": {
                "sent_prefix_count": 95
            },
            "show cpu usage": {
                "cpu_usage": 75
            },
            "show cpu user": {
                "user_usage": 45
            },
            "show cpu system": {
                "system_usage": 20
            },
            "show cpu idle": {
                "idle_percentage": 25
            },
            "show ospf area 0.0.0.0": {
                "area_id": "0.0.0.0",
                "active_interfaces": 4,
                "lsdb_entries": 200
            },
            "show ospf neighbors": [
                {"neighbor_id": "1.1.1.1","state": "full"},
                {"neighbor_id": "2.2.2.2","state": "full"}
            ],
            "show disk space": {
                "total_space": 1024000,
                "used_space": 500000,
                "available_space": 524000
            },
            "show disk health": {
                "disk_health": "good"
            }
        }
        
        output = cli_outputs.get(cli_command, None)
        if output is not None:
            return output
        return None

########################################################################################################################################
#                                                           Data Comparison                                                            #
########################################################################################################################################

'''
 --> Declare the Comparator class which provides static methods to normalize keys, convert units, adjust precision, and compare nested 
     data structures. These methods ensure uniformity and accuracy when comparing gNMI data with CLI outputs.
'''
class Comparator:

    '''
    Normalize key by converting to lowercase and removing special characters.
    '''
    @staticmethod
    def normalize_key(key):
        return key.lower().replace(" ", "").replace("-", "").replace("_", "")

    '''
    Convert units like K, KB, M, MB, G, GB, T, TB, ms, s, m, h, and % to base values.
    '''
    @staticmethod
    def convert_units(value):
        if isinstance(value, str):
            if value.endswith("K"):
                return int(float(value.replace("K", "")) * 1000)
            elif value.endswith("KB"):
                return int(float(value.replace("KB", "")) * 1024)
            elif value.endswith("M"):
                return int(float(value.replace("M", "")) * 1000000)
            elif value.endswith("MB"):
                return int(float(value.replace("MB", "")) * 000000)
            elif value.endswith("G"):
                return int(float(value.replace("G", "")) * 1000000000)
            elif value.endswith("GB"):
                return int(float(value.replace("GB", "")) * 1000000000)
            elif value.endswith("T"):
                return int(float(value.replace("T", "")) * 1000000000000)
            elif value.endswith("TB"):
                return int(float(value.replace("TB", "")) * 1000000000000)
            elif value.endswith("ms"):
                return int(float(value.replace("ms", "")))
            elif value.endswith("s"):
                return int(float(value.replace("s", "")) * 1000)  # Convert seconds to milliseconds
            elif value.endswith("m"):
                return int(float(value.replace("m", "")) * 1000 * 60)  # Convert minutes to milliseconds
            elif value.endswith("h"):
                return int(float(value.replace("h", "")) * 1000 * 60 * 60)  # Convert hours to milliseconds
            elif value.endswith("%"):
                return float(value.replace("%", ""))
        return value

    '''
    Round or adjust precision of numerical values.
    '''
    @staticmethod
    def adjust_precision(value):
        if isinstance(value, float):
            return round(value, 2)  # Round to 2 decimal places
        elif isinstance(value, int):
            return float(value)  # Convert integers to float for uniformity
        elif isinstance(value, str) and value.isdigit():
            return float(value)
        return value

    '''
    Recursively compare nested structures.
    '''
    @staticmethod
    def compare_nested(gnmi_data, cli_data):
        
        differences = {}  # Dictionary to store differences
        
        # Normalize GNMI data keys
        normalized_gnmi_data = {}
        for key, value in gnmi_data.items():
            normalized_key = Comparator.normalize_key(key)
            normalized_gnmi_data[normalized_key] = value
        
        # Normalize CLI data keys
        normalized_cli_data = {}
        for key, value in cli_data.items():
            normalized_key = Comparator.normalize_key(key)
            normalized_cli_data[normalized_key] = value
        
        # Compare normalized GNMI data with normalized CLI data
        for key, gnmi_value in normalized_gnmi_data.items():
            if key not in normalized_cli_data:
                differences[key] = {"GNMI": gnmi_value, "CLI": None, "explaine": "{} found in gNMI Output but missing in CLI Command Output".format(key)}
            else:
                cli_value = normalized_cli_data[key]
                if isinstance(gnmi_value, dict) and isinstance(cli_value, dict):
                    # Recursive comparison for nested dictionaries
                    nested_diff = Comparator.compare_nested(gnmi_value, cli_value)
                    differences.update(nested_diff)
                else:
                    # Normalize and adjust precision
                    gnmi_value = Comparator.convert_units(gnmi_value)
                    cli_value = Comparator.convert_units(cli_value)

                    gnmi_value = Comparator.adjust_precision(gnmi_value)
                    cli_value = Comparator.adjust_precision(cli_value)

                    if gnmi_value != cli_value:
                        differences[key] = {"GNMI": gnmi_value, "CLI": cli_value, "explaine": "{} found in both gNMI Output and CLI Command Output but have different values".format(key)}
        
        # Check for extra keys in CLI data
        for key in normalized_cli_data:
            if key not in normalized_gnmi_data:
                differences[key] = {"GNMI": None, "CLI": normalized_cli_data[key], "explaine": "{} found in CLI Command Output but missing in gNMI Output".format(key)}
        
        return differences

    '''
    Compare GNMI data and CLI output for mismatches.
    '''
    @staticmethod
    def compare_data(gnmi_output, cli_output):
        try:
            gnmi_data = json.loads(gnmi_output)
        except json.JSONDecodeError:
            return {"Error": "Invalid GNMI JSON format."}

        cli_data = {}
        for line in cli_output.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                cli_data[key.strip()] = value.strip()

        if isinstance(gnmi_data, dict) and isinstance(cli_data, dict):
            return Comparator.compare_nested(gnmi_data, cli_data)
        return {"Error": "Invalid input formats; expected dictionaries."}

########################################################################################################################################
#                                                              Make the Report                                                         #
########################################################################################################################################

'''
 --> Declare a class to generate the output report
'''
class ReportGenerator:
    @staticmethod
    def generate_report(differences):
        """Generate a discrepancy report in the specified format."""
        if not differences:
            return "No discrepancies found, all values match."
        else:
            report = "" 
            for key, diff in differences.items(): 
                report += f"\nField: {key}\n GNMI: {diff['GNMI']}\n CLI: {diff['CLI']}\nExplaine the difference: {diff['explaine']}" 
                return report
            
    def save_history(output_history):
        """Ask user if they want to save the history and in which format."""
        while True:
            save_option = input("Do you want to save your test history? [y/n]: ")
            if save_option.lower() == "y":
                file_format = input("Choose a file format to save (txt/csv/json): ")
                file_name = input("Enter the file name (without extension): ")

                if file_format.lower() == "txt":
                    with open(f"{file_name}.txt", "w") as file:
                        for entry in output_history:
                            file.write(json.dumps(entry, indent=4) + "\n")
                    print(f"History saved as {file_name}.txt")
                    break

                elif file_format == "csv":
                    with open(f"{file_name}.csv", "w", newline="") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(["Path", "Comparison Report"])
                        for entry in output_history:
                            for path, report in entry.items():
                                writer.writerow([path, report])
                    print(f"History saved as {file_name}.csv")
                    break

                elif file_format == "json":
                    with open(f"{file_name}.json", "w") as jsonfile:
                        json.dump(output_history, jsonfile, indent=4)
                    print(f"History saved as {file_name}.json")
                    break

                else:
                    print("Invalid file format. Please choose txt, csv, or json.")

            elif save_option == "n":
                print("Exiting without saving history.")
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

########################################################################################################################################
#                                                                Main Program                                                          #
########################################################################################################################################

def main():
    gNMI = GNMI("gNMI_Data.json")
    cli = CLI()
    output_history = []

    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~   Welcome in gNMI-CLI Path Verification and Data Comparison Program   ~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    print("\n\n --> If you want to exit the program just enter one of the following `e, E, Exit`\n\n")
    while True:
        
        user_input = input("\nEnter GNMI Path: ")
        
        if user_input.lower() in ["e", "exit"]:
            ReportGenerator.save_history(output_history)
            print("Exiting...")
            break

        gnmi_data = gNMI.fetch_data(user_input)
        cli_commands, cli_data = cli.execute_command(user_input)
        

        if gnmi_data is None or cli_data is None:
            print("\n - Error: Unknown gNMI path. Please provide a valid path.")
            if gnmi_data is None and cli_data is None:
                print("     GNMI Path '{}' not found in Both gNMI data and CLI data.".format(user_input))
            elif gnmi_data is None:
                print("     GNMI Path '{}' not found in gNMI data.".format(user_input))
            elif cli_data is None:
                print("     GNMI Path '{}' not found in CLI commands.".format(user_input))
        else:
            print("\n - gNMI data for gNMI path '{}' is:".format(user_input))
            print(gnmi_data)
            print("\n - CLI Commands for gNMI path '{}' is:".format(user_input))
            print(cli_commands)
            print("\n - CLI data for gNMI path '{}' is:".format(user_input))
            print(cli_data)
            comparison = Comparator.compare_data(gnmi_data, cli_data)
            report = ReportGenerator.generate_report(comparison)
            print("\n - Comparison result for gNMI path '{}' is: \n{}".format(user_input, report))
            output_history.append({user_input: report})

########################################################################################################################################
#                                                                Run The Code                                                          #
########################################################################################################################################

if __name__ == "__main__":
    main()