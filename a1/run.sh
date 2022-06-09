
python3 auth.py addUser hi ""
python3 auth.py addUser "" hi
python3 auth.py authenticate hi ""
python3 auth.py authenticate "" hi
python3 auth.py setdomain hi ""
python3 auth.py setdomain "" hi
python3 auth.py domaininfo ""
python3 auth.py settype hi ""
python3 auth.py settype "" hi
python3 auth.py typeinfo ""
python3 auth.py addaccess hi "" ""
python3 auth.py addaccess "" hi ""
python3 auth.py addaccess "" "" hi
python3 auth.py canaccess hi "" ""
python3 auth.py canaccess "" hi ""
python3 auth.py canaccess "" "" hi
echo
echo
a=0
while [ $a -lt 50 ]
do
    python3 auth.py addUser user-$a password-$a
    a=`expr $a + 1`
done
echo
echo

a=0
while [ $a -lt 50 ]
do
    python3 auth.py authenticate user-$a password-$a
    a=`expr $a + 1`
done
echo
echo

a=0
while [ $a -lt 50 ]
do
    python3 auth.py authenticate user-$a badpassword-$a
    a=`expr $a + 1`
done
echo
echo

a=0
while [ $a -lt 50 ]
do
    if [ $(expr $a % 2) != "0" ] 
    then
        python3 auth.py setDomain user-$a odd
    else
        python3 auth.py setDomain user-$a even
    fi
    a=`expr $a + 1`
done

python3 auth.py domaininfo odd
python3 auth.py domaininfo even
echo
echo

python3 auth.py setType hbo premium-content
python3 auth.py setType youtube free-content
python3 auth.py setType wwe premium-content
python3 auth.py setType twitch free-content
python3 auth.py setType "youtube red" premium-content
python3 auth.py setType pbs free-content
echo
echo

python3 auth.py typeinfo premium-content
python3 auth.py typeinfo free-content
echo
echo

python3 auth.py addaccess view odd premium-content
python3 auth.py addaccess view odd free-content
python3 auth.py addaccess make even free-content

a=0
while [ $a -lt 50 ]
do
    echo $a
    if [ $(expr $a % 2) != "0" ] 
    then
        python3 auth.py canaccess make user-$a twitch      
    else
        python3 auth.py canaccess view user-$a twitch
    fi
    a=`expr $a + 1`
done