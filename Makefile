.PHONY : clean

%.mp3 : %.txt
	@python3 txt2wave.py -i $<

clean :
	@rm -f *.mp3
