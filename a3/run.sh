
#VENCRYPT
python3 scrypt.py monkey01 b.txt c.txt > cdebug.txt
# ./hw10/linux/scrypt -d monkey01 b.txt d.txt > ddebug.txt

#check for differences
diff c.txt d.txt

#VDECRYPT
python3 scrypt.py monkey01 b.txt c.txt > cdebug.txt
# ./hw10/linux/scrypt -d monkey01 b.txt d.txt > ddebug.txt

#check for differences
diff c.txt d.txt


#SCRYPT

python3 scrypt.py monkey01 b.txt c.txt > cdebug.txt
# ./hw10/linux/scrypt -d monkey01 b.txt d.txt > ddebug.txt

#check for differences
diff c.txt d.txt

#SBENCRYPT
python3 sbencrypt.py monkey01 b.txt c.txt > cdebug.txt
# ./hw10/linux/sbencrypt -d monkey01 b.txt d.txt > ddebug.txt

#check for differences
diff c.txt d.txt


#SBDECRYPT
python3 sbdecrypt.py monkey01 c.txt cdecrypt.txt > cdebug.txt
# ./hw10/linux/sbdecrypt -d monkey01 d.txt ddecrypt.txt > ddebug.txt

#check for differences
diff cdecrypt.txt ddecrypt.txt

