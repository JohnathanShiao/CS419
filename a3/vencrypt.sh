echo -n "Enter the program name (vencrypt, vdecrypt, scrypt, sbencrypt, sbdecrypt):"
read PROG
echo -n "Enter path to keyfile or password:"
read KEY
echo -n "Enter path to source (plain or cipher):"
read IN
echo -n "Enter path to output (plain or cipher):"
read OUT

#VENCRYPT
if [ "$PROG" = "vencrypt" ]; then
    echo "vencrypt"
    python3 vencrypt.py $KEY $IN $OUT
#VDECRYPT
elif [ "$PROG" = "vdecrypt" ]; then
    python3 vdecrypt.py $KEY $IN $OUT
#SCRYPT
elif [ "$PROG" = "scrypt" ]; then
    python3 scrypt.py $KEY $IN $OUT
#SBENCRYPT
elif [ "$PROG" = "sbencrypt" ]; then
    python3 sbencrypt.py $KEY $IN $OUT
#SBDECRYPT
elif [ "$PROG" = "sbdecrypt" ]; then
    python3 sbdecrypt.py $KEY $IN $OUT
fi

