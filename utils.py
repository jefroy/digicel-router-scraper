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


# whatsapp stuff from dookie
import pywhatkit


def send_whatsapp_msg(msg):

    groupID = "GiEUSqYXTwp4mLtfcKpBm3"  # COTR Group ID
    # message = "Dear Ajay, I write this to you from the script. PEEPEE POO POO"  # use this to pass yuh info
    wait = 20
    close = 10

    pywhatkit.sendwhatmsg_to_group_instantly(groupID, msg, wait, True, close)
