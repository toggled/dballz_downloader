def merge(filea,fileb,dest):
	destfile=file(dest,'wb')
	for filename in [filea,fileb]:
		infile=open(filename,'rb')
 		print 'opening ',filename
		while 1:
			data=infile.read(65536)
			print 'again'
			if not data:
				break
			destfile.write(data)
		infile.close()
	destfile.close()

if __name__=="__main__":
	merge('dbz5_part1.mp4','dbz5_part2.mp4','dbz5.mp4')
