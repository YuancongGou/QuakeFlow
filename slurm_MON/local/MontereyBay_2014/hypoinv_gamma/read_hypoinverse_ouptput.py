f = open('hypoOut.arc','r')
g = open('hypoOut.arc.csv', 'w')

g.write('YR,MO,DY,HR,MI,SC,latitude,longitude,depth_km,mag,RMS,EH,EZ,nn\n')

nn = 0
for line in f:
        if (len(line) == 180):
            nn = nn + 1
            RMS = float(line[48:52]) / 100
            gap = int(line[42:45])
            dep = float(line[31:36])/100
            EH = float(line[85:89])/100
            EZ = float(line[89:93])/100
            mag = float(line[123:126])/100
                
            year = int(line[0:4])
            mon = int(line[4:6])
            day = int(line[6:8])
            hour = int(line[8:10])
            min = int(line[10:12])
            sec = int(line[12:16])/100
            if line[18] == ' ': #N
                lat = (float(line[16:18]) + float(line[19:23]) / 6000)
            else:
                lat = (float(line[16:18]) + float(line[19:23]) / 6000) * (-1)
            if line[26] == 'E':
                lon = (float(line[23:26]) + float(line[27:31]) / 6000)
            else:
                lon = (float(line[23:26]) + float(line[27:31]) / 6000) * (-1)

            g.write('{:4d},{:02d},{:02d},{:2d},{:2d},{:5.2f},{:7.4f},{:9.4f},{:5.2f},{:5.2f},{:5.2f},{:5.2f},{:5.2f},{:9d}\n'.format(
                            year, mon, day, hour, min, sec, lat, lon, dep, mag, RMS, EH, EZ, nn))

            #g.write()
f.close()
g.close()
