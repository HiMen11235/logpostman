#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import random
import time
from scapy.all import *
import ipaddress
import sys


def get_args():
    parser = argparse.ArgumentParser()
    ip_header_value = parser.add_argument_group("IP", "")
    ip_header_value.add_argument(
        "host", default=None, help="destination address", type=str
    )
    ip_header_value.add_argument(
        "-a", "--spoof", default=None, help="spoof source address"
    )
    udp_header_value = parser.add_argument_group("UDP", "")
    udp_header_value.add_argument(
        "-s",
        "--baseport",
        default=None,
        help="base source port (default random)",
        type=int,
    )
    udp_header_value.add_argument(
        "-p",
        "--destport",
        default=514,
        help="destination port (default 514)",
        type=int,
        metavar="514",
    )
    input_values = parser.add_mutually_exclusive_group(required=True)
    input_values.add_argument(
        "-f",
        "--file",
        default=None,
        help="send file contents",
        type=str,
        metavar="/path/to/file",
    )
    input_values.add_argument(
        "-m", "--message", default=None, help="send a message", type=str
    )
    syslog_priority = parser.add_argument_group("Syslog priority values", "")
    syslog_priority.add_argument(
        "-sf", "--facility", default=1, type=int, help="facility value (default 1)"
    )
    syslog_priority.add_argument(
        "-ss", "--severity", default=6, type=int, help="severity value (default 6)"
    )
    transmission_and_display = parser.add_argument_group(
        "Transmission and display options", ""
    )
    transmission_and_display.add_argument(
        "-r",
        "--raw",
        default=False,
        action="store_true",
        help="send raw data(No priority value added)",
    )
    transmission_and_display.add_argument(
        "--eps",
        default=1000,
        help="transmitted events per second (default 1000)",
        type=int,
        metavar="1000",
    )
    transmission_and_display.add_argument(
        "-q",
        "--quiet",
        default=False,
        action="store_true",
        help="suppresses display during and after execution",
    )
    try:
        args = parser.parse_args()
    except:
        sys.exit(1)
    return args


def validate_ip_address(ip_address: str):
    try:
        tmp = ipaddress.ip_address(ip_address)
    except:
        print("Invalid IP address.Please enter IPv4 or IPv6 format. :" + ip_address)
        sys.exit(1)


def validate_port_number(port_number: int):
    if 0 <= int(port_number) <= 65536:
        pass
    else:
        print("Please enter a valid port number. :" + str(port_number))
        sys.exit(1)


def validate_facility(facility: int):
    if 0 <= int(facility) <= 23:
        pass
    else:
        print("Invalid facility values. :" + str(facility))
        sys.exit(1)


def validate_severity(severity: int):
    if 0 <= int(severity) <= 7:
        pass
    else:
        print("Invalid severity values. :" + str(severity))
        sys.exit(1)


def ip_header(src_ip: str, dst_ip: str):
    if src_ip is None:
        return IP(dst=str(dst_ip))
    else:
        return IP(src=str(src_ip), dst=str(dst_ip))


def udp_header(src_port: int, dst_port: int):
    if src_port is None:
        return UDP(sport=random.randint(49152, 65535), dport=dst_port)
    else:
        return UDP(sport=src_port, dport=dst_port)


def absolute_path(file_path: str):
    if os.path.isabs(file_path):
        return file_path
    else:
        return os.path.abspath(file_path)


def sending_syslog(
    src_ip: str,
    dst_ip: str,
    src_port: int,
    dst_port: int,
    message: str,
    facility: int,
    severity: int,
    raw: bool,
):
    # Creating IP Headers.
    ip = ip_header(src_ip, str(dst_ip))
    # Creating UDP Headers.
    udp = udp_header(src_port, int(dst_port))
    # Calculate syslog priority value.
    PRI = "<" + str(int(facility) * 8 + int(severity)) + ">"
    if bool(raw):
        msg = message.strip()
    else:
        msg = PRI + message.strip()
    packets = ip / udp / msg
    send(packets, verbose=0)
    return True


def validate_arguments():
    args = get_args()
    # Validation of IP addresses.
    validate_ip_address(args.host)
    if args.spoof is not None:
        validate_ip_address(args.spoof)
    # Validation of port numbers.
    validate_port_number(int(args.destport))
    if args.baseport is not None:
        validate_port_number(int(args.baseport))
    # Facility and Severity Validation.
    validate_facility(int(args.facility))
    validate_severity(int(args.severity))
    return args


def main():
    # Argument validation and retrieval.
    args = validate_arguments()
    # Action when a message option is specified.
    if args.file is None and args.message is not None:
        sending_syslog(
            str(args.spoof),
            str(args.host),
            args.baseport,
            int(args.destport),
            str(args.message),
            int(args.facility),
            int(args.severity),
            bool(args.raw),
        )
        if args.quiet:
            pass
        else:
            print("Event message has been sent.")
            print("done!")
        sys.exit(0)
    # Action when a file option is specified.
    if args.file is not None and args.message is None:
        file_path = absolute_path(args.file)
        with open(file_path, "r") as f:
            sent_count = 0
            start_time = time.time()
            for i, message in enumerate(f):
                sending_syslog(
                    str(args.spoof),
                    str(args.host),
                    args.baseport,
                    int(args.destport),
                    str(message),
                    int(args.facility),
                    int(args.severity),
                    args.raw,
                )
                if i % args.eps == 0:
                    end_time = time.time()
                    if (end_time - start_time) >= 1.0:
                        start_time = end_time
                    else:
                        # Calculate milliseconds to wait, rounding up microseconds
                        wait_time = (
                            float(int((1.001 - (end_time - start_time)) * 1000)) / 1000
                        )
                        time.sleep(wait_time)
                        start_time = end_time
                    if args.quiet:
                        pass
                    else:
                        print(f"\r{i}" + " events sent.", end="", flush=True)
                sent_count += 1
        # Exit message.
        if args.quiet:
            pass
        else:
            print(f"\r{sent_count}" + " events sent.", end="", flush=True)
            print("\nEvent message has been sent.")
            print("done!")
        sys.exit(0)


if __name__ == "__main__":
    main()
