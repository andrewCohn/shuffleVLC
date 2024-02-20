import xml.etree.ElementTree as ET
import xml.dom.minidom
import os
import urllib.parse
import cv2
import random

def getDuration(filename):
    video = cv2.VideoCapture(filename)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_seconds = frame_count / fps
    return int(duration_seconds * 1000)

def getFilesList(dir = None):
    outList = []
    if dir is None:
        dir = input("Directory: \n")
    for dirname, dirnames, filenames in os.walk(dir):
        curDir = dirname.replace("\\\\", "\\")
        for file in filenames:
            if isVid(file):
                outList.append(r"{0}\{1}".format(curDir, file))
                
    return outList


def isVid(file):
    videoFileTypes = {
    "mkv", "mp4", "mov", "avi", "mpg", "mpeg", "wmv", "flv", "webm", "3gp",
    "m2v", "ts", "mts", "m2ts", "vob", "divx", "xvid", "rm", "rmvb", "asf",
    "mk3d", "f4v", "amv", "m2p", "m4v", "webm", "3g2", "flv", "mjp", "mov",
    "qt", "avi", "divx", "mxf", "ts", "webm", "asf", "wma", "wmv", "flv",
    "m2ts", "mts", "vob", "m4v", "ifo", "3gpp", "3g2"}
    return file.split(".")[-1] in videoFileTypes

def shuffleFiles(fileList,n=None):
    if n == None:
        n = len(fileList)*10
    for i in range(n):
        index1 = random.randint(0,len(fileList)-1)
        index2 = random.randint(0,len(fileList)-1)
        swapA = fileList[index1]
        swapB = fileList[index2]
        fileList[index1] = swapB
        fileList[index2] = swapA


def main():
    outName = input("Name of the playlist to output:\n")
    files = getFilesList()
    print("shuffling files")
    shuffleFiles(files)       
    
    
    # Create the root element
    root = ET.Element("playlist")
    root.set("xmlns", "http://xspf.org/ns/0/")
    root.set("xmlns:vlc", "http://www.videolan.org/vlc/playlist/ns/0/")
    root.set("version", "1")
    root.set("encoding", "UTF-8")

    # Create child elements
    title = ET.SubElement(root, "title")
    title.text = "testPlaylist"

    trackList = ET.SubElement(root, "trackList")
    for i, file in enumerate(files):
        thisTrack = ET.SubElement(trackList,"track")
        thisLocation = ET.SubElement(thisTrack,"location")
        thisLocation.text = "file:///"+urllib.parse.quote(file.replace("\\","/"))
        duration = getDuration(file)
        durationXML = ET.SubElement(thisTrack,"duration")
        durationXML.text = str(duration)
        extension = ET.SubElement(thisTrack, "extension")
        trackID = ET.SubElement(extension,"vlc:id")
        trackID.text = str(i)
        extension.set("application", "http://www.videolan.org/vlc/playlist/0")




    extension = ET.SubElement(root, "extension")
    extension.set("application", "http://www.videolan.org/vlc/playlist/0")
    for i in range(len(files)):
        vlcElem = ET.SubElement(extension,"vlc:item")
        vlcElem.set("tid",str(i))

    # Create XML tree
    tree = ET.ElementTree(root)

    # Convert tree to string with pretty formatting
    xml_str = ET.tostring(root, encoding="utf-8")
    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml_str = dom.toprettyxml(indent="    ")
    
    # Write pretty formatted XML to file
    with open(outName+".xspf", "w") as f:
        f.write(pretty_xml_str)
main()
