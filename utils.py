import time
import sys


def prune_row(row, internalPortToCheck='25565'):
    """
    get the next pcp mapping for the give port and return the
    external ip, external port, and result code
    :param internalPortToCheck:
    :param row:
    :return: None | dict
    """
    val = None
    if len(row.contents) > 7:
        externalIP = row.contents[2].text
        externalPort = row.contents[3].text
        internalPort = row.contents[4].text
        resultCode = row.contents[7].text
        if internalPort == internalPortToCheck:
            val = {
                "externalIP": externalIP,
                "externalPort": externalPort,
                "resultCode": resultCode
            }
    return val


def msg_ppl(pcpConfig):
    print("New config found!\n", pcpConfig)


def countdown(interval):
    for remaining in range(interval, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\rComplete!            \n")