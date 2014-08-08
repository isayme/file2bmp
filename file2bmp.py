import sys
import os
import struct

    
def file2bmp(src_file, dst_file, xpixel = 200):
    """
    Save src_file as dst_file.
    Generally, save a zip/rar compressed file as bmp picture file.
    """
    BMP_FILE_HEAD_LEN = 54;
    
    filehead = bytearray(14);   # bmp file head
    infohead = bytearray(40);   # bmp infomation head

    # in case that the src_file not exist
    if False == os.path.isfile(src_file) :
        print "Source File not Exsit"
        return False

    src_file_stat = os.stat(src_file);
    # get src_file bytes
    src_file_size = src_file_stat.st_size;

    dst_file_width = xpixel;
    dst_file_bytesline = (dst_file_width + 3)/4*4*3;
    dst_file_height = (src_file_size + dst_file_bytesline - 1)/dst_file_bytesline;

    dst_file_size = dst_file_height * dst_file_bytesline * 3;
    dst_file_size = dst_file_size + BMP_FILE_HEAD_LEN;

    # file head
    filehead[0] = "B";
    filehead[1] = "M";
    filehead[2:6] = struct.pack("L", dst_file_size);
    filehead[6:10] = struct.pack("L", 0);
    filehead[10:14] = struct.pack("L", BMP_FILE_HEAD_LEN);

    # info head
    infohead[0:4] = struct.pack("L", 40);
    infohead[4:8] = struct.pack("L", dst_file_width);
    infohead[8:12] = struct.pack("L", dst_file_height);
    infohead[12:14] = struct.pack("H", 1);
    infohead[14:16] = struct.pack("H", 24);
    infohead[16:20] = struct.pack("L", 0);
    infohead[20:24] = struct.pack("L", 0);
    infohead[24:32] = struct.pack("Q", 0);
    infohead[32:36] = struct.pack("L", 0);
    infohead[36:40] = struct.pack("L", 0);

    # write data to dst_file
    fp = open(dst_file, "wb");
    fp.write(filehead);
    fp.write(infohead);
    fp.write(open(src_file, "rb").read());
    if (dst_file_height*dst_file_bytesline > src_file_size):
        zeros = bytearray(dst_file_height*dst_file_bytesline - src_file_size);
        fp.write(zeros);
    fp.close();
    
if __name__ == "__main__":
    # src_file = raw_input("Input src_file name : ");
    # dst_file = raw_input("Input dst_file name : ");
    # file2bmp(src_file, dst_file);
    file2bmp("test.zip", "test.bmp", 40);
    
